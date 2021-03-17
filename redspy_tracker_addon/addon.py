import bpy
import mathutils
import os
import uuid
import math

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from . import redspy_tracker

class ImportRedspyTrackingdata(Operator, ImportHelper):

    bl_idname = "redspy_tracking_xml.import_project"
    bl_label = "Import redspy_tracking_xml"

    filename_ext = ".xml"

    filter_glob : StringProperty(
        default = "*.xml",
        options = { 'HIDDEN' },
        maxlen= 255
    )

    def execute(self, context):
        return self.import_redspy_xml(context, self.filepath) 

    def strTofloat(self, string, remove): 
        answer = string.replace(",",".") # , -> .
        return float(answer.rstrip(remove)) #changing str -> float

    def set_up_camera(self, cameraparam): 
        leng = len(cameraparam._index)


        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
        obj = bpy.context.object
        obj.animation_data_create()
        obj.animation_data.action = bpy.data.actions.new(name="MyAction")

            #Camera Setting
        camera = bpy.context.object

            #FovX = focal length (Unit: Field of View) //Camera
        camera.data.type = 'PERSP'
        camera.data.lens_unit = 'FOV'
        camera.data.angle = self.strTofloat(cameraparam._fov_X[0],' °') * math.pi / 180

            #Center-X,Y = shift X,Y // Camera
        camera.data.shift_x = self.strTofloat(cameraparam._center_X[0],' mm') #float(cameraparam.center_X[0].rstrip(' mm'))
        camera.data.shift_y = self.strTofloat(cameraparam._center_Y[0],' mm') #float(cameraparam.center_Y[0].rstrip(' mm'))

        
        # x
        fcu_x = obj.animation_data.action.fcurves.new(data_path="location", index=0)
        fcu_x.keyframe_points.add(leng)
        #camera param add
        for cnt in range(0,leng): #one cam, leng param
            fcu_x.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._location_X[cnt],' m') #float(cameraparam._frame[cnt]), float(cameraparam._location_X[cnt].rstrip(' m')) #(frame, location)

        # y 
        fcu_y = obj.animation_data.action.fcurves.new(data_path="location", index=1)
        fcu_y.keyframe_points.add(leng)
        for cnt in range(0,leng): #one cam, leng param
            fcu_y.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._location_Y[cnt],' m')#float(cameraparam._frame[cnt]), float(cameraparam._location_Y[cnt].rstrip(' m')) #(frame, location)

            # z
        fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)
        fcu_z.keyframe_points.add(leng)
        for cnt in range(0,leng): #one cam, leng param
            fcu_z.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._location_Z[cnt],' m')#float(cameraparam._frame[cnt]), float(cameraparam._location_Z[cnt].rstrip(' m')) #(frame, location)

            #pan
        fcu_p = obj.animation_data.action.fcurves.new(data_path="rotation_euler", index=0)
        fcu_p.keyframe_points.add(leng)
        for cnt in range(0,leng): #one cam, leng param
            fcu_p.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._rotation_X[cnt],' °') * math.pi / 180#float(cameraparam._frame[cnt]), float(cameraparam._rotation_X[cnt].rstrip(' °')) #(frame, location)

            #tilt
        fcu_t = obj.animation_data.action.fcurves.new(data_path="rotation_euler", index=1)
        fcu_t.keyframe_points.add(leng)
        for cnt in range(0,leng): #one cam, leng param
            fcu_t.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._rotation_Y[cnt],' °') * math.pi / 180#float(cameraparam._frame[cnt]), float(cameraparam._rotation_Y[cnt].rstrip(' °')) #(frame, location)

            #roll
        fcu_r = obj.animation_data.action.fcurves.new(data_path="rotation_euler", index=2)
        fcu_r.keyframe_points.add(leng)
        for cnt in range(0,leng): #one cam, leng param
            fcu_r.keyframe_points[cnt].co = self.strTofloat(cameraparam._index[cnt],''), self.strTofloat(cameraparam._rotation_Z[cnt],' °') * math.pi / 180#float(cameraparam._frame[cnt]), float(cameraparam._rotation_Z[cnt].rstrip(' °')) #(frame, location)


    def import_redspy_xml(self, context, filepath):
        try:
            camera_param = redspy_tracker.CameraParameters(filepath)
            try:
                camera = self.set_up_camera(camera_param) #카메라에 대입해야 한다.
            except Exception as e:
                self.report({ 'ERROR' }, str(e))
                return { 'CANCELLED' }
            return {'FINISHED'}
        except redspy_tracker.ParsingError as e:
            self.report({ 'ERROR' }, 'trackingdata import error: ' + str(e))
            return {'CANCELLED'}