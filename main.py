"""
                    APPENDIX A
(1)  <program>        -> <clause-list> <query> | <query>
(2)  <clause-list>    -> <clause> | <clause> <clause-list>
(3)  <clause>         -> <predicate> . | <predicate> :- <predicate-list> .
(4)  <query>          -> ?- <predicate-list> .
(5)  <predicate-list> -> <predicate> | <predicate> , <predicate-list>
(6)  <predicate>      -> <atom> | <atom> ( <term-list> )
(7)  <term-list>      -> <term> | <term> , <term-list>
(8)  <term>           -> <atom> | <variable> | <structure> | <numeral>
(9)  <structure>      -> <atom> ( <term-list> )
(10) <atom>           -> <small-atom> | ' <string> '
(11) <small-atom>     -> <lowercase-char> | <lowercase-char> <character-list>
(12) <variable>       -> <uppercase-char> | <uppercase-char> <character-list>
(13) <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
(14) <alphanumeric>   -> <lowercase-char> | <uppercase-char> | <digit>
(15) <lowercase-char> -> a | b | c | ... | x | y | z
(16) <uppercase-char> -> A | B | C | ... | X | Y | Z | _
(17) <numeral>        -> <digit> | <digit> <numeral>
(18) <digit>          -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
(19) <string>         -> <character> | <character> <string>
(20) <character>      -> <alphanumeric> | <special>
(21) <special>        -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | &
"""

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

errorFile = open("ErrorFile.txt", 'w')


# We followed 4.2 Lexical Analysis page 173
# the following class defines the character classes, each charater with its constant respectively
class CharacterClasses(Enum):
    LOWER, UPPER, DIGIT, SPECIAL, EOF, UNKNOWN = 0, 1, 2, 3, 38, 99


# We followed 4.2 Lexical Analysis page 173
# the following class defines Token Codes, each token with its constant respectively
class TokenCodes(Enum):
    ADD_OP, SUBTRACT_OP, MULTIPLY_OP, DIVIDE_OP, SLASH, PERCENT, UNKNOWN = (i for i in range(20, 27))


numOfLines = 1  # denoting number of lines in the code
currentfile = None  # holds the object of current file
charClass = 99  # code of current character we read (set to unkown for initial)
nextToken = 0  # integer denoting the next token
operators = ['+', '-', '*', '/', '%'] #list to store all prolog symbolss
lexeme = ""  # string denoting the lexeme
nextCharacter = ''  # character denoting the next character
IsError = False  # check if the program has an error
index = -1
""""Lexical Analyzer Start"""""


def appendChar():  # append a character to the lexeme
    globals()['lexeme'] = globals()['lexeme'] + nextCharacter


################################ UPDATED #########################################
def getChar():      # read one character and identify which character class it belongs to
    global nextCharacter;
    global currentfile;
    global charClass;
    global index
    
    nextCharacter = currentfile.read(1)
    index+=1
    
    if nextCharacter: 
        if str.isalpha(nextCharacter): #### CHECK IF ITS A LETTER
            charClass = CharacterClasses.LETTER
        
        elif str.isdigit(nextCharacter): ##### CHECK IF ITS A DIGIT
            charClass = CharacterClasses.DIGIT
            
        else: ############### CHECK FOR OPERATOR and NEW LINE
            if nextCharacter == "\n":
                globals()['numOfLines'] += 1
                index = 0
            if nextCharacter in operators:
                charClass = CharacterClasses.OPERATOR
            else:
                charClass = CharacterClasses.UNKNOWN
    else:
        charClass = CharacterClasses.EOF


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
    if charClass == CharacterClasses.DIGIT:  # this implements rule 17 (<numeral>)
        appendChar()
        getChar()
        while (charClass == CharacterClasses.DIGIT):
            appendChar()
            getChar()
        nextToken = TokenCodes.INT_LIT
    elif charClass == CharacterClasses.LOWER:  # this implements rule 11 (<small-atom>)
        appendChar()
        getChar()
        while (
                charClass == CharacterClasses.LOWER or charClass == CharacterClasses.UPPER or charClass == CharacterClasses.DIGIT):
            appendChar()
            getChar()
        nextToken = TokenCodes.SMALLATOM
    elif charClass == CharacterClasses.UPPER:  # this implements rule 12 (<variable>)
        appendChar()
        getChar()
        while (
                charClass == CharacterClasses.LOWER or charClass == CharacterClasses.UPPER or charClass == CharacterClasses.DIGIT):
            appendChar()
            getChar()
        nextToken = TokenCodes.VARIABLE

    elif charClass == CharacterClasses.SPECIAL:  # this implements rule 21 which has the special characters (<special>)
        lookup(globals()['nextCharacter'])
        getChar()
        if nextToken == TokenCodes.COLON:
            lookup(globals()['nextCharacter'])
            if nextToken == TokenCodes.SUBTRACT_OP:
                getChar()
                nextToken = TokenCodes.COLONDASH
        elif nextToken == TokenCodes.QUESTION:
            lookup(globals()['nextCharacter'])
            if nextToken == TokenCodes.SUBTRACT_OP:
                getChar()
                nextToken = TokenCodes.QUERYSTART
    elif charClass == CharacterClasses.UNKNOWN:
        lookup(globals()['nextCharacter'])
        getChar()
        if nextToken == TokenCodes.SINGLEQUOTE:
            appendChar()
            getChar()
            while (
                    charClass == CharacterClasses.LOWER or charClass == CharacterClasses.UPPER or charClass == CharacterClasses.DIGIT or (
                    charClass == CharacterClasses.SPECIAL and nextCharacter != '\'')):
                appendChar()
                getChar()
            if nextCharacter == "\'":
                appendChar()
                getChar()
                nextToken = TokenCodes.ATOM
    elif charClass == CharacterClasses.EOF:
        nextToken = TokenCodes.EOF
        lexeme = "EOF"
    if nextToken == TokenCodes.SMALLATOM:
        nextToken = TokenCodes.ATOM
    return nextToken

