from instruction import *

# Label erhalten intern eine eigene ID, daher sollte man den Variablenname nicht
# mit dem Labelnamen verwechseln !!!
L4=Label()
L7=Label()
L15=Label()

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

print_prog(test_prog2)
