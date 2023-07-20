import ROOT
import math
import numpy as np
#from matplotlib import pyplot as pl
from array import array
import time

hist_pd=ROOT.TH2F("histo","E_delayed vs E_prompt",100, 0, 13, 100, 0, 14)
hist_pos = ROOT.TH1F("histopos", "delta r", 200, 0, 25000)
hist_time = ROOT.TH1F("histotime", "delta t", 100, 0, 2000000)
hist_prompt = ROOT.TH1F("histoprompt", "E_prompt",200, 0, 14)
hist_delayed = ROOT.TH1F("histodelayed", "E_delayed", 300, 0, 14)
hist_vol = ROOT.TH1F("histovol", "histovol", 100, 0, 23000)

nEntriesTot = 0
count = 0
sel = 0

energy = []
pos = []
x = []
y = []
z = []
ident1 = []

#numFile = 3599
numFile = 300
for k in range (0, numFile+1):
    if k < 1800: f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/nikhilmohan/new_production_05July/acc_06Sep/output/user-rec-"+str(k)+".root")
    elif k == 2680: continue 
    else: f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/ameraviglia/IBD_Okt12_Ferrara/output/user-rec-"+str(k)+".root")
    #else: f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_00"+str(k)+".root")
    #/storage/gpfs_data/juno/junofs/users/vcerrone/IBD_production/production_nov12/user_files/rec_user_"+str(k)+".root"
    #/storage/gpfs_data/juno/junofs/users/vcerrone/IBD_production/production_nov12/new_reco/
    #/storage/gpfs_data/juno/junofs/users/ameraviglia/IBD_Okt12_Ferrara/output/user-rec- (escludi il 1808, 1820 perché non contiene TRec)
    #/storage/gpfs_data/juno/junofs/users/nikhilmohan/new_production_05July/acc_06Sep/output/user-rec- (da 0 a 1799)

    #Controllo se sia presente il tree TRec, perché non tutti i file di radioattività lo contengono
    isFile = False
    for key in f.GetListOfKeys():
        kname = key.GetName()
        if (kname == "TRec"):
            isFile = True

    if(isFile == True):
        print("Opening file number " + str(k))

        T = f.Get("TRec")
        nEntries = T.GetEntries()

        ind_prompt=[]
        ind_del=[]
        pe_prompt=[]
        pe_del=[]
        hist_pe = array('f', [0])
        hist_t = array ('d', [0])
        hist_t0 = array('f', [0])
        hist_x = array ('f', [0])
        hist_y = array ('f', [0])
        hist_z = array ('f', [0])
        T.SetBranchAddress("m_QEn", hist_pe)
        T.SetBranchAddress("m_triggerT", hist_t)
        T.SetBranchAddress("recQTt0", hist_t0)
        T.SetBranchAddress("recx", hist_x)
        T.SetBranchAddress("recy", hist_y)
        T.SetBranchAddress("recz", hist_z)

        i=0
        while i < nEntries:
                T.GetEntry(i)
                p0 = hist_pe[0]*0.92
                x0 = hist_x[0]
                y0 = hist_y[0]
                z0 = hist_z[0]
                r0 = (x0**2 + y0**2 + z0**2)**0.5
                
                energy.append(p0)
                pos.append(r0)
                x.append(x0)
                y.append(y0)
                z.append(z0)

                nEntriesTot = nEntriesTot+1
                i = i+1

for u in range (0, nEntriesTot):
    
    if (energy[u] > 0.7): ident1.append(u)

start = time.time() 

for s in range (0, len(ident1)):
    for t in range (s+1, len(ident1)):
        print("Controllo della coppia " + str(s) + " - " + str(t))
        deltar = ((x[ident1[s]] - x[ident1[t]])**2 + (y[ident1[s]] - y[ident1[t]])**2 + (z[ident1[s]] - z[ident1[t]])**2)**0.5

        if(energy[ident1[t]] < 12 and pos[ident1[s]] < 17200 and pos[ident1[t]] < 17200 and ((energy[ident1[s]] > 1.9 and energy[ident1[s]] < 2.5) or (energy[ident1[s]] > 4.4 and energy[ident1[s]] < 5.5)) and deltar < 1500): 
            sel = sel+1
        elif(energy[ident1[s]] < 12 and pos[ident1[s]] < 17200 and pos[ident1[t]] < 17200 and ((energy[ident1[t]] > 1.9 and energy[ident1[t]] < 2.5) or (energy[ident1[t]] > 4.4 and energy[ident1[t]] < 5.5)) and deltar < 1500): sel = sel+1

nComb = len(ident1)*(len(ident1)-1)

end = time.time()

print("Numero eventi in totale: " + str(nEntriesTot))
print("Numero coppie che soddisfano il taglio in energia preliminare: "+str(nComb))
print("Numero coppie selezionate: "+str(sel))
print("Efficienza: "+str(sel/nComb))
print("Tempo impiegato: "+ str(end - start))
                
