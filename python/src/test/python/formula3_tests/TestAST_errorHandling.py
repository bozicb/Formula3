from formula3.ast_lexer import AST_Lexer 
import formula3.ast_parser as ast_parser
import unittest
import ply.lex as lex 
import ply.yacc as yacc

from formula3.exceptions.Formula3LexerException import Formula3LexerException
from formula3.exceptions.Formula3ParserException import Formula3ParserException


# The purpose of this module is to test the error handling behaviour of the F3 (AST) parser



class TestAST(unittest.TestCase):
    

    def testLexerException(self):
        lexer_ast=AST_Lexer()
        parser_ast = yacc.yacc(module=ast_parser)
        try:
            result=parser_ast.parse("@A %")
            self.fail("A message expected was not thrown")
        except Formula3LexerException, e:
            self.assertEquals('%', e.remainder)
            self.assertEquals(3, e.column)
            self.assertEquals(1, e.row)

    def testParserError(self):
        lexer_ast=AST_Lexer()
        parser_ast = yacc.yacc(module=ast_parser)
        try:
            result=parser_ast.parse("@A <<XXX>>")
            self.fail("A message expected was not thrown")
        except Formula3ParserException, e:
            self.assertEquals(8, e.column)
            self.assertEquals(1, e.row)
            self.assertEquals('>>', e.token)


    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
