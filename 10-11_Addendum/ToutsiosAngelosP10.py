#
#CompilationEngine.py
#
# CS2011   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 14 Oct 2021
#

from JTConstants import *
from SymbolTable import *

# Used for the peek/get/replace functions
TT_TOKEN = 0
TT_XML = 1


#map from Jack language purpose term in SymbolTable, to VM segment name
SEG = {'static':'static', 'field':'this', 'arg':'argument', 'var':'local'}
   
############################################
# Class
class CompilationEngine(object):

############################################
#static class variables
#   these will be shared across multiple instances

    labelID = 0

############################################
# Constructor
    def __init__(self, tokenList):
        self.tokens = tokenList
        self.indentation = 0

        #self.st = SymbolTable()             #for ch11
        #self.vmInstList = []                #for ch11

        #self.currentClassName = None        #for ch11
        

############################################
# static class methods
#    these methods are owned by the Class not one instance
#    note they do not have self as the first argument and they have the @staticmethod tag


    @staticmethod
    def __getLabelNumber():
        ''' a static utility method to access the class variable '''
        label = CompilationEngine.labelID
        CompilationEngine.labelID += 1
        return ( str(label) )



############################################
# instance methods
    def compileTokens(self):
        ''' primary call to do the final compilation.
            returns a list of properly identified structured XML with appropriate indentation.'''

        #the compilation recursive descent always starts with the <tokens> tag, and then calls __compileClass(),
        #  if it does not -- fail early because something is wrong, either in the tokenizing or how the file was output.
        #  **use the fail early technique throughout the compilation, you will always know which of a small number of
        #  possibilities you are looking for, if none of them are there raise the exception so you can start debugging
        
        result = []

        tokenTuple = self.__getNextEntry()

        if ( tokenTuple[TT_XML] == '<tokens>' ):
            result.extend( self.__compileClass() )

            tokenTuple = self.__getNextEntry()
            if ( tokenTuple[TT_XML] != '</tokens>' ):
                raise RuntimeError('Error, this file was not properly tokenized, missing </tokens>')
                
        else:
            raise RuntimeError('Error, this file was not properly tokenized, missing <tokens>')

        return result



    #for Ch11
    def get_vmInstructions(self):
        ''' returns a fully translated list of vm instructions, one instruction per list element '''
        return self.vmInstList
        


