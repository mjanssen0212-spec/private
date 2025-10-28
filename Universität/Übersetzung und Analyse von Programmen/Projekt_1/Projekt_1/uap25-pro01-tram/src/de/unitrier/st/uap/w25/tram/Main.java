package de.unitrier.st.uap.w25.tram;

import java.util.ArrayList;
import java.util.List;

final class Main
{
	private Main(){}
	
	public static void main(String[] argv)
	{
		Instruction[] code = Assembler.readTRAMCode(
				"tramcode\\square.tram"
//				 "tramcode\\wrapper.tram"
//                 "tramcode\\example1.tram"
//				 "tramcode\\example2.tram"
//				 "tramcode\\example3.tram"
//				"tramcode\\test.tram"
		);

		int lineNr=0;
		for(Instruction instr: code) {
			if (instr != null) {
				System.out.println(String.format("%03d", lineNr) + "| " + instr.toString());
				lineNr++;
			}
		}

		// TODO: Create an instance of the abstract machine with reasonable parameters
        AbstractMachine am = new AbstractMachine(new ArrayList<>(/*List.of(0, 0)*/), -1, 0, 0, 0);
        List<Integer> stack = am.runProgram(code);
	}
}