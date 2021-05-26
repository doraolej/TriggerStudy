import os, sys
import ROOT
from os import listdir

from TriggerList import *
sys.path.append('../')
from Helper.CosmeticCode import *

def get_parser():
    ''' Argument parser.                                                                                                                                                
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--infile',           action='store',                     type=str,            default='TrigHist_SingleElectron_Data.root',                    help="Which input root file?" )
    argParser.add_argument('--sample',           action='store',                     type=str,            default='SingleElectron_Data',                    help="Which sample?" )
    argParser.add_argument('--trigger',          action='store',                     type=str,           default='AltMETTriggers',                           help="Which triggers?")
    return argParser

options = get_parser().parse_args()

f = options.infile
sample = options.sample
trigger = options.trigger

lepOpt = 'Ele' if 'Ele' in sample else 'Mu'

if trigger == 'METTriggers':
    tr=METTriggers
else:
    tr=AltMETTriggers

numTrigHist = dict((key, 'hMET_'+key) for key in tr)

if os.path.exists(f):
    hfile = ROOT.TFile.Open(f)
else:
    print 'Trigger histogram file does not exist'

plotDir= os.getcwd()+"/Plots/"

trigDict = {}

if trigger == 'METTriggers':
    for trig, hist in numTrigHist.items():
        trigDict[trig] = [hfile.Get(hist+'_MET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_den_'+sample), hfile.Get(hist+'_MET_phi_num_'+sample), hfile.Get(hist+'_MET_phi_den_'+sample), hfile.Get(hist+'_Muon_pt_num_'+sample), hfile.Get(hist+'_Muon_pt_den_'+sample), hfile.Get(hist+'_Electron_pt_num_'+sample), hfile.Get(hist+'_Electron_pt_den_'+sample)]
if trigger == 'AltMETTriggers':
    for trig, hist in numTrigHist.items():
        trigDict[trig] = [hfile.Get(hist+'_MET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_den_'+sample), hfile.Get(hist+'_MET_phi_num_'+sample), hfile.Get(hist+'_MET_phi_den_'+sample), hfile.Get(hist+'_Muon_pt_num_'+sample), hfile.Get(hist+'_Muon_pt_den_'+sample), hfile.Get(hist+'_Electron_pt_num_'+sample), hfile.Get(hist+'_Electron_pt_den_'+sample), hfile.Get(hist+'_deltaMET_pt_num_'+sample), hfile.Get(hist+'_deltaMET_pt_den_'+sample), hfile.Get(hist+'_deltaMET_rel_pt_num_'+sample), hfile.Get(hist+'_deltaMET_rel_pt_den_'+sample), hfile.Get(hist+'_AltMET_pt_num_'+sample), hfile.Get(hist+'_AltMET_pt_den_'+sample), hfile.Get(hist+'_MET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_MET_pt_Muon_pt_den_'+sample), hfile.Get(hist+'_MET_pt_AltMET_pt_num_'+sample), hfile.Get(hist+'_MET_pt_AltMET_pt_den_'+sample), hfile.Get(hist+'_AltMET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_AltMET_pt_Muon_pt_den_'+sample), hfile.Get(hist+'_deltaMET_pt_Muon_pt_num_'+sample), hfile.Get(hist+'_deltaMET_pt_Muon_pt_den_'+sample)]

mg_MET_pt = ROOT.TMultiGraph()
mg_MET_phi = ROOT.TMultiGraph()
mg_Muon_pt = ROOT.TMultiGraph()
mg_Electron_pt = ROOT.TMultiGraph()
mg_MET_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
mg_MET_phi_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
mg_Muon_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
mg_Electron_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)

if trigger == 'AltMETTriggers':
    mg_AltMET_pt = ROOT.TMultiGraph()
    mg_deltaMET_pt = ROOT.TMultiGraph()
    mg_deltaMET_rel_pt = ROOT.TMultiGraph()
    mg_AltMET_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
    mg_deltaMET_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)
    mg_deltaMET_rel_pt_leg = ROOT.TLegend(0.5, 0.75, 0.9, 0.9)


for trig, hist in trigDict.items():

    heff_MET_pt = ROOT.TGraphAsymmErrors()
    heff_MET_phi = ROOT.TGraphAsymmErrors()
    heff_Muon_pt = ROOT.TGraphAsymmErrors()
    heff_Electron_pt = ROOT.TGraphAsymmErrors()
    heff_MET_pt.BayesDivide(hist[0],hist[1])
    heff_MET_phi.BayesDivide(hist[2],hist[3])
    heff_Muon_pt.BayesDivide(hist[4],hist[5])
    heff_Electron_pt.BayesDivide(hist[6],hist[7])
    
    if trigger == 'AltMETTriggers':
        heff_AltMET_pt = ROOT.TGraphAsymmErrors()
        heff_deltaMET_pt = ROOT.TGraphAsymmErrors()
        heff_deltaMET_rel_pt = ROOT.TGraphAsymmErrors()
        heff_AltMET_pt.BayesDivide(hist[12],hist[13])
        heff_deltaMET_pt.BayesDivide(hist[8],hist[9])
        heff_deltaMET_rel_pt.BayesDivide(hist[10],hist[11])
    
    #num and den plots
    for i in hist:
        
        if i==hist[0] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("MET_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/MET_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_MET_pt_num_"+sample+".png")
        
        if i==hist[1] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("MET_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/MET_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_MET_pt_den_"+sample+".png")
           
        if i==hist[2] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("MET_phi")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/MET_Phi/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_MET_phi_num_"+sample+".png")
            
        if i==hist[3] :
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("MET_phi")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/MET_Phi/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_MET_phi_den_"+sample+".png")
        
        if i==hist[4] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("Muon_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/Muon_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_Muon_pt_num_"+sample+".png")
        
        if i==hist[5] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("Muon_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/Muon_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_Muon_pt_den_"+sample+".png")
            
        if i==hist[6] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("Electron_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/Electron_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_Electron_pt_num_"+sample+".png")
        
        if i==hist[7] : 
            i.GetYaxis().SetTitle("Entries")
            i.GetXaxis().SetTitle("Electron_pt")
            c = ROOT.TCanvas('c', '', 600, 800)
            i.Draw()
            ROOT.gPad.SetGrid()
            outPath=(plotDir+sample+"_"+trigger+"/Electron_Pt/")
            if not os.path.exists(outPath):
                os.makedirs(outPath)
            c.SaveAs(outPath+trig+"_Electron_pt_den_"+sample+".png")
        
        if trigger == 'AltMETTriggers':
            if i==hist[8] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("deltaMET_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_pt_num_"+sample+".png")

            if i==hist[9] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("deltaMET_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_pt_den_"+sample+".png")
        
            if i==hist[10] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("deltaMET_rel_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_rel_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_rel_pt_num_"+sample+".png")
        
            if i==hist[11] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("deltaMET_rel_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_rel_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_rel_pt_den_"+sample+".png")
                
            if i==hist[12] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("altMET_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_altMET_pt_num_"+sample+".png")
        
            if i==hist[13] : 
                i.GetYaxis().SetTitle("Entries")
                i.GetXaxis().SetTitle("altMET_pt")
                c = ROOT.TCanvas('c', '', 600, 800)
                i.Draw()
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_altMET_pt_den_"+sample+".png")
        
            if i==hist[14] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("MET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/MET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_MET_pt_Muon_pt_num_"+sample+".png")
        
            if i==hist[15] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("MET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/MET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_MET_pt_Muon_pt_den_"+sample+".png")
        
            if i==hist[16] : 
                i.GetYaxis().SetTitle("AltMET_pt")
                i.GetXaxis().SetTitle("MET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/MET_Pt-AltMET_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_MET_pt_AltMET_pt_num_"+sample+".png")
        
            if i==hist[17] : 
                i.GetYaxis().SetTitle("AltMET_pt")
                i.GetXaxis().SetTitle("MET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/MET_Pt-AltMET_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_MET_pt_AltMET_pt_den_"+sample+".png")
        
            if i==hist[18] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("AltMET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_AltMET_pt_Muon_pt_num_"+sample+".png")
        
            if i==hist[19] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("AltMET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_AltMET_pt_Muon_pt_den_"+sample+".png")
        
            if i==hist[20] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("deltaMET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_pt_Muon_pt_num_"+sample+".png")
        
            if i==hist[21] : 
                i.GetYaxis().SetTitle("Muon_pt")
                i.GetXaxis().SetTitle("deltaMET_pt")
                c = ROOT.TCanvas('c', '', 800, 800)
                i.Draw("COLZ")
                ROOT.gPad.SetGrid()
                outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt-Muon_pt/")
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                c.SaveAs(outPath+trig+"_deltaMET_pt_Muon_pt_den_"+sample+".png")
	    c.Close()
    
    #efficiency plots
    mg_MET_pt.Add(heff_MET_pt)
    mg_MET_pt_leg.AddEntry(heff_MET_pt, trig ,"p")

    heff_MET_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
    heff_MET_pt.GetYaxis().SetTitle("Efficiency")
    heff_MET_pt.GetXaxis().SetTitle("MET_pt")
    heff_MET_pt.GetYaxis().SetTitleSize(0.05)
    heff_MET_pt.GetYaxis().SetTitleOffset(0.7)
    heff_MET_pt.GetYaxis().SetLabelSize(0.03)
    heff_MET_pt.GetXaxis().SetTitleSize(0.04)
    heff_MET_pt.GetXaxis().SetTitleOffset(0.8)
    heff_MET_pt.GetXaxis().SetLabelSize(0.04)
    heff_MET_pt.SetLineColor(getTrigColor(trig))
    heff_MET_pt.SetLineWidth(2)
    heff_MET_pt.SetMarkerSize(0.8)
    if 'Inclusive' in trig:heff_MET_pt.SetMarkerStyle(24)
    else:heff_MET_pt.SetMarkerStyle(20)
    heff_MET_pt.SetMarkerColor(getTrigColor(trig))
    leg_MET_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
    leg_MET_pt.AddEntry(heff_MET_pt, trig ,"p")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    heff_MET_pt.Draw("AP")
    leg_MET_pt.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/MET_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_MET_pt_"+trig+"_"+lepOpt+".png")
    c.Close()

    mg_MET_phi.Add(heff_MET_phi)
    mg_MET_phi_leg.AddEntry(heff_MET_phi, trig ,"p")

    heff_MET_phi.GetYaxis().SetRangeUser(0.3 , 1.1)
    heff_MET_phi.GetYaxis().SetTitle("Efficiency")
    heff_MET_phi.GetXaxis().SetTitle("MET_phi")
    heff_MET_phi.GetYaxis().SetTitleSize(0.05)
    heff_MET_phi.GetYaxis().SetTitleOffset(0.7)
    heff_MET_phi.GetYaxis().SetLabelSize(0.03)
    heff_MET_phi.GetXaxis().SetTitleSize(0.04)
    heff_MET_phi.GetXaxis().SetTitleOffset(0.8)
    heff_MET_phi.GetXaxis().SetLabelSize(0.04)
    heff_MET_phi.SetLineColor(getTrigColor(trig))
    heff_MET_phi.SetLineWidth(2)
    heff_MET_phi.SetMarkerSize(0.8)
    if 'Inclusive' in trig:heff_MET_phi.SetMarkerStyle(24)
    else:heff_MET_phi.SetMarkerStyle(20)
    heff_MET_phi.SetMarkerColor(getTrigColor(trig))
    leg_MET_phi = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
    leg_MET_phi.AddEntry(heff_MET_phi, trig ,"p")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    heff_MET_phi.Draw("AP")
    leg_MET_phi.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/MET_Phi/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_MET_phi_"+trig+"_"+lepOpt+".png")
    c.Close()
    
    mg_Muon_pt.Add(heff_Muon_pt)
    mg_Muon_pt_leg.AddEntry(heff_Muon_pt, trig ,"p")

    heff_Muon_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
    heff_Muon_pt.GetYaxis().SetTitle("Efficiency")
    heff_Muon_pt.GetXaxis().SetTitle("Muon_pt")
    heff_Muon_pt.GetYaxis().SetTitleSize(0.05)
    heff_Muon_pt.GetYaxis().SetTitleOffset(0.7)
    heff_Muon_pt.GetYaxis().SetLabelSize(0.03)
    heff_Muon_pt.GetXaxis().SetTitleSize(0.04)
    heff_Muon_pt.GetXaxis().SetTitleOffset(0.8)
    heff_Muon_pt.GetXaxis().SetLabelSize(0.04)
    heff_Muon_pt.SetLineColor(getTrigColor(trig))
    heff_Muon_pt.SetLineWidth(2)
    heff_Muon_pt.SetMarkerSize(0.8)
    if 'Inclusive' in trig:heff_Muon_pt.SetMarkerStyle(24)
    else:heff_Muon_pt.SetMarkerStyle(20)
    heff_Muon_pt.SetMarkerColor(getTrigColor(trig))
    leg_Muon_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
    leg_Muon_pt.AddEntry(heff_Muon_pt, trig ,"p")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    heff_Muon_pt.Draw("AP")
    leg_Muon_pt.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/Muon_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_Muon_pt_"+trig+"_"+lepOpt+".png")
    c.Close()
    
    mg_Electron_pt.Add(heff_Electron_pt)
    mg_Electron_pt_leg.AddEntry(heff_Electron_pt, trig ,"p")
    
    heff_Electron_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
    heff_Electron_pt.GetYaxis().SetTitle("Efficiency")
    heff_Electron_pt.GetXaxis().SetTitle("Electron_pt")
    heff_Electron_pt.GetYaxis().SetTitleSize(0.05)
    heff_Electron_pt.GetYaxis().SetTitleOffset(0.7)
    heff_Electron_pt.GetYaxis().SetLabelSize(0.03)
    heff_Electron_pt.GetXaxis().SetTitleSize(0.04)
    heff_Electron_pt.GetXaxis().SetTitleOffset(0.8)
    heff_Electron_pt.GetXaxis().SetLabelSize(0.04)
    heff_Electron_pt.SetLineColor(getTrigColor(trig))
    heff_Electron_pt.SetLineWidth(2)
    heff_Electron_pt.SetMarkerSize(0.8)
    if 'Inclusive' in trig:heff_Electron_pt.SetMarkerStyle(24)
    else:heff_Electron_pt.SetMarkerStyle(20)
    heff_Electron_pt.SetMarkerColor(getTrigColor(trig))
    leg_Electron_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
    leg_Electron_pt.AddEntry(heff_Electron_pt, trig ,"p")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    heff_Muon_pt.Draw("AP")
    leg_Muon_pt.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/Electron_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_Electron_pt_"+trig+"_"+lepOpt+".png")
    c.Close()
    
    
    if trigger == 'AltMETTriggers':
        mg_AltMET_pt.Add(heff_AltMET_pt)
        mg_AltMET_pt_leg.AddEntry(heff_AltMET_pt, trig ,"p")

        heff_AltMET_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
        heff_AltMET_pt.GetYaxis().SetTitle("Efficiency")
        heff_AltMET_pt.GetXaxis().SetTitle("AltMET_pt")
        heff_AltMET_pt.GetYaxis().SetTitleSize(0.05)
        heff_AltMET_pt.GetYaxis().SetTitleOffset(0.7)
        heff_AltMET_pt.GetYaxis().SetLabelSize(0.03)
        heff_AltMET_pt.GetXaxis().SetTitleSize(0.04)
        heff_AltMET_pt.GetXaxis().SetTitleOffset(0.8)
        heff_AltMET_pt.GetXaxis().SetLabelSize(0.04)
        heff_AltMET_pt.SetLineColor(getTrigColor(trig))
        heff_AltMET_pt.SetLineWidth(2)
        heff_AltMET_pt.SetMarkerSize(0.8)
        if 'Inclusive' in trig:heff_AltMET_pt.SetMarkerStyle(24)
        else:heff_AltMET_pt.SetMarkerStyle(20)
        heff_AltMET_pt.SetMarkerColor(getTrigColor(trig))
        leg_AltMET_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
        leg_AltMET_pt.AddEntry(heff_AltMET_pt, trig ,"p")
    
        c = ROOT.TCanvas('c', '', 600, 800)
        heff_AltMET_pt.Draw("AP")
        leg_AltMET_pt.Draw("same")
        ROOT.gPad.SetGrid()
        outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt/")
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        c.SaveAs(outPath+"TriggerEff_AltMET_pt_"+trig+"_"+lepOpt+".png")
        c.Close()
    
        mg_deltaMET_pt.Add(heff_deltaMET_pt)
        mg_deltaMET_pt_leg.AddEntry(heff_deltaMET_pt, trig ,"p")

        heff_deltaMET_pt.GetYaxis().SetRangeUser(0.0 , 0.3)
        heff_deltaMET_pt.GetYaxis().SetTitle("Efficiency")
        heff_deltaMET_pt.GetXaxis().SetTitle("deltaMET_pt")
        heff_deltaMET_pt.GetYaxis().SetTitleSize(0.05)
        heff_deltaMET_pt.GetYaxis().SetTitleOffset(0.7)
        heff_deltaMET_pt.GetYaxis().SetLabelSize(0.03)
        heff_deltaMET_pt.GetXaxis().SetTitleSize(0.04)
        heff_deltaMET_pt.GetXaxis().SetTitleOffset(0.8)
        heff_deltaMET_pt.GetXaxis().SetLabelSize(0.04)
        heff_deltaMET_pt.SetLineColor(getTrigColor(trig))
        heff_deltaMET_pt.SetLineWidth(2)
        heff_deltaMET_pt.SetMarkerSize(0.8)
        if 'Inclusive' in trig:heff_deltaMET_pt.SetMarkerStyle(24)
        else:heff_deltaMET_pt.SetMarkerStyle(20)
        heff_deltaMET_pt.SetMarkerColor(getTrigColor(trig))
        leg_deltaMET_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
        leg_deltaMET_pt.AddEntry(heff_deltaMET_pt, trig ,"p")
    
        c = ROOT.TCanvas('c', '', 600, 800)
        heff_deltaMET_pt.Draw("AP")
        leg_deltaMET_pt.Draw("same")
        ROOT.gPad.SetGrid()
        outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt/")
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        c.SaveAs(outPath+"TriggerEff_deltaMET_pt_"+trig+"_"+lepOpt+".png")
        c.Close()
	    
        mg_deltaMET_rel_pt.Add(heff_deltaMET_rel_pt)
        mg_deltaMET_rel_pt_leg.AddEntry(heff_deltaMET_rel_pt, trig ,"p")
	
        heff_deltaMET_rel_pt.GetYaxis().SetRangeUser(0.0 , 0.3)
        heff_deltaMET_rel_pt.GetYaxis().SetTitle("Efficiency")
        heff_deltaMET_rel_pt.GetXaxis().SetTitle("deltaMET_rel_pt")
        heff_deltaMET_rel_pt.GetYaxis().SetTitleSize(0.05)
        heff_deltaMET_rel_pt.GetYaxis().SetTitleOffset(0.7)
        heff_deltaMET_rel_pt.GetYaxis().SetLabelSize(0.03)
        heff_deltaMET_rel_pt.GetXaxis().SetTitleSize(0.04)
        heff_deltaMET_rel_pt.GetXaxis().SetTitleOffset(0.8)
        heff_deltaMET_rel_pt.GetXaxis().SetLabelSize(0.04)
        heff_deltaMET_rel_pt.SetLineColor(getTrigColor(trig))
        heff_deltaMET_rel_pt.SetLineWidth(2)
        heff_deltaMET_rel_pt.SetMarkerSize(0.8)
        if 'Inclusive' in trig:heff_deltaMET_rel_pt.SetMarkerStyle(24)
        else:heff_deltaMET_rel_pt.SetMarkerStyle(20)
        heff_deltaMET_rel_pt.SetMarkerColor(getTrigColor(trig))
        leg_deltaMET_rel_pt = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
        leg_deltaMET_rel_pt.AddEntry(heff_deltaMET_rel_pt, trig ,"p")
	    
        c = ROOT.TCanvas('c', '', 600, 800)
        heff_deltaMET_rel_pt.Draw("AP")
        leg_deltaMET_rel_pt.Draw("same")
        ROOT.gPad.SetGrid()
        outPath=(plotDir+sample+"_"+trigger+"/deltaMET_rel_Pt/")
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        c.SaveAs(outPath+"TriggerEff_deltaMET_rel_pt_"+trig+"_"+lepOpt+".png")
        c.Close()
    


mg_MET_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
mg_MET_pt.GetYaxis().SetTitle("Efficiency")
mg_MET_pt.GetXaxis().SetTitle("MET_pt")
mg_MET_pt.GetYaxis().SetTitleSize(0.05)
mg_MET_pt.GetYaxis().SetTitleOffset(0.7)
mg_MET_pt.GetYaxis().SetLabelSize(0.03)
mg_MET_pt.GetXaxis().SetTitleSize(0.04)
mg_MET_pt.GetXaxis().SetTitleOffset(0.8)
mg_MET_pt.GetXaxis().SetLabelSize(0.04)
c = ROOT.TCanvas('c', '', 600, 800)
mg_MET_pt.Draw("AP")
mg_MET_pt_leg.Draw("same")
ROOT.gPad.SetGrid()
outPath=(plotDir+sample+"_"+trigger+"/MET_Pt/")
if not os.path.exists(outPath):
    os.makedirs(outPath)
c.SaveAs(outPath+"TriggerEff_MET_pt_together_"+lepOpt+".png")
c.Close()

mg_MET_phi.GetYaxis().SetRangeUser(0.3 , 1.1)
mg_MET_phi.GetYaxis().SetTitle("Efficiency")
mg_MET_phi.GetXaxis().SetTitle("MET_phi")
mg_MET_phi.GetYaxis().SetTitleSize(0.05)
mg_MET_phi.GetYaxis().SetTitleOffset(0.7)
mg_MET_phi.GetYaxis().SetLabelSize(0.03)
mg_MET_phi.GetXaxis().SetTitleSize(0.04)
mg_MET_phi.GetXaxis().SetTitleOffset(0.8)
mg_MET_phi.GetXaxis().SetLabelSize(0.04)
c = ROOT.TCanvas('c', '', 600, 800)
mg_MET_phi.Draw("AP")
mg_MET_phi_leg.Draw("same")
ROOT.gPad.SetGrid()
outPath=(plotDir+sample+"_"+trigger+"/MET_Phi/")
if not os.path.exists(outPath):
    os.makedirs(outPath)
c.SaveAs(outPath+"TriggerEff_MET_phi_together_"+lepOpt+".png")
c.Close()

mg_Muon_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
mg_Muon_pt.GetYaxis().SetTitle("Efficiency")
mg_Muon_pt.GetXaxis().SetTitle("Muon_pt")
mg_Muon_pt.GetYaxis().SetTitleSize(0.05)
mg_Muon_pt.GetYaxis().SetTitleOffset(0.7)
mg_Muon_pt.GetYaxis().SetLabelSize(0.03)
mg_Muon_pt.GetXaxis().SetTitleSize(0.04)
mg_Muon_pt.GetXaxis().SetTitleOffset(0.8)
mg_Muon_pt.GetXaxis().SetLabelSize(0.04)
c = ROOT.TCanvas('c', '', 600, 800)
mg_Muon_pt.Draw("AP")
mg_Muon_pt_leg.Draw("same")
ROOT.gPad.SetGrid()
outPath=(plotDir+sample+"_"+trigger+"/Muon_Pt/")
if not os.path.exists(outPath):
    os.makedirs(outPath)
c.SaveAs(outPath+"TriggerEff_Muon_pt_together_"+lepOpt+".png")
c.Close()

mg_Electron_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
mg_Electron_pt.GetYaxis().SetTitle("Efficiency")
mg_Electron_pt.GetXaxis().SetTitle("Electron_pt")
mg_Electron_pt.GetYaxis().SetTitleSize(0.05)
mg_Electron_pt.GetYaxis().SetTitleOffset(0.7)
mg_Electron_pt.GetYaxis().SetLabelSize(0.03)
mg_Electron_pt.GetXaxis().SetTitleSize(0.04)
mg_Electron_pt.GetXaxis().SetTitleOffset(0.8)
mg_Electron_pt.GetXaxis().SetLabelSize(0.04)
c = ROOT.TCanvas('c', '', 600, 800)
mg_Electron_pt.Draw("AP")
mg_Electron_pt_leg.Draw("same")
ROOT.gPad.SetGrid()
outPath=(plotDir+sample+"_"+trigger+"/Electron_Pt/")
if not os.path.exists(outPath):
    os.makedirs(outPath)
c.SaveAs(outPath+"TriggerEff_Electron_pt_together_"+lepOpt+".png")
c.Close()

if trigger == 'AltMETTriggers':
    mg_AltMET_pt.GetYaxis().SetRangeUser(0.0 , 1.5)
    mg_AltMET_pt.GetYaxis().SetTitle("Efficiency")
    mg_AltMET_pt.GetXaxis().SetTitle("AltMET_pt")
    mg_AltMET_pt.GetYaxis().SetTitleSize(0.05)
    mg_AltMET_pt.GetYaxis().SetTitleOffset(0.7)
    mg_AltMET_pt.GetYaxis().SetLabelSize(0.03)
    mg_AltMET_pt.GetXaxis().SetTitleSize(0.04)
    mg_AltMET_pt.GetXaxis().SetTitleOffset(0.8)
    mg_AltMET_pt.GetXaxis().SetLabelSize(0.04)
    c = ROOT.TCanvas('c', '', 600, 800)
    mg_AltMET_pt.Draw("AP")
    mg_AltMET_pt_leg.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/AltMET_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_AltMET_pt_together_"+lepOpt+".png")
    c.Close()

    mg_deltaMET_pt.GetYaxis().SetRangeUser(0.0 , 0.3)
    mg_deltaMET_pt.GetYaxis().SetTitle("Efficiency")
    mg_deltaMET_pt.GetXaxis().SetTitle("deltaMET_pt")
    mg_deltaMET_pt.GetYaxis().SetTitleSize(0.05)
    mg_deltaMET_pt.GetYaxis().SetTitleOffset(0.7)
    mg_deltaMET_pt.GetYaxis().SetLabelSize(0.03)
    mg_deltaMET_pt.GetXaxis().SetTitleSize(0.04)
    mg_deltaMET_pt.GetXaxis().SetTitleOffset(0.8)
    mg_deltaMET_pt.GetXaxis().SetLabelSize(0.04)
    c = ROOT.TCanvas('c', '', 600, 800)
    mg_deltaMET_pt.Draw("AP")
    mg_deltaMET_pt_leg.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/deltaMET_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_deltaMET_pt_together_"+lepOpt+".png")
    c.Close()
	
    mg_deltaMET_rel_pt.GetYaxis().SetRangeUser(0.0 , 0.2)
    mg_deltaMET_rel_pt.GetYaxis().SetTitle("Efficiency")
    mg_deltaMET_rel_pt.GetXaxis().SetTitle("deltaMET_rel_pt")
    mg_deltaMET_rel_pt.GetYaxis().SetTitleSize(0.05)
    mg_deltaMET_rel_pt.GetYaxis().SetTitleOffset(0.7)
    mg_deltaMET_rel_pt.GetYaxis().SetLabelSize(0.03)
    mg_deltaMET_rel_pt.GetXaxis().SetTitleSize(0.04)
    mg_deltaMET_rel_pt.GetXaxis().SetTitleOffset(0.8)
    mg_deltaMET_rel_pt.GetXaxis().SetLabelSize(0.04)
    c = ROOT.TCanvas('c', '', 600, 800)
    mg_deltaMET_rel_pt.Draw("AP")
    mg_deltaMET_rel_pt_leg.Draw("same")
    ROOT.gPad.SetGrid()
    outPath=(plotDir+sample+"_"+trigger+"/deltaMET_rel_Pt/")
    if not os.path.exists(outPath):
        os.makedirs(outPath)
    c.SaveAs(outPath+"TriggerEff_deltaMET_rel_pt_together_"+lepOpt+".png")
    c.Close() 
    
