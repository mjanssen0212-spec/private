package de.unitrier.st.uap.w25.tram;

import java.util.ArrayList;
import java.util.List;

final class Main
{
	private Main(){}
	
	public static void main(String[] argv)
	{
        String filename = "";
        if(argv.length > 0) {
            if(argv[0].equals("-d")) {
                filename = argv[1];
            } else {
                filename = argv[0];
            }
        }
		Instruction[] code = Assembler.readTRAMCode(
//				"tramcode\\square.tram"
//				 "tramcode\\wrapper.tram"
//                 "tramcode\\example1.tram"
//				 "tramcode\\example2.tram"
//				 "tramcode\\example3.tram"
//				"tramcode\\test.tram"
                filename
		);

		int lineNr=0;
		for(Instruction instr: code) {
			if (instr != null) {
				System.out.println(String.format("%03d", lineNr) + "| " + instr.toString());
				lineNr++;
			}
		}

		// TODO: Create an instance of the abstract machine with reasonable parameters
        AbstractMachine am = new AbstractMachine(new ArrayList<>(), -1, 0, 0, 0);
        List<Integer> stack = am.runProgram(code);
	}
}