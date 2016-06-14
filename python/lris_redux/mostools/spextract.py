"""
Extracts a spectrum from 2d mask and variance images.
"""

import scipy,os
from astropy.io import fits as pyfits
from mostools import spectools
import special_functions as sf
from scipy import signal

def extract(outname,root,slit,pos,width=1.):
	"""
	extract(outname,root,slit,pos,width=1.)

	Extracts a spectrum from 2d mask and variance images.

	Inputs:
	  outname - name of output FITS file
	  root    - root name of input data (ie ROOTNAME_bgsub.fits)
	  slit    - number of slit to extract from (1 = bottom slit)
	  pos     - position along slit to extract
	  width   - gaussian-sigma width to extract

	Outputs:
	  FITS file containing extracted spectrum.
	"""
	infile = root+"_bgsub.fits"
	spectools.cutout(infile,outname,slit)
	wave = spectools.wavelength(outname)
	data = pyfits.open(outname)[0].data.astype(scipy.float32)
	os.remove(outname)
	infile = root+"_var.fits"
	spectools.cutout(infile,outname,slit)
	varimg = pyfits.open(outname)[0].data.astype(scipy.float32)
	os.remove(outname)

	yvals = scipy.arange(data.shape[0]).astype(scipy.float32)

	fit = scipy.array([0.,1.,pos,width])
	weight = sf.ngauss(yvals,fit)
	weight[abs(yvals-pos)/width>1.5] = 0.
	weight /= weight.sum()

	spec = weight*data.T
	spec = spec.sum(axis=1)
	varspec = weight*varimg.T
	varspec = varspec.sum(axis=1)
	spec[varspec==0] = 0.
	smooth = signal.wiener(spec,7,varspec)
	smooth[scipy.isnan(smooth)] = 0.

	hdu = pyfits.PrimaryHDU()
	hdu.header.update('CENTER',pos)
	hdu.header.update('WIDTH',width)
	hdulist = pyfits.HDUList([hdu])

	crval = wave[0]
	scale = wave[1]-wave[0]
	for i in [spec,smooth,varspec]:
		thdu = pyfits.ImageHDU(i)
		thdu.header.update('CRVAL1',crval)
		thdu.header.update('CD1_1',scale)
		thdu.header.update('CRPIX1',1)
		thdu.header.update('CRVAL2',1)
		thdu.header.update('CD2_2',1)
		thdu.header.update('CRPIX2',1)
		thdu.header.update('CTYPE1','LINEAR')
		hdulist.append(thdu)

	hdulist.writeto(outname)
