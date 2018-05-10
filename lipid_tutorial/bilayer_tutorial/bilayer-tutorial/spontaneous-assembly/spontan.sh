gmx insert-molecules -ci dspc_single.gro -nmol 128 -box 7.5 7.5 7.5 -try 500 -o 128_noW.gro
gmx grompp -f minimization.mdp -c 128_noW.gro -p dspc.top -maxwarn 10 -o dspc-min-init.tpr

gmx mdrun -deffnm dspc-min-init -v -c 128_minimised.gro
gmx solvate -cp 128_minimised.gro -cs water.gro -o waterbox.gro -maxsol 768 -radius 0.21 

gmx grompp -f minimization.mdp -c waterbox.gro -p dspc.top -maxwarn 10 -o dspc-min-solvent.tpr
gmx mdrun -deffnm dspc-min-solvent -v -c minimised.gro 


gmx grompp -f martini_md.mdp -c minimised.gro -p dspc.top -maxwarn 10 -o dspc-md.tpr
gmx mdrun -x trajectories2.xtc -deffnm dspc-md -v
