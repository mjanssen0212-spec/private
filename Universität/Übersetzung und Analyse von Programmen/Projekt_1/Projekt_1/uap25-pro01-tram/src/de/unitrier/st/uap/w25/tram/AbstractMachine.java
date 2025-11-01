package de.unitrier.st.uap.w25.tram;

import java.util.List;

import static de.unitrier.st.uap.w25.tram.Main.isDebug;
import static de.unitrier.st.uap.w25.tram.Main.logger;

public class AbstractMachine {
    private List<Integer> stack;
    private int TOP;
    //parameter pointer
    private int PP;
    //Frame Pointer
    private int FP;
    //Program counter
    private int PC;

    public AbstractMachine(List<Integer> stack, int TOP, int PP, int FP, int PC) {
        this.stack = stack;
        this.TOP = TOP;
        this.PP = PP;
        this.FP = FP;
        this.PC = PC;
    }

    public List<Integer> runProgram(Instruction[] instructions) {
        while (PC != -1) {
            Instruction i = instructions[PC];
            switch (i.getOpcode()) {
                case 1:
                    //CONST
                    stack.add(TOP + 1, i.getArg1());
                    TOP++;
                    PC++;
                    break;
                case 2:
                    //LOAD
                    stack.add(TOP + 1, stack.get(spp(i.getArg2(), PP, FP) + i.getArg1()));
                    TOP++;
                    PC++;
                    break;
                case 3:
                    //STORE
                    stack.set(spp(i.getArg2(), PP, FP) + i.getArg1(), stack.get(TOP));
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 4:
                    //ADD
                    stack.set(TOP - 1, stack.get(TOP - 1) + stack.get(TOP));
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 5:
                    //SUB
                    stack.set(TOP - 1, stack.get(TOP - 1) - stack.get(TOP));
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 6:
                    //MUL
                    stack.set(TOP - 1, stack.get(TOP - 1) * stack.get(TOP));
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 7:
                    //DIV
                    stack.set(TOP - 1, stack.get(TOP - 1) / stack.get(TOP));
                    stack.remove(TOP - 1);
                    TOP--;
                    PC++;
                    break;
                case 8:
                    //LT
                    if (stack.get(TOP - 1) < stack.get(TOP)) {
                        stack.set(TOP - 1, 1);
                    } else {
                        stack.set(TOP - 1, 0);
                    }
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 9:
                    //GT
                    if (stack.get(TOP - 1) > stack.get(TOP)) {
                        stack.set(TOP - 1, 1);
                    } else {
                        stack.set(TOP - 1, 0);
                    }
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 10:
                    //EQ
                    if (stack.get(TOP - 1) == stack.get(TOP)) {
                        stack.set(TOP - 1, 1);
                    } else {
                        stack.set(TOP - 1, 0);
                    }
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 11:
                    //NEQ
                    if (stack.get(TOP - 1) != stack.get(TOP)) {
                        stack.set(TOP - 1, 1);
                    } else {
                        stack.set(TOP - 1, 0);
                    }
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
                case 12:
                    //IFZERO
                    if (stack.get(TOP) == 0) {
                        PC = i.getArg1();
                    } else {
                        PC++;
                    }
                    stack.remove(TOP);
                    TOP--;
                    break;
                case 13:
                    //GOTO
                    PC = i.getArg1();
                    break;
                case 14:
                    //HALT
                    PC = -1;
                    break;
                case 15:
                    //NOP
                    PC++;
                    break;
                case 16:
                    //INVOKE
                    stack.add(TOP + 1, PC + 1);
                    stack.add(TOP + 2, PP);
                    stack.add(TOP + 3, FP);
                    stack.add(TOP + 4, spp(i.getArg3(), PP, FP));
                    stack.add(TOP + 5, sfp(i.getArg3(), PP, FP));
                    PP = TOP - i.getArg1() + 1;
                    FP = TOP + 1;
                    TOP = TOP + 5;
                    PC = i.getArg2();
                    break;
                case 17:
                    //RETURN
                    int res = stack.get(TOP);
                    TOP = PP;
                    PC = stack.get(FP);
                    PP = stack.get(FP + 1);
                    FP = stack.get(FP + 2);
                    stack.set(TOP, res);
                    while (stack.size() > TOP + 1) {
                        stack.removeLast();
                    }
                    break;
                case 18:
                    //POP
                    stack.remove(TOP);
                    TOP--;
                    PC++;
                    break;
            }
            if (isDebug) {
                logger.debug(formatHelper(
                        i, stack
                ));
            }
        }
        if (isDebug) {
            logger.debug("PP={}, FP={}, PC={}, STACK={}", PP, FP, PC, stack);
        }
        return stack;
    }

    private int spp(int d, int pp, int fp) {
        if (d == 0) {
            return pp;
        } else {
            spp(d - 1, stack.get(fp + 3), stack.get(fp + 4));
        }
        return -1;
    }

    private int sfp(int d, int ppp, int fp) {
        if (d == 0) {
            return fp;
        } else {
            sfp(d - 1, stack.get(fp + 3), stack.get(fp + 4));
        }
        return -1;
    }

    public List getStack() {
        return stack;
    }

    public void setStack(List stack) {
        this.stack = stack;
    }

    public int getTOP() {
        return TOP;
    }

    public void setTOP(int TOP) {
        this.TOP = TOP;
    }

    public int getPP() {
        return PP;
    }

    public void setPP(int PP) {
        this.PP = PP;
    }

    public int getFP() {
        return FP;
    }

    public void setFP(int FP) {
        this.FP = FP;
    }

    public int getPC() {
        return PC;
    }

    public void setPC(int PC) {
        this.PC = PC;
    }

    private String formatHelper(Instruction instr, List<Integer> stack) {
        StringBuilder sb = new StringBuilder();

        sb.append(String.format("After instruction = %s; configuration = PC = %d; PP = %d; FP = %d; TOP = %d", instr.toString().split(" ")[0], PC, PP, FP, TOP));
        sb.append(System.lineSeparator());
        sb.append("Stack:").append(System.lineSeparator());

        if (TOP == -1) {
            sb.append("[]").append(System.lineSeparator());
        }
        for (int i = 0; i <= TOP; i++) {
            sb.append(String.format("[%d] = %d", i, stack.get(i)));

            if ((int) PP == i) {
                String label = "PP";
                sb.append(String.format(" <-- %s (%s = %d)", label, label, i));
            }
            if (FP == i) {
                String label = "FP";
                sb.append(String.format(" <-- %s (%s = %d)", label, label, i));
            }
            if (TOP == i) {
                String label = "TOP";
                sb.append(String.format(" <-- %s (%s = %d)", label, label, i));
            }

            sb.append(System.lineSeparator());
        }

        return sb.toString();
    }

}
