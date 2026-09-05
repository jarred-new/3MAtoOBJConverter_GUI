# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 19:04:09 2023

@author: Gxiraudon
@forked by: Jarred

3d modeling app 3ma to obj converter with Tkinter GUI
"""

import json

# Gui
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog 

# The global variables of input and output paths
input_filename_3ma = ""
output_filename_3ma = ""

class Application:
    def convert(self):
        file_3ma = open(input_filename_3ma)
        fjile_3ma = json.loads(file_3ma.read())
        fout = open(output_filename_3ma,"wt")
        vertex_index = 0
        prev_vertex_index = vertex_index
        forward = 0
        meshes = fjile_3ma["meshes"]
        mesh_num = len(meshes)
        
        for msh in range(mesh_num):
            
            fout.write("\ng \n")
            preciseFactor = meshes[msh]["preciseFactor"]
            prev_vertex_index = vertex_index
            for vtx in range(0,len(meshes[msh]["_positions"]),3):
                _pos_0 = meshes[msh]["_positions"][vtx]/preciseFactor 
                _pos_1 = meshes[msh]["_positions"][vtx+1]/preciseFactor 
                _pos_2 = (meshes[msh]["_positions"][vtx+2]*-1)/preciseFactor 
                vtx_string = "v "+str(_pos_0)+" "+str(_pos_1)+" "+str(_pos_2)+"\n"
                fout.write(vtx_string)
                vertex_index = vertex_index+1
                
            if msh>0:
                forward = 1
            
            UnivertsList = meshes[msh]["facesUnivertsList"]
            fout.write("\ng name"+str(msh)+" \n")
            for fcx in UnivertsList:
                fout.write("f")
                for fcx_ndx in fcx["u"]:
                    fout.write(" "+str(fcx_ndx+1+(forward*prev_vertex_index)))
                fout.write("\n")    
        
        file_3ma.close()
        fout.close()
        
    def main(self):
        self.root = tk.Tk()
        tk.mainloop()
        
if __name__ == "__main__":
    Application().main()