import silabs_cp2110
import ctypes
import random
import time
import connection
import threading
from tkinter import *
from tkinter.ttk import *

device = connection.connect()

BASE_FREQ = 1915000  # Taken from machine HZ^6 -> MHz
ITU_WIDTH = 500     # ITU channels are 50GHZ

INNER_TUNE_SLEEP = 3
MIN_HOLD_TIME = 2

root = Tk()
root.title('Laser control')
outputFreq = StringVar()

def set_itu_channel(channel):
    command = 'LASER:CHANnel: ' + str(channel)
    resp = connection.send_command(device, command)
    assert resp == '1'


def get_itu_channel():
    command = 'LASER:CHANnel?'
    resp = connection.send_command(device, command)

    return int(resp)


def set_fine_freq(freq):
    command = 'LASER:FINE: ' + str(freq)
    resp = connection.send_command(device, command)
    assert resp == '1'


def get_fine_freq():
    command = 'LASER:FINE?'
    resp = connection.send_command(device, command)
    return int(resp)


def get_optical_freq():
    command = 'LASER:FREQ?'
    resp = connection.send_command(device, command)
    return int(resp)


def get_status():
    command = 'LASER:SETpoint?'
    resp = connection.send_command(device, command)
    return int(resp)


def get_dbm():
    command = 'LASER:OOP?'
    resp = connection.send_command(device, command)
    return float(resp)


def control_freq(freq,step):
    # This is the easy math
    # Just divide it by freq
    # Minus the offset of the start
    freq -= BASE_FREQ

    itu = int(freq / ITU_WIDTH)

    # Add one back for ITU chan 1
    itu += 1

    # Get the fine frequency
    # This does no bounds checking
    fine = (freq % ITU_WIDTH) * 100

    # For example, the highest we can go on chan 1
    # Is 1915300, offset of 30000
    if fine > 30000:
        # Readjust for next ITU channel
        new = itu * ITU_WIDTH
        fine = (freq - new) * 100
        itu += 1

    set_itu_channel(itu)

    compare = get_itu_channel()
    # Are we changing ITUs, laser will turn off and on
    if itu != compare:
        print('Changing from ITU channel:', compare, 'to:', itu)

        time.sleep(10)

        # See if laser is happy with its status
        # See manual for what this command does
        while not get_status():
            print('Not in good status:', get_status())
            time.sleep(.5)

        while get_dbm() < 13.4:
            print('Want power higher: ', get_dbm())
            time.sleep(.5)

    #Now we nedd to tune the fine freq
    compare_fine = get_fine_freq()
    set_fine_freq(fine)

    #For example, 30,000 to -30,000 -> 60,000
    diff = abs(compare_fine - fine)
    
    #if we are chaning ITU, give it some more time
    if itu != compare:
        diff *= 1.5

    wait = 0
    if compare_fine != fine:
        wait = max(diff / 1000, 10)
    
    #laser says it can move about 1Ghz per second
    time.sleep(INNER_TUNE_SLEEP + wait)

    while get_optical_freq() != freq:
        print('mismatch between actual and requested freq!',
            'Requested:', freq,
            'Actual:',get_optical_freq(),
        )
        time.sleep(.1)

def sweep(start, stop, step, hold):
    print('Sweeping between', start, 'and', stop, 'by', step)

    freq = start
    control_freq(freq, step)
    time.sleep(hold)

    # We don't want to overshoot
    while (step > 0 and freq + step <= stop) or (step < 0 and freq + step >= stop):
        freq += step

        print('request freq: ', freq)

        control_freq(freq,step)

        outputFreq.set(str(freq/10) + 'GHz')
        print('finished setting to freq: ', freq)
        time.sleep(hold + MIN_HOLD_TIME)
        
    outputFreq.set('Done!')


def start_gui():
    # test_loop()
    unitLabel = Label(root, text='GHz')
    unitLabel.grid(column=1, row=0)

    startLabel = Label(root, text='Start Freq')
    endLabel = Label(root, text='End Freq')
    stepLabel = Label(root, text='Step Size')
    holdLabel = Label(root, text="Hold Time (s)")

    outputLabel = Label(root, text='Curr Freq')
    outputActual = Label(root, textvariable=outputFreq)

    startLabel.grid(column=0, row=1)
    endLabel.grid(column=0, row=2)
    stepLabel.grid(column=0, row=3)
    holdLabel.grid(column=0,row=4)

    outputLabel.grid(column=0, row=5)
    outputActual.grid(column=1, row=5)

    startEntry = Entry(root)
    startEntry.grid(column=1, row=1)

    endEntry = Entry(root)
    endEntry.grid(column=1, row=2)

    stepEntry = Entry(root)
    stepEntry.grid(column=1, row=3)

    holdEntry = Entry(root)
    holdEntry.grid(column=1,row=4)

    def sweep_gui():
        start = int(float(startEntry.get()) * 10)
        end = int(float(endEntry.get()) * 10)
        step = int(float(stepEntry.get()) * 10)

        hold = holdEntry.get()
        if hold != '':
            hold = float(holdEntry.get())
        else:
            hold = 0

        thread = threading.Thread(target=sweep, args=(start,end,step, hold))
        thread.start()
    
    B = Button(root, text="Sweep", command=sweep_gui)
    B.grid(column=1, row=6)

    root.mainloop()


start_gui()
