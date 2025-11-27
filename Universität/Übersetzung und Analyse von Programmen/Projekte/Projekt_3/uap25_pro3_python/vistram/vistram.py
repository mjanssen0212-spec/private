# (c) Stephan Diehl, University of Trier, Germany, 2025


import tkinter as tk
from copy import deepcopy
from tkinter import ttk
from tkinter import filedialog
import os

from assembler import *
from tram import *

import inspect
import re

"""
test_prog1=[const(1), const(2), const(5), store(1, 0), load(1, 0), add(), halt()]

L4=Label(4)
L7=Label(7)
L15=Label(15)
test_prog2=[const(4),
            const(10),
            invoke(2,L4,0),
            halt(),
            load(0,0,assigned_label=L4),
            invoke(1,L7,0),
            ireturn(),
            load(0,0,assigned_label=L7),
            load(0,0),
            mul(),
            load(1,1),
            gt(),
            ifzero(L15),
            load(0,0),
            ireturn(),
            load(0,0,assigned_label=L15),
            load(0,0),
            mul(),
            ireturn()]
"""

class AbstractMachine(TRAM):
    def __init__(self):
        self.initial_program = [] #Assembler.read_tram_code("examples/tramprograms/test.tram")
        #self.initial_program = test_prog2
        print(self.initial_program)
        self.reset()

    def reset(self):
        super().__init__(self.initial_program)
        self.program_text = [f"{instr.toString()}" for i, instr in enumerate(self.program)]
        self.running = False

    def step(self):
        if self.pc >= len(self.program):
            self.running = False
            return ("Error: End of program store reached!", None)

        if self.pc == -1:
            self.running = False
            return ("The program terminated normally!", None)

        instr=self.program[self.pc]
        self.print_instruction(instr)
        instr.execute(self)

        return (f"Ausgeführt: {instr.toString()}", instr)

class MachineUI:
    def __init__(self, root):
        self.root = root
        self.machine = AbstractMachine()
        self.previous_state = None
        self.minimal_vis = False
        self.current_instruction = None

        root.title("Visual TRAM")

        # Frames
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)

        display_frame = ttk.Frame(root)
        display_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Buttons
        ttk.Button(control_frame, text="Start", command=self.start).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Stop", command=self.stop).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Step", command=self.step).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset).grid(row=0, column=3, padx=5)
        button = ttk.Button(control_frame, text="Open File", command=self.open_file).grid(row=0, column=4, padx=5)

        # Add a label to show the selected file
        self.label = ttk.Label(root, text="No file selected.", wraplength=800, justify="center")
        self.label.pack(pady=20)

        # Add a button to open the file browser
        #button = ttk.Button(root, text="Open File", command=self.open_file)
        #button.pack(pady=10)

        # Textfelder
        self.code_text = tk.Text(display_frame, width=35, height=32, wrap="none", bg="#f8f8f8")
        self.code_text.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        self.code_text.tag_configure('highlight', background='#AAFFAA')

        self.prev_state_text = tk.Text(display_frame, width=35, height=32, wrap="none", bg="#f0f8ff")
        self.prev_state_text.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.state_text = tk.Text(display_frame, width=35, height=32, wrap="none", bg="#f0f8ff")
        self.state_text.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.instr_text = tk.Text(display_frame, width=70, height=32, wrap="none", bg="#f0f8ff")
        self.instr_text.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.state_text.tag_configure('blue', background='#AAAAFF')
        self.prev_state_text.tag_configure('blue', background='#AAAAFF')

        self.update_display()

    def update_display(self):
        # Programmkode anzeigen
        self.code_text.delete("1.0", tk.END)
        for i, line in enumerate(self.machine.program_text):
            if i == self.machine.pc:
                prefix = "-> "
                self.code_text.insert(tk.END, f"{prefix}{i:02d}: {line}\n",'highlight')
            else:
                self.code_text.insert(tk.END, f"   {i:02d}: {line}\n")

        # Maschinenzustand anzeigen
        self.update_state_display(self.machine, self.state_text)
        if self.previous_state!=None:
            self.update_state_display(self.previous_state, self.prev_state_text)
        else:
            self.prev_state_text.delete("1.0", tk.END)
        self.previous_state = deepcopy(self.machine)

        # Aktuell ausgeführte Instruktion anzeigen
        if self.current_instruction != None:
            (msg,instr) = self.current_instruction
            self.instr_text.delete("1.0", tk.END)
            self.instr_text.insert(tk.END, f"\n{msg}\n\n")
            if instr!=None:
                source_text= inspect.getsource(instr.execute)
                source_text=source_text.replace("tram.","")
                rest = source_text.split('\n', 1)[1] if '\n' in source_text else source_text
                source_text = '\n'.join(line.lstrip() for line in rest.splitlines())
                self.instr_text.insert(tk.END, source_text)
        else:
            self.instr_text.delete("1.0", tk.END)


    def update_state_display(self, machine, tk_text):
        tk_text.delete("1.0", tk.END)
        tk_text.insert(tk.END, f"PC : {machine.pc}\n")
        tk_text.insert(tk.END, f"FP : {machine.fp}\n")
        tk_text.insert(tk.END, f"PP : {machine.pp}\n")
        tk_text.insert(tk.END, f"TOP: {machine.top}\n\n")
        if (self.minimal_vis == True):
            tk_text.insert(tk.END, f"Stack: {machine.stack}\n")
        else:
            for i, value in enumerate(machine.stack):
                suffix = " "
                if i == machine.top: suffix += "<-TOP "
                if i == machine.pp: suffix += "<-PP "
                if i == machine.fp: suffix += "<-FP "
                if i == machine.fp + 4: suffix += "<-end of frame "
                if i >= machine.pp and i < machine.fp + 5:
                    tk_text.insert(tk.END, f"{i:02d}: {value}{suffix}\n", 'blue')
                else:
                    tk_text.insert(tk.END, f"{i:02d}: {value}{suffix}\n")
    def start(self):
        self.machine.running = True
        self.run_next()

    def stop(self):
        self.machine.running = False

    def step(self):
        self.current_instruction = self.machine.step()
        self.update_display()


    def run_next(self):
        if self.machine.running:
            self.step()
            #msg = self.machine.step()
            #self.update_display()
            #if msg:
            #    self.state_text.insert(tk.END, f"\n{msg}\n")
            if self.machine.running:
                self.root.after(500, self.run_next)  # Automatische Ausführung

    def reset(self):
        self.machine.reset()
        self.previous_state=None
        self.current_instruction=None
        self.update_display()

    def open_file(self):
        # Define the starting directory
        start_dir = os.path.expanduser("examples/tramprograms")

        # Open the file browser starting in start_dir
        filename = filedialog.askopenfilename(
            initialdir=start_dir,
            title="Select a File",
            filetypes=(("TRAM files", "*.tram"), ("All files", "*.*"))
        )

        # Display the selected file path in the label
        if filename:
            self.label.config(text=f"Selected file:\n{filename}")
            self.machine.initial_program = Assembler.read_tram_code(filename) #examples/tramprograms/test.tram")
            self.reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = MachineUI(root)
    root.mainloop()
