#!/usr/bin/env python
# -*- coding: utf-8 -*-

#========================================================
# Analysis of the Inverse Square Law data (ROOT version)
#========================================================
#
# See the README.md for more information.

# Import the code needed to manage files and sort the data.
import os, inspect, glob
from operator import itemgetter

# Import the plotting libraries.
import pylab as plt
import numpy as n
from matplotlib import rc

# Set the default tick label distance.
plt.rcParams['xtick.major.pad']='8'
plt.rcParams['ytick.major.pad']='8'

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

# Import the clustering and web-page writing code.
from clustering import *

# Uncomment these if you have ROOT installed on your system.
from ROOT import TGraphErrors
from ROOT import TF1

# The class for handling data entries.
class Entry:
    def __init__(self, r, dots, blobs, time):
        self.r          = r       # [mm]
        self.Ndots      = dots
        self.Nblobs     = blobs
        self.Dtime      = time    # [s]
    def Nphot(self):
        N = float(self.Ndots + self.Nblobs) / self.Dtime
        return N
    def NphotErr(self):
        N = float(self.Ndots + self.Nblobs)
        errN = n.sqrt(N)
        return errN / self.Dtime

# Get the path of the current directory
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#=============================================================================
# The main program.
#=============================================================================
if __name__=="__main__":

    print("===============================================")
    print("    CERN@school Inverse Square Law Analysis    ")
    print("===============================================")
    print("*")

    # Create the dictionary for the data entries.
    data = {}

    # A JSON format data structure for our data files.
    datafiles = [
        {"r": 40.0, "path":"data/C08-W0082/2012/11/29/145250/", "t":66.8},
        {"r": 50.0, "path":"data/C08-W0082/2012/11/29/141114/", "t":67.0},
        {"r": 60.0, "path":"data/C08-W0082/2012/11/29/141512/", "t":67.0},
        {"r": 70.0, "path":"data/C08-W0082/2012/11/29/141907/", "t":66.3},
        {"r": 80.0, "path":"data/C08-W0082/2012/11/29/142422/", "t":66.4},
        {"r": 90.0, "path":"data/C08-W0082/2012/11/29/142731/", "t":66.3},
        {"r":100.0, "path":"data/C08-W0082/2012/11/29/143259/", "t":66.6},
        {"r":110.0, "path":"data/C08-W0082/2012/11/29/143547/", "t":66.7},
        {"r":120.0, "path":"data/C08-W0082/2012/11/29/143810/", "t":66.3},
        {"r":130.0, "path":"data/C08-W0082/2012/11/29/144048/", "t":66.5},
        {"r":140.0, "path":"data/C08-W0082/2012/11/29/144315/", "t":66.6},
        {"r":150.0, "path":"data/C08-W0082/2012/11/29/144544/", "t":66.5},
        ]

    print("* |-------------------------------------------|")
    print("* | r/mm  |  Dots  | Blobs  | Others |  Dt/s  |")
    print("* |-------------------------------------------|")

    # Loop over the datasets sorted by radius.
    for dataset in sorted(datafiles, key=itemgetter('r')):
        #print("* Current dataset is '%s'" % (dataset['path']))
        #print("* r = %5.1f [mm]." % (dataset['r']))

        n_1 = 0; n_2 = 0; n_3 = 0; n_4 = 0
        n_else  = 0

        # Loop over the datafiles and read the data.
        for datafilename in glob.glob(dataset['path'] + "/*.txt"):

            #print("*--> Data file is '%s'" % (datafilename))

            # Open the file and read in the data.
            f = open(datafilename, 'r')
            payload = f.read()
            f.close()

            # Create a "dictionary" for the pixel information.
            pixels = {}

            # Loop over the X Y C values in the file and add them to the
            # pixel dictionary.
            for datarow in payload.splitlines():
                #print dataline
                v = datarow.split('\t') # Separates the x y C values
                x = int(v[0]); y = int(v[1]); C = int(v[2])
                X = 256 * y + x
                pixels[X] = C

            # Create a "BlobFinder" to cluster the pixels we've just extracted.
            # See clustering.py for more about how this is done.
            blob_finder = BlobFinder(pixels, 256, 256)

            # Loop over the blobs found in the blob finder and record their
            # properties for plotting.
            for b in blob_finder.blob_list:
                if   b.get_size() == 1:
                    n_1  += 1
                elif b.get_size() == 2:
                    n_2  += 1
                elif b.get_size() == 3:
                    #print("*----> n_3, r = %f" % b.r_u)
                    if b.r_u < 0.75:
                        n_3  += 1
                elif b.get_size() == 4:
                    #print("*----> n_4, r = %f" % b.r_u)
                    if b.r_u < 0.71:
                        n_4  += 1
                else:
                    n_else += 1

        # Update the user.
        #print("* Number of dots   = %6d" % (n_1 + n_2))
        #print("* Number of blobs  = %6d" % (n_3 + n_4))
        #print("* Number of others = %6d" % (n_else)   )
        n_d = n_1 + n_2; n_b = n_3 + n_4
        print("* | %5.1f | %6d | %6d | %6d |   %4.1f |" % \
            (dataset['r'],n_d,n_b,n_else,dataset['t']))

        # Populate the data.
        data[dataset['r']] = Entry(dataset['r'],n_1+n_2,n_3+n_4,dataset['t'])

    print("* |-------------------------------------------|")
    print("*")

    #-------------------------------------------------------------------------
    # Analysing the data
    #-------------------------------------------------------------------------
    #
    # Create the arrays for the data analysis and plots.
    ra   = n.array([]) # The distance values [mm].
    er   = n.array([]) # The error on the distance [mm].
    Ng   = n.array([]) # The number of photons/s [s^{-1}].
    eNg  = n.array([]) # The error on the number of photons/s [s^{-1}]
    oosqrtNg  = n.array([]) # One Over the square root of N_g.
    eoosqrtNg = n.array([]) # The error on 1/sqrt(N_g).

    # Populate the arrays with the data.
    for r, e in sorted(data.iteritems()):

        # Add the distance to the array.
        ra        = n.append(ra, r)

        # The error on the distance. We measured to the nearest millimeter.
        er        = n.append(er, 1.)

        # Calculate the number of photons/s using the Entry class method.
        Ng        = n.append(Ng,  e.Nphot())

        # Get the error using the Entry class method.
        eNg       = n.append(eNg, e.NphotErr())

        # Calculate 1/sqrt(N_g) and the error.
        oosqrtNg  = n.append(oosqrtNg,  1./n.sqrt(e.Nphot()))
        eoosqrtNg = n.append(eoosqrtNg, \
          0.5 * (1./n.sqrt(e.Nphot())) * ((e.NphotErr())/(e.Nphot())))


    # Here we use the ROOT software suite to calculate the line of best fit.
    # If you have ROOT installed, uncomment this section to produce the
    # m and c variables yourself.
    #
    datagraph = TGraphErrors(len(ra), ra, oosqrtNg, er, eoosqrtNg)
    #
    fitB = TF1("fitB", "[0] * x + [1]", 39., 151.)
    fitB.SetParameter(0, 100.)
    fitB.SetParameter(1,   0.)
    datagraph.Fit("fitB", "R")
    #
    m = fitB.GetParameter(0)
    c = fitB.GetParameter(1)
    #
    datagraph.Draw("A*")

    # If you're not using the ROOT functionality, we have provided the hard-coded
    # values. Comment these out if you're using the code above.
    #m =  0.002398
    #c = -0.003646

    print("*")
    print("*------------------------")
    print("* Fit parameters: mx + c ")
    print("*------------------------")
    print("* m = % 8.6f" % (m))
    print("* c = % 8.6f" % (c))
    print("*------------------------")
    print("*")

    #-------------------------------------------------------------------------

    # Now we've made read in the data and recorded the cluster properties,
    # we can make the plot.

    # Fig. 1: r vs. sqrt(N_phot/s)
    #-------------------------------------------------------------------------
    # Create the plot.
    rvsplot = plt.figure(101, figsize=(5.0, 5.0), \
                              dpi=150, \
                              facecolor='w', \
                              edgecolor='w')
    #
    rvsplot.subplots_adjust(bottom=0.15, left=0.15)
    rvsplotax = rvsplot.add_subplot(111)

    # y axis
    plt.ylabel('$1 / \\sqrt{N_{\\gamma}}$ / s$\,^{1/2}$')

    # x axis
    plt.xlabel('$r$ / mm')

    # Add a grid.
    plt.grid(1)
    #

    # Plot the data with error bars.
    plt.errorbar(ra, oosqrtNg, yerr=eoosqrtNg, xerr=er, \
                 fmt='', \
                 lw=0, \
                 color='black', \
                 ecolor='black', \
                 capthick=0, \
                 elinewidth=1, \
                 label='data')

    # Create and plot the line of best fit.
    x = n.arange(0.,160.,0.1)
    y = m*x + c
    plt.plot(x,y,'r-',label='line of best fit')

    # Set the axis limits.
    rvsplotax.set_xlim([0,160])
    rvsplotax.set_ylim([0,0.4])

    # Now add the legend with some customizations.
    legend = rvsplotax.legend(loc='upper left', shadow=False, numpoints=1)

    # Set the fontsize of the legend.
    for label in legend.get_texts():
        label.set_fontsize(12)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('w')
    frame.set_linewidth(0.5)

    # Save the figure.
    rvsplot.savefig("r_vs_oosqrtNg.png")

    print("*")
    print("* Analysis complete!")
    print("*")
