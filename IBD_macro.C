// this macro takes user files from simulation and creates a new TTree

#include <fstream>
using namespace std;

TChain* read_file(const char* filename, const char* treename);

void IBD_macro(){ 

  ofstream fout;
  fout.open("rec_paths.txt");
  for(int k = 0; k < 40; ++k){
    if(k < 10){
      fout << "/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_000" << k << ".root" <<  endl;
    }
    else {
      fout << "/storage/gpfs_data/juno/junofs/users/mmalabarba/NMO_spectrum/risultati/all/NO/antinu/root/antinu_rec_user_r14000_00" << k << ".root" <<  endl;
    }
  }
  fout.close();

  TChain *recsimTC = read_file("rec_paths.txt","TRec");

  float m_NQE_t, Eprec_t, x_rec_t, y_rec_t, z_rec_t, r_rec_t, m_QTtime_t;  // for new tree branches
 
  // set branch address fro TRec tree
  printf("Setting branch addresses for recTC\n");
  recsimTC->SetBranchAddress("recQTx",&x_rec_t);
  recsimTC->SetBranchAddress("recQTy",&y_rec_t);
  recsimTC->SetBranchAddress("recQTz",&z_rec_t);
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

  // do stuff to fill the new tree

  for(UInt_t i = 0; i < recsimTC->GetEntries() ; i++){

    recsimTC->GetEntry(i);
    
    r_rec_t = sqrt(pow(x_rec_t,2)+pow(y_rec_t,2)+pow(z_rec_t,2));

    tot->Fill();
		 
  }


  printf("Saving new tree in root file\n");
  // save new tree on root file
  TFile *f2= TFile::Open("IBD_matched.root","RECREATE");
  if (!f2) {
    ////std::cerr << "Can't open file " << outputpath << std::endl;
    return;
  }
  tot->Write();
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
