# BMW Coding

The software is diagnostic scan tool for BMW E38/E39. It still under development.
It reads engine & transmission real-time information and DTC (Diagnostic Trouble Code)

## Hardware requirement

You need a K+DCAN cable and PC notebook.

## Software requirement

PYTHON 2.7 or 3.x

## ECU and Protocol

It's now supports BMW DS2 protocol and KWP2000. The tested ECU is bosch ME7.2 (M62tu engine) and GS 8.60.2 (ZF5HP24 transmission).
MS41/43 is there but NOT tested ...

## Do scan

Connect K+DCAN with PC notebook and 20 pin round connector. Ignition On then run

$ cd bmw-coding
$ python ./ds2.py






