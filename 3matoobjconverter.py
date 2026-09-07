# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 2023
Modified on Fri Sep 4 2026

@author: Gxiraudon
@forked by: Jarred

3d modeling app 3ma to obj converter with Tkinter GUI
"""

import json
import threading
import asyncio
import os

# Gui
import tkinter as tk
from tkinter import font
import tkinter.messagebox as messagebox
from tkinter import filedialog as fd

# The global variables of input and output paths
input_filename_3ma = ""
output_filename_3ma = ""

class Application:
    # ------Status Bar Manipulation------
    # Set Status Text Function
    async def setStatusText(self, statusText, length=1, *args, **kwargs):
        self.statusbar.config(text=statusText)
        await asyncio.sleep(length)
        self.statusbar.config(text="Ready")

    # Convertion Status   
    async def convertingStatus(self):
        await self.setStatusText("Converting to OBJ")

    async def doneStatus(self):
        await self.setStatusText("Convert Done")

    # Browse File Status
    async def inputImportDoneStatus(self):
        await self.setStatusText("Input File Loaded", 2)

    async def outputImportDoneStatus(self):
        await self.setStatusText("Output File Loaded", 2)

    async def inputImportCancelledStatus(self):
        await self.setStatusText("Input File Load Cancelled by User", 2)

    async def outputImportCancelledStatus(self):
        await self.setStatusText("Output File Load Cancelled by User", 2)   

    # ------Get Entry Texts------
    def getInputBox(self):
        inputText = self.inputBox.get()
        return inputText

    def getOutputBox(self):
        outputText = self.outputBox.get()
        return outputText
        
    # ------Clear/Set Entrys------
    def setInputBox(self, inputText):
        self.inputBox.delete(0, tk.END)
        self.inputBox.insert(0, inputText)
        
    def setOutputBox(self, outputText):
        self.outputBox.delete(0, tk.END)
        self.outputBox.insert(0, outputText)

    # ------Check Path Exists or Empty------
    def checkInputPathExist(self):
        strInputPath = self.getInputBox()
        if not os.path.exists(strInputPath):
            messagebox.showerror(
                "Error",
                "The path in the input file does not exist",
                parent=self.root
            )
            return False
        else:
            return True

    def checkOutputPathExist(self):
        strOutputPath = self.getOutputBox()
        if not os.path.isdir(os.path.dirname(strOutputPath)):
            messagebox.showerror(
                "Error",
                "The path in the output file does not exist",
                parent=self.root
            )
            return False
        else:
            return True

    def checkInputPathEmpty(self):
        strInputPath = self.getInputBox()
        if not strInputPath:
            messagebox.showerror(
                "Error",
                "The path in the input box is left empty",
                parent=self.root
            )
            return True
        else:
            return False

    def checkOutputPathEmpty(self):
        strOutputPath = self.getOutputBox()
        if not strOutputPath:
            messagebox.showerror(
                "Error",
                "The path in the output box is left empty",
                parent=self.root
            )
            return True
        else:
            return False

    # code from the author: Gxiraudon
    def convert(self):
        global input_filename_3ma, output_filename_3ma
        file_3ma = open(input_filename_3ma)
        fjile_3ma = json.loads(file_3ma.read())
        fout = open(output_filename_3ma,"wt")
        vertex_index = 0
        prev_vertex_index = vertex_index
        forward = 0
        meshes = fjile_3ma["meshes"]
        mesh_num = len(meshes)

        asyncio.run(self.convertingStatus())

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
        asyncio.run(self.doneStatus())

    # ------Events------    
    # Input Browse on Click
    def on_input_browse_click(self):
        global input_filename_3ma
        filterInput = [
            ("3ma Files", "*.3ma"),
            ("All Files", "*.*")
        ]

        input_selection = fd.askopenfilename(
            title="Open 3ma File...",
            filetypes=filterInput            
        )

        if input_selection:
            input_filename_3ma = input_selection
            #self.inputBox.config(text=input_selection)
            self.setInputBox(input_selection)
            asyncio.run(self.inputImportDoneStatus())            
        else:
            asyncio.run(self.inputImportCancelledStatus())

    # Output Browse on Click
    def on_output_browse_click(self):
        global output_filename_3ma
        filterOutput = [
            ("Obj Files", "*.obj"),
            ("All Files", "*.*")
        ]

        output_selection = fd.asksaveasfilename(
            title="Save Converted obj File as...",
            filetypes=filterOutput            
        )

        if output_selection:
            output_filename_3ma = output_selection
            #self.outputBox.config(text=output_selection)
            self.setOutputBox(output_selection)
            asyncio.run(self.outputImportDoneStatus())            
        else:
            asyncio.run(self.outputImportCancelledStatus())

    # Convert Button on Click
    def on_convert_click(self):
        if self.checkInputPathExist() == False:
            return
        if self.checkOutputPathExist() == False:
            return
        if self.checkInputPathEmpty() == True:
            return
        if self.checkOutputPathEmpty() == True:
            return

        convertThread = threading.Thread(
            target=self.convert
        )

        convertThread.start()      
        convertThread.join()

    def main(self):
        # ------Root------
        self.root = tk.Tk()
        self.root.geometry("500x445")
        self.root.update_idletasks()

        # ------Title, Controls, and Footer------
        self.title = tk.Label(
            self.root,
            text="3ma To Obj Converter",
            bg="#000555",
            foreground="#FFFFFF",
            font=font.Font(weight="bold", size=45)
        )
        self.title.pack(
            side="top",
            fill="both"           
        )

        """
        winwidth = self.root.winfo_width()
        winheight = self.root.winfo_height()
        """

        self.controlLayout = tk.Frame(
            self.root,            
        )
        self.controlLayout.pack_propagate(True)
        self.controlLayout.place(
            relx=0.5, rely=0.5, 
            anchor="center"
        )

        self.inputText = tk.Label(
            self.controlLayout,
            text="Input File:"
        )
        self.inputText.pack(
            anchor="nw",
            padx=10,
            pady=10
        )

        self.inputBox = tk.Entry(
            self.controlLayout    
        )
        self.inputBox.pack(
            fill="both",
            padx=20,
            pady=10
        )

        self.browseInputButton = tk.Button(
            self.controlLayout,
            text="...",
            bg="#050055",
            foreground="#FFFFFF",
            command=self.on_input_browse_click
        )
        self.browseInputButton.pack(
            anchor="ne",
            padx=23
        )

        self.outputText = tk.Label(
            self.controlLayout,
            text="Converted Output File:"
        )
        self.outputText.pack(
            anchor="nw",
            padx=10,
            pady=10
        )

        self.outputBox = tk.Entry(
            self.controlLayout    
        )
        self.outputBox.pack(
            fill="both",
            padx=20,
            pady=10
        )

        self.browseOutputButton = tk.Button(
            self.controlLayout,
            text="...",
            bg="#050055",
            foreground="#FFFFFF",
            command=self.on_output_browse_click
        )
        self.browseOutputButton.pack(
            anchor="ne",
            padx=23
        )

        self.convertButton = tk.Button(
            self.controlLayout,
            text="Convert Now",
            bg="#050055",
            foreground="#FFFFFF",
            command=self.on_convert_click
        )
        self.convertButton.pack(
            pady=23
        )

        self.statusbar = tk.Label(
            self.root,
            text="Ready",
            bg="#000555",
            foreground="#FFFFFF",
            font=font.Font(weight="bold", size=14)
        )
        self.statusbar.pack(
            side="bottom",
            fill="both"           
        )

        self.footer = tk.Label(
            self.root,
            text="author: Gxiraudon | forked by: Jarred",
            bg="#000555",
            foreground="#FFFFFF",
            font=font.Font(weight="bold", size=14)
        )
        self.footer.pack(
            side="bottom",
            fill="both"           
        )

        # ------MainLoop------        
        tk.mainloop()

if __name__ == "__main__":
    Application().main()