#
#JTConstants.py
#
# CS2011   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 15 Nov 2022
#

import string

##############################################################
#Chapter 10 stuff
#
KEYWORDS = ('boolean', 'char', 'class', 'constructor', 'do', 'else',
            'false', 'field', 'function', 'if', 'int', 'let', 'method',
            'null', 'return', 'static', 'this', 'true', 'var', 'void', 'while')

# A string of all the different symbols, can use list methods on this string
SYMBOLS = '{}()[].,;+-*/&|<>=~'

DELIMITERS = ' ' + SYMBOLS 

#If 0th char of token is a digit, it is an integer constant
#Else it is an identifier
IDENTIFIER_START_CHARS = string.ascii_letters + '_'
IDNETIFIER_CHARS = IDENTIFIER_START_CHARS + string.digits 

# These symbols are reserved characters in xml language, use the value in key/value pairs
glyphSubstitutes = {'<':'&lt;', '>':'&gt;' , '&':'&amp;'}


##############################################################
#Chapter 11 stuff
#
SUBROUTINES = ('constructor', 'method', 'function')

STATEMENTS = ('let', 'if', 'else', 'while', 'do', 'return')

KEYWORD_CONSTANTS = {'true':-1, 'false':0, 'null':0, 'this':999999999}

UNARY_OPERATORS = {'-':'neg', '~':'not'}

BINARY_OPERATORS = {    '+':'add',
                        '-':'sub',
                        '*':'Math.multiply',
                        '/':'Math.divide',
                    '&amp;':'and',
                        '|':'or',
                     '&lt;':'lt',
                     '&gt;':'gt',
                        '=':'eq'}


TOKEN_STRINGS = ( 'unknown', 'keyword', 'symbol', 'identifier',
                  'integerConstant', 'stringConstant',
                  'IDENTIFIER-Defined', 'SCOPE-Subroutine')

