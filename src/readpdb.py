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

                cpt += 1

    def energy_Hbonds(self, idx1, idx2):
        """ method that return the energy between atoms that form Hbonds, dans ma tête cette fonction calcul les distances r_ON , r_CH ..
        entre deux residus et genre on lappelle dans find n_turns et ca lutilise pour des résidus eloignés de 3, 4 ou 5 mais je sais pas
        si c'est faisable
        Une H_bond existe si E < 0.5  E = q1*q2*(1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)*f  """
        q1 = 0.42
        q2 = 0.20
        f = 332

        r_ON = math.sqrt((self.content[list(self.content.keys())[idx1]][9] - self.content[list(self.content.keys())[idx2]][1])**2 +
                       (self.content[list(self.content.keys())[idx1]][10] - self.content[list(self.content.keys())[idx2]][2])**2 +
                       (self.content[list(self.content.keys())[idx1]][11] - self.content[list(self.content.keys())[idx2]][3])**2)
        r_CH = math.sqrt((self.content[list(self.content.keys())[idx1]][5] - self.content[list(self.content.keys())[idx2]][13])**2 +
                       (self.content[list(self.content.keys())[idx1]][6] - self.content[list(self.content.keys())[idx2]][14])**2 +
                       (self.content[list(self.content.keys())[idx1]][7] - self.content[list(self.content.keys())[idx2]][15])**2)
        r_OH = math.sqrt((self.content[list(self.content.keys())[idx1]][9] - self.content[list(self.content.keys())[idx2]][13])**2 +
                       (self.content[list(self.content.keys())[idx1]][10] - self.content[list(self.content.keys())[idx2]][14])**2 +
                       (self.content[list(self.content.keys())[idx1]][11] - self.content[list(self.content.keys())[idx2]][15])**2)
        r_CN = math.sqrt((self.content[list(self.content.keys())[idx1]][5] - self.content[list(self.content.keys())[idx2]][1])**2 +
                       (self.content[list(self.content.keys())[idx1]][6] - self.content[list(self.content.keys())[idx2]][2])**2 +
                       (self.content[list(self.content.keys())[idx1]][7] - self.content[list(self.content.keys())[idx2]][3])**2)

        E = q1*q2*(1/r_ON + 1/r_CH - 1/r_OH - 1/r_CN)*f
        return E


    def find_nturns(self):
        """ ici normalement ca devrait chercher chaque trois, 4, ou 5 residus sil y a une H bond yaane le 1er résidu avec le 3eme, le 1er
        avec le 4eme, le 1 er avec le 5e, etc..  si il ya il la save qqpart"""
        dict_nturns = {}
        for i, j in enumerate(list(self.content.keys())):
            for nb in range(3,6):
                try:
                    if self.energy_Hbonds(i, i+nb ) < - 0.5:
                        if ((j in dict_nturns and (nb - dict_nturns[j]) == 1) or (j not in dict_nturns)):
                            dict_nturns[j] = nb
                except IndexError:
                    pass

        print(3, self.count(dict_nturns, 3))
        print(4, self.count(dict_nturns, 4))
        print(5, self.count(dict_nturns, 5))


    def count(self, dict, value):
        nb_nturns = 0
        for key, val in dict.items():
            if val == value:
                nb_nturns += 1
        return nb_nturns


    def find_bridges(self):
        """ Deux sortes de bridges
         bridge paralleles: h_bond(i-1,j) et h_bond(j,i+1) OU h_bond(j-1,i) et h_bond(i,j+1)
        bridge anti paralleles: h_bond(i,j) et h_bond(j,i) OU h_bond(i-1, j+1) et h_bond(j-1, i+1)

        i et j sont deux résidus differents
        """
        dict_bridges= {}

        for idx1, value1 in enumerate(list(self.content.keys())[1:-3]):
            for idx2, value2 in enumerate(list(self.content.keys())[idx1+4:-1]):
                try:
                    idc1 = idx1 + 1
                    idc2 = idx2 + idx1 + 4

                    if (((self.energy_Hbonds(idc1, idc2) < -0.5) and (self.energy_Hbonds(idc2 , idc1) < -0.5))
                        or ((self.energy_Hbonds(idc1-1, idc2+1) < -0.5) and (self.energy_Hbonds(idc2-1 , idc1+1) < -0.5))):
                        dict_bridges[value1 +' '+ value2] = 'AP'

                    elif (((self.energy_Hbonds(idc1-1, idc2) < -0.5) and (self.energy_Hbonds(idc2 , idc1+1) < -0.5))
                        or ((self.energy_Hbonds(idc2-1, idc1) < -0.5) and (self.energy_Hbonds(idc1 , idc2+1) < -0.5))):
                        dict_bridges[value1 +' '+ value2] = 'P'

                except IndexError:
                    pass

        print('P', self.count(dict_bridges, 'P'))
        print('AP', self.count(dict_bridges, 'AP'))

#    def find_helices(self):



if __name__ == '__main__':
    pdb = Pdb(sys.argv[1])
    #pdb=Pdb()
    #pdb.read_top()
    pdb.get_info()
    #pdb.find_nturns()
    pdb.find_bridges()

    #print(pdb.content["16"][1])
    #print(int(list(pdb.content.keys())[0]))
