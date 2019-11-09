import urllib
import http.server
import socketserver
from urllib.parse import urlparse
from multiprocessing import Process
import os
import traceback
import re
import json
import shutil
from datetime import datetime, timedelta

import nanome
from nanome.util import Logs

enable_logs = False

# Format, MIME type, Binary
Types = {
    "ico" : ("image/x-icon", True),
    "html" : ("text/html; charset=utf-8", False),
    "css" : ("text/css", False),
    "js" : ("text/javascript", False),
    "png" : ("image/png", True),
    "jpg" : ("image/jpeg", True),
    "" : ("text/plain", False) # Default
}

# Utility to get type specs tuple
def get_type(format):
    try:
        return Types[format]
    except:
        return Types[""]

SERVER_DIR = os.path.join(os.path.dirname(__file__), 'WebUI/dist')
FILES_DIR = os.path.expanduser('~/Documents/nanome-web-loader')
if not os.path.exists(os.path.join(FILES_DIR, 'shared')):
    os.makedirs(os.path.join(FILES_DIR, 'shared'))

class DataManager(object):
    def __init__(self):
        self.newline_length = 1
        self.data = bytes()
        self.boundary = None
        self.byte = 0
        self.file_name = ""
        self.body = bytes()

    def find_boundary(self):
        while not self.done():
            n = self.get_current()
            if n == 0x0A:
                self.newline_length = 1
                self.boundary = self.data[:self.byte]
                return
            if n == 0x0D:
                self.newline_length = 2
                self.boundary = self.data[:self.byte]
                return
            self.move_next_utf8()

    def is_newline(self):
        result = False
        curr_byte = self.get_current()
        if self.newline_length == 1:
            result = curr_byte == 0x0A
        elif self.newline_length == 2:
            result = curr_byte == 0x0D
            if result:
                result = self.data[self.byte + 1] == 0x0A
        return result

    def find_newline(self):
        while not self.is_newline():
            self.move_next()

    def curr_index(self):
        return self.byte

    def get_current(self):
        return self.data[self.byte]

    def move_next(self):
        if self.is_newline():
            self.byte += self.newline_length
        else:
            self.byte +=1

    def move_next_utf8(self):
        n = self.get_current()
        if n < 0x80:
            self.byte += 1
        elif n < 0xc0:
            self.byte += 1
        elif n < 0xe0:
            self.byte += 3
        else:
            self.byte += 4

    def done(self):
        return self.byte >= len(self.data)

    def split(self, start, end):
        return self.data[start:end]

