import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("---------------------------------------------")
print("\n    graphene PDOS plotter by meha \n -- only for DZ data, for DZP calculations you can use the tool at daemonplot.com \n -- type your answer and press ENTER to continue")
path=input("\npath to the desired .PDOS file \n (hint: you are now in your directory at the CURRENT LOCATION from above) \n (example: /home/student-CM/me/project/graphene) \n")
input_file=input("\nsystem label \n (hint: PDOS file name, WITHOUT THE '.PDOS' termination: \n")
output_file=path+"/"+ input_file + ".png"
input_file=path+"/"+input_file+".PDOS"

shift=input("\nShifted in Ef: True / [False]: \n")
if shift=="":
    shift=False
shift=bool(shift)

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
            print("Ef =",fermi,"eV")
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
    PDOS=np.transpose(np.array(PDOS, dtype=float))

    print("shape of PDOS array:" , PDOS.shape)


atom=input("\nPDOS on atom number: \n (hint: look at the index in the PDOS file. if none given, [default=1]) \n")
if atom=="":
    atom=1
atom=int(atom)

labels=[]
for index in range(len(PDOS[0])):
    labels.append(f"n={int(n[index])}, l={int(l[index])}, m={int(m[index])}, z={int(z[index])} ")

flattt=PDOS[:,8*(atom-1):8*(atom-1)+8].flatten()
print("plotting . . . ")
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
    plt.plot(energy-fermi,PDOS[:,8*(atom-1):8*(atom-1)+8], label=labels[8*(atom-1):8*(atom-1)+8],linewidth=0.9, alpha=1)
    plt.xlim(-28-fermi,28-fermi)
    plt.xlabel("E-$\mathrm{{E_F}}$(eV)")
else:
    plt.text(x=fermi,y=max(flattt)*1.3, s=f"$\mathrm{{E_F}}$ = {fermi} eV")
    plt.vlines(x=0,ymin=0,ymax=np.max(flattt)*1.25, linestyles="dashed", linewidth=3, alpha=0.5, colors="yellow")
    plt.plot(energy,PDOS[:,8*(atom-1):8*(atom-1)+8], label=labels[8*(atom-1):8*(atom-1)+8],linewidth=0.9, alpha=1)
    plt.xlim(-28,28)
    plt.xlabel("E (eV)")
plt.legend(fontsize=8,loc="upper left")
plt.savefig(output_file)
print(f"Image saved at {output_file}")
plt.show()
