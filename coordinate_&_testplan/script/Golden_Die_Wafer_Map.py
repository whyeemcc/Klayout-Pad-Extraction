import sys
import json
import xlrd
import re
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Main():

    '''
    draw a circle signify a wafer
    square means independent die
    '''
    def __init__(self):
        path           = sys.path[0].rstrip('script')
        input_testplan = path + 'Testplan.xlsx'
        test_structure = path + '/script/Testplan_Structure.json'

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
        
        self.coordinate = self.die_info()
        if len(self.coordinate) == 0:
            print(' none golden die...');exit()
        else:
            fig=plt.figure()
            self.ax = fig.add_subplot(111,aspect='equal')
            self.draw()
            time0 = time.strftime("%Y%m%d", time.localtime())   
            fig.savefig(path + '/output/' + 'golden_die_map_%s.png'%time0)
            print(' golden_die_map_%s 已生成完毕...'%time0)
            
    def title_col_data(self,title):
        first_row = self.ws.row_values(0)
        index = first_row.index(title)
        return self.ws.col_values(index)[1:]

    def die_info(self):
        dies = self.title_col_data('Golden_Die')   
        dies_ = []
        for die in dies:
            x_y = re.findall('-?\d',die)
            if x_y == [] : pass
            else : dies_.append((eval(x_y[0]),eval(x_y[1])))        
        return dies_

    def non_repeat(self):
        dies_ = self.coordinate
        return len(set(dies_))
        
    def radius(self):
        # max value of coordinates
        s = str(self.coordinate).lstrip('[').rstrip(']').replace('(','').replace(')','')
        maxXY = max([abs(eval(x)) for x in s.split(',') if x.strip()])
        return maxXY + 1  
        
    def draw(self):
        maxDie = self.radius()
        # draw a circle
        self.addCircle(0,0,maxDie,'none','black')
        # draw squares
        for die in [(x,y) for x in range(-maxDie+1,maxDie) for y in range(-maxDie+1,maxDie)]:
            x,y = die[0],die[1]
            if die in self.coordinate:
                self.addRectangle(x,y,'blue','white')
            else:
                if (abs(x)+0.5)**2 + (abs(y)+0.5)**2 <= maxDie**2:
                    self.addRectangle(x,y,'grey','white')        
        self.style()

    def style(self):
        maxDie = self.radius()
        try:
            self.ax.set_xticks(range(-maxDie,maxDie+1))
            self.ax.set_yticks(range(-maxDie,maxDie+1))
            self.ax.set_xlim(-maxDie,maxDie)
            self.ax.set_ylim(-maxDie,maxDie)
        except:
            pass
        self.ax.invert_yaxis() 
        plt.title('Total : %s'%self.non_repeat())

    def addCircle(self,x,y,radius,faceColor,edgeColor):
        self.ax.add_patch(patches.Circle(
                            (x,y),          # center
                            radius,         # radius
                            facecolor = faceColor,
                            edgecolor = edgeColor)
                        )

    def addRectangle(self,x,y,faceColor,edgeColor):
        self.ax.add_patch(patches.Rectangle(
                            (x-0.5,y-0.5),  # left,bottom
                            1,              # width
                            1,              # height
                            facecolor = faceColor,
                            edgecolor = edgeColor)
                        )
if __name__=='__main__':
    Main()                        