########### UPDATED ############
def lookup(ch):
    global nextToken; global violation
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

""""Lexical Analyser End"""

""""Syntax Analyser Start -note: all rules are available at appendix A-"""


# following rule (1)
def program():
    if nextToken == TokenCodes.QUERYSTART:
        query()
    else:
        clauseList()
        query()

    # following rule (2)


def clauseList():
    clause()
    while nextToken == TokenCodes.ATOM:
        clause()


# following rule (3)
def clause():
    predicate()
    if nextToken == TokenCodes.DOT:
        generateLex()
    if nextToken == TokenCodes.COLONDASH:
        generateLex()
        predicatelist()
        if nextToken == TokenCodes.DOT:
            generateLex()
        else:
            print(f'Error in line {numOfLines}, expected a .')
            errorFile.write(f'error in line {numOfLines}, expected a .\n')
            globals()['IsError'] = True
            generateLex()
    if nextToken == TokenCodes.ATOM:
        clause()
    elif nextToken == TokenCodes.QUERYSTART:
        return
    else:
        print(f'Error in line {numOfLines} at index {index}, expected a (.) or (:-)')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a (.) or (:-)\n')
        globals()['IsError'] = True
        generateLex()
        if nextToken == TokenCodes.ATOM:
            clause()
        elif nextToken == TokenCodes.QUERYSTART:
            return


# following rule (4)
def query():
    global nextToken
    if nextToken == TokenCodes.QUERYSTART:
        generateLex()
        predicatelist()
    else:
        print(f'Error in line {numOfLines} at index {index}, expected a (?-)')
        errorFile.write(f'Error in line {numOfLines} at index {index}, expected a (?-)\n')
        globals()['IsError'] = True


# following rule (5)
def predicatelist():
    global nextToken
    predicate()
    while (nextToken == TokenCodes.COMMA):
        generateLex()
        predicate()


# following rule (6)
def predicate():
    if nextToken == TokenCodes.ATOM:
        generateLex()
        if nextToken == TokenCodes.L_PAREN:
            generateLex()
            termlist()
            if nextToken == TokenCodes.R_PAREN:
                generateLex()
            else:
                print(f"Error in line {numOfLines} at index {index}, missing )")
                errorFile.write(f"Error in line {numOfLines} at index {index}, missing )\n")
                globals()['IsError'] = True
                while nextToken != TokenCodes.EOF and nextToken != TokenCodes.DOT and nextToken != TokenCodes.COMMA:
                    generateLex()
    else:
        print(f"Error in line {numOfLines} at index {index}, no atom")
        errorFile.write(f"Error in line {numOfLines} at index {index}, no atom\n")
        globals()['IsError'] = True
        while nextToken != TokenCodes.EOF and nextToken != TokenCodes.DOT and nextToken != TokenCodes.COMMA:
            generateLex()

        # following rule (7)


def termlist():
    term()
    while nextToken == TokenCodes.COMMA:
        generateLex()
        term()


# following rule (8)
def term():
    if nextToken == TokenCodes.ATOM:
        generateLex()
        if nextToken == TokenCodes.L_PAREN:
            generateLex()
            termlist()
            if nextToken != TokenCodes.R_PAREN:
                print(f"error in line {numOfLines} at index {index}, missing )")
                globals()['IsError'] = True
                errorFile.write(f"error in line {numOfLines} at index {index}, missing ) \n")
            generateLex()
    elif nextToken == TokenCodes.VARIABLE:
        generateLex()
    elif nextToken == TokenCodes.INT_LIT:
        generateLex()
    else:
        print(f"the term is invalid in line {numOfLines} at index {index}")
        errorFile.write(f"the term is invalid in line {numOfLines} at index {index} \n")
        globals()['IsError'] = True
        while nextToken != TokenCodes.EOF and nextToken != TokenCodes.R_PAREN and nextToken != TokenCodes.COMMA:
            generateLex()


"""Syntax Analyzer End -note: all rules are available at appendix A-"""

"""Main Start"""


def Driver():
    global currentfile, numOfLines, index
    fileNumber = 1
    while (Path(str(fileNumber) + ".txt").is_file()):
        index = -1
        print("Checking file" + str(fileNumber))
        globals()['IsError'] = False
        numOfLines = 1
        currentfile = open(str(fileNumber) + ".txt")
        errorFile.write('---OPENING FILE ' + str(fileNumber) + "---\n")
        getChar()
        generateLex()
        program()
        if not globals()['IsError']:
            errorFile.write('File' + str(fileNumber) + ' program is correct\n')
        errorFile.write('---FILE ' + str(fileNumber) + " IS DONE---\n\n")
        fileNumber = fileNumber + 1

    errorFile.close()


"""Main End"""
Driver()

