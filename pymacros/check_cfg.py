import pya
# Author : Grothendieck
class Check:
    """
    check the config value which you filled in.
    """
    def __init__(self,search_cells,layer_num,data_type):
        self.layout = pya.CellView().active().layout()
        self.search_cells = search_cells
        self.layer_num = layer_num
        self.data_type = data_type
        # start to check
        self.Pass = True
        self.check_cell()
        self.check_layer()
        self.report()
        
    def check_cell(self):
        for cell in self.search_cells:
            if self.layout.has_cell(cell) is False:            
                print('%s cell do not exist in this acticve layout !'%cell)
                self.Pass = False

    def check_layer(self):
        if self.layout.find_layer(self.layer_num,self.data_type) is None:
            print('%s/%s layer do not exist in this acticve layout !'%(self.layer_num,self.data_type))
            self.Pass = False
            
    def report(self):
        if self.Pass is True:
            print('pass the check.\n')
        else:
            exit()