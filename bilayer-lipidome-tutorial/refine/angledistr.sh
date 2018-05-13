#!/bin/bash

# source /usr/local/gromacs-4.6.1/bin/GMXRC

NMOL=128
NAT=12

rm -rf ANGLES
mkdir -p ANGLES

IFS=$'\n'

# Angles

ACOUNTER=0
for j in `cat ./anglelist`
    do 
    COUNTER=0
    while [ $COUNTER -lt $NMOL ]
       do
       rm -f angle.ndx
       echo "[ ga ]" > angle.ndx
       IFS=' ' read -a indices <<< $j
       for i in "${indices[@]}"
          do
          index=$(expr $COUNTER \* $NAT + $i)
          echo "$index" >> angle.ndx
          done
          gmx angle -f CGFRAMES/cg-mapped.xtc -n angle.ndx -ov ANGLES/cga_$ACOUNTER.$COUNTER.xvg
       let COUNTER=COUNTER+1
       rm -f \#*
       done
    let ACOUNTER=ACOUNTER+1
    done

rm -f ANGLES/\#*

cd ANGLES

ACOUNTER=0
for j in `cat ../anglelist`
    do 
    cat cga_$ACOUNTER.*.xvg > cga_all_$ACOUNTER.xvg
    gmx analyze -f cga_all_$ACOUNTER.xvg -bw 1 -dist cga_$ACOUNTER-distr.xvg
    let ACOUNTER=ACOUNTER+1
    done

exit
