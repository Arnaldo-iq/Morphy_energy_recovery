import os, fnmatch

import numpy as np

import matplotlib.pyplot as plt

home = os.getcwd()

directories=[d for d in os.listdir(home) if os.path.isdir(d) if fnmatch.fnmatch(d,'*.dir')]

directories=sorted(directories)

tot_morp= []
tot_g09 = []

for dir in directories:
    os.chdir(os.path.join(dir))
    corr_morp = []
    for tipo in os.listdir('.'):
        if fnmatch.fnmatch(tipo,'test.mout'):
            with open(tipo, 'r') as inte:
                  for info in inte:
                      if 'with all atoms (including self) is' in info:
                          atom_data = []
                          atom_data = next(inte).split()
                          corr = float(atom_data[0])
                          corr_morp.append(corr)
                          
    tot_morp.append(sum(corr_morp))
    
    os.chdir(os.path.join(home))
    
#    
for dir in directories:
    os.chdir(os.path.join(dir))
    mp2_g09 = []
    mp3_g09 = []
    mp4_g09 = []
    g09_corr = []
    for tipo in os.listdir('.'):
        if fnmatch.fnmatch(tipo,'gen-MP4'):
            with open(tipo, 'r') as inte:
                  for info in inte:
                      if ' E2 =    ' in info:
                          mp2_data = []
                          mp2_data = info.split()
                          corr_mp2 = str(mp2_data[2].strip())
                          
                          corr_mp2 = corr_mp2.replace('D','E')
                          corr_mp2_g09 = float(corr_mp2)
                          mp2_g09.append(corr_mp2_g09)
                         
                      if 'E3=       ' in info:
                          mp3_data = []
                          mp3_data = info.split() 
                          corr_mp3 = str(mp3_data[1].strip())
                          
                          corr_mp3 = corr_mp3.replace('D','E')
                          corr_mp3_g09 = float(corr_mp3)
                          mp3_g09.append(corr_mp3_g09)
                          
                      if 'E4(SDQ)=  ' in info:
                          mp4_data = []
                          mp4_data = info.split()
                          corr_mp4 = str(mp4_data[1].strip())
                      
                          corr_mp4 = corr_mp4.replace('D','E')
                          corr_mp4_g09 = float(corr_mp4)
                          mp4_g09.append(corr_mp4_g09)
                          
                          g09_corr = [(mp2_g09[i]+mp3_g09[i]+mp4_g09[i]) for i in range(len(mp2_g09))]
                          
                          
                 
       
                        
    tot_g09.append(sum(g09_corr))                 
    
    os.chdir(os.path.join(home))
    

Err = [(tot_morp[i]-tot_g09[i])*2625.5 for i in range(len(tot_morp))]



for i in range(len(Err)):
    print i
    print 'The Integration Error is (kJ.mol-1)', Err[i] 
    
print sum(Err)/len(Err)
