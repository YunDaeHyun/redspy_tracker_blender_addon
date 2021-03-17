import os
import xml.etree.ElementTree as ET
from struct import *

class ParsingError(Exception):
    pass

class CameraParameters:

    cnt = 0
    _index = []
    _frame = []

    _location_X = []
    _location_Y = []
    _location_Z = []

    _rotation_X = []
    _rotation_Y = []
    _rotation_Z = []

    _fov_X = []

    _aspect_ratio = []
    _focus = []
    _zoom = []
    _center_X = []
    _center_Y = []
    _sensor_width = []

    def __init__(self, project_path):
        project_file = open(project_path, "rb")
        self.file_name = os.path.basename(project_path)
        doc = ET.parse(project_path)
        if doc is None:
            raise ParsingError("params reading error")
        root = doc.getroot()
        data_sample = root.findall("Data_sample")

        for object in root.iter("Data_sample"): #여기서 멤버 변수 읽을 수 있게 해주자.
            self._index.append(data_sample[self.cnt].find("Index").text)
            self._frame.append(data_sample[self.cnt].find("Frame").text)
            
            self._location_X.append(data_sample[self.cnt].find("X_Value").text)
            self._location_Y.append(data_sample[self.cnt].find("Y_Value").text)
            self._location_Z.append(data_sample[self.cnt].find("Z_Value").text)
            
            self._rotation_X.append(data_sample[self.cnt].find("Pan").text)
            self._rotation_Y.append(data_sample[self.cnt].find("Tilt").text)
            self._rotation_Z.append(data_sample[self.cnt].find("Roll").text)
            
            self._fov_X.append(data_sample[self.cnt].find("FovX").text)
            self._aspect_ratio.append(data_sample[self.cnt].find("Aspect_Ratio").text)
            self._focus.append(data_sample[self.cnt].find("Focus").text)
            self._zoom.append(data_sample[self.cnt].find("Zoom").text)
            
            self._center_X.append(data_sample[self.cnt].find("Center-X").text)
            self._center_Y.append(data_sample[self.cnt].find("Center-Y").text)
            #self._sensor_width.append(data_sample[self.cnt].find("PA_width").text)
            self.cnt += 1