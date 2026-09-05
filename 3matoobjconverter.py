# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 2023
Modified on Fri Sep 4 2026

@author: Gxiraudon
@forked by: Jarred

3d modeling app 3ma to obj converter with Tkinter GUI
"""

import json

# Gui
import tkinter as tk
from tkinter import font
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
        # ------Root------
        self.root = tk.Tk()
        self.root.geometry("500x445")
        
        # ------Title and Controls------
        self.title = tk.Label(
            self.root,
            text="3ma To Obj Converter",
            bg="#000555",
            foreground="#FFFFFF",
            font=font.Font(weight="bold", size=45)
        )
        self.title.pack(
            fill="both"           
        )
        
        self.inputText = tk.Label(
            self.root,
            text="Input File:"
        )
        self.inputText.pack(
            anchor="nw",
            padx=10,
            pady=10
        )
        
        self.inputBox = tk.Entry(
            self.root    
        )
        self.inputBox.pack(
            fill="both",
            padx=20,
            pady=10
        )
        
        self.browseInputButton = tk.Button(
            self.root,
            text="...",
            bg="#050055",
            foreground="#FFFFFF"
        )
        self.browseInputButton.pack(
            anchor="ne",
            padx=23
        )
        
        self.outputText = tk.Label(
            self.root,
            text="Converted Output File:"
        )
        self.outputText.pack(
            anchor="nw",
            padx=10,
            pady=10
        )
        
        self.outputBox = tk.Entry(
            self.root    
        )
        self.outputBox.pack(
            fill="both",
            padx=20,
            pady=10
        )
        
        self.browseInputButton = tk.Button(
            self.root,
            text="...",
            bg="#050055",
            foreground="#FFFFFF"
        )
        self.browseInputButton.pack(
            anchor="ne",
            padx=23
        )
        
        self.convertButton = tk.Button(
            self.root,
            text="Convert Now",
            bg="#050055",
            foreground="#FFFFFF"
        )
        self.convertButton.pack(
            pady=23
        )
        
        # ------MainLoop------
        tk.mainloop()
        
if __name__ == "__main__":
    Application().main()