import os, sys
import ROOT
import types

import FileList_2016
import FileList_2017
import FileList_2018

class SampleChain():
    luminosity_2016           = 35922.0
    luminosity_2017           = 41856.0
    luminosity_2018           = 58905.0


    def __init__(self, sample, startfile, filestorun, year=2016, treename = "Events"):
        self.sample = sample
        self.startfile = startfile
        self.filestorun = filestorun
        self.treename = treename
        if year==2016:
            self.samplelist = FileList_2016.samples 
        elif year==2017:
            self.samplelist = FileList_2017.samples 
        else:
            self.samplelist = FileList_2018.samples

        self.gredir = 'root://cms-xrd-global.cern.ch//'

    def getchain(self):
        ch = ROOT.TChain(self.treename)
        filelist = []
        if isinstance(self.samplelist[self.sample], types.ListType):
            for s in self.samplelist[self.sample]:
                    filelist.extend(self.getfilelist(s))
        else:
            filelist = self.getfilelist(self.samplelist[self.sample])
        self.addtochain(ch, filelist, self.startfile, self.filestorun)
        return ch
    
    @staticmethod
    def getfilelist(txtfile):
        files = []
        with open(txtfile,'r') as ifile:
            for line in ifile:
                line = line.rstrip()
                files.append(line)
        return files

    def addtochain(self, ch, filelist, startfile, filestorun):
        files = len(filelist)-startfile if filestorun == -1 else filestorun 
        for i in range(len(filelist)):
            if i < startfile or i > (startfile+files)-1: continue
            ch.Add(self.gredir+filelist[i])

    def getEntries(self, ch):
        return ch.GetEntries()
