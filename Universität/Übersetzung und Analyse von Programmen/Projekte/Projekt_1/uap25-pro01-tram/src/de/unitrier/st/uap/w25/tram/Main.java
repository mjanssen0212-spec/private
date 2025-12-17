package de.unitrier.st.uap.w25.tram;
//Matthias Janßen
//1871808

import java.util.ArrayList;
import java.util.List;

import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;


final class Main {
    private Main() {
    }

    protected static final Logger logger = LogManager.getLogger(Main.class);
    protected static Boolean isDebug = false;

    public static void main(String[] argv) {
        String filename = "";
        if (argv.length > 0) {
            if (argv[0].equals("-d")) {
                isDebug = true;
                filename = argv[1];
            } else {
                filename = argv[0];
            }
            if (filename == null) {
                filename = "tramcode\\test.tram";
            }
        }
        Instruction[] code = Assembler.readTRAMCode(
//				"tramcode\\square.tram"
//				 "tramcode\\wrapper.tram"
//                 "tramcode\\example1.tram"
//				 "tramcode\\example2.tram"
//				 "tramcode\\example3.tram"
//				"tramcode\\test.tram"
//                filename
//                "tramcode\\euklid.tram"
                "tramcode\\complex.tram"
        );

        int lineNr = 0;
        for (Instruction instr : code) {
            if (instr != null) {
                if (isDebug) {
                    logger.debug(String.format("%03d", lineNr) + "| " + instr.toString());
                }
                lineNr++;
            }
        }

        // TODO: Create an instance of the abstract machine with reasonable parameters
        AbstractMachine am = new AbstractMachine(new ArrayList<>(), -1, 0, 0, 0);
        List<Integer> stack = am.runProgram(code);
    }
}