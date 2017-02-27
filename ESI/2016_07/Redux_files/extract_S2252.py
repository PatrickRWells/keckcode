from extract_generic import extract

method = 'cdf'
#method = 'oldham'
stdOrderCorr = 'orderCorr_Feige110.dat'
fullname = 'S2252+1349'
name='S2252'
frames = [45]
apcent = [0.]
aplab = ['test']
nsig = 1. # Width of aperture in terms of sigma.  Normal value is 1.0
apmin = -1.*nsig
apmax = nsig
#frames = [45,46]
#apcent = [-0.45,0.45]
#aplab = ['A','B']
#nsig = 0.6 # Width of aperture in terms of sigma.  Normal value is 1.0

for i in range(len(aplab)):
    extract(fullname,name,frames,i,apcent,aplab,stdOrderCorr,wid=nsig,
            method=method,apmin=apmin,apmax=apmax)