#!/bin/bash

# source /usr/local/gromacs-5.1.3/bin/GMXRC

rm -rf FRAMES
mkdir -p FRAMES

echo 0 | gmx trjconv -sep -pbc whole -o FRAMES/fg.gro -s fg.tpr -f fg.xtc

rm -rf CGFRAMES
mkdir -p CGFRAMES

COUNTER=0

for j in $( ls FRAMES/*)  
    do 
    echo "$COUNTER $j" 
    python backward.py -from gromos -to martini -f $j -o CGFRAMES/cg_$COUNTER.gro
    let COUNTER=COUNTER+1
    done

cd CGFRAMES
gmx trjcat -cat -o cg-mapped.xtc -f cg_*.gro

exit
