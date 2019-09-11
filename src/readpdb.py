import sys


class Pdb:

    def read_pdb(self):
        with open(filename) as filin:
            return(filin.readlines())

    def read_top(self):
        dico = {}
        for line in self.rawlines:
            if(line[0:10] == "HEADER    "):
                dico['header'] = line
            elif(line[0:10] == "COMPND   2"):
                dico['compound'] = line
            elif(line[0:10] == "SOURCE   2"):
                dico['source'] = line
            elif(line[0:10] == "AUTHOR   "):
                dico['author'] = line

    def __init__(self, filename):
        self.rawlines = self.read_pdb(filename)
        self.dico = self.read_top()


if __name__ == '__main__':
    if(len(sys.argv)<2):
        print("not enough arguments")
    else:
        pdb = Pdb(sys.argv[1]).rawlines
