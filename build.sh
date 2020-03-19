#!/bin/bash
MAIN=count

yosys -p "synth_ice40 -blif target/$MAIN.blif" $MAIN.v
arachne-pnr -d 1k -p icestick.pcf target/$MAIN.blif -o target/$MAIN.txt
icepack target/$MAIN.txt target/$MAIN.bin
iceprog target/$MAIN.bin
