from __future__ import print_function
from vicon_dssdk import ViconDataStream
import time
import socket
import xml.etree.ElementTree as ET

#XML opsætning
XML = """
<data>
    <string1>data1</string1>
    <string2>data2</string2>
    <coordinate>
        <rotation>
            <x>1.0</x>
            <y>1.0</y>
            <z>1.0</z>
            <condition>true</condition>
        </rotation>
        <translation>
            <x>1.0</x>
            <y>1.0</y>
            <z>1.0</z>
            <condition>true</condition>
        </translation>
    </coordinate>
</data>
"""


root = ET.fromstring(XML)

string1 = root.find('string1')
string2 = root.find('string2')
rotation = root.find('coordinate/rotation')
rot_x = rotation.find('x')
rot_y = rotation.find('y')
rot_z = rotation.find('z')
rot_bol = rotation.find('condition')
translation = root.find('coordinate/rotation')
trans_x = translation.find('x')
trans_y = translation.find('y')
trans_z = translation.find('z')
trans_bol = translation.find('condition')
#print( string, string, [[float, float, float]. bool], [[float, float, float]. bool] )
#segmentName, 'has static rotation( EulerXYZ )', client.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ), client.GetSegmentGlobalTranslation(subjectName, segmentName)
def xmller():
    

    
    
    
    














