import nanome
from nanome.util import Logs
from nanome.api.structure import Complex

from _APILoaderServer import APILoaderServer
from _APILoaderMenu import APILoaderMenu

import os
import socket
from timeit import default_timer as timer

SERVER_PORT = 80

# Plugin instance (for Nanome)
class APILoader(nanome.PluginInstance):
    def start(self):
        self.__menu = APILoaderMenu(self)
        self.__menu.build_menu(APILoader.get_server_url())
        self.__refresh()
        self.__timer = timer()

    def update(self):
        if timer() - self.__timer >= 3.0:
            self.__refresh()
            self.__timer = timer()

    def __refresh(self):
        file_list = [filename for filename in os.listdir("_APILoader") if APILoaderServer.file_filter(filename)]
        self.__menu.update_list(file_list)

    def on_run(self):
        self.__menu.open_menu()

    def load_molecule(self, name):
        extension = name.split(".")[-1]
        if extension == "pdb":
            complex = Complex.io.from_pdb("_APILoader/" + name)
            self.add_bonds([complex], self.send_complexes)
            return
        elif extension == "sdf":
            complex = Complex.io.from_sdf("_APILoader/" + name)
        elif extension == "cif":
            complex = Complex.io.from_mmcif("_APILoader/" + name)
            self.add_bonds([complex], self.send_complexes)
            return
        else:
            Logs.warning("Unknown file extension for file", name)
            return
        self.send_complexes([complex])

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
    # Plugin server (for API)
    server = APILoaderServer(SERVER_PORT)
    server.start()

    # Plugin
    plugin = nanome.Plugin("Load from Web", "Gives access to a folder of molecules that can be modified by a Web API", "Loading", False)
    plugin.set_plugin_class(APILoader)
    plugin.run('127.0.0.1', 8888)