# Class handling HTTP requests
class RequestHandler(http.server.BaseHTTPRequestHandler):
    # Utility function to set response header
    def _set_headers(self, code, type='text/html; charset=utf-8'):
        self.send_response(code)
        self.send_header('Content-type', type)
        self.end_headers()

    def _write(self, message):
        try:
            self.wfile.write(message)
        except:
            Logs.warning("Connection reset while responding", self.client_address)

    def _path_is_safe(self, base_path, sub_path):
        safe = os.path.realpath(base_path)
        path = os.path.realpath(os.path.join(base_path, sub_path))
        common = os.path.commonprefix((safe, path))
        return os.path.exists(path) and common == safe

    # Special GET case: get file list
    def _send_list(self, folder=None):
        if WebLoaderServer.keep_files_days > 0:
            self.file_cleanup()

        path = FILES_DIR if folder is None else os.path.join(FILES_DIR, folder)
        if not self._path_is_safe(FILES_DIR, path):
            return self._send_json_error(404, 'File not found')

        self._set_headers(200, 'application/json')
        response = dict()
        response['success'] = True
        response['folders'] = []
        response['files'] = []

        items = [item for item in os.listdir(path) if not item.startswith('.')]
        for item in items:
            is_dir = os.path.isdir(os.path.join(path, item))
            response['folders' if is_dir else 'files'].append(item)
        response['folders'].sort()
        response['files'].sort()
        self._write(json.dumps(response).encode("utf-8"))

    # Standard GET case: get a file
    def _try_get_resource(self, base_dir, path):
        path = os.path.join(base_dir, path)
        if not self._path_is_safe(base_dir, path):
            return self._send_json_error(404, 'File not found')

        try:
            ext = path.split(".")[-1]
            (mime, is_binary) = get_type(ext)
            f = open(path, 'rb' if is_binary else 'r')
        except:
            self._set_headers(404)
            return

        file = f.read()
        data = file if is_binary else file.encode("utf-8")

        self._set_headers(200, mime)
        self._write(data)
        f.close()

    # Called on GET request
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            path = urllib.parse.unquote(path)
        except:
            pass

        base_dir = SERVER_DIR
        is_file = re.search(r'\.[^/]+$', path) is not None

        if path.startswith('/files'):
            if not is_file:
                self._send_list(path[7:] or None)
                return
            else:
                base_dir = FILES_DIR
                path = path[7:]

        # if path doesn't contain extension, serve index
        if not is_file:
            path = 'index.html'
        if path.startswith('/'):
            path = path[1:]

        self._try_get_resource(base_dir, path)

    def _send_json_success(self, code=200):
        self._set_headers(code, 'application/json')
        response = dict()
        response['success'] = True
        self._write(json.dumps(response).encode("utf-8"))

    def _send_json_error(self, code, message):
        response = dict()
        response['success'] = False
        response['error'] = message
        self._set_headers(code, 'application/json')
        self._write(json.dumps(response).encode("utf-8"))

    # Called on POST request
    def do_POST(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            path = urllib.parse.unquote(path)

            content_len = int(self.headers.get('Content-Length'))
            data = self.rfile.read(content_len)
        except:
            Logs.warning("Error trying to parse request:\n", traceback.format_exc())
            self._send_json_error(400, "Parsing problem")
            return

        if not path.startswith('/files'):
            self._send_json_error(403, "Forbidden")
            return

        folder = os.path.join(FILES_DIR, path[7:])

        # no files provided, create folders
        if not content_len:
            if os.path.exists(folder):
                self._send_json_error(400, "Name already exists")
            else:
                os.makedirs(folder)
                self._send_json_success()
            return

        data_manager = DataManager()
        data_manager.data = data
        data_manager.find_boundary()

        done = False
        while not done:
            RequestHandler.read_header(data_manager)
            RequestHandler.read_data(data_manager)
            done = RequestHandler.check_EOF(data_manager)

            file_name = data_manager.file_name
            file_body = data_manager.body

            if file_name == "":
                continue

            # If file is not supported
            if not WebLoaderServer.file_filter(file_name):
                self._send_json_error(400, file_name + " format not supported")
                return

            subfolder = os.path.join(folder, os.path.dirname(file_name))
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)

            file_path = os.path.join(folder, file_name)

            # rename on duplicates: file.txt -> file (n).txt
            reg = r'(.+/)([^/]+?)(?: \((\d+)\))?(\.\w+)'
            (path, name, copy, ext) = re.search(reg, file_path).groups()
            copy = 1 if copy is None else int(copy)

            while os.path.isfile(file_path):
                copy += 1
                file_path = '%s%s (%d)%s' % (path, name, copy, ext)

            # Create file
            with open(file_path, "wb") as f:
                f.write(file_body)

        self._send_json_success()

    @classmethod
    def read_file_name(cls, data):
        header = data.decode("utf-8")
        m = re.search('filename="(.*)"', header)
        return m.group(1)

    #looks for 2 newlines in a row. This marks the end of a header
    @classmethod
    def skip_header(cls, data_manager):
        curr = False
        last = False
        while True:
            data_manager.move_next()
            curr = data_manager.is_newline()
            if curr and last:
                data_manager.move_next()
                return
            last = curr

    @classmethod
    def read_header(cls, data_manager):
        start = data_manager.curr_index()
        cls.skip_header(data_manager)
        end = data_manager.curr_index()
        header = data_manager.split(start, end)
        data_manager.file_name = cls.read_file_name(header)

    #returns whether or not the current character is the beggining of the first line of the header
    @classmethod
    def is_header(cls, data_manager):
        curr_index = data_manager.curr_index()
        boundary = data_manager.boundary
        #increment by 1 so we don't compare the newline itself
        start = curr_index + data_manager.newline_length
        header_l = data_manager.split(start, start + len(boundary))
        return boundary == header_l

    #looks for header
    @classmethod
    def skip_data(cls, data_manager):
        while True:
            data_manager.find_newline()
            if cls.is_header(data_manager):
                return
            data_manager.move_next()

    @classmethod
    def read_data(cls, data_manager):
        start = data_manager.curr_index()
        cls.skip_data(data_manager)
        end = data_manager.curr_index()
        data_manager.body = data_manager.split(start, end)

    @classmethod
    def check_EOF(cls, data_manager):
        #read the newline before the boundary
        data_manager.move_next()
        #read the boundary
        for _ in range(len(data_manager.boundary)):
            data_manager.move_next()
        #check for EOF
        return not data_manager.is_newline()

    # Called on DELETE request
    def do_DELETE(self):
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            path = urllib.parse.unquote(path)
        except:
            Logs.warning("Error trying to parse request:\n", traceback.format_exc())
            self._send_json_error(200, "Parsing problem")
            return

        if not path.startswith('/files'):
            self._send_json_error(403, "Forbidden")
            return

        path = path[7:]
        if not path:
            self._send_json_error(403, "Forbidden")
            return

        path = os.path.join(FILES_DIR, path)

        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except:
            self._send_json_error(200, "Cannot find file to delete")
            return

        self._send_json_success()

    # Override to prevent HTTP server from logging every request if enable_logs is False
    def log_message(self, format, *args):
        if enable_logs:
            http.server.BaseHTTPRequestHandler.log_message(self, format, *args)

    # Check file last accessed time and remove those older than 28 days
    def file_cleanup(self):
        # don't execute more than once every 5 min
        if datetime.today() - WebLoaderServer.last_cleanup < timedelta(minutes=5):
            return

        WebLoaderServer.last_cleanup = datetime.today()
        expiry_date = datetime.today() - timedelta(days=WebLoaderServer.keep_files_days)

        for (dirpath, _, filenames) in os.walk(FILES_DIR):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                last_accessed = datetime.fromtimestamp(os.path.getatime(file_path))

                if last_accessed < expiry_date:
                    os.remove(file_path)

class WebLoaderServer():
    last_cleanup = datetime.fromtimestamp(0)
    keep_files_days = 0

    def __init__(self, port, keep_files_days):
        WebLoaderServer.keep_files_days = keep_files_days
        self.__process = Process(target=WebLoaderServer._start_process, args=(port,))

    @staticmethod
    def file_filter(name):
        valid_ext = (".pdb", ".sdf", ".cif", ".ppt", ".pptx", ".odp", ".pdf", ".png", ".jpg")
        return name.endswith(valid_ext)

    def start(self):
        self.__process.start()

    @classmethod
    def _start_process(cls, port):
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer(("", port), RequestHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
