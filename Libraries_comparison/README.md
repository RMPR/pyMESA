# Comparison between libraries
## Motivation
There are mainly three great python libraries that allow to load and work with MESA output files. Thus, as all can load data from the data 
header name, a performance comparison between them can make grafics_mesa.py faster, which should be taken into account. 
 
## Results

The results of executing the different codes with the `time` command before gave the following results for the different tasks that can 
be performed by the code. All codes are thought to be used either for history or profile files independently and with the same exact syntax. 

### Show data header names
The computation time reading a history file of 3144 lines was:
- [mesaPlot](https://github.com/rjfarmer/mesaplot) 
  - real	0m2.222s; 0m2.215s
  - user	0m2.120s; 0m2.032s
  - sys	0m0.400s; 0m0.448s
- [mesa_reader](https://github.com/wmwolf/py_mesa_reader)
  - real	0m3.298s; 0m3.293s
  - user	0m3.236s; 0m3.228s
  - sys	0m0.060s; 0m0.060s
- [NuGridPy](https://github.com/NuGrid/NuGridPy) (`mesa` module)
  - real	0m0.960s; 0m0.953s
  - user	0m0.920s; 0m0.920s
  - sys	0m0.332s; 0m0.332s

### Save .eps figure (using Matplotlib)
Computation time calculated with the same history file plotting log_H and log_LH versus star_age, and using also the `-np` flag:
- mesaPlot
  - real	0m2.570s; 0m2.680s
  - user	0m2.356s; 0m2.360s
  - sys	0m0.484s; 0m0.532s
- mesa_reader
  - real	0m3.801s; 0m3.731s
  - user	0m3.676s; 0m3.584s
  - sys	0m0.108s; 0m0.136s
- NuGridPy
  - real	0m1.121s; 0m1.132s
  - user	0m1.116s; 0m1.076s
  - sys	0m0.300s; 0m0.348s

## Conclusion
It can be clearly seen that the fastest way to read mesa files is using NuGridPy. It does not mean that NuGridPy is automatically the 
best because the functionalities of every package are deifferent, and in general, not all 3 will provide the same exact funcionality 
as in this case, thus, other aspects must be taken into account when chosing which library to use.