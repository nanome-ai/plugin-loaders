import nanome
from nanome.util import Logs
from nanome.api.structure import Complex

from _WebLoaderServer import WebLoaderServer
from _WebLoaderMenu import WebLoaderMenu

import os
import socket
from timeit import default_timer as timer

SERVER_PORT = 80

# Plugin instance (for Nanome)
class WebLoader(nanome.PluginInstance):
    def start(self):
        self.__menu = WebLoaderMenu(self)
        self.__menu.build_menu(WebLoader.get_server_url())
        self.__refresh()
        self.__timer = timer()

    def update(self):
        if timer() - self.__timer >= 3.0:
            self.__refresh()
            self.__timer = timer()

    def __refresh(self):
        file_list = [filename for filename in os.listdir("_WebLoader") if WebLoaderServer.file_filter(filename)]
        self.__menu.update_list(file_list)

    def on_run(self):
        self.__menu.open_menu()

    def load_molecule(self, name):
        extension = name.split(".")[-1]
        if extension == "pdb":
            complex = Complex.io.from_pdb("_WebLoader/" + name)
            self.add_bonds([complex], self.bonds_ready)
            return
        elif extension == "sdf":
            complex = Complex.io.from_sdf("_WebLoader/" + name)
            self.bonds_ready([complex])
        elif extension == "cif":
            complex = Complex.io.from_mmcif("_WebLoader/" + name)
            self.add_bonds([complex], self.bonds_ready)
            return
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

if __name__ == "__main__":
    # Plugin server (for Web)
    server = WebLoaderServer(SERVER_PORT)
    server.start()

    # Plugin
    plugin = nanome.Plugin("Load from Web", "Gives access to a folder of molecules that can be modified by a Web UI", "Loading", False)
    plugin.set_plugin_class(WebLoader)
    plugin.run('127.0.0.1', 8888)