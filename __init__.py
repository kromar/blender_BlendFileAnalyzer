# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


from tokenize import String
import bpy
import time
from bpy.utils import register_class, unregister_class
from bpy.types import Operator, Panel, PropertyGroup, UIList
from bpy.props import IntProperty, StringProperty, BoolProperty, CollectionProperty


bl_info = {
    "name": "Blend File Analyzer",
    "description": "",
    "author": "Daniel Grauer",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties space > Scene > Blend Analyzer",
    "wiki_url": "https://github.com/kromar/blender_BlendFileAnalyzer",
    "tracker_url": "https://github.com/kromar/blender_BlendFileAnalyzer/issues",
    "category": "Scene"}


#bfa_list = []


class BFA_List(PropertyGroup): 
    """Group of properties representing an button in the list."""
    button_name: StringProperty(
        name="", 
        description="button_name", 
        default="Name") 

    button_operator: StringProperty(
        name="", 
        description="button_operator", 
        default="screen.userpref_show") 

    button_icon: StringProperty(
        name="", 
        description="buton_icon", 
        default="FUND")  

    show_button_name: BoolProperty(
        name="",
        description="Show Button Name",
        default=False) 
        

class BFA_UL_List(UIList): 
    """Custom Buttons List."""    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        
        layout.operator('scene.blend_analyzer', text='', icon = 'RESTRICT_SELECT_OFF') #.button_input=str(i[0])
        layout.label(text="test")
        layout.label(text=str(len("test count")))
        layout.label(text=str(i[0]))
        #row.prop(props, 'chart', text=str(i[0]), slider=True)
        layout.label(text=str(i[1]))


class BFA_OT_BlendAnalyzer(Operator):    
    bl_idname = 'scene.blend_analyzer'
    bl_label = 'Analyze Blend File'
    bl_description = 'Analyze Blend File'
    
    button_input: StringProperty()
            
    def get_mesh_size(self, context):        
        scene = context.scene
        objects = bpy.data.objects
        scene.bfa_list.clear()
        for ob in objects:
            if  ob.type == 'MESH':
                depsgraph = bpy.context.evaluated_depsgraph_get() 
                object_eval = ob.evaluated_get(depsgraph)
                object_eval.data.calc_loop_triangles()
                numTris = len(object_eval.data.loop_triangles) 
                scene.bfa_list.add()                  
                #scene.bfa_list.append([ob.name, numTris]) 
                    
        #scene.bfa_list.sort(key = lambda i: i[1], reverse = True)    
        """ for i in bfa_list:
            print(i[0], i[1]) """


    def execute(self, context):  
        if self.button_input=='ANALYZE':
            self.get_mesh_size(context) 
        else:      
            objname = self.button_input
            try:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[objname].select_set(True)
                context.view_layer.objects.active = bpy.data.objects[objname]
            except:
                pass
        return {'FINISHED'}


def profiler(start_time=0, string=None): 
    elapsed = time.time()
    print("{:.4f}".format(elapsed-start_time), "<< ", string)  
    start_time = time.time()
    return start_time  


class BFA_PG_Props(PropertyGroup):    
    bl_idname = __package__

    chart: IntProperty(
        name='test chart', 
        description='test chart', 
        default=5000,
        min = 1,
        soft_max = 10000,
        step = 1,
        subtype='NONE', 
    )
        

class BFA_PT_UI(Panel):
    """Panel for the magic weights, located in Properties > Mesh."""

    bl_label = 'Blend File Analyzer'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        props = bpy.context.scene.CONFIG_BlendAnalyzer

        scene = context.scene 
        layout = self.layout        
        layout.use_property_split = False

        box = layout.box()
        box.label(text='Meshes', icon='MESH_DATA')

        row = box.row(align=True)
        col = box.column(align=True)
        col.operator('scene.blend_analyzer', text='Analyze Blend File').button_input = 'ANALYZE'

        col = box.column(align=True)
        
        col.template_list("BFA_UL_List", 
                            "Blend File Analisys", 
                            scene, 
                            "bfa_list", 
                            scene, 
                            "bfa_list_index",                            
                            type='DEFAULT',
                            columns=1,
                            rows = 1,
                        ) 
        
        
        """ for i in scene.bfa_list:            
            row = col.row(align=False) 
            row.operator('scene.blend_analyzer', text='', icon = 'RESTRICT_SELECT_OFF').button_input=str(i[0])
            row.label(text=str(i[0]))
            #row.prop(props, 'chart', text=str(i[0]), slider=True)
            row.label(text=str(i[1])) """
            


classes = (
    BFA_PT_UI,
    BFA_PG_Props,
    BFA_OT_BlendAnalyzer,
    BFA_List,
    BFA_UL_List,
    )


def register() -> None:
    [register_class(c) for c in classes]
    bpy.types.Scene.CONFIG_BlendAnalyzer = bpy.props.PointerProperty(type=BFA_PG_Props)
    
    bpy.types.Scene.bfa_list = CollectionProperty(type = BFA_List) 
    bpy.types.Scene.bfa_list_index = IntProperty(default = 0) 


def unregister() -> None:
    del bpy.types.Scene.bfa_list 
    del bpy.types.Scene.bfa_list_index 

    [unregister_class(c) for c in classes]
    del bpy.types.Scene.CONFIG_BlendAnalyzer


if __name__ == "__main__":
    register()