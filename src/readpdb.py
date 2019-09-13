import sys
import math
import os

class Pdb:

    def __init__(self, filename):
        self.filename = filename
        self.lines = self.read_pdb(filename)
        self.dico = self.read_top()

    def read_pdb(self, filename):
        with open(filename) as filin:
            return filin.readlines()

    def read_top(self):
        for line in self.lines:
            dico = {}
            if(line[0:10] == "HEADER    "):
                dico['header'] = line
            elif(line[0:10] == "COMPND   2"):
                dico['compound'] = line
            elif(line[0:10] == "SOURCE   2"):
                dico['source'] = line
            elif(line[0:10] == "AUTHOR   "):
                dico['author'] = lines


class Atom:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def calcul_distance3D(self):
        return math.sqrt((self.x - Atom.x)**2 + (self.y - Atom.y)**2 + (self.z - Atom.z)**2)


if __name__ == '__main__':
    pdb = Pdb(sys.argv[1]).lines
