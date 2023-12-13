#
#CompilationEngine.py
#
# CS2011   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 15 Nov 2022
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


#static class variables
#   these will be shared across multiple instances

    labelID = 0

############################################
# Constructor
    def __init__(self, tokenList):
        self.tokens = tokenList
        self.indentation = 0

        self.st = SymbolTable()             #for ch11
        self.vmInstList = []                #for ch11

        self.currentClassName = None        #for ch11
        

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

    def __peekAtSpecificEntry(self, index):
        ''' copies, but does not remove the next token from the datastream
            returns a tuple (token, <tag> token </tag>),
            TT_TOKEN and TT_XML should be used for accessing tuple parts'''
        tokenString = self.tokens[index]
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
        #note how the comments directly correlate to the syntax breakdown
        
        result = []
        tokenTuple = self.__getNextEntry()
        if tokenTuple[TT_TOKEN] == 'class':
            
            result.append( '<class>' ) 
            self.indentation += 2
            
            #keyword class
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) 
            tokenTuple = self.__getNextEntry()
            
            #classname identifier
            self.currentClassName = tokenTuple[TT_TOKEN]
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) 
            tokenTuple = self.__getNextEntry()
            
            #{
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML])
            tokenTuple = self.__peekAtNextEntry()
            
            #while peek not }
            while tokenTuple[TT_TOKEN] != '}':
                
                #if field | static
                if (tokenTuple[TT_TOKEN] == 'field') or (tokenTuple[TT_TOKEN] == 'static'):
                    #classVarDec
                    result.extend( self.__compileClassVarDec() ) 
                    
                #if in SUBROUTINES
                elif( tokenTuple[TT_TOKEN] in SUBROUTINES ):
                    #subroutineDec
                    result.extend( self.__compileSubroutine())
                else:
                    raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not subroutineDec or classVarDec')

                tokenTuple = self.__peekAtNextEntry()

            tokenTuple = self.__getNextEntry()
            
            #}
            result.append( (self.indentation * ' ') + tokenTuple[TT_XML]) 
            self.indentation -= 2
            result.append( '</class>' )
            
        else:
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not class')
        
        return result



    def __compileClassVarDec(self):
        ''' compiles a class variable declaration statement.
            returning a list of VM commands. '''
        result = []

        # <classVarDec>
        result.append((self.indentation * ' ') + '<classVarDec>')
        self.indentation += 2


        # <keyword> static | field <keyword>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        keyword = tokenTuple[TT_TOKEN]

        tokenTuple = self.__getNextEntry()
        # if next == <keyword>
        # <keyword> int | char | booleans </keyword>
        if(tokenTuple[TT_TOKEN]=='char' or tokenTuple[TT_TOKEN]=='int' or tokenTuple[TT_TOKEN]=='boolean'):
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            type = tokenTuple[TT_TOKEN]
        else:
            # else if next == <identifier>
            # <identifier> className </identifier>
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            type = tokenTuple[TT_TOKEN]

        # <identifier> varName </identifer>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        varname = tokenTuple[TT_TOKEN]

        self.st.define(varname, type, SEG[keyword], self.st.classScope)
        result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname,0))

        tokenTuple = self.__getNextEntry()
        while tokenTuple[TT_TOKEN] != ';':
            if tokenTuple[TT_TOKEN] == ',':
                # ,
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])
                tokenTuple = self.__getNextEntry()
                # varName
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                varname = tokenTuple[TT_TOKEN]
                self.st.define(varname, type, SEG[keyword], self.st.classScope)
                result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 0))

                tokenTuple = self.__getNextEntry()
            else:
                raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not , or ;')
        # ;
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        self.indentation -= 2

        # </classVarDec>
        result.append((self.indentation * ' ') + '</classVarDec>')
        return result

   
    def __compileSubroutine(self):
        ''' compiles a function/method.
            returning a list of VM commands. '''

        self.st.startSubroutine()

        result = []

        # <subRoutine>
        result.append((self.indentation * ' ') + '<subroutineDec>')
        self.indentation += 2

        # <keyword> (constructor|function|method) </keyword>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #VM
        type = tokenTuple[TT_TOKEN] # constructor|function|method

        # void | boolean | char | className
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #VM
        returnValueType = tokenTuple[TT_TOKEN]

        # <subroutineName> identifier </subroutineName>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # VM
        varName = tokenTuple[TT_TOKEN]  # main

        # add as first arg the class type in this
        if(type == 'method'):
            self.st.define('this', self.currentClassName, SEG['arg'],self.st.subroutineScope)

        # (
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # CALL __compileParameterList
        # Check if next token is )
        result.extend(self.__compileParameterList())

        # )
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # <subroutineBody>
        result.append((self.indentation * ' ') + '<subroutineBody>')
        self.indentation += 2

        # <symbol> { <symbol>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # varDec
        tokenTuple = self.__peekAtNextEntry()
        # num = 0
        while (tokenTuple[TT_TOKEN] == 'var'):
            # num = num+1
            result.extend(self.__compileVarDec())
            tokenTuple = self.__peekAtNextEntry()

        # Vm
        # In order to find the num of local vars in this function we can search for them in S.T
        num = self.st.howMany(SEG['var'],self.st.subroutineScope)
        # printType changes the constructor type to function, for the call function in vm.
        #printType = 'function' if type == 'constructor' else type
        self.vmInstList.append('function ' + self.currentClassName + '.' + varName + ' ' +str(num))

        if (type == 'method'):
            self.vmInstList.append('push argument 0')
            self.vmInstList.append('pop pointer 0')


        # In case our subroutine is a constructor we have to push the arg number to allocate space
        if (type == 'constructor'):
            number_of_args = self.st.howMany(SEG['field'], self.st.classScope)
            self.vmInstList.append('push constant ' + str(number_of_args))
            self.vmInstList.append('call Memory.alloc 1')
            self.vmInstList.append('pop pointer 0')

        # statements
        result.extend(self.__compileStatements())

        # }
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</subroutineBody>')

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</subroutineDec>')

        return result

     
    def __compileParameterList(self):
        ''' compiles a parameter list from a function/method.
            returning a list of VM commands. '''
        result = []
        # <parameterList>
        result.append((self.indentation * ' ') + '<parameterList>')
        self.indentation += 2

        tokenTuple = self.__peekAtNextEntry()
        while tokenTuple[TT_TOKEN] != ')':

            tokenTuple = self.__getNextEntry()

            # type
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            type = tokenTuple[TT_TOKEN]

            # <identifier> varName </identifer>
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            varname = tokenTuple[TT_TOKEN]

            self.st.define(varname,type,SEG['arg'],self.st.subroutineScope)
            result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 0))

            tokenTuple = self.__peekAtNextEntry()
            if (tokenTuple[TT_TOKEN] == ','):
                # ,
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])


                tokenTuple = self.__peekAtNextEntry()
            elif (tokenTuple[TT_TOKEN] != ')'):
                raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ) or ,)')

        self.indentation -= 2
        # </parameterList>
        result.append((self.indentation * ' ') + '</parameterList>')

        return result

  
    def __compileVarDec(self):
        ''' compiles a single variable declaration line. 
            returning a list of VM commands. '''
        result = []
        # <varDec>
        result.append((self.indentation * ' ') + '<varDec>')
        self.indentation += 2

        #var
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # <type>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        type = tokenTuple[TT_TOKEN]

        # <varName>
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        varname = tokenTuple[TT_TOKEN]

        # Add var in ST
        self.st.define(varname,type,SEG['var'],self.st.subroutineScope)
        result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname,0))

        tokenTuple = self.__peekAtNextEntry()
        while(tokenTuple[TT_TOKEN] == ','):
            # ,
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # <varName>
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            varname = tokenTuple[TT_TOKEN]
            self.st.define(varname, type, SEG['var'], self.st.subroutineScope)
            result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 0))

            tokenTuple = self.__peekAtNextEntry()

        if(tokenTuple[TT_TOKEN] != ';'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ;')

        # ;
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2

        # </varDec>
        result.append((self.indentation * ' ') + '</varDec>')

        return result


    def __compileStatements(self):
        ''' compiles statements.
            returning a list of VM commands. 
            assumes any leading and trailing braces are consumed by the caller'''
        result = []

        # <statements>
        result.append((self.indentation * ' ') + '<statements>')
        self.indentation += 2
        tokenTuple = self.__peekAtNextEntry()

        while(tokenTuple[TT_TOKEN] in STATEMENTS):
            if tokenTuple[TT_TOKEN] == 'let':
                result.extend(self.__compileLet())
                tokenTuple = self.__peekAtNextEntry()
            elif tokenTuple[TT_TOKEN] == 'if':
                result.extend(self.__compileIf())
                tokenTuple = self.__peekAtNextEntry()
            elif tokenTuple[TT_TOKEN] == 'while':
                result.extend(self.__compileWhile())
                tokenTuple = self.__peekAtNextEntry()
            elif tokenTuple[TT_TOKEN] == 'do':
                result.extend(self.__compileDo())
                tokenTuple = self.__peekAtNextEntry()
            else:
                result.extend(self.__compileReturn())
                tokenTuple = self.__peekAtNextEntry()
        self.indentation -= 2

        result.append((self.indentation * ' ') + '</statements>')
        # </statements>
        return result


    def __compileDo(self):
        ''' compiles a function/method call.
            returning a list of VM commands. '''
        result = []
        result.append((self.indentation * ' ') + '<doStatement>')
        self.indentation += 2

        # do
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        result.extend(self.__compileSubroutineCall())

        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != ';'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ;')

            # ;
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</doStatement>')

        # VM code
        # Because In every method we must return something, and Do doesn't, we have to trick compiler with the next vm code:
        self.vmInstList.append('pop temp 0')

        return result


    def __compileLet(self):
        ''' compiles a variable assignment statement.
            returning a list of VM commands. '''
        result = []
        result.append((self.indentation * ' ') + '<letStatement>')
        self.indentation += 2
        is_an_array = 0;

        # let
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # varName
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        varname = tokenTuple[TT_TOKEN]

        #st USED
        result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname,2))

        # [ | =
        tokenTuple = self.__getNextEntry()
        while tokenTuple[TT_TOKEN] == '[':
            is_an_array = 1
            # [
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # expression
            result.extend(self.__compileExpression())

            # In arrays before the expression we have to add the (varname + arrayIndex) in the vm list
            self.vmInstList.append('push ' + self.st.kindOf(varname) + ' ' + str(self.st.indexOf(varname)))

            self.vmInstList.append('add')

            tokenTuple = self.__getNextEntry()
            if(tokenTuple[TT_TOKEN] != ']'):
                raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ]')
            # ]
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            tokenTuple = self.__getNextEntry()

        if (tokenTuple[TT_TOKEN] != '='):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not =')

        # =
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # expression
        result.extend(self.__compileExpression())

        #VM
        if(is_an_array == 0):
            index = self.st.indexOf(varname)
            kind = self.st.kindOf(varname)
            self.vmInstList.append('pop '+kind+' '+str(index))
        else: #is an array
            self.vmInstList.append('pop temp 0')
            self.vmInstList.append('pop pointer 1')
            self.vmInstList.append('push temp 0')
            self.vmInstList.append('pop that 0')

        # ;
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != ';'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ;')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</letStatement>')
        return result


    def __compileWhile(self):
        ''' compiles a while loop.
            returning a list of VM commands. '''
        result = []
        result.append((self.indentation * ' ') + '<whileStatement>')
        self.indentation += 2

        # while
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # VM code - We need labels - while( )
        whileLabel = self.__getLabelNumber()
        self.vmInstList.append('label WHILE_TOP_'+whileLabel)

        # (
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '('):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not (')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # expression
        result.extend(self.__compileExpression())

        # We are checking if the expression is true in order to continue with the body, so if it is false we jump to end of while!
        self.vmInstList.append('not')
        self.vmInstList.append('if-goto WHILE_EXIT_'+whileLabel)

        # )
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != ')'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not )')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # {
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '{'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not {')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # statements
        result.extend(self.__compileStatements())

        # }
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '}'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not }')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # While loop - Jump to the starting point to recheck the value
        self.vmInstList.append('goto WHILE_TOP_'+whileLabel)
        self.vmInstList.append('label WHILE_EXIT_'+whileLabel)

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</whileStatement>')
        return result


    def __compileReturn(self):
        ''' compiles a function return statement. 
            returning a list of VM commands. '''
        result = []

        result.append((self.indentation * ' ') + '<returnStatement>')
        self.indentation += 2

        # return
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        tokenTuple = self.__peekAtNextEntry()
        if(tokenTuple[TT_TOKEN] != ';'):
            result.extend(self.__compileExpression())
        else:
            self.vmInstList.append('push constant 0')
        #VM
        self.vmInstList.append('return')

        # ;
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != ';'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not ;')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</returnStatement>')
        return result


    def __compileIf(self):
        ''' compiles an if(else)? statement  
            returning a list of VM commands. ''' 
        result = []

        result.append((self.indentation * ' ') + '<ifStatement>')
        self.indentation += 2

        ifLabel = self.__getLabelNumber()

        # if
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # (
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '('):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not (')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # expression
        result.extend(self.__compileExpression())

        # If the expression is false jump to DO_ELSE
        self.vmInstList.append('not')
        self.vmInstList.append('if-goto DO_ELSE_'+ifLabel)

        # )
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != ')'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not )')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # {
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '{'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not {')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # statements
        result.extend(self.__compileStatements())

        # }
        self.vmInstList.append('goto IF_THEN_COMPLETE_' + ifLabel)
        tokenTuple = self.__getNextEntry()
        if (tokenTuple[TT_TOKEN] != '}'):
            raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not }')
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        # The DO_ELSE label in case our initial If is false
        self.vmInstList.append('label DO_ELSE_' + ifLabel)

        tokenTuple = self.__peekAtNextEntry()
        if (tokenTuple[TT_TOKEN] == 'else'):

            # else
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # {
            tokenTuple = self.__getNextEntry()
            if (tokenTuple[TT_TOKEN] != '{'):
                raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not {')
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # statements
            result.extend(self.__compileStatements())

            # }
            tokenTuple = self.__getNextEntry()
            if (tokenTuple[TT_TOKEN] != '}'):
                raise RuntimeError('Error, token provided:', tokenTuple[TT_TOKEN], ', is not }')
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

        #Label that indicates the end of IF
        self.vmInstList.append('label IF_THEN_COMPLETE_' + ifLabel)

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</ifStatement>')

        return result


    def __compileExpression(self):
        ''' compiles an expression.
            returning a list of VM commands. '''
        result = []
        result.append((self.indentation * ' ') + '<expression>')
        self.indentation += 2

        # term
        result.extend(self.__compileTerm())

        tokenTuple = self.__peekAtNextEntry()
        while tokenTuple[TT_TOKEN] in BINARY_OPERATORS:


            op = tokenTuple[TT_TOKEN]

            # op
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # term
            result.extend(self.__compileTerm())

            #VM
            if op in ('*','/'):
                self.vmInstList.append('call '+BINARY_OPERATORS[op]+' 2')
            else:
                self.vmInstList.append(BINARY_OPERATORS[op])

            tokenTuple = self.__peekAtNextEntry()

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</expression>')

        return result


    def __compileTerm(self):
        ''' compiles a term. 
            returning a list of VM commands. '''
        result = []

        result.append((self.indentation * ' ') + '<term>')
        self.indentation += 2

        tokenTuple = self.__peekAtNextEntry()

        # Check for integerConstant
        if(tokenTuple[TT_TOKEN][0].isdigit()):
            # VM
            self.vmInstList.append('push constant '+tokenTuple[TT_TOKEN])
            # integer
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        elif(tokenTuple[TT_XML][1:3]=='st'):
            # string
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # VM code for String manipulation
            length = len(tokenTuple[TT_TOKEN])
            self.vmInstList.append('push constant '+str(length))
            self.vmInstList.append('call String.new 1')
            for char in tokenTuple[TT_TOKEN]:
                self.vmInstList.append('push constant '+str(ord(char)))
                self.vmInstList.append('call String.appendChar 2')

        elif(tokenTuple[TT_XML][1]=='k'):
            # keyword
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            #Handle true/false values for VM
            if(tokenTuple[TT_TOKEN]=='true'):
                self.vmInstList.append('push constant 0')
                self.vmInstList.append('not')
            elif(tokenTuple[TT_TOKEN]=='false'):
                self.vmInstList.append('push constant 0')
            elif(tokenTuple[TT_TOKEN]=='this'):
                self.vmInstList.append('push pointer 0')
            elif(tokenTuple[TT_TOKEN]=='null'):
                self.vmInstList.append('push constant 0')


        elif(tokenTuple[TT_TOKEN] in UNARY_OPERATORS):
            # unary op
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            unary = tokenTuple[TT_TOKEN]
            result.extend(self.__compileTerm())
            self.vmInstList.append(UNARY_OPERATORS[unary])
        elif(tokenTuple[TT_TOKEN][0]=='('):
            # (
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # expression
            result.extend(self.__compileExpression())

            # )
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        else:
            # Array
            if self.__peekAtSpecificEntry(1)[TT_TOKEN]=='[':
                # varname
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])
                varname = tokenTuple[TT_TOKEN]

                #TODO: get data from ST
                result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 2))

                # [
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                # expression
                result.extend(self.__compileExpression())

                # In arrays before the expression we have to add the (varname + arrayIndex) in the vm list
                self.vmInstList.append('push ' + self.st.kindOf(varname) + ' ' + str(self.st.indexOf(varname)))
                self.vmInstList.append('add')
                self.vmInstList.append('pop pointer 1')
                self.vmInstList.append('push that 0')


                # ]
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            elif (self.__peekAtSpecificEntry(1)[TT_TOKEN] == '('):
                # function
                result.extend(self.__compileSubroutineCall())
            elif (self.__peekAtSpecificEntry(1)[TT_TOKEN] == '.'):

                if(self.__peekAtSpecificEntry(3)[TT_TOKEN] =='('):
                    # subroutine method
                    result.extend(self.__compileSubroutineCall())
                else:
                    # fieldname

                    # varname
                    tokenTuple = self.__getNextEntry()
                    result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    # .
                    tokenTuple = self.__getNextEntry()
                    result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                    # fieldname
                    tokenTuple = self.__getNextEntry()
                    result.append((self.indentation * ' ') + tokenTuple[TT_XML])
            else:
                # varname
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                #VM
                varname = tokenTuple[TT_TOKEN]
                index = self.st.indexOf(varname)
                kind = self.st.kindOf(varname)
                self.vmInstList.append('push ' + kind + ' ' + str(index))

                result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 2))

        self.indentation -= 2
        result.append((self.indentation * ' ') + '</term>')

        return result


    def __compileExpressionList(self):
        ''' compiles a list of expressions such as found in a list of arguments for a
            function call (one expression per argument) 
            returning a tuple whose 0th item is a list of VM commands and the 1th item
            is the number of parameters in the subroutine. ''' 
        result = []
        num_params = 0

        result.append((self.indentation * ' ') + '<expressionList>')
        self.indentation += 2

        tokenTuple = self.__peekAtNextEntry()
        if tokenTuple[TT_TOKEN] != ')' :
            num_params = num_params + 1
            result.extend(self.__compileExpression())
            tokenTuple = self.__peekAtNextEntry()
            while tokenTuple[TT_TOKEN] == ',' :
                num_params = num_params + 1
                # ,
                tokenTuple = self.__getNextEntry()
                result.append((self.indentation * ' ') + tokenTuple[TT_XML])

                # expression
                result.extend(self.__compileExpression())
                tokenTuple = self.__peekAtNextEntry()


        self.indentation -= 2
        result.append((self.indentation * ' ') + '</expressionList>')

        # num_from_st = self.st.howMany(SEG['arg'],self.st.subroutineScope)

        return (result, num_params)


    def __compileSubroutineCall(self):
        ''' compiles a subroutine call.
            returning a list of VM commands. '''
        # Reset function dictionary
        #self.st.startSubroutine()

        result = []
        #no additional indentation or tag, just here as it is used multiple places
        #write once, use many

        # varname | classname
        tokenTuple = self.__getNextEntry()
        result.append((self.indentation * ' ') + tokenTuple[TT_XML])
        #VM
        varname = tokenTuple[TT_TOKEN]

        tokenTuple = self.__peekAtNextEntry()

        # function
        if(tokenTuple[TT_TOKEN] == '('):

            # (
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            self.vmInstList.append('push pointer 0')
            values = self.__compileExpressionList()
            num_of_args = values[1]
            xml_code = values[0]

            result.extend(xml_code)

            # )
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])


            self.vmInstList.append('call '+self.currentClassName+'.'+varname+' '+str(num_of_args+1))



        else:

            #TODO: get data from ST
            #Check if the varname is Object or a variable
            numOfargs = 0
            if(varname in self.st.subroutineScope or varname in self.st.classScope):
                result.append((self.indentation * ' ') + self.st.getIdentifierXML(varname, 2))
                # if varname is a variable then we have to add as first arg in ST.
                kindOfvar = self.st.kindOf(varname)
                indexOfvar = self.st.indexOf(varname)
                self.vmInstList.append('push '+kindOfvar+' '+str(indexOfvar))
                # in case we have an identifier we have to replace it with its Object type on call  .
                # self.st.define(varname, kindOfvar, SEG['arg'], self.st.subroutineScope)
                varname = self.st.typeOf(varname)
                numOfargs = 1

            # .
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # subroutine name
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # Add obj as first arg of method
            #VM
            subroutineName = tokenTuple[TT_TOKEN]

            # (
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # Handle tuple
            values = self.__compileExpressionList()
            xml_values = values[0]
            number_args_in_list = values[1]

            result.extend(xml_values)
            # )
            tokenTuple = self.__getNextEntry()
            result.append((self.indentation * ' ') + tokenTuple[TT_XML])

            # Method VM
            self.vmInstList.append('call '+varname+'.'+subroutineName+' '+str(numOfargs + number_args_in_list))
            # TODO: Whats going on here?
            # self.vmInstList.append('pop temp 0')
            # self.vmInstList.append('push constant 0')

        return result
        
        
    #
    #the above does not preclude you from defining and using any helper functions
    #
