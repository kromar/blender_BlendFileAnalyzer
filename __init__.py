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
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import IntProperty, StringProperty


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


objList = []

class BFA_OT_BlendAnalyzer(Operator):    
    bl_idname = 'scene.blend_analyzer'
    bl_label = 'Analyze Blend File'
    bl_description = 'Analyze Blend File'
    
    button_input: StringProperty()
            
    def get_mesh_size(self):
        objects = bpy.data.objects
        objList.clear()
        for ob in objects:
            if  ob.type == 'MESH':
                depsgraph = bpy.context.evaluated_depsgraph_get() 
                object_eval = ob.evaluated_get(depsgraph)
                object_eval.data.calc_loop_triangles()
                numTris =len(object_eval.data.loop_triangles)                   
                objList.append([ob.name, numTris]) 
                    
        objList.sort(key = lambda i: i[1], reverse = True)    
        """ for i in objList:
            print(i[0], i[1]) """


    def execute(self, context):  
        if self.button_input=='ANALYZE':
            self.get_mesh_size() 
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

        layout = self.layout        
        layout.use_property_split = False

        box = layout.box()
        box.label(text='Meshes', icon='MESH_DATA')

        row = box.row(align=True)
        col = box.column(align=True)
        col.operator('scene.blend_analyzer', text='Analyze Blend File').button_input = 'ANALYZE'
        
        col = box.column(align=True)
        
        for i in objList:            
            row = col.row(align=False) 
            row.operator('scene.blend_analyzer', text='', icon = 'RESTRICT_SELECT_OFF').button_input=str(i[0])
            row.label(text=str(i[0]))
            #row.prop(props, 'chart', text=str(i[0]), slider=True)
            row.label(text=str(i[1]))
            


classes = (
    BFA_PT_UI,
    BFA_PG_Props,
    BFA_OT_BlendAnalyzer,
    )


def register() -> None:
    [register_class(c) for c in classes]
    bpy.types.Scene.CONFIG_BlendAnalyzer = bpy.props.PointerProperty(type=BFA_PG_Props)


def unregister() -> None:
    [unregister_class(c) for c in classes]
    del bpy.types.Scene.CONFIG_BlendAnalyzer


if __name__ == "__main__":
    register()