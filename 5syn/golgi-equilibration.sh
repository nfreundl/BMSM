gmx grompp -f golgi-equilibration.mdp -c mitochondrial-membrane-minimized.gro -p topol-mito.top -o mitochondrial-md.tpr -maxwarn 10
gmx mdrun -deffnm mitochondrial-md -x mitochondrial-md-traj.xtc -v
