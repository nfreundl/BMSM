# using the itp file from first running, IMPORTANT donnot change the of Protein_A.itp and include this in the *.top files

gmx grompp -f minimization-parameters.mdp -c golgi-membrane.gro -p topol-golgi.top -o minimized-golgi.tpr -maxwarn 10

gmx grompp -f minimization-parameters.mdp -c mito-membrane.gro -p topol-mito.top -o minimized-mitochondrial.tpr -maxwarn 10

gmx mdrun -deffnm minimized-golgi -v -c golgi-membrane-minimized.gro 
gmx mdrun -deffnm minimized-mitochondrial -v -c mitochondrial-membrane-minimized.gro
