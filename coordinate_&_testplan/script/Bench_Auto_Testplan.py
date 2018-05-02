import sys
import time
import json
import xlrd
import re

class Main():

    def __init__(self):
        path           = sys.path[0].rstrip('script')
        input_testplan = path + 'Testplan.xlsx'
        input_Coordina = path + 'Absolute_Coordinates.json'
        test_structure = path + '/script/Testplan_Structure.json'

        with open(input_Coordina, 'r') as f:
            self.data = json.load(f)

        with open(test_structure, 'r') as f:
            self.struc = json.load(f)
        
        print(' 选择一个 sheet : ')
        all_dev = {};select = ''
        for i,dev in enumerate(self.struc):
            all_dev[str(i+1)] = dev; print(' ',i+1,' > ',dev)
        while select not in all_dev:
            select = input(' Sheet : ')
            
        dev        = all_dev[select]
        self.struc = self.struc[dev]
        self.ws    = xlrd.open_workbook(input_testplan).sheet_by_name(dev)
        
        time0      = time.strftime("%Y%m%d", time.localtime())
        self.fnew1 = open(path + '/output/' + 'bench_auto_die_info_%s.txt'%time0,'w')
        self.fnew2 = open(path + '/output/' + 'bench_auto_testplan_%s.txt'%time0,'w')
        self.write_die_info()
        print(' bench_auto_die_info_%s 已生成完毕...'%time0)
        self.write_auto_testplan()
        print(' bench_auto_testplan_%s 已生成完毕...'%time0)

    def title_col_data(self,title):
        first_row = self.ws.row_values(0)
        index = first_row.index(title)
        return self.ws.col_values(index)[1:]
        
    def col(self,x):
        if len(x) == 1 : col = ord(x)-ord('A')
        elif len(x) == 2 : col = 26 + ord(x[1]) - ord('A')
        return col

    def analysis(self,row,key):
        format = self.struc[key]
        if 'Auto_Generate' in format:
            # the subdie_index
            return str(row)
        if 'User_Defined_in_Col' in format:
            # the Item should be filled by user in excel
            col_U = self.col(re.search('Col_(\w)',format).groups()[0])
            value = self.ws.cell_value(row,col_U)
            # the number itself should be integer absolutely
            if '$int' in format: return str(int(value))
            # the number suggest to round 5
            elif '$round' in format: return str(round(value,5))
            else: return value
        else:
            # such as "N/A" "bsim4" "{}" ...
            return format
        
    def write_die_info(self):
        dies = self.title_col_data('Golden_Die')   
        dies_ = []
        for die in dies:
            x_y = re.findall('-?\d',die)
            if x_y == [] : dies_.append('')
            else : dies_.append(x_y[0]+'_'+x_y[1])
        
        if '' in set(dies_): 
            non_repeat = len(set(dies_)) - 1
        else:
            non_repeat = len(set(dies_))
            
        self.fnew1.write('List of group mesured\n')
        self.fnew1.write('*die group_index\n')
        for i,die in enumerate(dies_):
            self.fnew1.write(die + ' ' + str(i+1) + '\n')
        self.fnew1.close()

    def write_auto_testplan(self):
        setups = self.title_col_data('Setup_File_Name')
        max_setup = max([len(x) for x in setups])

        Total = self.ws.nrows - 1
        # write in header
        time1 = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        self.fnew2.write('************ BSIMPro+ Sub-die Naming Data *************\n')
        self.fnew2.write('************    Created by Grothendieck   *************\n')
        self.fnew2.write('TIME = %s\n'%time1)
        self.fnew2.write('PLAN_MAP =  C:/users/xxxxxxxxxxxxxxxxxxxxxxxxxx/ooooooooooooooooooooooooooooooo.wfd\n')
        self.fnew2.write('TOTAL_SUBDIE = %s\n'%Total)
        self.fnew2.write('\nSUBSITE :\n')
        self.fnew2.write('             ')
        # write in the titles
        for title in self.struc:
            if title == 'Setup_File_Name':
                self.fnew2.write(title.ljust(max_setup+10))
            else:
                self.fnew2.write(title.ljust(20))
        self.fnew2.write('\n')
        # write in values
        for row in range(1,Total+1):
            self.fnew2.write('             ')
            for key in self.struc:
                if key == 'Setup_File_Name':
                    self.fnew2.write(self.analysis(row,key).ljust(max_setup+10))
                else:
                    self.fnew2.write(self.analysis(row,key).ljust(20))
            self.fnew2.write('<Comments>:\n')

        self.fnew2.close()

if __name__=='__main__':
    Main()