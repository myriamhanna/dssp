import sys
import math
import os

class Pdb:
    def __init__(self):
        self.filename = "../data/1est_H.pdb"
        self.lines = self.read_pdb()
        self.dico = self.read_top()
        self.content = {}
        #self.atom_names = [' N  ', ' C  ', ' H01', ' O  ']
        self.atom_names = ['N', 'C', 'H01', 'O']

    def read_pdb(self):
        with open(self.filename) as filin:
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


    def get_info(self):
        cpt = 0
        mylist = []
        for line in self.lines:
            if cpt == 0:
                prev_nb = line[22:26]
                prev_resname = line[17:20].strip()
            if line[22:26] == prev_nb:
                if line[12:16].strip() in self.atom_names:
                    mylist.append(line[12:16].strip())
                    mylist.append(float(line[30:38]))
                    mylist.append(float(line[38:46]))
                    mylist.append(float(line[46:54]))
            else:
                mylist.append(prev_resname)
                self.content[str(prev_nb).strip()] = mylist
                prev_nb = line[22:26]
                prev_resname = line[17:20]
                mylist = []
            cpt += 1

"""
class Atom:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def calcul_distance3D(self):
        return math.sqrt((self.x - Atom.x)**2 + (self.y - Atom.y)**2 + (self.z - Atom.z)**2)
"""



if __name__ == '__main__':
    #pdb = Pdb(sys.argv[1]).lines
    pdb=Pdb()
    pdb.read_top()
    pdb.get_info()
    print(list(pdb.content.keys())[0])
