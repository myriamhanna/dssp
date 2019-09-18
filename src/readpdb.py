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
        self.dict_nturns = {}
        self.dict_bridges= {}
        self.list_ladders = []
        self.atom_names = ['N', 'C', 'H01', 'O']
        self.list_helices = []
        self.list_sheets = []


    def read_pdb(self, filename):
        """method """
        with open(filename) as filin:
            return filin.readlines()


    def get_info(self):
        """ gets the most useful information from the PDB files: Res name, Res ID, and atom coordinates """
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
        """ method that returns the energy between atoms that form Hbonds"""
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
        """ method that finds 3, 4, and 5 turns and save them in a dictionnary"""
        #dict_nturns = {}
        for i, j in enumerate(list(self.content.keys())):
            for nb in range(3,6):
                try:
                    if self.energy_Hbonds(i, i+nb ) < - 0.5:
                        if ((j in self.dict_nturns and (nb - self.dict_nturns[j]) == 1) or (j not in self.dict_nturns)):
                            self.dict_nturns[j] = nb
                except IndexError:
                    pass

        #print(3, self.count(self.dict_nturns, 3))
        #print(4, self.count(self.dict_nturns, 4))
        #print(5, self.count(self.dict_nturns, 5))
        #print(self.dict_nturns)


    def count(self, dict, value):
        nb_nturns = 0
        for key, val in dict.items():
            if val == value:
                nb_nturns += 1
        return nb_nturns


    def find_bridges(self):
        """ method that searches for antiparallel and parallel bridges """

        for idx1, value1 in enumerate(list(self.content.keys())[1:-1]):
            for idx2, value2 in enumerate(list(self.content.keys())[idx1+4:-1]):
                try:
                    idc1 = idx1 + 1
                    idc2 = idx2 + idx1 + 4
                    if (((self.energy_Hbonds(idc1, idc2) < -0.5) and (self.energy_Hbonds(idc2 , idc1) < -0.5))
                        or ((self.energy_Hbonds(idc1-1, idc2+1) < -0.5) and (self.energy_Hbonds(idc2-1 , idc1+1) < -0.5))):
                        self.dict_bridges[(value1, value2)] = 'AP'

                    elif (((self.energy_Hbonds(idc1-1, idc2) < -0.5) and (self.energy_Hbonds(idc2 , idc1+1) < -0.5))
                        or ((self.energy_Hbonds(idc2-1, idc1) < -0.5) and (self.energy_Hbonds(idc1 , idc2+1) < -0.5))):
                        self.dict_bridges[(value1, value2)] = 'P'

                except IndexError:
                    pass

        #print('P', self.count(self.dict_bridges, 'P'))
        #print('AP', self.count(self.dict_bridges, 'AP'))
        #print(self.dict_bridges)
        self.find_ladders()

    def find_ladders(self):
        prev_key = list(self.dict_bridges.keys())[0]
        prev_val = self.dict_bridges[prev_key]
        count = 0
        list_temp = []
        for key, val in self.dict_bridges.items():
            if count != 0:
                if math.fabs(int(key[0]) - int(prev_key[0])) == 1 and math.fabs(int(key[1] )- int(prev_key[1])) == 1 and (val == prev_val):
                    list_temp.extend([prev_key, key])
                else:
                    if len(list_temp) != 0:
                        self.list_ladders.append(list(dict.fromkeys(list_temp)))
                        list_temp = []
            prev_key = key
            prev_val = val
            count += 1
        print(self.list_ladders)
        print("\n")
        self.find_sheets()

    def merge_tuples(self,obj):
        merged_list = []
        for i in range(0, len(obj)):
            merged_list.append(str(int(obj[i][0])))
            merged_list.append(str(int(obj[i][1])))
        return merged_list

    def find_sheets(self):
        for idx, res1 in enumerate(self.list_ladders):
            for res2 in self.list_ladders[idx+1:]:
                result = self.merge_tuples(res1 + res2)
                if len(list(set([x for x in result if result.count(x) > 1])))!= 0:
                    self.list_sheets.append(res1 + res2)
        print(self.list_sheets)

    def find_helices(self):
        prev_key = list(self.dict_nturns.keys())[0]
        prev_val = self.dict_nturns[prev_key]
        list_temp = []
        for key, val in self.dict_nturns.items():
            if (int(key) - int(prev_key)) == 1 and (val == prev_val):
                list_temp.extend([prev_key, key, str(int(key)+1), str(int(key)+2)])
            else:
                if len(list_temp) != 0:
                    self.list_helices.append(list(dict.fromkeys(list_temp)))
                    list_temp = []
            prev_key = key
            prev_val = val
        print(self.list_helices)



if __name__ == '__main__':
    pdb = Pdb(sys.argv[1])
    #pdb=Pdb()
    #pdb.read_top()
    pdb.get_info()
    pdb.find_nturns()
    pdb.find_bridges()
    #pdb.find_helices()
