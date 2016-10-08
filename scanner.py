from parser import Parser

class Scanner:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.token = []
        self.parser = Parser(self)

    def moreTokens(self):
        if self.getToken() == '':
            return False
        else:
            return True

    def isSymbol(self,c):
        if c == '+' or c == '-' or c == '*' or c == '/' or c == '%':
            return True
        elif c == '[' or c == ']' or c == '(' or c == ')' or c == ',':
            return True
        else:
            return False

    def getWord(self):
        c = self.file.read(1)
        while c:
            if not c.isalpha():
                # make cursor point to previous c
                self.file.seek(-1, 1)
                break
            else:
                self.token.append(c)
                c = self.file.read(1)

    def getDigit(self):
        if self.token.pop() == '0':
            return
        else:
            c = self.file.read(1)
            while c:
                if c.isspace():
                    break
                else:
                    self.token.append(c)
                    c = self.file.read(1)

    def isComparisonOperator(self,c):
        if c == '!' or c == '=' or c == '>' or c == '<':
            return True
        else:
            return False

    def getComparisonOperator(self):
        c = self.file.read(1)
        if c == '=':
            self.token.append(c)
        # make cursor point back to '='
        else:
            self.file.seek(-1, 1)

    def getNextToken(self):
        c = self.file.read(1)
        self.token = []
        while c:
            if c.isspace():
                c = self.file.read(1)
                continue
            elif c.isalpha():
                self.token.append(c)
                self.getWord()
                break
            # just tokenizing one digit at a time!!!!!!
            elif c.isdigit():
                self.token.append(c)
                # getDigit(file,token)
                break
            elif self.isComparisonOperator(c):
                self.token.append(c)
                self.getComparisonOperator()
                self.token = ''.join(self.token)
                break
            if self.isSymbol(c):
                self.token.append(c)
                break
            else:
                c = self.file.read(1)

        return self.getToken()

    def getToken(self):
        return ''.join(self.token)

    def peekNextToken(self):
        self.getNextToken()
        temp = self.getToken()
        # for now i am just using this function for D[0], that is why i revert back only one character
        self.file.seek(-1,1)
        return temp

    def simulateParser(self):
        self.parser.program()