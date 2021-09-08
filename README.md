# pyMCSRT
Python Monte Carlo Simulation Read Tool

## Content
pyMCSRT contains reading modules: one for reading the MCNP mesh tally out format, the other one for reading the PHITS output tally format.

## How to use
To use these scripts, please add the main directory of this module to your system path before importing:

```
import sys
sys.path.append('PATH/TO/MODULE')
from pyMCSRT import read_mcnp_mesh as rmm 
```