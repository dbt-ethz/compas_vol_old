import compas_vol
from compas.geometry import *
from compas_vol.primitives import *
from compas_vol.combinations import *

import numpy as np
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_inverse as inverse

### Constants
#primitives id
sphere_id = 100
box_id = 101
torus_id = 102
cylinder_id = 103

#combinations id
union_id = 200
intersection_id = 201
smooth_union_id = 202

#modifications id
shell_id = 300


def  get_obj_name(id):
    if id == union_id:
            return "Union"
    elif id == intersection_id:
            return "Intersection"
    elif id == smooth_union_id:
            return "Smooth Union"
    elif id == sphere_id:
            return "Sphere"
    elif id == box_id:
            return "Box"
    elif id == torus_id:
            return "Torus"   
    elif id == cylinder_id:
            return "Cylinder"     
    elif id == shell_id:
            return "Shell"           
        
identity_matrix =  [[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]]

def is_vUnion(input_object):
        return isinstance(input_object, compas_vol.combinations.union.Union)
def is_vIntersection(input_object):
        return isinstance(input_object, compas_vol.combinations.intersection.Intersection)
def is_vSmooth_Union(input_object):
        return isinstance(input_object, compas_vol.combinations.smoothunion.SmoothUnion)
def is_vCOMBINATION(input_object):
        return is_vUnion(input_object) or is_vIntersection(input_object) or is_vSmooth_Union(input_object)


def is_vSphere(input_object):
        return isinstance(input_object, compas_vol.primitives.vsphere.VolSphere)
def is_vBox(input_object):
        return isinstance(input_object, compas_vol.primitives.vbox.VolBox)
def is_vTorus(input_object):
        return isinstance(input_object, compas_vol.primitives.vtorus.VolTorus)
def is_vCylinder(input_object):
        return isinstance(input_object, compas_vol.primitives.vcylinder.VolCylinder)
def is_vPRIMITIVE(input_object):
        return is_vSphere(input_object) or is_vBox(input_object) or is_vTorus(input_object) or is_vCylinder(input_object)


def is_vShell(input_object):
        return isinstance(input_object, compas_vol.modifications.shell.Shell)
def is_vMODIFICATION(input_object):
        return is_vShell(input_object)

############## primitives
class VSphere_data:
        def __init__(self, index, vSphere, parent_index, parent_id, order): ##add parent id 
                self.index = index
                self.id = sphere_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = identity_matrix
                self.size_xyzr = [vSphere.sphere.point.x, vSphere.sphere.point.y, vSphere.sphere.point.z , vSphere.sphere.radius]
                self.order = order

