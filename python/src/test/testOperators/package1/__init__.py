print "Hello, I'm loaded"

import formula3.F3System as F3System

def op():
    pass

F3System.addF3Operator("dynamicTest", op)   # Note, the unit test relies on this operator name.
