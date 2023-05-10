"""
<assignment-statement> ->
<identifier> = (<identifier> | <numerical-literal>)
{<operator> (<identifier> | <numerical-literal>)}
<identifier> -> <letter> {<letter> | <digit>}
<numerical-literal> -> [+|-] <digit> {<digit>} [. <digit> {<digit>}]
<digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letter> -> a | b | c | . . . | z | A | B | . . .| Z
<operator> -> + | - | * | / | %
"""
from pathlib import Path
from enum import Enum

numOfLines = 1  # denoting number of lines in the code
currentfile = None  # holds the object of current file
charClass = 99  # code of current character we read (set to unknown for initial)
nextToken = 0  # integer denoting the next token
operators = ['+', '-', '*', '/', '%']  # list to store all prolog symbols
lexeme = ""  # string denoting the lexeme
nextCharacter = ''  # character denoting the next character
IsError = False  # check if the program has an error
index = -1

errorFile = open("ErrorFile.txt", 'w')


# The character classes, each character and its constant
class CharacterClasses(Enum):
    OPERATOR, LETTER, DIGIT, EOF, SPECIAL, UNKNOWN = 0, 1, 2, 3, 4, 99


# The token codes, each token and its constant
class TokenCodes(Enum):
    IDENTIFIER, ADD_OP, SUBTRACT_OP, MULTIPLY_OP, DIVIDE_OP, SLASH, MOD_OP, SPACE_OP, EQUAL_OP, IDENTIFIER, NUM_LIT, UNKNOWN = (
        i for i in range(20, 33))


################################ UPDATED #########################################
def getChar():  # read one character and identify which character class it belongs to
    global nextCharacter;
    global currentfile;
    global charClass;
    global index

    nextCharacter = currentfile.read(1)
    index += 1

    if nextCharacter:
        if str.isalpha(nextCharacter):  #### CHECK IF ITS A LETTER
            charClass = CharacterClasses.LETTER

        elif str.isdigit(nextCharacter):  ##### CHECK IF ITS A DIGIT
            charClass = CharacterClasses.DIGIT

        elif nextCharacter == "\n":
            globals()['numOfLines'] += 1
            index = 0
        elif nextCharacter in operators:  #### If operators are found
            charClass = CharacterClasses.OPERATOR
        elif nextCharacter in ['(', ')']:  #### IF brackets are found
            charClass = CharacterClasses.SPECIAL
        else:
            charClass = CharacterClasses.UNKNOWN
    else:
        charClass = CharacterClasses.EOF


########### UPDATED ############
def lookup(ch):
    global nextToken;
    global violation
    if (ch == '+'):
        appendChar()
        nextToken = TokenCodes.ADD_OP
    elif (ch == '-'):
        appendChar()
        nextToken = TokenCodes.SUBTRACT_OP
    elif (ch == '*'):
        appendChar()
        nextToken = TokenCodes.MULTIPLY_OP
    elif (ch == '/'):
        appendChar()
        nextToken = TokenCodes.DIVIDE_OP
    elif (ch == '%'):
        appendChar()
        nextToken = TokenCodes.MOD_OP
    elif (ch == '.'):
        appendChar()
        nextToken = TokenCodes.DOT_OP
    elif (ch == ' '):
        appendChar()
        nextToken = TokenCodes.SPACE_OP
    elif (ch == ''):
        appendChar()
        nextToken = TokenCodes.EOF
    else:
        appendChar()
    return nextToken


def appendChar():  # append a character to the lexeme
    globals()['lexeme'] = globals()['lexeme'] + nextCharacter


def removeBlanks():  # this function is to remove or ignore all white spaces between characters
    global nextCharacter
    while (str.isspace(nextCharacter)):  # keep getting the next if there is a whitespace
        getChar()



def generateLex():
    removeBlanks()
    global lexeme;
    global charClass;
    global nextToken
    lexeme = ""

    if nextToken == TokenCodes.Letter:  ### Check to see if it starts by a letter
        generateLex()  #### TO move to next letter
        appendChar()
        if nextToken == TokenCodes.Letter or nextToken == TokenCodes.Digit:
            generateLex()
            appendChar()

        else:
            print(f'Error in line {numOfLines} at index {index}, expected a letter or a digit')
            errorFile.write(f'Error in line {numOfLines} at index {index}, expected a letter or a digit\n')
            globals()['IsError'] = True
    else:
        print(f'Error in line {numOfLines} at index {index}, expected a letter')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a letter\n')
        globals()['IsError'] = True




# DONE
def Assign_Statement():
    if nextToken == TokenCodes.IDENTIFIER:
        Identifier()
        if nextToken == TokenCodes.EQUAL_OP:
            if nextToken == TokenCodes.IDENTIFIER:
                Identifier()
            elif nextToken == TokenCodes.NUM_LIT:
                NumLit()
        else:
            print(f'Error in line {numOfLines} at index {index}, expected an Equals Sign')
            errorFile.write(f'Error in line {numOfLines} at index {index}, expected an Equals Sign\n')
            globals()['IsError'] = True

    else:
        print(f'Error in line {numOfLines} at index {index}, expected an Identifier')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a (?-)\n')
        globals()['IsError'] = True


# TODO:
# <numerical-literal> -> [+|-] <digit> {<digit>} [. <digit> {<digit>}]
def NumLit():
    if nextToken == TokenCodes.ADD_OP or nextToken == TokenCodes.SUBTRACT_OP or nextToken == TokenCodes.DIGIT:
        if nextToken == TokenCodes.DIGIT:
          ## Digit()

    else:
        print(f'Error in line {numOfLines} at index {index}, expected a digit or a +- sign')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a digit or a +- sign\n')
        globals()['IsError'] = True


'''  #### WIll be in lex instead
def Digit():
    if nextToken != TokenCodes.DIGIT:
        print(f'Error in line {numOfLines} at index {index}, expected a digit')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a digit\n')
        globals()['IsError'] = True
'''


# TODO: <identifier> -> <letter> {<letter> | <digit>}
def Identifier():
    global nextToken
    if nextToken == TokenCodes.Letter:  ### Check to see if it starts by a letter
        generateLex()  #### TO move to next letter
        if nextToken == TokenCodes.Letter or nextToken == TokenCodes.Digit:
            generateLex()
        else:
            print(f'Error in line {numOfLines} at index {index}, expected a letter or a digit')
            errorFile.write(f'Error in line {numOfLines} at index {index}, expected a letter or a digit\n')
            globals()['IsError'] = True
    else:
        print(f'Error in line {numOfLines} at index {index}, expected a letter')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a letter\n')
        globals()['IsError'] = True
