import os, fnmatch

import numpy as np

import matplotlib.pyplot as plt

home = os.getcwd()
print 'All Energy terms are in a.u.'
energy = []
files = os.listdir('.')
files.sort()
for file in files:
    if fnmatch.fnmatch(file,'*.wfn'):

       with open(file, 'r') as out:

            for line in out:
                if 'TOTAL ENERGY =' in line:
                    wfn_data = []
                    wfn_data = line.split()
                    number = float(wfn_data[3])
                    energy.append(number)

print ('The total Energy in the WFN file is', energy)
directories=[d for d in os.listdir(home) if os.path.isdir(d) if fnmatch.fnmatch(d,'*_atomicfiles')]

directories=sorted(directories)

Total_IQA = []
Inter_Coul = []
Inter_Exc = []

Kinetic =[]
Intra_Coul = []
Intra_Exc = []

for dir in directories:
    os.chdir(os.path.join(dir))
  
    VneAB = []
    VenAB = []
    VnnAB = []
    VeeAB = []
    VCAB = []
    VeeXAB = []
    VXAB = []
    
    TA = []
    VneAA = []
    VeeCAA = []
    VeeXAA = []

    for tipo in os.listdir('.'):
            if fnmatch.fnmatch(tipo,'*_*') and fnmatch.fnmatch(tipo,'*.int'):
                    with open(tipo, 'r') as inte:
                            for info in inte:
                                    if 'Ven(A,B)/2' in info:
                                            ven_data = []
                                            ven_data =  info.split()
                                            ven = float(ven_data[2])
                                            VenAB.append(ven)

                                    if 'Vne(A,B)/2' in info:
                                            vne_data = []
                                            vne_data =  info.split()
                                            vne = float(vne_data[2])
                                            VneAB.append(vne)

                                    if 'Vnn(A,B)/2' in info:
                                            vnn_data = []
                                            vnn_data =  info.split()
                                            vnn = float(vnn_data[2])
                                            VnnAB.append(vnn)
            
                                    if 'VeeC(A,B)/2' in info:
                                            vee_data = []
                                            vee_data =  info.split()
                                            vee = float(vee_data[2])
                                            VeeAB.append(vee)
                                    if 'VeeX(A,B)/2' in info:
                                            veex_data = []
                                            veex_data =  info.split()
                                            veex = float(veex_data[2])
                                            VeeXAB.append(veex)

                                            VCAB = [(VneAB[i]+VenAB[i]+VnnAB[i]+VeeAB[i])*2 for i in range(len(VneAB))]
                                            VXAB = VeeXAB*2

            if fnmatch.fnmatch(tipo,'*_*') == False and fnmatch.fnmatch(tipo,'*.int'):
                    with open(tipo, 'r') as inte:
                            for info in inte:
                                    if ' T(A)' in info:              
                                            ta_data = []
                                            ta_data =  info.split()
                                            ta = float(ta_data[2])
                                            TA.append(ta)
#
                                    if 'Vneen(A,A)/2 = Vne(A,A)' in info:
                                            vnea_data = []
                                            vnea_data =  info.split()
                                            vnea = float(vnea_data[4])
                                            VneAA.append(vnea)

                                    if ' VeeC(A,A)' in info:
                                            veea_data = []
                                            veea_data = info.split()
                                            veea = float(veea_data[2])
                                            VeeCAA.append(veea)

                                    if ' VeeX(A,A)           =' in info:
                                            veeax_data = []
                                            veeax_data =  info.split()
                                            veeax = float(veeax_data[2])
                                            VeeXAA.append(veeax)                                 
                                        
    Inter_Coul.append(sum(VCAB))
    Inter_Exc.append(sum(VXAB))
    Intra_Coul.append(sum(VneAA)+sum(VeeCAA))
    Intra_Exc.append(sum(VeeXAA))
    Kinetic.append(sum(TA))
    
    os.chdir(os.path.join(home))
       
Total_IQA = [Inter_Coul[i] + Inter_Exc[i] + Kinetic[i] + Intra_Coul[i] + Intra_Exc[i] for i in range(len(Kinetic))]

print('The Total Kinetic Energy is', Kinetic)  

print('The total Intra-atomic Coulomb Energy is', Intra_Coul)
print('The total Intra-atomic Exchange Energy is', Intra_Exc)

print('The total Interatomic Coulomb Energy is', Inter_Coul)
print('The total Interatomic Exchange Energy is', Inter_Exc)

print('The Total IQA Engergy is', Total_IQA)

Err = [(energy[i]-Total_IQA[i])*2625.5 for i in range(len(energy))]

print('The Integration Error is', Err)

for i in range(len(Err)):
    print directories[i] 
    print ' '
    print 'The Total Kinetic Energy is = ', Kinetic[i]
    print 'The total Intra-atomic Coulomb Energy is', Intra_Coul[i]
    print 'The total Intra-atomic Exchange Energy is', Intra_Exc[i]
    print 'The total Interatomic Coulomb Energy is', Inter_Coul[i]
    print 'The total Interatomic Exchange Energy is', Inter_Exc[i]
    print ' '
    print 'The Total IQA Engergy is', Total_IQA[i]
    print 'The Total WFN Engergy is', energy[i]
    print ' '
    print 'The Integration Error is', Err[i] 
    
    print ' '

x = np.arange(len(Err))

plt.plot( x, energy,    marker='', color='blue', linewidth=2, linestyle='dashed', label="WFN")
plt.plot( x, Total_IQA, marker='', color='red', linewidth=2, label='IQA')

plt.legend()

plt.show()
