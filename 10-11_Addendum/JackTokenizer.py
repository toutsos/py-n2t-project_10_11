#
#JackTokenizer.py
#
# CS2011   Project 10 & 11 Jack Compiler
#
# Summer 2013
# last updated 14 Oct 2021
#      last verified 15 Nov 2022
#

from JTConstants import *


############################################
# Class
class JackTokenizer(object):

    # This var will be used to keep track of the open multiline symbols that the filter will encounter while traversing the file
    openCommentSymbols = 0

############################################
# Constructor

    def __init__(self, filePath):
        loadedList = self.__loadFile(str(filePath))
        self.toParse = self.__filterFile(loadedList)
        self.line_to_parse = ''


############################################
# instance methods

    def advance(self):
        '''reads and returns the next token,
           returns None if there are no more tokens.'''
        if self.toParse:
            
        ##TODO: complete
            return

        else:
            return None


############################################
# private

    def __loadFile(self, fileName):
        '''Loads the file into memory.

           -fileName is a String representation of a file name,
           returns contents as a simple List'''
        
        # filtering of multi-line comments makes for more moving parts,
        # now is better to just load and just filter in separate functions
        #
        # adjusting this way is called "refactoring"
               
        fileList = []
        file = open(fileName,"r")
        
        for line in file:
            fileList.append(line)
            
        file.close()
        
        return fileList



    def __filterFile(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''
        
        #EOL coments, and block comments within a single line, are considered
        # as separate from multi-line comments, the inputs you get will never have
        # them mixed

        '''
            Step 1: We remove the multiline comments and return the new list
            Step 2: We traverse the new list and remove all in line comments ( start with //) 
            Step 3: We remove the element of list if it is empty string '' after strip()
        '''
        # Step 1
        filteredlist = self.__filterOutSingleLineBlockComments(fileList)
        # Step 2
        i=0
        while i< len(filteredlist):
            filteredlist[i] = self.__filterOutEndOfLineComments(filteredlist[i])
            # Step 3
            filteredlist[i] = filteredlist[i].strip()
            if(not filteredlist[i]):
                del filteredlist[i]
                i -= 1
            i += 1
        return filteredlist
        
    # x = 10 //this is an end line comment
    def __filterOutEndOfLineComments(self, line):
        '''Removes end-of-line comments and resulting whitespace.

           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty '''
        index = line.find('//')
        if index != -1:
            line = line[:index]
        return line



    ## if (x = /* this is a single line comment */ 10){
    ## /* this is a multi line comment
    ## */
    ## Be aware of the order of operations
    ## e.x /* this is a new //comment */ -> We must first check for the /* */ and then //

    ## I found it easier to traverse the whole file instead of each line in order to keep track of the open
    ## and close multiline symbols and the possibility that nested multiline comments exist.
    def __filterOutSingleLineBlockComments(self, filelist):
        '''Removes single line block comments and resulting whitespace.

           -line is a string representing single line, line endings already stripped
           returns the filtered line, which may be empty '''

        '''
           In this method we search and keep track of multiline comments.
           We return a list without multiline comments.
        '''

        in_comment = False
        comment_start = '/*'
        comment_end = '*/'
        list_without_multiline_comments = []

        for line in filelist:
            while True:
                if not in_comment:
                    start_index = line.find(comment_start)
                    if start_index != -1:
                        end_index = line.find(comment_end, start_index + len(comment_start))
                        if end_index != -1:
                            list_without_multiline_comments.append(line[:start_index] + line[end_index + len(comment_end):])
                        else:
                            list_without_multiline_comments.append(line[:start_index])
                            in_comment = True
                        break
                    else:
                        list_without_multiline_comments.append(line)
                        break
                else:
                    end_index = line.find(comment_end)
                    if end_index != -1:
                        list_without_multiline_comments.append(line[end_index + len(comment_end):])
                        in_comment = False
                        break
                    else:
                        break
        return list_without_multiline_comments

        
        
    ## Check that the next line element begins with a digit
    def __parseInt(self):
        ''' returns an integerConstant out of the line.
        
            -line is a string representing single line, line endings already stripped
            assumes there are no leading spaces '''

        '''
        POSSIBLE integers we can encounter:
            0
            0)
            0;
        '''
        intValue = ''
        for char in self.line_to_parse:
            if char.isdigit():
                intValue += char
            else:
                break
        self.line_to_parse = self.line_to_parse[len(intValue):].strip()
        return intValue



    ## Check that the next line element begins with a character
    def __parseCharacters(self):
        ''' returns a token out of the line which could be an identifier or a keyword.
        
            -line is a string representing single line, line endings already stripped
            assumes there are no leading spaces '''

        charValue = ''
        for char in self.line_to_parse:
           if char not in DELIMITERS:
               charValue += char
           else:
               break
        self.line_to_parse = self.line_to_parse[len(charValue):].strip()
        return charValue


    ## No escape chars
    ## Check that the next line element begins with " double quotes or '
    def __parseString(self):
        ''' returns a stringConstant out of the line.
        
            -line is a string representing single line, line endings already stripped
            assumes there are no leading spaces and 
            that the leading double quote has not been stripped.'''
        index = self.line_to_parse.find('"', 1)
        stringValue = self.line_to_parse[1:index]
        self.line_to_parse = self.line_to_parse[len(stringValue)+2:].strip() # +2 for the 2x " that are not part of stringValue
        return stringValue

    def __parseSymbol(self):
        ''' returns a stringConstant out of the line.

            -line is a string representing single line, line endings already stripped
            assumes there are no leading spaces and
            that the leading double quote has not been stripped.'''
        symbol = self.line_to_parse[0]
        length = 1

        # replace symbol with glyphSubstitutes
        if symbol in glyphSubstitutes:
            symbol = glyphSubstitutes[symbol]

        # Check if we have a pair of symbols (<= . >= , ++)
        if symbol in {'&lt;', '&gt;'} and self.line_to_parse[1] == '=':
            symbol =+ self.line_to_parse[1]
            length = 2
        elif symbol == '+' and self.line_to_parse[1] == '+':
            symbol =+ self.line_to_parse[1]
            length = 2

        self.line_to_parse = self.line_to_parse[length:].strip()
        return symbol


    '''
    parseLine method accepts a line as input.
    This method will continuously loop through the line removing token per token, until there is nothing left. 
    '''
    def parseLine (self, line):

        self.line_to_parse = line
        tokenList = []

        while self.line_to_parse:
            # Integer
            if self.line_to_parse[0].isdigit():
                token = self.__parseInt()
                tokenList.append('<integerConstant> '+token+' </integerConstant>')
            # Symbol
            elif self.line_to_parse[0] in SYMBOLS:
                token = self.__parseSymbol()
                tokenList.append('<symbol> ' + token + ' </symbol>')
            # String
            elif self.line_to_parse[0] == '"':
                token = self.__parseString()
                tokenList.append('<stringConstant> '+token+' </stringConstant>')
            # Character
            else:
                token = self.__parseCharacters()
                if token in KEYWORDS:
                    tokenList.append('<keyword> '+token+' </keyword>')
                else:
                    tokenList.append('<identifier> ' + token + ' </identifier>')

        return tokenList
