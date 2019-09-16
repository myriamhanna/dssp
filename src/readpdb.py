import sys
import math
import os

class Pdb:
    def __init__(self, filename):
        #self.filename = "../data/1est_H.pdb"
        self.filename = filename
        self.lines = self.read_pdb(filename)
        #self.dico = self.read_top()
        self.content = {}
        #self.atom_names = [' N  ', ' C  ', ' H01', ' O  ']
        self.atom_names = ['N', 'C', 'H01', 'O']

    def read_pdb(self, filename):
        with open(filename) as filin:
            return filin.readlines()


    def get_info(self):
        cpt = 0
        mylist = []
        for line in self.lines:
            if line[0:6].strip() == "ATOM":
                if cpt == 0:
                    prev_nb = line[22:26]
                    prev_resname = line[17:20].strip()
                if line[22:26] != prev_nb:
                    mylist.append(prev_resname)
                    self.content[(prev_nb.strip())] = mylist
                    prev_nb = line[22:26]
                    prev_resname = line[17:20]
                    mylist = []
                if line[12:16].strip() in self.atom_names:
                    mylist.append(line[12:16].strip())
                    mylist.append(float(line[30:38]))
                    mylist.append(float(line[38:46]))
                    mylist.append(float(line[46:54]))
                    #print(line[30:38])
                    #print(mylist)
                cpt += 1

    #def energy_Hbonds(self):
    #    """ method that return the energy between atoms that form Hbonds"""
    #    q1 = 0.42
    #    q2 = 0.20
    #    f = 332


    def find_nturns(self):
        q1 = 0.42
        q2 = 0.20
        f = 332

        for i, j in enumerate(list(self.content.keys())):
            #print(i, j)
            #print(type(i))
            #print(type(j))
            #print(self.content[list(self.content.keys())[i]][9])
            #print(self.content[list(self.content.keys())[i+3]][1])

            r_ON = math.sqrt((self.content[list(self.content.keys())[i]][9] - self.content[list(self.content.keys())[i+3]][1])**2 +
                            (self.content[list(self.content.keys())[i]][10] - self.content[list(self.content.keys())[i+3]][2])**2 +
                            (self.content[list(self.content.keys())[i]][11] - self.content[list(self.content.keys())[i+3]][3])**2)
            r_CH = math.sqrt((self.content[list(self.content.keys())[i]][5] - self.content[list(self.content.keys())[i+3]][13])**2 +
                            (self.content[list(self.content.keys())[i]][6] - self.content[list(self.content.keys())[i+3]][14])**2 +
                            (self.content[list(self.content.keys())[i]][7] - self.content[list(self.content.keys())[i+3]][15])**2)
            r_OH = math.sqrt((self.content[list(self.content.keys())[i]][9] - self.content[list(self.content.keys())[i+3]][13])**2 +
                            (self.content[list(self.content.keys())[i]][10] - self.content[list(self.content.keys())[i+3]][14])**2 +
                            (self.content[list(self.content.keys())[i]][11] - self.content[list(self.content.keys())[i+3]][15])**2)
            r_CN = math.sqrt((self.content[list(self.content.keys())[i]][5] - self.content[list(self.content.keys())[i+3]][1])**2 +
                            (self.content[list(self.content.keys())[i]][6] - self.content[list(self.content.keys())[i+3]][2])**2 +
                            (self.content[list(self.content.keys())[i]][7] - self.content[list(self.content.keys())[i+3]][3])**2)


        E = q1*q2*(1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)*f
        #E = 3
        #print(r_ON)
        #print(r_CH)
        #print(r_OH)
        #print(r_CN)
        return E



    #def find_bridges(self):


#    def find_helices(self):



if __name__ == '__main__':
    pdb = Pdb(sys.argv[1])
    #pdb=Pdb()
    #pdb.read_top()
    pdb.get_info()
    print(pdb.find_nturns())

    #print(pdb.content["16"][1])
    #print(int(list(pdb.content.keys())[0]))
