# This is to run trigger script in lxplus account

Log in to your lxplus account

Set up CMSSW area

```
cmsrel CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv
```
Checkout scipt from github

```
git clone git@github.com:1LStopBudapest/CMSSWTriggerRun.git
git clone git@github.com:1LStopBudapest/Helper.git
```
The trigger scripts are inside CMSSWTriggerRun directory. One can check. 

Now to submit the condor jobs which runs over the nanoAOD data samples

Make CMSSW tar file

```
cd ../..
tar -zcvf CMSSW_10_2_22.tar.gz CMSSW_10_2_22
mv CMSSW_10_2_22.tar.gz CMSSW_10_2_22/src/CMSSWTriggerRun/condor/
cd CMSSWTriggerRun/condor/
```
Set up proxy

```
voms-proxy-init --voms cms
```
It will create a proxy file in /tmp directory with format something like this x5..

please copy that file in your home directory
```
cp /tmp/ProxyFile ~/
```

Now Submit condor jobs
```
python condorScript.py --prxy ProxyFile
```
