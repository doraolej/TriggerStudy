import ROOT
import numpy as np

class HistInfo( ):

    def __init__(self, hname = None, sample = None, texX = None, texY = None, binning = [], histclass = None, binopt = 'norm'):
        self.hname = hname
        self.sample = sample
        self.texX = texX
        self.texY = texY
        self.binning = binning
        self.histclass = histclass
        self.binopt = binopt
        self.binArr = np.array(binning, dtype='float64')
        
    def make_hist1D(self):
        if self.binopt == 'norm':
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, self.binning[0], self.binning[1], self.binning[2])
        else:
            nbins = len(self.binning) - 1
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, nbins, self.binArr)
        hist.Sumw2()
        return hist

    def make_hist2D(self):
        hist = self.histclass(self.hname+'_'+self.sample, self.hname, self.binning[0][0], self.binning[0][1], self.binning[0][2], self.binning[1][0], self.binning[1][1], self.binning[1][2])
        hist.Sumw2()
        return hist

    def make_hist(self):
        return self.make_hist1D() if self.histclass == ROOT.TH1F else self.make_hist2D()

    def getType(self):
        return self.histclass
        
