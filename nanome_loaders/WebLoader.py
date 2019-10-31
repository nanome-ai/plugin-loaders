import nanome
from nanome.util import Logs
from nanome.util.enums import NotificationTypes
from nanome.api.structure import Complex

from .WebLoaderServer import WebLoaderServer
from .Menu.MenuManager import MenuManager, PageTypes
from .PPTConverter import PPTConverter
import sys
import os
import socket
from timeit import default_timer as timer

DEFAULT_SERVER_PORT = 80
DEFAULT_KEEP_FILES_DAYS = 0
FILES_DIR = os.path.expanduser('~/Documents/nanome-web-loader/shared')

# Plugin instance (for Nanome)
class WebLoader(nanome.PluginInstance):
    def start(self):
        self.running = False
        self.ppt_readers = {}
        self.files_dir = FILES_DIR
        self.current_dir = self.files_dir
        self.on_run()

    def update(self):
        if not self.running:
            return

        if self.menu_manager.selected_page == self.menu_manager.home_page:
            if timer() - self.__timer >= 3.0:
                for ppt_reader in self.ppt_readers.values():
                    ppt_reader.update()

                self.__refresh()
                self.__timer = timer()

        if timer() - self.big_timer >= 600:
            filtered_ppt_readers = {}
            for file in self.menu_manager.GetOpenFiles():
                for key, value in self.ppt_readers.items():
                    if not value.done or key.startswith(file):
                        filtered_ppt_readers[key] = value
            self.ppt_readers = filtered_ppt_readers
            self.big_timer = timer()

    def __refresh(self):
        items = os.listdir(self.current_dir)

        def isdir(item):
            return os.path.isdir(os.path.join(self.current_dir, item))

        files = [item for item in items if not isdir(item) and WebLoaderServer.file_filter(item)]
        folders = [item for item in items if isdir(item)]

        if self.current_dir != self.files_dir:
            folders.insert(0, '..')

        self.menu_manager.UpdateList(files, folders)

    def chdir(self, folder):
        self.current_dir = os.path.abspath(os.path.join(self.current_dir, folder))
        self.menu_manager.ClearList()

        # calculate breadcrumbs
        subpath = self.current_dir[len(self.files_dir):]
        path = 'folder: shared' + subpath.replace('/', ' / ')
        self.menu_manager.home_page.UpdateBreadcrumbs(path)

        self.__refresh()

    def on_run(self):
        self.running = True
        self.menu_manager = MenuManager(self, WebLoader.get_server_url(), self.load_molecule)
        self.chdir('.')
        self.__timer = timer()
        self.big_timer = timer()

    def load_molecule(self, name):
        complex_name = '.'.join(name.split(".")[:-1])
        extension = name.split(".")[-1]
        file_path = os.path.join(self.current_dir, name)

        if extension == "pdb":
            complex = Complex.io.from_pdb(path=file_path)
            complex.name = complex_name
            self.add_bonds([complex], self.bonds_ready)
        elif extension == "sdf":
            complex = Complex.io.from_sdf(path=file_path)
            complex.name = complex_name
            self.bonds_ready([complex])
        elif extension == "cif":
            complex = Complex.io.from_mmcif(path=file_path)
            complex.name = complex_name
            self.add_bonds([complex], self.bonds_ready)
        elif extension == "ppt" or extension == "pptx" or extension == "pdf":
            self.display_ppt(file_path)
        else:
            Logs.warning("Unknown file extension for file", name)
            return

    def save_molecule(self, save_type, complex):
        path = os.path.join(self.current_dir, complex.name)

        if save_type == "PDB":
            complex.io.to_pdb(path + ".pdb")
        elif save_type == "SDF":
            complex.io.to_sdf(path + ".sdf")
        elif save_type == "MMCIF":
            complex.io.to_mmcif(path + ".cif")

        self.send_notification(NotificationTypes.success, complex.name + " saved")

    def bonds_ready(self, complex_list):
        self.add_dssp(complex_list, self.send_complexes)

    def send_complexes(self, complex_list):
        self.add_to_workspace(complex_list)

    @staticmethod
    def get_server_url():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()

        if DEFAULT_SERVER_PORT != 80:
            ip += ":" + str(DEFAULT_SERVER_PORT)
        return ip

    def display_ppt(self, file_name):
        key = os.path.basename(file_name) + str(os.path.getmtime(file_name))
        if key in self.ppt_readers:
            ppt_reader = self.ppt_readers[key]
        else:
            ppt_reader = PPTConverter(file_name)
            self.ppt_readers[key] = ppt_reader
        def done_delegate(images):
            if len(images) == 1:
                self.menu_manager.OpenPage(PageTypes.Image, images[0], file_name)
            elif len(images) > 1:
                self.menu_manager.OpenPage(PageTypes.PPT, images, file_name)
        def error_delegate():
            #cleanup ppt_reader
            pass
        ppt_reader.Convert(done_delegate, error_delegate)

def main():
    # Plugin server (for Web)
    web_port = DEFAULT_SERVER_PORT
    keep_files_days = DEFAULT_KEEP_FILES_DAYS

    try:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-w":
                web_port = int(sys.argv[i + 1])
            elif sys.argv[i] == "-k":
                keep_files_days = int(sys.argv[i + 1])
    except:
        pass
    server = WebLoaderServer(web_port, keep_files_days)
    server.start()

    # Plugin
    plugin = nanome.Plugin("Load from Web", "Gives access to a folder of molecules that can be modified by a Web UI", "Loading", False)
    plugin.set_plugin_class(WebLoader)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
