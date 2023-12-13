#
#SymbolTable.py
#
# CS2011   Project 10/11 Jack Compiler
#
# Fall 2019
# last updated 14 Oct 2021
#      last verified 15 Nov 2022
#


from JTConstants import *

#public constant
SYM_DEFINE = 0
SYM_USE = 2


#constant only needed inside this file
TYPE = 0
KIND = 1
INDEX = 2

#map from Jack language purpose term in SymbolTable, to VM segment name
SEG_VM_TO_JACK = {'static':'static', 'this':'field', 'argument':'arg', 'local':'var'}

class SymbolTable(object):

############################################
# Constructor
    def __init__(self):
        self.classScope = dict()
        self.subroutineScope = dict()



############################################
# instance methods

    def startSubroutine(self):
        ''' starts a subroutine scope. '''
        # Reset the values of dict in order to be used in the next function!
        self.subroutineScope.clear()

    
    def define(self, name, identifierType, kind, dictionary):
        ''' defines a new identifier into the table.
            gets index for appropriate segment and places entry into correct scope
             static and field into class
             arg and var into subroutine
     
            arguments:
             -name:             the identifier itself
             -identifierType:   string identifying the type
             -kind:             'static' | 'field' | 'arg' | 'var'
        '''

        last_index = self.howMany(kind,dictionary)

        # Check that this var doesn't already exist
        if (name in dictionary):
            raise RuntimeError('Error, you cannot define the same var 2 times')
        else:
            dictionary[name] = (identifierType,kind,last_index)


    def typeOf(self, name):
        ''' returns the type of the identifier'''

        if name in self.subroutineScope:
            return self.subroutineScope[name][TYPE]
        elif name in self.classScope:
            return self.classScope[name][TYPE]
        else:
            raise RuntimeError('Error, the var '+name+' hasn\'t defined in the program!')


    def kindOf(self, name):
        ''' returns the kind of the identifiers:
            'static' | 'field' | 'arg' | 'var' '''

        if name in self.subroutineScope:
            return self.subroutineScope[name][KIND]
        elif name in self.classScope:
            return self.classScope[name][KIND]
        else:
            raise RuntimeError('Error, the var ' + name + ' hasn\'t defined in the program!')


    def indexOf(self, name):
        ''' returns the segment index of the identifier'''

        if name in self.subroutineScope:
            return self.subroutineScope[name][INDEX]
        elif name in self.classScope:
            return self.classScope[name][INDEX]
        else:
            raise RuntimeError('Error, the var ' + name + ' hasn\'t defined in the program!')



    def getIdentifierXML(self, name, how):
        ''' returns a properly formatted XML line for the variable -name
                -how:  SYM_DEFINE | SYM_USE '''
        
        type = self.typeOf(name)
        kind = self.kindOf(name)
        index = self.indexOf(name)
        dic = ''
        if(name in self.subroutineScope):
            dic = 'subroutine'
        else:
            dic = 'class'

        if (how == SYM_DEFINE ):
            return '<SYMBOL-Defined> '+dic+'.'+name+' ('+SEG_VM_TO_JACK[kind]+' '+type+') = '+str(index)+' </SYMBOL-Defined>'
        else:
            return '<SYMBOL-Used> ' + dic + '.' + name + ' (' + SEG_VM_TO_JACK[kind] + ' ' + type + ') = ' + str(index) + ' </SYMBOL-Used>'



    def howMany(self, kind, dictionary):
        ''' returns how many variables have been declared for segment kind
                -kind:  'static' | 'field' | 'arg' | 'var' '''

        count = 0
        for key,value in dictionary.items():
            if kind == value[KIND]:
                count = count+1
        return count