class VBox_data:
        def __init__(self, index, vBox, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = box_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = inverse(matrix_from_frame(vBox.box.frame)) 
                self.size_xyzr = [vBox.box.xsize , vBox.box.ysize , vBox.box.zsize ,  vBox.radius]
                self.order = order

class VTorus_data:
        def __init__(self, index, vTorus, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = torus_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                frame = Frame.from_plane(vTorus.torus.plane)
                self.matrix = inverse(matrix_from_frame(frame)) 
                self.size_xyzr = [vTorus.torus.radius_axis , vTorus.torus.radius_pipe , 0. , 0.]
                self.order = order

class VCylinder_data:
        def __init__(self, index, vCylinder, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = cylinder_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                frame = Frame.from_plane(vCylinder.cylinder.plane)
                self.matrix = inverse(matrix_from_frame(frame)) 
                self.size_xyzr = [vCylinder.cylinder.height , vCylinder.cylinder.radius , 0. , 0.]
                self.order = order

################### combinations
class VUnion_data:
        def __init__(self, index, vUnion, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = union_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = identity_matrix
                self.size_xyzr = [1 , 1 , 1 , 1]
                self.order = order

class VIntersection_data:
        def __init__(self, index, vIntersection, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = intersection_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = identity_matrix
                self.size_xyzr = [1 , 1 , 1 , 1]
                self.order = order

class VSmooth_Union_data:
        def __init__(self, index, vSmoothUnion, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = smooth_union_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = identity_matrix
                self.size_xyzr = [vSmoothUnion.r , 1 , 1 , 1]
                self.order = order


################### modifications
class VShell_data:
        def __init__(self, index, vShell, parent_index, parent_id, order): #add parent id 
                self.index = index
                self.id = shell_id
                self.parent_index = parent_index
                self.parent_id = parent_id
                self.matrix = identity_matrix
                self.size_xyzr = [vShell.thickness , vShell.side , 1 , 1]
                self.order = order


###########################################################

class Translator:
        def __init__(self, input_object_):
                self.index_count = 1
                self.input_object = input_object_
                self.objects_unwrapped_list = []
                self.final_data = []
                self.shader_start_vaues = []

                self.translate_data(self.input_object, 0, union_id, 0) ## starting object, parent id = 0, 0 start_order
                self.create_final_data()
                self.create_shader_start_values()
                
        
        def translate_data(self, in_obj, parent_index_, parent_id_, parent_order):
                current_index = self.index_count
                parent_index = parent_index_
                parent_id = parent_id_
                self.index_count += 1

                if is_vPRIMITIVE(in_obj): 
                        if is_vSphere(in_obj):
                                new = VSphere_data(current_index, in_obj, parent_index, parent_id, parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                        elif is_vBox(in_obj):  
                                new = VBox_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                        elif is_vTorus(in_obj):
                                new = VTorus_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                        elif is_vCylinder(in_obj):
                                new = VCylinder_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                        else: 
                                print ("Warning: Unknown primitive")
    
                elif is_vCOMBINATION(in_obj):
                        if is_vUnion(in_obj):
                                new = VUnion_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                                for o in in_obj.objs:
                                        self.translate_data(o, current_index, union_id,  parent_order +1)
                        elif is_vIntersection(in_obj):
                                new = VIntersection_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                                for o in in_obj.objs:
                                        self.translate_data(o, current_index, intersection_id, parent_order +1)
                        elif is_vSmooth_Union(in_obj):
                                new = VSmooth_Union_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                                objects = [in_obj.a , in_obj.b]
                                for o in objects:
                                        self.translate_data(o, current_index, smooth_union_id, parent_order +1)

                elif is_vMODIFICATION(in_obj):
                        if is_vShell(in_obj):
                                new = VShell_data(current_index, in_obj, parent_index, parent_id,  parent_order + 1)
                                self.objects_unwrapped_list.append(new) 
                                self.translate_data(in_obj.o, current_index, shell_id, parent_order +1)
                        else: 
                                print ("Warning: Unknown combination mathod")
                                self.translate_data(o, current_index, smooth_union_id, parent_order +1)
                                
                else: 
                        print ("Warning: Unknown SOMETHING")

        def create_data_array_of_single_object(self, object):
                data_array = []
                data_array.append([object.index, object.id ,object.parent_index ,object.parent_id]) # box id, combination function id
                for k in object.matrix:
                        data_array.append(k)
                data_array.append(object.size_xyzr)
                return data_array

        def create_final_data(self):
                self.objects_unwrapped_list.reverse()
                print ("List of objects reversed")
                for primitive in self.objects_unwrapped_list:
                        data_array = self.create_data_array_of_single_object(primitive)
                        for vec4 in data_array:
                                vec4_rounded = [round(d, 2) for d in vec4]
                                self.final_data.append(vec4_rounded)
                print ("")
                print ("lentgh of shader data : ", len(self.final_data))
                print ("")
                for obj in self.objects_unwrapped_list:
                        print ("order : " , obj.order)
                        print("index: ", obj.index, ",  id: ", get_obj_name(obj.id), ",  parent_index: ", obj.parent_index,  ",  parent_id: " , get_obj_name(obj.parent_id) , \
                              "\nmatrix: ",obj.matrix, ",  size_xyzr: ", obj.size_xyzr )
                        print ("")
                # print (self.final_data)
                print ("")





        def create_shader_start_values(self):
                values = []
                values.append(100.)
                self.objects_unwrapped_list.reverse()
                my_obj_list = self.objects_unwrapped_list
                for obj in my_obj_list:
                        #combination
                        if obj.id == union_id:
                                values.append(100.) #very big value
                        elif obj.id == intersection_id:
                                values.append(-100.) #very small value
                        elif obj.id == smooth_union_id:
                                values.append(100.) #very big value
                        
                        # primitive
                        elif obj.id  == sphere_id :
                                values.append(0.)
                        elif obj.id  == box_id :
                                values.append(0.)
                        elif obj.id  == torus_id :
                                values.append(0.)
                        elif obj.id  == cylinder_id :
                                values.append(0.)

                        # modifications
                        elif obj.id  == shell_id :
                                values.append(0.)

                        else: 
                                print ("Unknown object, id : " , obj.id , " , index : ", obj.index)


                self.shader_start_vaues = values
                print ("")
                print ("shader_start_vaues : " , self.shader_start_vaues)



        


# def Spheres_union(myUnion):
    
#     #  gather data of shapes for reconstructing distance function at the shader (at the moment upper limit of shapes: 100, only Union, only Spheres)
#     if isinstance(myUnion, compas_vol.combinations.union.Union):
#         spheres_xyzw = [[o.sphere.point.x, o.sphere.point.y, o.sphere.point.z , o.sphere.radius] for o in myUnion.objs if isinstance(o, compas_vol.primitives.vsphere.VolSphere)]
#         return spheres_xyzw