############################################
# private/utility methods


    def __getNextEntry(self):
        ''' removes the next token from the list of tokens
            returns a tuple (token, <tag> token </tag>),
            TT_TOKEN and TT_XML should be used for accessing tuple parts'''
        tokenString = self.tokens.pop(0)
        startIndex = tokenString.find('>') + 2   #handles included space assumption
        endIndex = tokenString.find('</') - 1
        tokenTuple = (tokenString[startIndex:endIndex], tokenString)
        return tokenTuple


    def __peekAtNextEntry(self):
        ''' copies, but does not remove the next token from the datastream
            returns a tuple (token, <tag> token </tag>),
            TT_TOKEN and TT_XML should be used for accessing tuple parts'''
        tokenString = self.tokens[0]
        startIndex = tokenString.find('>') + 2   #handles included space assumption
        endIndex = tokenString.find('</') - 1
        tokenTuple = (tokenString[startIndex:endIndex] , tokenString)
        return tokenTuple

    

    def __replaceEntry(self, entry):
        ''' returns a token to the head of the stream
            entry must properly be in the form <tag>token</tag>''' 
        self.tokens.insert(0, entry)





    def __compileClass(self):
        ''' compiles a class declaration.
            returning a list of VM commands. '''

        #<class>
        #indentation level adjustment
            #keyword class
            #classname identifier
            #{          
            #while peek not }
                #if field | static
                #   classVarDec
                #if in SUBROUTINES
                #   subroutineDec
            #}
        #indentation level re-adjustment. 
        #</class>


    def __compileClassVarDec(self):
        ''' compiles a class variable declaration statement.
            returning a list of VM commands. '''
        #<classVarDec>

            # <keyword> static | field <keyword>
            tokenTuple = self.__getNextEntry()
            result.append(self.indentation * ' ')+tokenTuple[TT_XML]

            # <type>
                # if next == <keyword>
                    # <keyword> int | char | booleans </keyword>
                # else if next == <identifier>
                    # <identifier> className </identifier>
            # </type>
            # do
                # <identifier> varName </identifer>
                # <symbol> , | ; </symbol>
            # while next == , (comma)
        # </classVarDec>


    def __compileSubroutine(self):
        ''' compiles a function/method.
            returning a list of VM commands. '''
        # <subRoutine>
            # <keyword> (constructor|function|method) </keyword>
            # if next == <keyword>
                # <keyword> void </void>
            # else
                # <type> typeName </type>
            # <subroutineName> identifier </subroutineName>
            # <symbol> ( </symbol>
            # CALL __compileParameterList
            # <symbol> ) </symbol>
            # <subroutineBody>
                # <symbol> { <symbol>
                # while peek not <symbol> } </symbol>
                    # if next == <keyword>
                        # CALL __compileVarDec
                    #else
                        #CALL __compileStatements
                    # if <symbol>
                        # <symbol> } </symbol>}
        # </subRoutine>



    def __compileParameterList(self):
        ''' compiles a parameter list from a function/method.
            returning a list of VM commands. '''
        # <parameterList>
            # if next == <type>
                # <type>
                    # if next == <keyword>
                        # <keyword> int | char | boolean </keyword>
                    # else
                        # <className> className </className>
                # </type>
                # <varName> identifier </varName>
                # if next == <symbol>
                    # while next == <symbol>
                        # <symbol> , </symbol>
                        # <type>
                        # if next == <keyword>
                            # <keyword> int | char | boolean </keyword>
                        # else
                            # <className> className </className>
                        # </type>
                        # <varName> identifier </varName>
        # </parameterList>

    def __compileVarDec(self):
        ''' compiles a single variable declaration line. 
            returning a list of VM commands. '''
        # <varDec>
            # keyword var
            # <type>
            # if next == <keyword>
                # <keyword> int | char | boolean </keyword>
            # else
                # <className> className </className>
            # </type>
            # <varName> identifier </varName>
            # while next == <symbol> , </symbol>
                # <symbol> , </symbol>
                # <varName> identifier </identifier>
            # <symbol> ; </symbol>
        # </varDec>



    ## We must pass multiple statements manimpulate with While not {
    def __compileStatements(self):
        ''' compiles statements.
            returning a list of VM commands. 
            assumes any leading and trailing braces are consumed by the caller'''
        # <statements>
            # if next == <keyword> let
                # CALL __compileLet
            # else if next ==  <keyword> if
                # CALL __compileIf
            # else if next == <keyword> while
                # CALL __compileWhile
            # else if next == <keyword> do
                # CALL __compileDo
            # else:
                # <keyword> return
                # CALL __compileReturn
        # </statements>



    def __compileDo(self):
        ''' compiles a function/method call.
            returning a list of VM commands. '''
        #<doStatement>
            # <keyword> do </keyword>
            # CALL __compileSubroutineCall
        #</doStatement>


    def __compileLet(self):
        ''' compiles a variable assignment statement.
            returning a list of VM commands. '''
        #<letStatement>
            # <keyword> let </keyword>
            # <varName> identifier </varName>
            # if next == <symbol> [ </symbol>
                # CALL __compileExpression
                # <symbol> ] </symbol>
            # <symbol> = </symbol>
            # CALL __compileExpression
            # <symbol> ; </symbol>
        #</letStatement>


    def __compileWhile(self):
        ''' compiles a while loop.
            returning a list of VM commands. '''
        #<whileStatement>
            # <keyword> while </keyword>
            # <symbol> ( </symbol>
            # CALL __compileExpression
            # <symbol> ) </symbol>
            # <symbol> { </symbol>
            # CALL __compileStatements
            # <symbol> } </symbol>
        #</whileStatement>


    def __compileReturn(self):
        ''' compiles a function return statement. 
            returning a list of VM commands. '''
        #<returnStatement>
            # <keyword> return </keyword>
            # if next != <symbol>
                # CALL __compileExpression
            # <symbol> ; </symbol>
        #</returnStatement>


    def __compileIf(self):
        ''' compiles an if(else)? statement block. 
            returning a list of VM commands. '''
        #<ifStatement>
            # <keyword> if </keyword>
            # <symbol> { </symbol>
            # CALL __compileExpression
            # <symbol> ) </symbol>
            # <symbol> { </symbol>
            # CALL __compileStatements
            # <symbol> } </symbol>
            # if next == <keyword>
                # <keyword> else </keyword>
                # symbol {
                # CALL __compileStatements
                # symbol }
        #</ifStatement>


    def __compileExpression(self):
        ''' compiles an expression.
            returning a list of VM commands. '''
        #<expression>
            # CALL __compileTerm
            # while next is symbol in JTConstants.BINARY_OPERATORS
                # <symbol> JTConstants.BINARY_OPERATORS </symbol>
                # CALL __compileTerm
        #</expression>



    def __compileTerm(self):
        ''' compiles a term. 
            returning a list of VM commands. '''
        #
        #This is a lot more complex than it looks!
        #it is exceptionally easy to cheeze out in the pseudocode and not consider order of
        #  operations with respect to how low-hanging a fruit each stage is
        #This is important to think through because this is the most complex function (by far), 
        #  even if it will not be the longest
        #Crappy pseudocode will work OK for ch10 because there is no symbol table functionality, 
        #   *** that is a trap ***
        #Then ch11 requires things to be differently arranged to satisfy why a variable exists,
        #   or you create a Rube Golberg machine and it gets exceptionally dificult to get right.
        #   getting this wrong that way will also make it exceptionally hard to get __compileSubroutineCall correct

        #<term>
            # if next ==  <integerConstant>
                # <integerConstant> integerConstant </integerConstant>
            # else if next == <stringConstant>
                # <stringConstant> stringConstant </stringConstanct>
            # else if next in JTConstants.KEYWORD_CONSTANTS
                # <keywordConstant> keywordConstant </keywordConstant>
            # else if next == <varName>
                # if next == <symbol> [ </symbol>                   # look one more step inside
                    # --------------- Case: foo[expression]------------------
                    # <varName> identifier </varName>
                    # <symbol> [ </symbol>
                    # CALL __compileExpression
                    # <symbol> ] </symbol>
                # else if next == <symbol> . <symbol>
                    # --------------- Case: foo.bar(list) | Foo.bar(list) | bar(list) ------------------
                    # CALL __compileSubroutineCall
                # else if next in JTConstants.UNARY_OPERATORS
                    # -------------- Case: -5 ------------------
                    # <unartOp> JTConstants.UNARY_OPERATORS </unaryOp>
                    # CALL __compileTerm
                # else
                    # -------------- Case: 'iAmJustAString' ]------------------
                    # <varName> identifier </varName>
        # </term>


    def __compileExpressionList(self):
        ''' compiles a list of expressions such as found in a list of arguments for a
            function call (one expression per argument) 
            returning a tuple whose 0th item is a list of VM commands and the 1th item
            is the number of parameters in the subroutine. ''' 
        #<expressionList>
            # if next == <expression>
                # CALL __compileExpression
                # while next == <symbol> , </symbol>
                    # CALL __compileExpression
        #</expressionList>



    def __compileSubroutineCall(self):
        ''' compiles a subroutine call.
            returning a list of VM commands. '''
        #no additional indentation or tag

        #<subroutineCall>
            # if <symbol> . <symbol> IN subroutineCall
                # if next == <className>
                    # <className> identifier </className>
                # else
                    # <varName> identifier </varName>
                # <symbol> . </symbol>
            # <subroutineName> identifier </subroutineName>
            # <symbol> ( </symbol>
            # CALL __compileExpressionList
            # <symbol> ) </symbol>
        #</subroutineCall>


    

