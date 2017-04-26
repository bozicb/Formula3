# The parser creates an AST which is composed mainly from lists and dicts
# To harmonize the keys and to avoid code bloating all
# strings are mentioned here once and should NOT be used as literals
# in other places. Note: This is work in progress and not all these strings have been replaced yet. 


TYPE = "type"
TYPE_FUNCCALL = "func_call"
TYPE_SLICE = "SLICE"
TYPE_PROPCOPY = "PROPCOPY"


ARG_LIST = "arg_list"


SLICE_TYPE_LOGICAL  = "LOGICAL"
SLICE_TYPE_PHYSICAL = "PHYSICAL"

ID="id"

OPEN="OPEN"
CLOSED = "CLOSED"

STMT = 'stmt'
PARAMETERS = 'parameters'

SUBDEF = 'subdef'
SUBNAME = "subname"
