import os, sys
import ROOT
from os import listdir

from TriggerList import *
sys.path.append('../')
from Helper.HistInfo import HistInfo

def get_parser():
    ''' Argument parser.                                                                                                                                                
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--sample',           action='store',                    type=str,            default='SingleElectron_Data',                    help="Which sample?" )
    argParser.add_argument('--trigger',          action='store',                    type=str,            default='AltMETTriggers',                         help="Which triggers?")
    argParser.add_argument('--folder',           action='store',                    type=str,            default='rootfiles',                      help="Which folder contains the root files?")
    return argParser

options = get_parser().parse_args()

sample = options.sample
trigger = options.trigger
folder = options.folder

if trigger == 'METTriggers':
    tr=METTriggers
else:
    tr=AltMETTriggers

numTrigHist = dict((key, 'hMET_'+key) for key in tr)

histext = sample
hfile = ROOT.TFile( 'TrigHist_'+sample+'.root', 'RECREATE')
histos={}
for key in numTrigHist:
    histos[numTrigHist[key]+'_MET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_MET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_MET_phi_den'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_den', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_MET_phi_num'] = HistInfo(hname = numTrigHist[key]+'_MET_phi_num', sample = histext, binning=[-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Muon_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_Electron_pt_den'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_den', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
    histos[numTrigHist[key]+'_Electron_pt_num'] = HistInfo(hname = numTrigHist[key]+'_Electron_pt_num', sample = histext, binning=[0,20,40,60,80,100,150,200,250], histclass = ROOT.TH1F, binopt='').make_hist()
    if trigger == 'AltMETTriggers':
        histos[numTrigHist[key]+'_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_den', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_num', sample = histext, binning=[0,50,80,100,120,140,160,180,200,220,240,260,300,350,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_den', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_num', sample = histext, binning=[0,20,40,60,80,100,120,140,160,200,300,400,500], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_rel_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_den', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_rel_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_rel_pt_num', sample = histext, binning=[0,0.2,0.4,0.6,0.8,1], histclass = ROOT.TH1F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_pt_AltMET_pt_den'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_den', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_MET_pt_AltMET_pt_num'] = HistInfo(hname = numTrigHist[key]+'_MET_pt_AltMET_pt_num', sample = histext, binning=[[15,0,500],[15,0,500]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_den', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_AltMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_AltMET_pt_Muon_pt_num', sample = histext, binning=[[15,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_den'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_den', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()
        histos[numTrigHist[key]+'_deltaMET_pt_Muon_pt_num'] = HistInfo(hname = numTrigHist[key]+'_deltaMET_pt_Muon_pt_num', sample = histext, binning=[[12,0,500],[8,0,250]], histclass = ROOT.TH2F, binopt='').make_hist()

posSamples=["SingleElectron_Run2016B", "SingleElectron_Run2016C", "SingleElectron_Run2016D", "SingleElectron_Run2016E", "SingleElectron_Run2016F", "SingleElectron_Run2016G", "SingleElectron_Run2016H", "SingleElectron_Data"]
files=[f for f in listdir(os.getcwd()+"/"+folder)]
for i in range(len(files)):
    savedfile=ROOT.TFile.Open(os.getcwd()+"/"+folder+"/"+files[i])
    for key in histos.keys():
        for s in posSamples:
            if savedfile.Get(key+'_'+s):
                histos[key].Add(savedfile.Get(key+'_'+s))
        
hfile.Write()        
