import sys

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
    
    def error(nonterminal):
        print("self.error: not a valid " + "<" + nonterminal + ">")
        sys.exit()

    def printAll(self):
        self.scanner.getNextToken()
        while self.scanner.moreTokens():
            print(self.scanner.getToken())
            self.scanner.getNextToken()

    def program(self):
        print("Program")
        while self.statement():
            continue

    def statement(self):
        print("Statement")
        if self.set():
            return True
        elif self.jump():
            return True
        elif self.jumpt():
            return True
        elif self.halt():
            return False
        else:
            self.error("Statement")

    def jump(self):
        if self.scanner.getToken() == "jump":
            print("Jump")
            self.scanner.getNextToken()
            return self.expression()
        else:
            return False

    def jumpt(self):
        if (self.scanner.getToken() == "jumpt"):
            print("Jumpt")
            self.scanner.getNextToken()

            if not self.expression():
                self.error("Jumpt")

            if (self.scanner.getToken() == ","):
                self.scanner.getNextToken()

                if not self.expression():
                    self.error("Jumpt")

                if self.equalitiesCheck():
                    self.scanner.getNextToken()

                    if not self.expression():
                        self.error("Jumpt")
                else:
                    self.error("Jumpt")
            else:
                self.error("Jumpt")

            return True
        else:
            return False

    def equalitiesCheck(self):
        token = self.scanner.getToken()
        if token == "<" or token == "<=" or token == ">" or token == ">=":
            return True
        elif token == "==" or token == "!=":
            return True
        else:
            return False

    def expression(self):
        print("Expr")
        truth = self.term()

        while self.termCheck():
            truth = self.term()
            continue

        return truth

    def termCheck(self):
        if self.scanner.getToken() == "+" or self.scanner.getToken() == "-":
            self.scanner.getNextToken()
            return True
        else:
            return False

    def term(self):
        print("Term")
        truth = self.factor()

        while self.factorCheck():
            truth = self.factor()
            continue

        return truth

    def factorCheck(self):
        if self.scanner.getToken() == '*' or self.scanner.getToken() == '/' or self.scanner.getToken() == '%':
            self.scanner.getNextToken()
            return True
        else:
            return False

    def factor(self):
        print("Factor")
        # the problem is here with the 5 followed by the comma,
        # sets if number to false
        if self.number():
            print("Number")
            return True
        elif self.scanner.getToken() == 'D':
            temp = self.scanner.peekNextToken()
            if temp == '[':
                # the token matches so consume the char '['
                self.scanner.getNextToken()
                # call getNextToken one more time to advance to digit between '0..9'
                self.scanner.getNextToken()

                if not self.expression():
                    self.error("Factor")

                if self.scanner.getToken() == ']':
                    # we have matched with D[<Expr>]
                    self.scanner.getNextToken()
                    return True
                else:
                    self.error("Factor")
            else:
                self.error("Factor")
            return True

        elif self.scanner.getToken() == '(':
            self.scanner.getNextToken()
            self.expression()
            if self.scanner.getToken() == ')':
                # we have matched with (<Expr>)
                self.scanner.getNextToken()
                return True
            else:
                self.error("Factor")
        else:
            return False

    def number(self):
        if self.scanner.getToken().isdigit():
            if self.scanner.getToken() == '0':
                self.scanner.getNextToken()
            else:
                self.scanner.getNextToken()
                self.pullAllNumbers()
            return True
        else:
            return False

    def pullAllNumbers(self):
        while self.scanner.getToken().isdigit():
            self.scanner.getNextToken()

    def set(self):
        if self.scanner.getToken() == "set":
            print("Set")
            self.scanner.getNextToken()

            if self.scanner.getToken() == "write":
                self.scanner.getNextToken()
            else:
                if not self.expression():
                    self.error("Set")

            if self.scanner.getToken() == ",":
                self.scanner.getNextToken()

                if self.scanner.getToken() == "read":
                    self.scanner.getNextToken()
                else:
                    if not self.expression():
                        self.error("Set")

            else:
                self.error("Set")

            return True

        else:
            False

    def halt(self):
        return self.scanner.getToken() == "halt"
