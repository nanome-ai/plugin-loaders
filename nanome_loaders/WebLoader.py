import nanome
from nanome.util import Logs
from nanome.api.structure import Complex

from .WebLoaderServer import WebLoaderServer
from .Menu.MenuManager import MenuManager, PageTypes
from .PPTConverter import PPTConverter
import sys
import os
import socket
from timeit import default_timer as timer

DEFAULT_SERVER_PORT = 80

# Plugin instance (for Nanome)
class WebLoader(nanome.PluginInstance):
    def start(self):
        self.running = False
        self.ppt_readers = {}

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
        files = [filename for filename in os.listdir(os.path.join(os.path.dirname(__file__), '_WebLoader')) if WebLoaderServer.file_filter(filename)]
        self.menu_manager.UpdateFiles(files)

    def diff_files(self, old_files, new_files):
        old_files = set(old_files)
        new_files = set(new_files)
        remove_files = old_files - new_files
        add_files = new_files - old_files
        return add_files, remove_files

    def on_run(self):
        self.running = True
        self.menu_manager = MenuManager(self, WebLoader.get_server_url(), self.load_molecule)
        self.__refresh()
        self.__timer = timer()
        self.big_timer = timer()

    def load_molecule(self, name):
        extension = name.split(".")[-1]
        file_path = os.path.join(os.path.dirname(__file__), '_WebLoader/') + name
        if extension == "pdb":
            complex = Complex.io.from_pdb(path=file_path)
            self.add_bonds([complex], self.bonds_ready)
            return
        elif extension == "sdf":
            complex = Complex.io.from_sdf(path=file_path)
            self.bonds_ready([complex])
        elif extension == "cif":
            complex = Complex.io.from_mmcif(path=file_path)
            self.add_bonds([complex], self.bonds_ready)
            return
        elif extension == "ppt" or extension == "pptx" or extension == "pdf":
            self.display_ppt(file_path)
        else:
            Logs.warning("Unknown file extension for file", name)
            return

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
    try:
        for i in range(len(sys.argv)):
            if sys.argv[i] == "-w":
                web_port = int(sys.argv[i + 1])
    except:
        pass
    server = WebLoaderServer(web_port)
    server.start()

    # Plugin
    plugin = nanome.Plugin("Load from Web", "Gives access to a folder of molecules that can be modified by a Web UI", "Loading", False)
    plugin.set_plugin_class(WebLoader)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
