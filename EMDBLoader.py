import requests
import tempfile
import traceback
import os
import nanome
from nanome.util import Logs

##################
##### CONFIG #####
##################

url = "ftp://ftp.wwpdb.org/pub/emdb/structures/EMD-{{NAME}}/map/emd_{{NAME}}.map.gz" # {{NAME}} indicates where to write emdb code
type = "EM"

##################
##################
##################

class EMDBLoader(nanome.PluginInstance):
    def start(self):
        def btn_click(button):
            self.load_cry_em(self.__field.input_text)

        # Request and set menu window
        menu = nanome.ui.Menu.get_plugin_menu()
        menu.title = "EM DB Loader"
        menu._width = 0.8
        menu._height = 0.7
        menu.enabled = True
        self.__menu = menu

        # Create all needed layout nodes
        menu.root.clear_children()
        content = menu.root.create_child_node()
        ln_field = content.create_child_node()
        ln_field.forward_dist = .03 # TMP, should be fixed soon
        ln_field.set_padding(top=0.07, down=0.04)
        ln_button = content.create_child_node()
        ln_button.set_padding(top=0.1)

        # Create the text field
        self.__field = ln_field.add_new_text_input()
        self.__field.placeholder_text = "EMDB Code"

        # Create the load button
        btn = ln_button.add_new_button(text="Load")
        btn.register_pressed_callback(btn_click)

        # Update menu
        self.update_menu(menu)

    # When user clicks on "Run", open menu
    def on_run(self):
        self.__menu.enabled = True
        self.update_menu(self.__menu)

    def load_cry_em(self, code):
        url_to_load = url.replace("{{NAME}}", code)
        response = requests.get(url_to_load)
        file = tempfile.NamedTemporaryFile(delete=False)
        self._name = code
        try:
            file.write(response.text.encode("utf-8"))
            file.close()
            self.upload_cyro_em(file.name, self.on_em_uploaded)
        except: # Making sure temp file gets deleted in case of problem
            Logs.error("Error while loading data:\n", traceback.format_exc())
        os.remove(file.name)

    def on_em_uploaded(self):
        pass

if __name__ == "__main__":
    plugin = nanome.Plugin("EM DB Loader", "Load a cryo-EM file from database", "Loading", False)
    plugin.set_plugin_class(EMDBLoader)
    plugin.run('127.0.0.1', 8888)