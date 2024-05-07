from __future__ import print_function
from vicon_dssdk import ViconDataStream
import argparse

import logging
import time
from threading import Thread

import cflib
from cflib.crazyflie import Crazyflie
from cflib.utils import uri_helper

uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

logging.basicConfig(level=logging.ERROR)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', help="Host name, in the format of server:port", default = "localhost:801")
args = parser.parse_args()

client = ViconDataStream.Client()

client.GetFrameRate

thrust = 0
pitch = 0
roll = 0
yawrate = 0

class MotorRampExample:
    """Example that connects to a Crazyflie and ramps the motors up/down and
    the disconnects"""

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie(rw_cache='./cache')

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
        print('Connected');
        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        Thread(target=self._ramp_motors).start()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)

    def _ramp_motors(self):
        # Unlock startup thrust protection
        self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
        time.sleep(0.)            


try:
    print('Vi er her 1')
    client.Connect( args.host )
    print('Vi er her 2')
    # Check the version
    print( 'Version', client.GetVersion() )
    print('Vi er her 3')
    # Check setting the buffer size works
    client.SetBufferSize( 1 )
    print('Vi er her 4')
    #Enable all the data types
    client.EnableSegmentData()
    client.EnableMarkerData()
    client.EnableUnlabeledMarkerData()
    client.EnableMarkerRayData()
    client.EnableDeviceData()
    client.EnableCentroidData()
    print('Vi er her 5')
    cflib.crtp.init_drivers()
    print('Vi er her 6')
    while( True ):
        le = MotorRampExample(uri)


except ViconDataStream.DataStreamException as e:
    print( 'Handled data stream error', e )
