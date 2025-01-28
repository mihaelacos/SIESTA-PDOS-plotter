import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

print("-------------------------------------------------------------------------------")
print('''         PDOS plotter by mihaelacos \n-------------------------------------------------------------------------------
--- only for SIESTA-DZ data (!!COLUMN!!) --- \n--- type your answer and press ENTER to continue ---''')

print(f'''-------------------------------------------------------------------------------
-- CURRENT DIRECTORY: {os.path.dirname(os.path.abspath(__file__))}
-------------------------------------------------------------------------------''')

path=input("\n ? absolute path to the desired .PDOS file \n   (example: /home/me/project/graphene) \n   (note: if none given, the default is the current directory)\n > ")
if path=="":
    path=os.path.dirname(os.path.abspath(__file__))
input_file=input("\n ? system label \n   (hint: PDOS file name, WITHOUT THE '.PDOS' termination: \n > ")
output_file=path+"/"+ input_file + ".png"
input_file=path+"/"+input_file+".PDOS"

shift=input("\n ? Shifted in E_F: yes / [no]: \n > ")
print(shift)
if "y" in shift: 
    shift=True
    print(shift) 
else: 
    shift=False
    print(shift)

# /home/mihaela/faculta/computational methods/cluster/pdos_plotter.py
with open(input_file,"r") as pdos:
    lines=pdos.readlines()
    n=[]
    l=[]
    m=[]
    z=[]
    PDOS=[]
    for i, line in enumerate(lines):
        if "<energy_values" in line:
            e0=i
        if "</energy_values" in line:
            e1=i
            points=e1-e0-1 
            energy=lines[e0+1:e1]
            energy=np.array(energy,dtype=float)
            # print(energy.shape)
        if "fermi_energy" in line:
            fermi=line.split(sep=">")
            fermi=fermi[1].split(sep="<")
            fermi=np.float64(fermi[0])
        if 'n="     ' in line:
            n.append(np.float64(line.split(sep='"')[1]))
        if 'l="     ' in line:
            l.append(np.float64(line.split(sep='"')[1]))
        if 'm="     ' in line:
            m.append(np.float64(line.split(sep='"')[1]))    
        if 'z="     ' in line:
            z.append(np.float64(line.split(sep='"')[1]))    
        if "<data>" in line:
            data=lines[i+1:i+1+points]
            PDOS.append(data)
        if ' index="  ' in line:
            index=np.int16((line.split(sep=None))[1][:-1])
            atom_index=np.int16(lines[i+1].split(sep=None)[1][:-1])
    num_orbitals=int((index)/(atom_index))

    PDOS=np.transpose(np.array(PDOS, dtype=float))


atom=input(f"\n ? projected on atom number #: \n  (hint: in range 1-{atom_index}, look at the index in the PDOS file. if none given, default is 1) \n > ")
if atom=="":
    atom=1
atom=int(atom)
interactive=input("\n ? want to preview the graphic interactivelly?   yes / [no] \n > ")
print(interactive)
if "y" in interactive:
    interactive=True
    print(interactive)
    
else: 
    interactive=False
    print(interactive)


print("E_F =",fermi,"eV")
print("number of orbitals:", num_orbitals)
print("number of atoms:", atom_index)
print("shape of PDOS array:" , PDOS.shape)
print("\n   plotting . . . \n")


labels=[]
for index in range(len(PDOS[0])):
    labels.append(f"n={int(n[index])}, l={int(l[index])}, m={int(m[index])}, z={int(z[index])} ")

flattt=PDOS[:,num_orbitals*(atom-1):num_orbitals*(atom-1)+num_orbitals].flatten()

plt.figure(figsize=(14,6))
plt.subplot(121)
plt.subplots_adjust(left=0.15, top=0.93, bottom=0.13, right=0.99)
plt.ylabel( f"PDOS")
plt.grid(alpha=0.7, axis="both", linestyle="--")
plt.title(f"PDOS of atom {atom}")
plt.ylim(np.min(flattt)*1.4,np.max(flattt)*1.4)
if shift==True:
    plt.text(x=0,y=max(flattt)*1.3, s=f"$\mathrm{{E_F}}$ = {fermi} eV")
    plt.vlines(x=0,ymin=0,ymax=np.max(flattt)*1.25, linestyles="dashed", linewidth=3, alpha=0.5, colors="yellow")
    plt.plot(energy-fermi,PDOS[:,num_orbitals*(atom-1):num_orbitals*(atom-1)+num_orbitals], label=labels[num_orbitals*(atom-1):num_orbitals*(atom-1)+num_orbitals],linewidth=0.9, alpha=1)
    plt.xlim(-28-fermi,28-fermi)
    plt.xlabel("E-$\mathrm{{E_F}}$(eV)")
else:
    plt.text(x=fermi,y=max(flattt)*1.3, s=f"$\mathrm{{E_F}}$ = {fermi} eV")
    plt.vlines(x=fermi,ymin=0,ymax=np.max(flattt)*1.25, linestyles="dashed", linewidth=3, alpha=0.5, colors="yellow")
    plt.plot(energy,PDOS[:,num_orbitals*(atom-1):num_orbitals*(atom-1)+num_orbitals], label=labels[num_orbitals*(atom-1):num_orbitals*(atom-1)+num_orbitals],linewidth=0.9, alpha=1)
    plt.xlim(-28,28)
    plt.xlabel("E (eV)")
plt.legend(fontsize=8,loc="upper left")
plt.savefig(output_file)
print(f"Image saved at {output_file}")
if interactive==True: plt.show()

