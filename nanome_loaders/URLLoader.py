import requests
import tempfile
import traceback
import os

import nanome
from nanome.util import Logs

##################
##### CONFIG #####
##################

version = "01"
default_ext = "pdb"
# {{NAME}} indicates where to write molecule code
url = "http://resdev.gene.com/gyst/str/STR{{NAME}}_{{VERSION}}.{{EXT}}".replace("{{VERSION}}", str(version))

##################
##################
##################

class URLLoader(nanome.PluginInstance):
    def start(self):
        self._loading = False

        def btn_click(button):
            if self._loading == True:
                return
            self._loading = True
            self.turn_on_overlay(self.__field.input_text)
            self.load_molecule(self.__field.input_text)

        # Request and set menu window
        menu = nanome.ui.Menu.io.from_json('Menu/URLLoader.json')
        self.menu = menu

        # Create the text field
        self.__field = menu.root.find_node('Input').get_content()
        self._ln_overlay = menu.root.find_node('Input Overlay')
        self._label_version = menu.root.find_node('Version').get_content()
        self._label_version.text_value = "_"+version
        self._ln_extension = menu.root.find_node('Extension')

        self._ln_extension.get_content().input_text = default_ext
        # Create the load button
        btn = menu.root.find_node('Load').get_content()
        btn.register_pressed_callback(btn_click)

        # Update menu
        self.update_menu(menu)

    # When user clicks on "Run", open menu
    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    def load_molecule(self, code):
        ext = self._ln_extension.get_content().input_text.lower()
        url_to_load = url.replace("{{NAME}}", code).replace("{{EXT}}", ext)
        response = requests.get(url_to_load)
        file = tempfile.NamedTemporaryFile(delete=False)
        self._name = code
        try:
            file.write(response.text.encode("utf-8"))
            file.close()
            if ext == "pdb":
                complex = nanome.structure.Complex.io.from_pdb(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            elif ext == "sdf":
                complex = nanome.structure.Complex.io.from_sdf(path=file.name)
                self.bonds_ready([complex])
            elif ext == "cif":
                complex = nanome.structure.Complex.io.from_mmcif(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            else:
                Logs.error("Unknown file extension")
        except: # Making sure temp file gets deleted in case of problem
            self._loading = False
            Logs.error("Error while loading molecule:\n", traceback.format_exc())
        os.remove(file.name)

    def bonds_ready(self, complex_list):
        self.add_dssp(complex_list, self.complex_ready)

    def complex_ready(self, complex_list):
        self._loading = False
        self.turn_off_overlay()
        complex_list[0].molecular.name = self._name
        self.add_to_workspace(complex_list)

    def turn_on_overlay(self, text):
        self._ln_overlay.enabled = True
        self._ln_overlay.get_content().color = nanome.util.color.Color(240, 240, 240, 255)
        self._ln_overlay.find_node('Overlay Text').get_content().text_value = text
        self.update_menu(self.menu)

    def turn_off_overlay(self):
        self._ln_overlay.enabled = False
        self.update_menu(self.menu)

def main():
    plugin = nanome.Plugin("URL Loader", "Load molecule from database", "Loading", False)
    plugin.set_plugin_class(URLLoader)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()