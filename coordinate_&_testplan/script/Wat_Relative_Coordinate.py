import sys
import time
import xlrd
import json

class Main():

    def __init__(self):
        path           = sys.path[0].rstrip('script')
        input_testplan = path + 'Testplan.xlsx'
        input_Coordina = path + 'Absolute_Coordinates.json'
        
        with open(input_Coordina, 'r') as f:
            self.data = json.load(f)

        self.ws = xlrd.open_workbook(input_testplan).sheet_by_name('For_WAT')
        
        time0 = time.strftime("%Y%m%d", time.localtime())
        self.fnew = open(path + '/output/' + 'wat_relative_%s.die'%time0,'w')
        self.write()
        print(' wat_relative_%s 已生成完毕...'%time0)

    def frame(self,max1,max2):
        self.fnew.write('$----'+' ')
        self.fnew.write('-'*(max1+2)+' ')
        self.fnew.write('-'*max2+' ')
        self.fnew.write('- - -\n')

    def write(self):
        time1 = time.strftime("%m/%d/%Y", time.localtime())
        time2 = time.strftime("%H:%M:%S", time.localtime())
        self.fnew.write(
        '''\
#Die   Unknow   1    %s   %s    Grothendieck auto Create this Die spec.

$Type: Die
$Name: Unknow
$Vers: 1
$Desc: Grothendieck auto Create this Die spec.
$Date: %s
$Time: %s
$User: tdeng
'''%(time1,time2,time1,time2))

        modules  = [x.upper() for x in self.ws.col_values(0)[1:]]
        # check the module list, if not in Absolute_Coordinates.json, stop
        for mdu in modules:
            if mdu not in self.data:
                input("\n '%s' module does not exist in Absolute_Coordinates.json !"%mdu);exit()

        shrink = self.data['Shrink']
        reference = eval(self.data['Reference'])
        center_r  = (reference[0]+1/2*reference[2],reference[1]+1/2*reference[3])

        coordinate_str_list = []
        for mdu in modules:
            coordinate = eval(self.data[mdu]["1"])
            center = (coordinate[0]+1/2*coordinate[2],coordinate[1]+1/2*coordinate[3])
            # y axis should be inverse due to the wat machine (Except MPPT machine)
            delta_x = round((center[0]-center_r[0])*shrink)
            delta_y = round((center[1]-center_r[1])*shrink*-1)
            coordinate_str_list.append(str(delta_x)+','+str(delta_y))

        mdu_len = [len(x) for x in modules]
        cor_len = [len(x) for x in coordinate_str_list]
        max_mdu_len = max(mdu_len) 
        max_cor_len = max(cor_len)        

        self.frame(max_mdu_len,max_cor_len)
        self.fnew.write(' BODY\n')
        for mdu,co in zip(modules,coordinate_str_list):
            self.fnew.write('      '+('`%s`'%mdu).ljust(max_mdu_len+2)+' '+ co.ljust(max_cor_len) + '\n')
        self.frame(max_mdu_len,max_cor_len)

        self.fnew.close()

if __name__=='__main__':
    Main()