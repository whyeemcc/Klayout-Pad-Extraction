import sys
import time
import xlrd
import json

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
        
        time0     = time.strftime("%Y%m%d", time.localtime())
        self.fnew = open(path + '/output/' + 'bench_sub_die_card_%s.txt'%time0,'w')
        self.write()
        print(' bench_sub_die_card_%s 已生成完毕...'%time0)

    def title_col_data(self,title):
        first_row = self.ws.row_values(0)
        index = first_row.index(title)
        return self.ws.col_values(index)[1:]        

    def write(self):
        devices = self.title_col_data('Device_Name')
        tks  = [x.upper() for x in devices]
        # check the module list, if not in Absolute_Coordinates.json, stop
        for tk in tks:
            mdu = tk[:-1]
            if mdu not in self.data:
                input("\n '%s' module does not exist in Absolute_Coordinates.json !"%mdu);exit()

        shrink = self.data['Shrink']
        reference = eval(self.data['Reference'])

        for tk in tks:
            mdu = tk[:-1]
            coordinate = eval(self.data[mdu]["1"])
            # y axis should be inverse due to the wat machine
            x = round((coordinate[0]-reference[0])*shrink)
            y = round((coordinate[1]-reference[1])*shrink)
            self.fnew.write(str(x) + ',' + str(y) + ',' + tk + '\n')

        self.fnew.close()

if __name__=='__main__':
    Main()