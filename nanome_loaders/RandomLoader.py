import requests
import tempfile
import traceback
import os
import random
import numpy as np
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
url_file_summary = "https://www.rcsb.org/pdb/static.do?p=general_information/about_pdb/summaries.html"
local_protein_file = "./protein_list.txt"
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
        self.check_local_file(local_protein_file)
        #self.load_proteinlist(url_idx)
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
                Logs.debug("calling load_molecule")
                self.load_molecule(self.chosenProtein)

        # import the json menu
        menu = nanome.ui.Menu.io.from_json("random_loader_menu.json")
        menu.title = "Random Loader"
        menu.enabled = True
        self.menu = menu

        # Create all needed layout nodes
        ln_field = menu.root.find_node("text",True)
        ln_generate = menu.root.find_node("Generate",True)
        ln_load = menu.root.find_node("Load",True)
        
        # Create the label field
        self.__field = ln_field.get_content()

        # Create the generate button
        btn_generate = ln_generate.get_content()
        btn_generate.register_pressed_callback(generate_click)

        # Create the load button
        btn_load = ln_load.get_content()
        btn_load.register_pressed_callback(load_click)

        # Update menu
        self.update_menu(menu)

    # When user clicks on "Run", open menu
    def on_run(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    def load_molecule(self, code):
        Logs.debug("loading molecule")
        url_to_load = url.replace("{{NAME}}", code)
        print("url to load is: ",url_to_load)
        response = requests.get(url_to_load)
        file = tempfile.NamedTemporaryFile(delete=False)
        self._name = code
        try:
            Logs.debug("trying to load")
            file.write(response.text.encode("utf-8"))
            file.close()
            print(file.name)
            print(response.text.encode("utf-8")[:100])
            if type == "PDB":
                complex = nanome.structure.Complex.io.from_pdb(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            elif type == "SDF":
                complex = nanome.structure.Complex.io.from_sdf(path=file.name)
                self.bonds_ready([complex])
            elif type == "MMCIF":
                Logs.debug("complex is MMCIF")
                complex = nanome.structure.Complex.io.from_mmcif(path=file.name)
                self.add_bonds([complex], self.bonds_ready)
            else:
                Logs.error("Unknown file type")
        except: # Making sure temp file gets deleted in case of problem
            self._loading = False
            Logs.error("Error while loading molecule:\n", traceback.format_exc())
        os.remove(file.name)

    def check_local_file(self,file_name):
        # check if file_name exist
        if os.path.exists(file_name):
            Logs.debug("file exists")
            # try open it
            temp_list = []
            try:
                Logs.debug("start trying to load the local file")
                protein_file = open(file_name,"r")
                line = protein_file.readline()
                while line:
                    temp_list.append(line.strip()).tolist()
                    line = protein_file.readline()
                if len(temp_list)>1:
                    self.proteinList = temp_list
                else:
                    protein_file.close()
                    os.remove(file_name)
                    self.load_proteinlist(url_idx)

    
            # if failed, download it from the internet
            except:
                self.load_proteinlist(url_idx)
        # no local protein list file, download it
        else:
            Logs.debug("file does not exist")
            self.load_proteinlist(url_idx)
    # download the idx file of the list of all the protein on PDB and 
    # and parase it to an array 
    def load_proteinlist(self,idx_url):

        #download the list of all protein using the url 
        response = urllib.request.urlretrieve(url_idx)
        dl_file = open(response[0])
        indexFile = pd.read_csv(dl_file,header=3,sep=";")
        dl_file.close()
        os.remove(response[0])
        self.proteinList = indexFile['IDCODE'].str.strip()
        self.proteinCount = self.proteinList.shape[0]

        # write the protein list to a local file
        write_file = open(local_protein_file,"w")
        #np.savetxt(fname = local_protein_file,X = pd.Series(self.proteinList))
        with open(local_protein_file, 'w') as f:
            for item in self.proteinList:
                f.write("%s\n" % item)
        write_file.close()


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