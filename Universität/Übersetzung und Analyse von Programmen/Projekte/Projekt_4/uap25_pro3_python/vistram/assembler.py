# (c) Stephan Diehl, University of Trier, Germany, 2025

import tram as tram


class Assembler:

    @staticmethod
    def read_tram_code(filename):
        code = []
        lines = []
        labelmap = {}
        linemap = {}

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line_number = 0
                for raw_line in f:
                    line = raw_line.strip()
                    if line.startswith("//") or line.startswith("#") or not line:
                        continue
                    if ":" in line:
                        labels_part = line[:line.index(':')]
                        labels = [label.strip() for label in labels_part.split(',')]
                        linemap[line_number] = labels
                        for label in labels:
                            labelmap[label] = tram.Label(line_number,label)
                        line = line[line.index(':') + 1:].strip()
                    lines.append(line)
                    line_number += 1
        except IOError as e:
            print(f"Fehler beim Lesen der Datei: {e}")

        for i, line in enumerate(lines):
            labels = [labelmap.get(label,None) for label in linemap.get(i,[])]
            instr = Assembler.convert_to_instruction(line, labelmap, labels)
            code.append(instr)

        return code

    @staticmethod
    def convert_to_instruction(line, labelmap={}, labels=None):
        parts = line.split()
        instr =parts[0].upper()
        arg1 = Assembler.arg_to_number(parts, 1, labelmap)
        arg2 = Assembler.arg_to_number(parts, 2, labelmap)
        arg3 = Assembler.arg_to_number(parts, 3, labelmap)
        if instr == "CONST": code=tram.const(arg1,assigned_label=labels)
        elif instr == "LOAD": code=tram.load(arg1, arg2,assigned_label=labels)
        elif instr == "STORE": code=tram.store(arg1,arg2,assigned_label=labels)
        elif instr == "ADD": code=tram.add(assigned_label=labels)
        elif instr == "SUB": code=tram.sub(assigned_label=labels)
        elif instr == "MUL": code=tram.mul(assigned_label=labels)
        elif instr == "DIV": code=tram.div(assigned_label=labels)
        elif instr == "LT": code=tram.lt(assigned_label=labels)
        elif instr == "GT": code=tram.gt(assigned_label=labels)
        elif instr == "EQ": code=tram.eq(assigned_label=labels)
        elif instr == "NEQ": code=tram.neq(assigned_label=labels)
        elif instr == "IFZERO": code=tram.ifzero(arg1,assigned_label=labels)
        elif instr == "GOTO": code=tram.goto(arg1,assigned_label=labels)
        elif instr == "HALT": code=tram.halt(assigned_label=labels)
        elif instr == "NOP": code=tram.nop(assigned_label=labels)
        elif instr == "INVOKE": code=tram.invoke(arg1,arg2,arg3,assigned_label=labels)
        elif instr == "RETURN": code=tram.ireturn(assigned_label=labels)
        elif instr == "POP": code=tram.pop(assigned_label=labels)
        else:
            print(f"Keine gültige Instruktion: {line}")
            code = None
        return code

    @staticmethod
    def arg_to_number(parts, index, labelmap):
        if index >= len(parts):
            return 0
        arg = parts[index]
        try:
            return int(arg)
        except ValueError:
            return labelmap.get(arg, 0)
