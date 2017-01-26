# CERN@school: Investigating the Inverse Square Law
This repository contains the code required for performing
the analysis described in the CERN@school inverse square law experiment,
as decribed by the _Physics Education_ paper here:

http://dx.doi.org/10.1088/0031-9120/48/3/344

In this paper, a CERN@school Timepix detector is used to count the
photons emitted by an Americium-241 source at various distances.
This is an ideal demonstration experiment for schools with both
a detector and an Am-241 source - and the code here may be used
to analyse any data collected in doing so - but in case neither
of those is available we have provided the data used in the paper
so that the analysis may be repeated and discussed.


## Disclaimers
* _This code dates from 2014. While every attempt has been
made to ensure that it is usable, some work may be required to get it
running on your own particular system.
We recommend using a GridPP CernVM; please refer to
[this guide](http://doi.org/10.6084/m9.figshare.4552825.v1)
for further instructions.
Unfortunately CERN@school cannot guarantee further support for this code.
Please proceed at your own risk_.
* _This repository is now deprecated, and remains here for legacy purposes.
For future work regarding CERN@school, please refer to the
[Institute for Research in Schools](http://researchinschools.org) (IRIS)
[GitHub repository](https://github.com/InstituteForResearchInSchools).
Please also feel free to fork and modify this code as required for
your own research._


## Getting the code
You can clone the repository to your local machine with the following
command:

```bash
$ git clone https://github.com/CERNatschool/inverse-square-law.git
$ cd inverse-square-law
```


## Getting the data
We have put the data used in 
([Whyntie et al., 2013](http://dx.doi.org/10.1088/0031-9120/48/3/344))
on [FigShare](http://figshare.com) so that you can recreate the analysis
yourself, and test the code before using it with your own data.
To obtain the data from the
[Figshare repository](https://dx.doi.org/10.6084/m9.figshare.949631.v1),
use the following commands on your CernVM:

```bash
$ wget http://files.figshare.com/1404724/CERNatschool_C08_W0082_121129_inv_square_law.zip
$ unzip CERNatschool_C08_W0082_121129_inv_square_law.zip
```

This will create the `data` directory in your working area, which is what
the `analysis.py` script runs over to produce the analysis results.


## Running the code

To run the example code from a CernVM, type the following commands
from the directory you cloned the repository into:

```bash
$ . setup.sh
$ python analysis.py
```

_Note: if you are not using a GridPP CernVM, the `setup.sh` script
will not work as you won't have access to the CERN@school CVMFS
repository and will have to source your own version of
`matplotlib` via e.g. the
[Anaconda Python distribution](http://anaconda.org)._


## Viewing the plot
The plot is created as `r_vs_oosqrtNg.png`, which can be viewed in
any image viewing software. We'll use Eye of Gnome, `eog`, which can
be installed on the GridPP CernVM with:

```bash
$ sudo yum install eog
[... installation output ...]
```

To view the plot, you can then type:

```bash
eog r_vs_oosqrtNg.png &
```

This is Figure 5 in
([Whyntie et al., 2013](http://dx.doi.org/10.1088/0031-9120/48/3/344)).


## Note for advanced users
Some of the advanced analysis functionality requires
CERN's ROOT software framework to be installed on your system.
This has been commented out in `analysis.py`, but you can
use `analysis_with_ROOT.py` if you're running a GridPP CernVM
(or have otherwise installed ROOT in your system with Python
integration):

```bash
$ source setup.sh
$ python analysis_with_ROOT.py
```


## Acknowledgements
_CERN@school was supported by
the UK [Science and Technology Facilities Council](http://www.stfc.ac.uk) (STFC)
via grant numbers ST/J000256/1 and ST/N00101X/1,
as well as a Special Award from the Royal Commission for the Exhibition of 1851.
The CERN@school Collaboration would also like to acknowledge the support
provided by the [GridPP Collaboration](http://www.gridpp.ac.uk)
in terms of both computing resources and technical guidance from
collaboration members._


## Useful links
* [Whyntie et al., 2013](http://dx.doi.org/10.1088/0031-9120/48/3/344) - the original paper in Physics Education;
* The [Am-241 dataset](https://dx.doi.org/10.6084/m9.figshare.949631.v1) on FigShare - as used in ([Whyntie et al., 2013](http://dx.doi.org/10.1088/0031-9120/48/3/344));
* [Setting up a GridPP CernVM](http://doi.org/10.6084/m9.figshare.4552825.v1);
* The [Institute for Research in Schools](http://researchinschools.org) (IRIS) homepage;
* The [IRIS CERN@school website](http://researchinschools.org/CERN);
* The [Official IRIS GitHub Organization](https://github.com/InstituteForResearchInSchools).
