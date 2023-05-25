import ROOT
import math
import numpy as np
#from matplotlib import pyplot as pl
from array import array

hist_pd=ROOT.TH2F("pd","pd",100, 0, 5e4, 100, 0, 5e4)
f = ROOT.TFile.Open("/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_0000.root")
T = f.Get("TRec")
branch = ["posx", "posy", "posz", "pe_tot", "m_QTtime"]
nEntries = T.GetEntries()

ind_prompt=[]
ind_del=[]
pe_prompt=[]
pe_del=[]
hist_pe = array('f', [0])
hist_t = array ('d', [0])
T.SetBranchAddress("m_PESum", hist_pe)
T.SetBranchAddress("m_triggerT", hist_t)
j=nEntries
for i in range (0,j):
	T.GetEvent(i)
	t0=hist_t[0]
	p0=hist_pe[0]
	T.GetEvent(i+1)
	t1=hist_t[0]
	p1=hist_pe[0]
	if ((t1-t0)<1e6):
		ind_prompt.append(t0)
		ind_del.append(t1)
		pe_prompt.append(p0)
		pe_del.append(p1)
		hist_pd.Fill(p1,p0)
		i+1
		j-1

c1 = ROOT.TCanvas("c1", "c1")
#hist_pd.Fill(pe_prompt,pe_del)
hist_pd.Draw()
