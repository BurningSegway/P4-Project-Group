from __future__ import print_function
from vicon_dssdk import ViconDataStream
import time
import socket
import xml.etree.ElementTree as ET

#XML setup
#XML structure
XML = """
<data>
    <name>data1</name>
    <time>time</time>
    <coordinate>
        <rotation>
            <e1>1.0</e1>
            <e2>1.0</e2>
            <e3>1.0</e3>
            <e4>1.0</e4>
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

#Pick the root from which we will look for our variables
root = ET.fromstring(XML)


#Slet understående
string1 = root.find('name')
string2 = root.find('time')
rotation = root.find('coordinate/rotation')
rot_e1 = rotation.find('e1')
rot_e2 = rotation.find('e2')
rot_e3 = rotation.find('e3')
rot_e4 = rotation.find('e4')
rot_bol = rotation.find('condition')
translation = root.find('coordinate/rotation')
trans_x = translation.find('x')
trans_y = translation.find('y')
trans_z = translation.find('z')
trans_bol = translation.find('condition')

#Function which takes the vicon data and inserts it into the XML
#The function returns the XML in a string format, like the one above.
def xmller(object_name, time_stamp, rotation_values, rotation_bool, translation_values, translation_bool):
    root.find('name').text = object_name
    root.find('time').text = time_stamp
    root.find('coordinate/rotation')
    rotation.find('e1').text = str(rotation_values[0])
    rotation.find('e2').text = str(rotation_values[1])
    rotation.find('e3').text = str(rotation_values[2])
    rotation.find('e4').text = str(rotation_values[3])
    rotation.find('condition').text =str(rotation_bool)
    translation = root.find('coordinate/translation')
    translation.find('x').text = str(translation_values[0])
    translation.find('y').text = str(translation_values[1])
    translation.find('z').text = str(translation_values[2])
    translation.find('condition').text = str(translation_bool)
    return ET.tostring(root, encoding='unicode')
    
    
    
#P2P connection setup
#determine what type of conection we want, in this case (IPv4, Connection based protocol)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 

#setup IP and port for host machine 
HOST = "192.168.1.35"
PORT = 65432
 
# Connect to the server 
client_socket.connect((HOST, PORT))







#instaciate client class from ViconDataStream. This enables the functions used below
client = ViconDataStream.RetimingClient()


#establish connection to the Vicon server. 
try:
    #Since vicon is running on this computer we use localhost, and vicon then always transmits data over port 801
    client.Connect( "localhost:801" )
    
    #setting up the vicon environment. determining world axis directions (page 59)
    client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )
    xAxis, yAxis, zAxis = client.GetAxisMapping()

    #predictions could be implementet, but are probably not neded.
    #Prediction is used with a time in ms. The system makes prediction on where an object is based on the precious frames until the time is exceeded.
    #When the time is exceeded the system will instead return "LateDataRequested"
    #client.SetMaximumPrediction( 10 )

    #Process and send the data to the other server
    while( True) :
        try:
            #get the latest frame from vicon
            client.UpdateFrame()

            #Get the name of the subjects and segments
            subjectName = client.GetSubjectNames()
            segmentName = client.GetSegmentNames( subjectName )       
                     
            #get their postion
            translation_values, T_frame_condition = client.GetSegmentGlobalTranslation(subjectName, segmentName)
            Q_rotation_values,  QR_frame_condition = client.GetSegmentGlobalRotationQuaternion( subjectName, segmentName )
            
            #debugging
            print('tid: ',time.time())
            print(Q_rotation_values, QR_frame_condition)
 
            
            data_to_send = xmller(segmentName, str(time.time()), Q_rotation_values, QR_frame_condition, translation_values, T_frame_condition)

            client_socket.sendall(data_to_send.encode())

            data = client_socket.recv(1024)
            print(f"Recieved: {data}")
            time.sleep(0.01)
                
                
            #print( string, string, [[float, float, float]. bool], [[float, float, float]. bool] )
            #print( segmentName, 'has static rotation( EulerXYZ )', client.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ), client.GetSegmentGlobalTranslation(subjectName, segmentName) )
            #data_to_send = "Hello" 
            #client_socket.send(data_to_send.encode())
            #data_to_send = segmentName, 'has static rotation( EulerXYZ )', client.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ), client.GetSegmentGlobalTranslation(subjectName, segmentName) 
            #client_socket.send(data_to_send.encode()) 
                                   

        except ViconDataStream.DataStreamException as e:
            print( 'Handled data stream error', e )
 
except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error', e )

client_socket.close() 