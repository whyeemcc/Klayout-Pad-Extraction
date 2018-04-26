import sys
import json
# Author : Grothendieck
path = sys.path[0]
path_json = path.rstrip('lib\\python\\DLLs')+'/coordinate_&_testplan'
file_json = 'Absolute_Coordinates.json'

class To_json:
    
    def __init__(self,dic):
        self.dic = dic
        # sort the modules according to their names
        self.module_list = sorted(self.dic.keys())
        self.json = open(path_json + '/' + file_json,'w')

    def write(self,words):
        self.json.write(words + '\n') 

    def puts(self):
        """
        generate a legible json format file
        """
        self.write('{')
        self.write('"Shrink" : 1,\n')
        self.write('"Reference" : "(0,0)",\n')
        for i,module in enumerate(self.module_list):
            pad_cor = self.dic[module]
            self.write('"%s" :' %module.upper())
            self.write('        {')
            for j,pad in enumerate(pad_cor):
                if j != len(pad_cor) - 1:
                  self.write('        "%s" : "%s",'%(j+1,pad)) 
                else:
                  self.write('        "%s" : "%s"'%(j+1,pad))
            if i != len(self.module_list) - 1:
                self.write('        },')
            else:
                self.write('        }')
        self.write('}')
        self.json.close()
        print("%s generate successfully."%file_json)