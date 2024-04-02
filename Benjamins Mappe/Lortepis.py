from __future__ import print_function
from vicon_dssdk import ViconDataStream
import time
import socket
import xml.etree.ElementTree as ET

#XML opsætning
XML = """
<data>
    <name>data1</name>
    <time>time</time>
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

string1 = root.find('name')
string2 = root.find('time')
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
def xmller(navn, time, rot, rot2, tran1, tran2):
    root.find('name').text = navn
    root.find('time').text = time
    root.find('coordinate/rotation')
    rotation.find('x').text = str(rot[0])
    rotation.find('y').text = str(rot[1])
    rotation.find('z').text = str(rot[2])
    rotation.find('condition').text =str(rot2)
    translation = root.find('coordinate/translation')
    translation.find('x').text = str(tran1[0])
    translation.find('y').text = str(tran1[1])
    translation.find('z').text = str(tran1[2])
    translation.find('condition').text = str(tran2)

    
    print(root.find('time').text, rotation.find('condition').text)
    
    return ET.tostring(root, encoding='unicode')
    
    
    
    
    
    
    
    
    
    
    
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
# Get the hostname of the server machine 
#server_host = socket.gethostname() 
server_host = "192.168.1.37"
# Define the port to connect to 
server_port = 32007 

HOST = "192.168.1.37"
PORT = 65432
 
# Connect to the server 
client_socket.connect((HOST, PORT))


#se side 217 i manualen. Det er en klasse man bruger når man vil have minimal latency på den data man hiver ud, og den åbner op for en masse funktioner
client = ViconDataStream.RetimingClient()




try:
    #print('Vi er her ---------- ')
    #Først bruger vi connect("computeren der kører vicon systemet:porten der bliver transmiteret data over")
    client.Connect( "localhost:801" )
    
    
    # Printer bare versionen af Datastream
    #print( 'Version', client.GetVersion() )
    
    #Her indstiller vi det generelle coordinatsystem for vicon. Vi fortæller den altså hvilken retning de forskellige akser skal have fra vores synspunkt.
    #Se mere på side 59
    #forward, left, og up betyder at x pejer fremad, y venstre og z op fra mit sysnpunkt bag glasset.
    client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )
    xAxis, yAxis, zAxis = client.GetAxisMapping()
    #print( 'X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis )

    #prediction er tid i ms fra sidste modtaget frame, hvori systemet selv kan gætte hvis det altså ikke har modtaget et fram. standarden er 100ms.
    #Hvis tiden bliver overskredet returnere systemet ikke en position med istedet "LateDataRequested"
    #client.SetMaximumPrediction( 10 )
    #print( 'Maximum Prediction', client.MaximumPrediction() )

    #debug_log = 'e:\\tmp\\debug_log.txt'
    #output_log = 'e:\\tmp\\output_log.txt'
    #client_log = 'e:\\tmp\\client_log.txt'
    #stream_log = 'e:\\tmp\\stream_log.txt'

    #client.SetDebugLogFile( debug_log )
    #client.SetOutputFile( output_log )
    #client.SetTimingLog( client_log, stream_log )

    while( True) :
        try:
           
            print('tid: ',time.time())
            #Updatefram()
            #Update the current frame state to represent the position of all active subjects at the current time. The position of each segment is estimated by predicting forwards from the most recent frames received 
            #from the DataStream, taking into account the latency reported by the system to determine the amount of prediction required.
            #The results of calls which return details about the current frame state such as GetSubjectCount() and
            #GetSegmentGlobalRotationQuaternion() will all return the stream contents and position at the time that
            #this call was made.
            #If no call to UpdateFrame() is made, calls querying the stream state will return NoFrame.

            client.UpdateFrame()

            #få navne på de aktive objekter i trackeren og begynd så proccessen med at udskrive der pose og alt det for hvert object
            subjectNames = client.GetSubjectNames()
            #print("subject", subjectNames)
            for subjectName in subjectNames:
                #print( subjectName )
                segmentNames = client.GetSegmentNames( subjectName )
                #print("segment", segmentNames)
                for segmentName in segmentNames:
                    segmentChildren = client.GetSegmentChildren( subjectName, segmentName )        
                     

                    rotation_values,  R_frame_condition = client.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName )
                    translation_values, T_frame_condition = client.GetSegmentGlobalTranslation(subjectName, segmentName)
                     

                     
                    #print(client.GetSegmentGlobalTranslation(subjectName, segmentName))
                     
                    data_to_send = xmller(segmentName, str(time.time()), rotation_values, T_frame_condition, translation_values, T_frame_condition)

                    client_socket.sendall(data_to_send.encode())

                    data = client_socket.recv(1024)
                    print(f"Recieved: {data}")
                    time.sleep(1)
                     
                     
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