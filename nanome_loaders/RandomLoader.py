import requests
import tempfile
import traceback
import os
import random
import numpy
import pandas as pd
import urllib.request
import nanome
from nanome.util import Logs

##################
##### CONFIG #####
##################

url = "https://files.rcsb.org/download/{{NAME}}.cif" # {{NAME}} indicates where to write molecule code
type = "MMCIF" # PDB / SDF / MMCIF
url_idx = "ftp://ftp.wwpdb.org/pub/pdb/derived_data/index/author.idx"
##################
##################
##################

class RandomLoader(nanome.PluginInstance):
    def start(self):
        self._loading = False
        self.proteinCount = 0
        self.randomIndex=0
        self.proteinList=['2r73']
        self.chosenProtein='2r73'
        self.load_proteinlist(url_idx)
        self.hasGenerated=0
       

        def generate_click(button):
            self.randomIndex = random.randint(0,self.proteinCount)
            self.chosenProtein = self.proteinList[self.randomIndex]
            self.__field.text_value=self.chosenProtein
            self.update_menu(self.menu)
            self.hasGenerated=1


        def load_click(button):                
            if self._loading == True:
                return
            self._loading = True
            if self.hasGenerated==0:
                self.__field.text_value="Please Generate"
                self.update_menu(self.menu)
            else:
                self.load_molecule(self.chosenProtein)

        
        # Request and set menu window
        menu = self.menu
        menu.title = "Random Loader"
        menu._width = 0.8
        menu._height = 0.7
        menu.enabled = True

        # Create all needed layout nodes
        menu.root.clear_children()
        content = menu.root.create_child_node()
        ln_field = content.create_child_node()
        ln_field.forward_dist = .03 # TMP, should be fixed soon
        ln_field.set_padding(left=0.05,right=0.05,top=0.1, down=0.1)
        ln_btns = content.create_child_node()
        ln_btns.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.horizontal
        ln_generate = ln_btns.create_child_node()
        ln_generate.set_padding()
        ln_load = ln_btns.create_child_node()
        ln_load.set_padding()

        # Create the label field
       
        self.__field = ln_field.add_new_label(text="Click buttons below to generate a random protein and load it")
        self.__field.text_size=0

        # Create the generate button
        btn_generate = ln_generate.add_new_button(text="Generate")
        btn_generate.ButtonText.size=0.5
        btn_generate.register_pressed_callback(generate_click)

        # Create the load button
        btn_load = ln_load.add_new_button(text="Load")
        btn_load.register_pressed_callback(load_click)

        # Update menu
        self.update_menu(menu)

        

    # When user clicks on "Run", open menu
    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    def load_molecule(self, code):
        url_to_load = url.replace("{{NAME}}", code)
        response = requests.get(url_to_load)
        file = tempfile.NamedTemporaryFile(delete=False)
        self._name = code
        try:
            file.write(response.text.encode("utf-8"))
            file.close()
            if type == "PDB":
                complex = nanome.structure.Complex.io.from_pdb(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            elif type == "SDF":
                complex = nanome.structure.Complex.io.from_sdf(path=file.name)
                self.bonds_ready([complex])
            elif type == "MMCIF":
                complex = nanome.structure.Complex.io.from_mmcif(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            else:
                Logs.error("Unknown file type")
        except: # Making sure temp file gets deleted in case of problem
            self._loading = False
            Logs.error("Error while loading molecule:\n", traceback.format_exc())
        os.remove(file.name)

    #download the idx file of the list of all the protein on PDB and 
    #and parase it to an array 
    def load_proteinlist(self,idx_url):
        # response = requests.get(idx_url)
        # file = tempfile.NamedTemporaryFile(delete=False)
        # try:
        #     file.write(response.text.encode("utf-8"))
        #     file.close()
        #     self.proteinFile = open(file) #the list of all the protein in the file
            
        #     self.line = self.proteinFile.readline()
        #     #loop through the whole file to get all the protein and construct the list of proteins
        #     while self.line:
        #         proteinName=self.line.strip()
        #         self.proteinCount+=1
        #         self.proteinList.append(proteinName)
        #         self.line = self.proteinFile.readline()
            

        # except:
        #     Logs.error("Error while downloading the protein list")
        # os.remove(file.name)

     #download the list of all protein using the url 
        try:
            response=urllib.request.urlretrieve(url_idx)
            file=open(response[0])
            indexFile = pd.read_csv(file,header=3,sep=";")
            file.close()
            os.remove(response[0])
            self.proteinList=indexFile['IDCODE']
            self.proteinCount=self.proteinList.shape[0]
        except:
            Logs.error("failed to download the list of all the protein from PDB")





    def bonds_ready(self, complex_list):
        self.add_dssp(complex_list, self.complex_ready)

    def complex_ready(self, complex_list):
        self._loading = False
        complex_list[0].molecular.name = self._name
        self.add_to_workspace(complex_list)

def main():
    plugin = nanome.Plugin("Random Loader", "Load a random molecule", "Loading", False)
    plugin.set_plugin_class(RandomLoader)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()