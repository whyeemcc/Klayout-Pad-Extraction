import pya
# Author : Grothendieck

class Core:
    """
    Extract the absolute coordinates from the given cells and pad layer
    """
    def __init__(self,search_cells,layer_num,data_type):
        self.layout = pya.CellView().active().layout()
        self.dbu = self.layout.dbu    
        # get the layer's indice
        self.search_cells = search_cells
        self.pad_layer = self.layout.layer(layer_num,data_type)
    
    def find_parent(self,child):
        """
        get the child-cell's parent-cell name
        """
        # return the child-cell object
        child_cell = self.layout.cell(child)
        for cell_index in child_cell.each_parent_cell():
            index = cell_index
        return self.layout.cell_name(index)    
    
    def cell_vector(self,parent,child):
        """
        get the vector from parent's cell origin to child's cell origin
        """
        cell_object = self.layout.cell(parent)
        for inst in cell_object.each_inst():
            if inst.cell.name == child:
                x = inst.trans.disp.x*self.dbu
                y = inst.trans.disp.y*self.dbu
                return (x,y)

    def pad_vectors(self,cell):
        """
        get the vector list from module-cell's origin to all the pad-layer's p1 point
        """
        module = self.layout.cell(cell)
        iter = self.layout.begin_shapes(module,self.pad_layer)
        pad_list = []
        while not iter.at_end():
            shape = iter.shape()
            # the pad's shape must be a box
            if shape.is_box():
                # the bbox object should be transformed into pad-cell's origin 
                box = shape.bbox().transformed(iter.trans())
                p1_x = box.p1.x*self.dbu
                p1_y = box.p1.y*self.dbu
                width = box.width()*self.dbu
                height = box.height()*self.dbu
                pad_list.append((p1_x,p1_y,width,height))
            iter.next()
        return pad_list
        
    def get_hierarchy(self,search_cell):
        """
        get the hierarchy from top_cell to the search_cell
        """
        top_cell = self.layout.top_cell().name
        hierarchy = [search_cell]
        # back propagation
        parent = self.find_parent(search_cell)
        while parent != top_cell:
           hierarchy.append(parent)
           parent = self.find_parent(parent)
        hierarchy.append(top_cell)
        hierarchy.reverse()
        
        return hierarchy
    
    def get_coordinates(self):
        """
        extract all the pad's coordinate from given cells
        dic = {'module_name_1':[(x1,y1,width,height),(x2,y2,width,height)...],...}
        """
        dic = {}
        for search_cell in self.search_cells:
            hierarchy = self.get_hierarchy(search_cell)
            # add all the vectors step by step
            x0,y0 = 0,0
            for i,cell in enumerate(hierarchy[:-1]):
                parent = hierarchy[i]
                child  = hierarchy[i+1]
                vector = self.cell_vector(parent,child)
                x0 += vector[0]
                y0 += vector[1]
            # add this module's vector,then add each pad's vector
            for i in self.layout.cell(search_cell).each_child_cell():
                module = self.layout.cell_name(i)
                vector = self.cell_vector(search_cell,module)
                x1 = x0 + vector[0]
                y1 = y0 + vector[1]
                vectors = self.pad_vectors(module)
                vectors = [(round(x1+X),round(y1+Y),round(W),round(H)) for (X,Y,W,H) in vectors]
                dic[module] = vectors
        return dic
