#
#JackAnalyzer.py
#
# CS2011   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 15 Nov 2022
#

import sys  #for command line launch functionality
from pathlib import *  #for sane and modern file access

from JackTokenizer import *
from CompilationEngine import *
from JTConstants import *


############################################
# Class
class JackAnalyzer(object):

##########################################
#Constructor

    def __init__(self, target):
        self.targetPath = Path(target)







##########################################
#instance methods

    def process(self):
        ''' manages overall flow for the input FilePath being compiled. 
            returns a string representing the name of the target being compiled when complete 
        '''
        if self.targetPath.is_dir():
            
            #manage cross OS differences in directory iterations
            paths_for_rearranging = [
                Path(path)
                for path in self.targetPath.iterdir()
            ]
            sorted_paths = sorted(paths_for_rearranging)
            
            for eachFile in sorted_paths:
                if eachFile.suffix == '.jack':
                    self.__processFile(eachFile)
        else:
            if (self.targetPath.suffix != '.jack'):
                raise RuntimeError("Error, cannot use the filename: " + self.targetPath.name )

            self.__processFile(self.targetPath)
        
        return str(self.targetPath)



##########################################
#private methods
    
    def __processFile(self, filePath):
        ''' Compiles the target Path passed via the arg -filePath.
            while it does not return anything, it outputs various text files for compilation process.
               an XML file named xxxT.XML as a raw list of tagged tokens
               a formatted XML file named xxx.XML indicating the full syntax and semantic relationships of the tokens
               a text file named xxx.vm which is the compiled final output.
          '''

        # XML.Tokens file

        tokenOutputFilePath = filePath.parent / (filePath.stem + 'T.xml')
        tokenList = self.__tokenize(filePath)
        self.__output(tokenOutputFilePath, tokenList)

        #XML file

        intermediateOutputFilePath = filePath.parent / (filePath.stem + '.xml')
        ce = CompilationEngine(tokenList)
        compiledXML = ce.compileTokens()
        self.__output(intermediateOutputFilePath, compiledXML)

        # VM file

        vmFile = filePath.parent / (filePath.stem + '.vm')
        self.__output(vmFile, ce.get_vmInstructions())


    def __tokenize(self, filePath):
        ''' tokenizes the file, returns a list of one XML-formatted token per line'''

        # Convert the .jack file into a list with a line in every element
        # Filter the list to remove comments and whitespaces through the various filter methods in JackTokenizer
        # Traverse each line, identify each word and create the appropriate token through __wrapTokenInXML method

        ''' 
        STEP 1:Read file and return a list with each element to be a line of the .jack file
        STEP 2 Filter the list to remove all kind of comments!
        STEP 3 Read the list and return a new list with a word in each element
        STEP 4 Tokenize the list and add the right token type before and after. '''

        tokenList = []

        jt = JackTokenizer(filePath)

        # STEP 1 and 2
        filteredlist = jt.toParse

        # list_per_word = [word for sentence in filteredlist for word in sentence.split()]


        tokenList.append('<tokens>')
        for line in filteredlist:
            tokenList.extend(jt.parseLine(line))
        tokenList.append('</tokens>')
        return tokenList


    def __wrapTokenInXML(self, token):
        ''' returns a string where the token is properly sandwiched between type tags'''
        # identify each word received and create the appropiate token through the 3 methods (__parseInt, __parseString, __parseChar)



    def __output(self, filePath, codeList):
        ''' outputs the VM code codeList into a file and returns the file path'''
            
        file = open(str(filePath), 'w')
        file.write("\n".join(codeList))
        file.close()
        return filePath

    


#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

##    target = sys.argv[1]         # use this one for final deliverable
    
    #project 10 tests
##   target = 'ExpressionlessSquare'
##     target = 'ArrayTest'
##    target = 'Square10'


    #project 11 tests
##    target = 'Seven'
##    target = 'ConvertToBin'
##    target = 'square11'
##    target = 'Average'
##    target = 'Pong'
    target = 'ComplexArrays'
    
    analyzer = JackAnalyzer(target)
    print('\n' + analyzer.process() + ' has  been translated.')






