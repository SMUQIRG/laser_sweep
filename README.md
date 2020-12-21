# Thorlabs TLX Laser Sweep
We use a Thorlabs TLX laser in our SMU photonics lab and needed the ability to automatically sweep through a set of frequencies. This uses the USB interface dicussed in the TLX programming guide. 

# Usage
The only external package required is tkinter and is provided by almost all standard installations. Therefore the program can be run by 
>python3 sweep.py

# Design
The TLX manual does not make many guarantees on laser tuning speeds, so this program attemps to be on the safe side. The laser provides feedback on the status of an ITU channel so we can easily and safely monitor that, but there is no method to determining if an inner channel tune has been completed. Because of this, we take the manuals reccomendation on allowing upwards of 1 second per 1 GHz of tuning. We wait longer when changing ITU channels and have a minimum sleep time of 10 seconds per tune to be on the safe side. The outputs were evaluated on an OSA and appear to provide valid waiting times for correct frequencies.

# License
Copyright 2020 Troy McNitt

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

# Contact
Troy McNitt - tmcnitt@smu.edu
