from __future__ import print_function
from vicon_dssdk import ViconDataStream
import time
client = ViconDataStream.RetimingClient()

try:
    print('Vi er her ---------- ')
    client.Connect( "localhost:801" )

    # Check the version
    print( 'Version', client.GetVersion() )

    client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )
    xAxis, yAxis, zAxis = client.GetAxisMapping()
    print( 'X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis )

    #client.SetMaximumPrediction( 10 )
    print( 'Maximum Prediction', client.MaximumPrediction() )

    #debug_log = 'e:\\tmp\\debug_log.txt'
    #output_log = 'e:\\tmp\\output_log.txt'
    #client_log = 'e:\\tmp\\client_log.txt'
    #stream_log = 'e:\\tmp\\stream_log.txt'

    #client.SetDebugLogFile( debug_log )
    #client.SetOutputFile( output_log )
    #client.SetTimingLog( client_log, stream_log )
   
    while( True ):
        try:
           
            print('tid: ',time.time())
            client.UpdateFrame()

            subjectNames = client.GetSubjectNames()
            for subjectName in subjectNames:
                 print( subjectName )
                 segmentNames = client.GetSegmentNames( subjectName )
                 for segmentName in segmentNames:
                     segmentChildren = client.GetSegmentChildren( subjectName, segmentName )
                     for child in segmentChildren:
                         try:
                             print( child, 'has parent', client.GetSegmentParentName( subjectName, segmentName ) )
                         except ViconDataStream.DataStreamException as e:
                             print( 'Error getting parent segment', e )            
                     print( segmentName, 'has static rotation( EulerXYZ )', client.GetSegmentStaticRotationEulerXYZ( subjectName, segmentName ) )              
                     try:
                         print( segmentName, 'has static scale', client.GetSegmentStaticScale( subjectName, segmentName ) )
                     except ViconDataStream.DataStreamException as e:
                         print( 'Scale Error', e )               

        except ViconDataStream.DataStreamException as e:
            print( 'Handled data stream error', e )
 
except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error', e )
