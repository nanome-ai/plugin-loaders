import nanome
from nanome.util import Logs
from nanome.api.structure import Complex

from ._WebLoaderServer import _WebLoaderServer
from .Menu.MenuManager import MenuManager, PageTypes
from .PPTConverter import PPTConverter
import os
import socket
from timeit import default_timer as timer

SERVER_PORT = 80

# Plugin instance (for Nanome)
class WebLoader(nanome.PluginInstance):
    def start(self):
        self.running = False
        self.ppt_readers = []

    def update(self):
        if not self.running:
            return
        for ppt_reader in self.ppt_readers:
            ppt_reader.update()

        if (self.menu_manager.selected_page == self.menu_manager.home_page):
            if timer() - self.__timer >= 3.0:
                self.__refresh()
                self.__timer = timer()

    def __refresh(self):
        file_list = [filename for filename in os.listdir(os.path.join(os.path.dirname(__file__), '_WebLoader')) if _WebLoaderServer.file_filter(filename)]
        self.menu_manager.UpdateFiles(file_list)

    def on_run(self):
        self.running = True
        self.menu_manager = MenuManager(self, self.load_molecule)
        self.__timer = timer()

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

        if SERVER_PORT != 80:
            ip += ":" + str(SERVER_PORT)
        return ip

    def display_ppt(self, file_name):
        ppt_reader = PPTConverter()
        def done_delegate(images):
            if len(images) == 1:
                self.menu_manager.OpenPage(PageTypes.Image, images[0], file_name)
            elif len(images) > 1:
                self.menu_manager.OpenPage(PageTypes.PPT, images, file_name)
            self.ppt_readers.remove(ppt_reader)
        def error_delegate():
            #cleanup ppt_reader
            self.ppt_readers.remove(ppt_reader)
        self.ppt_readers.append(ppt_reader)
        ppt_reader.Convert(file_name, done_delegate, error_delegate)

def main():
    # Plugin server (for Web)
    server = _WebLoaderServer(SERVER_PORT)
    server.start()

    # Plugin
    plugin = nanome.Plugin("Load from Web", "Gives access to a folder of molecules that can be modified by a Web UI", "Loading", False)
    plugin.set_plugin_class(WebLoader)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()