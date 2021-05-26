import os, sys

sys.path.append('../')
from FileList_2016 import samples as samples_2016
from FileList_2017 import samples as samples_2017
from FileList_2018 import samples as samples_2018
from SampleChain import SampleChain

def get_parser():
    ''' Argument parser.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--sample',           action='store',                     type=str,            default='SingleElectron_Data2018',                                help="Which sample?" )
    argParser.add_argument('--year',             action='store',                     type=int,            default=2018,                                             help="Which year?" )
    argParser.add_argument('--channel',          action='store',                     type=str,            default='SingleElectron',                                   help="Which dataset?" )
    argParser.add_argument('--filesperjob',      action='store',                     type=int,            default=1,                                               help="No of files to run per condor job" )
    argParser.add_argument('--prxy',             action='store',                     type=str,            default='x509up_u133446',                                help="grid proxy file" )
    argParser.add_argument('--prxyPath',         action='store',                     type=str,            default='/afs/cern.ch/user/d/dolej/',                  help="grid proxy file" )
    
    return argParser

options = get_parser().parse_args()
sample  = options.sample
channel = options.channel
fpj = options.filesperjob
year = options.year
proxy = options.prxy
ppath = options.prxyPath

if year==2016:
    samplelist = samples_2016
    DataLumi = SampleChain.luminosity_2016
elif year==2017:
    samplelist = samples_2017
    DataLumi = SampleChain.luminosity_2017
else:
    samplelist = samples_2018
    DataLumi = SampleChain.luminosity_2018

flist = 'File'+sample+'.txt'
if not os.path.islink(flist):
    os.system('ln -s ../%s %s'%(flist, flist))

tfiles = len(SampleChain.getfilelist(samplelist[sample]))
cq = (tfiles/fpj) + 1 if tfiles%fpj else tfiles/fpj

print 'sample: ', sample
print 'tot files: ',tfiles
print 'no fo files per job: ', fpj
if fpj>2: print 'consider putting no of files per job 1 or 2'
print 'total noo of jobs: ',cq


bashline = []
bashline.append("#!/bin/bash\n")
bashline.append("\n")
bashline.append("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
bashline.append("export X509_USER_PROXY=$1\n")
bashline.append("voms-proxy-info -all\n")
bashline.append("voms-proxy-info -all -file $1\n")
bashline.append("\n")
bashline.append("tar -zxvf CMSSW_10_2_22.tar.gz\n")
bashline.append("cd CMSSW_10_2_22/src/\n")
bashline.append("scram b ProjectRename\n")
bashline.append("eval `scramv1 runtime -sh`\n")
bashline.append("scram b\n")
bashline.append("\n")
bashline.append("job=$3\n")
bashline.append("startfile=$((job*%i))\n"%fpj)
bashline.append("\n")
bashline.append("cd CMSSWTriggerRun\n")
bashline.append("python TrigHistMaker.py --sample %s --year %s --channel %s --startfile $startfile --nfiles %i --jtype condor\n"%(sample, year, channel, fpj))
bashline.append("\n")
bashline.append("cp *.root /eos/user/d/dolej/")
bashline.append("\n")
bashline.append("cd ../../../")
fsh = open("TriggerCondor.sh", "w")
fsh.write(''.join(bashline))
fsh.close()


outputf = 'TrigHist_'+sample
subline = []
subline.append('executable              = TriggerCondor.sh\n')
subline.append('Universe                = vanilla\n')
subline.append('+JobFlavour             = "tomorrow"\n')
subline.append('output                  = TriggerCondor.$(ClusterId).$(ProcId).out\n')
subline.append('error                   = TriggerCondor.$(ClusterId).$(ProcId).err\n')
subline.append('log                     = TriggerCondor.$(ClusterId).$(ProcId).log\n')
subline.append('getenv                  = True\n')
subline.append('should_transfer_files   = YES\n')
subline.append('when_to_transfer_output = ON_EXIT\n')
subline.append('transfer_output_files   = ""')
subline.append('\n\n')
subline.append('Proxy_filename = %s\n'%proxy)
subline.append('Proxy_path = %s$(Proxy_filename)\n'%ppath)
subline.append('Transfer_Input_Files    = $(Proxy_path), TriggerCondor.sh, CMSSW_10_2_22.tar.gz\n')
subline.append('arguments               = $(Proxy_path) $(ClusterId) $(ProcId)\n')
subline.append('queue %i\n'%cq)

fs = open("TriggerCondor.sub", "w")
fs.write(''.join(subline))
fs.close()
os.system('condor_submit TriggerCondor.sub')
