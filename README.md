# netcdf-specification-v1.3
I/Ocean NetCDF convention for delayed mode underway data from research vessels

## I/Ocean NetCDF principle
The NetCDF consists of a root group that contains the routine underway data and information relevant to them. The file is supplimented by deployments, instruments, calibrations and installations (instrument locations) NetCDF groups. Each group contains sub-groups that represent an instance. For example, an instance of an instrument or calibration that is relevant to the data. Each each is governed by valid dates. The image below summaries the principle of instances to the data.

Click on the image to enlarge.

![NetCDF-workflow](images/NetCDF_workflow.png)

## Full NetCDF specification
The following examples contain information for implementing an enriched NetCDF specification:

* [example NetCDF file](iocean_example_v1_3.nc):
* [example NetCDF CDL file](iocean_example_cdl_v1_3):
* [Python code](ioceanPythonCode_v1_3.py):
* [NetCDF data variable names and attribute values](NetcdfVariableIDsAndAttributes-V1-3.xlsx):

## Minimal NetCDF specification
Users are able to implement a less enriched version of the NetCDF files. The following examples can be used for producing a minimal specification:

* [Minimal NetCDF specification and python code](NetcdfMinimalSpecification-V1-3.xlsx):
* [NetCDF data variable names and attribute values](NetcdfVariableIDsAndAttributes-V1-3.xlsx):



