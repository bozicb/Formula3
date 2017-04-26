from formula3.exceptions.exception import Formula3Exception

class Formula3ParserException(Formula3Exception):
    ''' An exception thrown when the lexer finds an illegal character
        Fields (beside message)are
        line, column. The coordinates within the user input
        remainder: the still unparsed input 
    '''
    
    def __init__(self, msg, row, column, token):
        self.message=msg
        self.token=token
        self.row=row
        self.column=column

    def __str__(self):
        return "%s at line %d column %d. Offending token is %s " % (self.message, self.row, self.column, self.token)
