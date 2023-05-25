// This macro distinguishes between prompt and delayed event and does some analysis

#include <fstream>
using namespace std;

TChain* read_file(const char* filename, const char* treename);

void IBD_analysis(){ 

  TChain *recsimTC = read_file("tree_path.txt","tot");

  float m_NQE_t, Eprec_t, x_rec_t, y_rec_t, z_rec_t, r_rec_t, m_QTtime_t;  // for new tree branches

  // set branch address fro TRec tree
  printf("Setting branch addresses for recTC\n");
  recsimTC->SetBranchAddress("x_rec",&x_rec_t);
  recsimTC->SetBranchAddress("y_rec",&y_rec_t);
  recsimTC->SetBranchAddress("z_rec",&z_rec_t);
  recsimTC->SetBranchAddress("r_rec",&r_rec_t);
  recsimTC->SetBranchAddress("m_QTtime",&m_QTtime_t);
  recsimTC->SetBranchAddress("m_NQE",&m_NQE_t);

  // define a new TTree and set branch
  printf("Creating new tree\n");
  TTree *tot = new TTree("tot","tot");
  tot->Branch("x_rec",&x_rec_t,"x_rec/F");;
  tot->Branch("y_rec",&y_rec_t,"y_rec/F");
  tot->Branch("z_rec",&z_rec_t,"z_rec/F");
  tot->Branch("r_rec",&r_rec_t,"r_rec/F");
  tot->Branch("m_QTtime",&m_QTtime_t,"m_QTtime/F");
  tot->Branch("m_NQE",&m_NQE_t,"m_NQE/F");

  // new branches
  /*int IBD_selection_t;
  tot->Branch("IBD_selection", &IBD_selection_t);

  double deltar_t;
  tot->Branch("deltar_t", &deltar_t);

  double deltat_t;
  tot->Branch("deltat_t", &deltat_t);*/

  int prompt_t;
  tot->Branch("prompt", &prompt_t);

  TH2F *histo = new TH2F("histo","E_delayed vs E_prompt",200,0.,7.,200,0.,12.);
  TH1F *h_prompt = new TH1F("h_prompt","h_prompt",200,0.,12.);
  TH1F *h_delayed = new TH1F("h_delayed","h_delayed",200,0.,7.);

  for(UInt_t i = 0; i < recsimTC->GetEntries() ; i++){

    recsimTC->GetEntry(i);
    /*int rec = r_rec_t

    for(int k = 1; k < recsimTC->GetEntries(); k++){
      deltar_t = rec - 
      }*/

    if(m_QTtime_t < 1.9){     //taglio in tempo per distinguere tra prompt e delayed (300 micro s)
      prompt_t = 1;
      h_prompt->Fill(m_NQE_t);
    }
    else{
      prompt_t = 0;
      h_delayed->Fill(m_NQE_t);
    }

    tot->Fill();
		 
  }

  for(int i = 0; i < h_delayed->GetNbinsX(); i++){
    for(int j = 0; j < h_prompt->GetNbinsX(); j++){

      histo->SetBinContent(i, j, h_delayed->GetBinContent(i)+h_prompt->GetBinContent(j));
    }

  }

  TCanvas *c = new TCanvas("c","c");
  //histo->SetMarkerSize(0.1);
  histo->GetXaxis()->SetTitle("E_delayed [MeV]");
  histo->GetYaxis()->SetTitle("E_prompt [MeV]");
  histo->Draw();

  TCanvas *c2 = new TCanvas("c2","c2");
  h_prompt->GetXaxis()->SetTitle("E_prompt [MeV]");
  h_prompt->Draw();

  TCanvas *c3 = new TCanvas("c3","c3");
  h_delayed->GetXaxis()->SetTitle("E_delayed [MeV]");
  h_delayed->Draw();

  printf("Saving new tree in root file\n");
  // save new tree on root file
  TFile *f2= TFile::Open("IBD_analysis.root","RECREATE");
  if (!f2) {
    ////std::cerr << "Can't open file " << outputpath << std::endl;
    return;
  }
  tot->Write();
  histo->Write();
  f2->Close();

}


TChain* read_file(const char* filename, const char* treename) {

		std::ifstream path_file(filename);
		printf("Opening %s\n",filename);
		TChain *TC = new TChain(treename);

		if (path_file.is_open()){
				std::string line;
				while (std::getline(path_file,line)) {
				  //printf("Reading %s\n",line.c_str());
						TC->Add(line.c_str());
				}
				path_file.close();
		}

		return TC;
}
