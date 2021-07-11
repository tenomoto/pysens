pysens: Python scripts for ensemble singular vector sensitivity analysis

pysens contains Python scripts to conduct
ensemble singular vector sensitivity analysis (EnSVSA) using ensemble forecast. 
The singular values and vectors for a specified verification region
are computed using numpy.linalg.eig().
The eigen solver is chosen over singular vector solver
assuming that the number of state variables is
larger than the ensemble size giving a smaller covariance matrix.
In addition to the Python scripts, a samle configuration file and
a shell script to generate perturbations are provided.

# References

We appreciate if you cite the following papers in your publication.

* [Enomoto et al. 2015](https://doi.org/10.2151/jmsj.2015-011)
* [Nakashita and Enomoto 2021](https://doi.org/10.2151/sola.17A-006)

# Requirements

* [cdo](https://code.mpimet.mpg.de/projects/cdo/)
* [ecCodes](https://confluence.ecmwf.int/display/ECC)
* [numpy](https://numpy.org/)
* [xarray](http://xarray.pydata.org)

# Files

* pert.sh: split GRIB files and calculate perturbations
* sens.py: conduct EnSVSA
* regress.py: conduct regression

# Usage

1. Download ensemble forecast, e.g. from the ECMWF TIGGE database.
2. Create directories grib, pert, sv, mode with a subdirectory with initial time (yyyymmddhh).
3. Run pert.sh to generate perturbations in NetCDF.
4. Edit config.py to set experimental settinga such as the verification region.
5. Run sens.py to conduct eigenanalysis.
6. Run regress.py to conduct regression.
