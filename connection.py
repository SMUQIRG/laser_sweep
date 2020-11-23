import silabs_cp2110
import ctypes
import random
import time

def send_command(device_opaque_obj, command: str) -> str:
    #Need to add ending to command
    command += '\r'

    reply = bytearray( 100 )

    write_result = silabs_cp2110.Write( device_opaque_obj, command, len( command ) )

    #TODO: Does this need to be a second? Was just set here from example
    #time.sleep( 1 ) # Seconds
    read_result = silabs_cp2110.Read( device_opaque_obj, reply, 100 )

    return reply.decode()[:read_result - 1] 


def close(device):
    close_result = silabs_cp2110.Close( device )
    print( "Close() returned " + str( close_result ) )

def connect():
    print('Starting up')
    thorlabs_devices = 0

    # Search for devices in the Thorlabs range for MX/TLX/MBX instruments
    pid = 0x5001

    while pid <= 0x501F:
        devices_for_pid = silabs_cp2110.GetNumDevices( 0x1313, pid )
        if devices_for_pid > 0:
            thorlabs_devices += devices_for_pid
            break
        else:
            pid += 0x0001

    if ( thorlabs_devices != 1 ):
        print( "This example will only work with one Thorlabs MX/TLX/MBX family device (found {} eligible devices).".format( str( thorlabs_devices ) ) )
        exit(-1)
    else:
        # A matching device was identified
        print( "Found one Thorlabs device device. The device strings are as follows:" )
        print( silabs_cp2110.GetVIDString( 0x1313, pid ) )
        print( silabs_cp2110.GetPIDString( 0x1313, pid ) )
        print( silabs_cp2110.GetPathString( 0x1313, pid ) )
        serial_num_str = silabs_cp2110.GetSerialString( 0x1313, pid )
        print( int( serial_num_str[:4], 16 ) )
        print( int( serial_num_str[5:], 16 ) )
        print( silabs_cp2110.GetManufacturerString( 0x1313, pid ) )
        print( silabs_cp2110.GetProductString( 0x1313, pid ) )

        # Attempt to open device
        print( "\r\nAttempting to open device:" )
        device_opaque_obj = silabs_cp2110.Open( 0x1313, pid )

        # Works in Python 3.8
        # addr = PyCapsule_GetPointer( device_opaque_obj )
        print( "Open() returned {}".format( str( device_opaque_obj ) ) )

        # Works in Python 2.7
        # addr = PyCObject_AsVoidPtr( device_opaque_obj )
        # print( "Open() returned opaque object capsule " + str( addr ) )

        # Double-check that it was opened by calling the GetIsOpened API
        is_opened = silabs_cp2110.GetIsOpened( device_opaque_obj )
        if False == is_opened:
            print( "Device was not correctly opened; IsOpened() API returned false." )
        else:
            configure_uart_result = silabs_cp2110.ConfigureUART( device_opaque_obj );
            if False == configure_uart_result:
                print( "ConfigureUART() API returned false." )
            else:
                set_timeouts_result = silabs_cp2110.SetTimeouts( device_opaque_obj, 500, 500 );
                if False == set_timeouts_result:
                    print( "SetTimeouts() API returned false." )
                else:
                    # Device is fully configured; start sending lighting commands in a loop
                    print('Successfully connected to device')
                    return device_opaque_obj