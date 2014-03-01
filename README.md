inverse-square-law
==================

The code and data required for the CERN@school inverse square law experiment.

##Getting the data

To obtain the data from the Figshare repository, use the following commands:

```bash
wget http://files.figshare.com/1404724/CERNatschool_C08_W0082_121129_inv_square_law.zip
unzip CERNatschool_C08_W0082_121129_inv_square_law.zip
```

This will create the `data` directory in your working area, which is what
the `analysis.py` script runs over to produce the analysis results.

##Running the code

Once you have the data, the code should run out of the box.

```bash
python analysis.py
```

##Viewing the plot

The plot is created in `r_vs_oosqrtNg.png`, which can be viewed in
any image viewing software.

```bash
ristretto r_vs_oosqrtNg.png &
```

## Further information

* [The paper in Physics Education](http://dx.doi.org/10.1088/0031-9120/48/3/344);
* [CERN@school homepage](http://cernatschool.web.cern.ch);
* [The Langton Star Centre](http://www.thelangtonstarcentre.org).
