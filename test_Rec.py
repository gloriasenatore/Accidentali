import ROOT
import math
import numpy as np
#from matplotlib import pyplot as pl
from array import array 

hist_pd=ROOT.TH2F("histo","E_delayed vs E_prompt",100, 0, 13, 100, 0, 14)

numFile = 40
for k in range (0, numFile):
    if(k < 10):
        f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_000"+str(k)+".root")
    else: f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_00"+str(k)+".root")

    print("Opening file number " + str(k))

    T = f.Get("TRec")
    branch = ["recx", "recy", "recz", "m_NQE", "m_triggerT"]
    nEntries = T.GetEntries()

    ind_prompt=[]
    ind_del=[]
    pe_prompt=[]
    pe_del=[]
    hist_pe = array('f', [0])
    hist_t = array ('d', [0])
    hist_x = array ('f', [0])
    hist_y = array ('f', [0])
    hist_z = array ('f', [0])
    T.SetBranchAddress("m_NQE", hist_pe)
    T.SetBranchAddress("m_triggerT", hist_t)
    T.SetBranchAddress("recx", hist_x)
    T.SetBranchAddress("recy", hist_y)
    T.SetBranchAddress("recz", hist_z)

    i = 0
    while i < nEntries:
            T.GetEvent(i)
            t0=hist_t[0]
            p0=hist_pe[0]
            x0=hist_x[0]
            y0=hist_y[0]
            z0=hist_z[0]
            r0 = (x0**2 + y0**2 + z0**2)**0.5

            T.GetEvent(i+1)
            t1=hist_t[0]
            p1=hist_pe[0]
            x1=hist_x[0]
            y1=hist_y[0]
            z1=hist_z[0]
            r1 = (x1**2 + y1**2 + z1**2)**0.5

            if ((t1-t0)<1e6 and abs(r0-r1) < 1500):
                    ind_prompt.append(t0)
                    ind_del.append(t1)
                    pe_prompt.append(p0)
                    pe_del.append(p1)
                    hist_pd.Fill(p1,p0)
                    i=i+2
            else:
                    i=i+1

c1 = ROOT.TCanvas("c1", "c1")
#hist_pd.Fill(pe_prompt,pe_del)
hist_pd.GetXaxis().SetTitle("E_delayed [MeV]")
hist_pd.GetYaxis().SetTitle("E_prompt [MeV]")
hist_pd.SetStats(1)
hist_pd.Draw("COLZ")


