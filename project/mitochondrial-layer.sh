python  insane.py -o mito-membrane.gro -p topol-mito.top  -l POPC:40  -l POPE:34  -l CDL2:18 -sol PW  -box  13,13,19  -pbc square  -dm 6
gmx insert-molecules -f 1fj2-martinized.gro -ci mito-membrane.gro -o system-mito.gro -radius 0.21 -box 13 13 19 -nmol 1
