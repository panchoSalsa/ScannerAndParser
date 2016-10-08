from scanner import Scanner
import sys

class App:
    def run(self):
        scanner = Scanner(sys.argv[1])
        scanner.getNextToken()
        scanner.simulateParser()
