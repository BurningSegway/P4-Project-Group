from vicon_dssdk import ViconDataStream

client = ViconDataStream.Client()
client.Connect("192.168.1.33:801")

client.GetFrame()
client.GetFrameNumber()
client.Disconnect()
