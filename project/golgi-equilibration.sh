gmx grompp -f golgi-equilibration.mdp -c golgi-membrane-minimized.gro -p topol-golgi.top -o golgi-md.tpr -maxwarn 10
gmx mdrun -deffnm golgi-md -x golgi-md-traj.xtc -v
