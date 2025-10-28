package de.unitrier.st.uap.w25.tram;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;

public class Assembler {
    static Instruction[] readTRAMCode(String filename) {
        LinkedList<Instruction> code = new LinkedList<Instruction>();
        LinkedList<String> lines = new LinkedList<String>();
        HashMap<String, Integer> labelmap = new HashMap<String, Integer>();
        try (BufferedReader in = new BufferedReader(new FileReader(filename));) {
            String line;
            int lineNumber = 0;
            while ((line = in.readLine()) != null) {
                line = line.trim();
                if (line.startsWith("//") || line.startsWith("#")) continue;
                if (line.contains(":")) {
                    String[] labels = line.substring(0, line.indexOf(':')).split(",");
                    for (String label : labels) labelmap.put(label, lineNumber);
                    line = line.substring(line.indexOf(':') + 1).trim();
                }
                lines.add(line);
                lineNumber++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        for (String line : lines) {
            code.add(convertToInstruction(line, labelmap));
        }

        return (Instruction[]) code.toArray(new Instruction[]{});
    }

    static Instruction convertToInstruction(String line, HashMap<String, Integer> labelmap) {
        String[] parts = line.split("\\s+");


        return new Instruction(
                stringToOpcode(parts[0]),
                argToNumber(parts, 1, labelmap),
                argToNumber(parts, 2, labelmap),
                argToNumber(parts, 3, labelmap));
    }

    static int stringToOpcode(String instr) {
        switch (instr) {
            case "CONST":
                return Instruction.CONST;
            case "LOAD":
                return Instruction.LOAD;
            case "STORE":
                return Instruction.STORE;
            case "ADD":
                return Instruction.ADD;
            case "SUB":
                return Instruction.SUB;
            case "MUL":
                return Instruction.MUL;
            case "DIV":
                return Instruction.DIV;
            case "LT":
                return Instruction.LT;
            case "GT":
                return Instruction.GT;
            case "EQ":
                return Instruction.EQ;
            case "NEQ":
                return Instruction.NEQ;
            case "IFZERO":
                return Instruction.IFZERO;
            case "GOTO":
                return Instruction.GOTO;
            case "HALT":
                return Instruction.HALT;
            case "NOP":
                return Instruction.NOP;
            case "INVOKE":
                return Instruction.INVOKE;
            case "RETURN":
                return Instruction.RETURN;
            case "POP":
                return Instruction.POP;
        }
        return -1;
    }

    static Integer argToNumber(String[] parts, int index, HashMap<String, Integer> labelmap) {
        if (index > parts.length - 1) return 0;
        String arg = parts[index];
        try {
            return Integer.valueOf(arg);
        } catch (NumberFormatException e) {
            return labelmap.get(arg);
        }
    }
}