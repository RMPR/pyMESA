import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('/home/oriol/Publico/mesaplot/mesaPlot')
import file_reader as mp
from NuGridPy import mesa as ms
#import mesaPlot as mp
import re

m=mp.MESA()

log_fold='LOGS'
#p=ms.mesa_profile(sldir=log_fold,num=1)
p=ms.mesa_profile()
p._profiles_index()
models=p.model
profs=p.log_ind

# find all profiles to import with mesaPlot
#m._loadProfileIndex(log_fold)
#profiles = m.prof_ind['profile']
first=True
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
start=0
end=200
length=len(models)
Z1vec=np.arange(length, dtype=float)
Z2vec=np.arange(length, dtype=float)
agevec=np.arange(length, dtype=float)

#for i,prof in enumerate(profiles):
for i,mod_num in enumerate(models):
    #m.loadProfile(f=log_fold, prof=prof, silent=True)
    doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
    length=pym.file_len(doc)
    hdr, cols, data=ms._read_mesafile(doc, length-6)
    if first:
        abun_list=pym.getIsos(cols.keys())
        for iso in abun_list:
            abunMatch = abunPat.match(iso)
            el = abunMatch.groups(1)[0]
            if np.any(np.array(['h', 'he'])==el):
                nonmetals.append(iso)
            else:
                metals.append(iso)
        first=False
    Z1=0.
    w=10**data[:,cols['logdq']-1]  # get mass fractions
    wsum=sum(w[start:end])
    # Add all mass fractions (with respect to the cell) for h and he
    for iso in nonmetals:
        Z1+=data[:,cols[iso]-1][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z1*=w[start:end]
    Z1=sum(Z1)/wsum
    Z1vec[i]=1-Z1
    Z2=0.
    # Add all mass fractions (with respect to the cell) for metals 
    for iso in metals:
        Z2+=data[:,cols[iso]-1][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z2*=w[start:end]
    Z2vec[i]=sum(Z2)/wsum
    agevec[i]=hdr['star_age']

plt.plot(agevec,Z1vec,agevec,Z2vec)
#plt.show()
