
"""
#######################
# Setting Environment
#######################
"""
"""
You need to install following modules:
netCDF4
pandas
matplotlib
"""
#help('modules');

import netCDF4 as nc
import numpy as np
import datetime
from datetime import datetime, timezone
import pandas as pd

"""
#######################
# Description
#######################
"""
"""
IOcean-1.3
The I/Ocean NetCDF format is based on NetCDF4. The NetCDF consists of a root group that contains the routine underway data and information relevant 
to them. The file is supplimented by platforms, deployments, instruments, calibrations and installations (instrument locations) NetCDF groups. Each 
group contains sub-groups that represent an instance. For example, an instance of an instrument or calibration that is relevant to the data. Each 
is governed by valid dates. For more information see: https://github.com/I-Ocean/netcdf-specification.

Daily files should be created at 1 second or Hz and 1 min resolutions

All dates and times are ISO 8601. Ideally they should be UTC. 

Common metadata are described in https://github.com/I-Ocean/common-metadata.

"""

"""
#########################
ROOTGROUP - [Mandatory]
#########################

DESCRIPTION: Central group that contains attributes relevant to the whole file. It also contains the data variables.
"""


"""
Create/open file
"""
rootgrp = nc.Dataset('iocean_example.nc','w',format='NETCDF4')  # overwrite

"""
Global attributes
DESCRIPTION: 
https://github.com/I-Ocean/common-metadata/blob/master/globalProperties.md
"""
rootgrp.deployment_id = '/deployments/DY122' # [Mandatory]
rootgrp.title = 'I/Ocean trajectory file Climate Forecast 1.8' # [Mandatory]
rootgrp.Conventions = 'CF-1.8 SeaDataNet-1.0 ACDD-1.3 IOcean-1.0' # [Mandatory]
rootgrp.source = 'Underway observations from RRS Discovery navigation, meteorology and sea surface hydrography sensor arrays' # [Mandatory]
rootgrp.history =  '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': (NMF) File created' # [Recommended] 
rootgrp.date_created = datetime(2020, 1, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Mandatory]
rootgrp.date_update = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z') # [Mandatory]
rootgrp.processing_level = 'Raw instrument data' # [Mandatory] 
rootgrp.standard_name_vocabulary = 'http://vocab.nerc.ac.uk/collection/P07/current/' # [Recommended]
rootgrp.sdn_vocabulary = 'http://vocab.nerc.ac.uk/' # [Recommended]
rootgrp.featureType = 'trajectory' # [Mandatory] 
rootgrp.data_interval = '1Hz' # [Mandatory] 
rootgrp.comment = '\n'+datetime(2020, 1, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')+': XXXXX' # [Optional]

"""
Dimensions
"""
rootgrp.createDimension('INSTANCE',None)  # this allows more than one trajectory (e.g. with a second timestamp) in the file
rootgrp.createDimension('MAXT',6)  # [Mandatory] May be set to 'unlimited' 
rootgrp.createDimension('STRING80',80) # [Mandatory] 

"""
Pass variable data
"""
TRAJECTORYID = nc.stringtochar(np.array(['DY122_UWAY1'], 'S80'))
CRS = 0  # grid mapping coordinate always = 0
TIME = np.array([1615900594, 1615900595, 1615900596, 1615900597, 1615900598, 1615900599],'f8')
TIME_QC = np.array([49, 49, 49, 49, 49, 49], 'i1')
LAT = np.array([-51.71759033, -51.71879196, -51.72002792, -54.596138  , -54.59526443, -54.59444046],'f8')
LON = np.array([-57.65376663, -57.65382767, -57.65382385, -58.36009979, -58.36487961, -58.3693428 ],'f8')
POS_QC = np.array([49, 49, 49, 49, 49, 49], 'i1')
DEPTH = np.array([0,0,0,0,0,0],'f4')
DEPTH_QC = np.array([49, 49, 49, 49, 49, 49], 'i1')
SST = np.array([7.4809, 7.4390, -9, 7.4030, 7.3647, 7.3497],'f4') # note 3rd element = -9 (fill value)
SST_QC = np.array([49, 49, 57, 49, 49, 49], 'i1') # note 3rd element of ancilliary data to SST = 57 (fill value)


"""
Coordinate Reference Systems
DESCRIPTION: 
https://github.com/I-Ocean/common-metadata/blob/master/featureTypes.md
https://github.com/I-Ocean/common-metadata/blob/master/gridMapping.md
"""
# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
Traj = rootgrp.createVariable('trajectory','S1',('INSTANCE','STRING80')) # ID needed per instance that is needed to be CF compliant. This can't be deployment as there may be more than one time stamp (instance) per deployment
Traj.long_name = 'Trajectory identifier'
Traj.cf_role = "trajectory_id" 
Traj[:] = TRAJECTORYID

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
Crs = rootgrp.createVariable('crs','i4')
Crs.grid_mapping_name = 'latitude_longitude' 
Crs.epsg_code = 'EPSG:4326' 
Crs.semi_major_axis = 6378137. 
Crs.inverse_flattening = 298.257223563 
Crs[:] = CRS



"""
Coordinate variables
DESCRIPTION: 
https://github.com/I-Ocean/common-metadata/blob/master/coordinateVariables.md
"""

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise]  
time = rootgrp.createVariable('TIME', 'f8', ('INSTANCE', 'MAXT'), fill_value=-1)
time.long_name = 'Time'
time.standard_name = 'time'
time.units = 'seconds since 1970-01-01T00:00:00Z'
time.calendar = 'standard'
time.valid_min = 0 # [Optional]
time.valid_max = 9000000000 # [Optional]
time.axis = 'T'
time.ancillary_variables = 'TIME_SEADATANET_QC'
time.sdn_parameter_urn = 'SDN:P01::ELTMEP01'
time.sdn_uom_urn = 'SDN:P06::UTBB'
time.sdn_parameter_name = 'Elapsed time relative to 1970-01-01T00:00:00Z'
time.sdn_uom_name = 'Seconds'
time.instrument = '' # [Mandatory - if there are instruments reported in the file that directly outputs the variable]
time.calibration = '' # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]
time.deployment = '' # [Mandatory - if deployment is unique to time variable]
time[0,0:] = TIME


# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
timeqc = rootgrp.createVariable('TIME_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57)
timeqc.long_name = 'SeaDataNet quality flag'
timeqc.Conventions = 'SeaDataNet measurand qualifier flags' 
timeqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE'
timeqc.sdn_conventions_urn = 'SDN:L20::'
timeqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1')
timeqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain' # must use blank separated list
timeqc[0,0:] = TIME_QC

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise]  
latitude = rootgrp.createVariable('LATITUDE', 'f8', ('INSTANCE', 'MAXT'), fill_value=-99)
latitude.long_name = 'Latitude'
latitude.standard_name = 'latitude'
latitude.units = 'degrees_north'
latitude.valid_min = -90 #[Optional]
latitude.valid_max = 90 #[Optional]
latitude.axis = 'Y'
latitude.ancillary_variables = 'POSITION_SEADATANET_QC'
latitude.sdn_parameter_urn = 'SDN:P01::ALATGP01'
latitude.sdn_uom_urn = 'SDN:P06::DEGN'
latitude.sdn_parameter_name = 'Latitude north relative to WGS84 by unspecified GPS system'
latitude.sdn_uom_name = 'Degrees north'
latitude.grid_mapping = 'crs'
latitude.instrument = '' # [Mandatory - if there are instruments reported in the file that directly outputs the variable]
latitude.calibration = '' # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]
latitude.deployment = '' # [Mandatory - if deployment is unique to variable]
latitude[0,0:] = LAT

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
longitude = rootgrp.createVariable('LONGITUDE', 'f8', ('INSTANCE', 'MAXT'), fill_value=-999)
longitude.long_name = 'Longitude'
longitude.standard_name = 'longitude'
longitude.units = 'degrees_east'
longitude.valid_min = -180 # [Optional]
longitude.valid_max = 180 # [Optional]
longitude.axis = 'X'
longitude.ancillary_variables = 'POSITION_SEADATANET_QC'
longitude.sdn_parameter_urn = 'SDN:P01::ALONGP01'
longitude.sdn_uom_urn = 'SDN:P06::DEGE'
longitude.sdn_parameter_name = 'Longitude east relative to WGS84 by unspecified GPS system'
longitude.sdn_uom_name = 'Degrees east'
longitude.grid_mapping = 'crs'
longitude.instrument = '' # [Mandatory - if there are instruments reported in the file that directly outputs the variable]
longitude.calibration = '' # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]
longitude.deployment = '' # [Mandatory - if deployment is unique to variable]
longitude[0,0:] = LON

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
posqc = rootgrp.createVariable('POSITION_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57)
posqc.long_name = 'SeaDataNet quality flag' 
posqc.Conventions = 'SeaDataNet measurand qualifier flags' 
posqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' 
posqc.sdn_conventions_urn = 'SDN:L20::' 
posqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1')
posqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain'  # must use blank separated list
posqc[0,0:] = POS_QC

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
depth = rootgrp.createVariable('DEPTH', 'f4', ('INSTANCE', 'MAXT'), fill_value=-1)
depth.long_name = 'DepBelowSurf'
depth.standard_name = 'depth'
depth.units = 'm'
depth.valid_min = 0 # [Optional]
depth.valid_max = 9999 # [Optional]
depth.axis = 'Z'
depth.ancillary_variables = 'DEPTH_SEADATANET_QC'
depth.positive = 'down'
depth.sdn_parameter_urn = 'SDN:P01::ADEPZZ01'
depth.sdn_uom_urn = 'SDN:P06::ULAA'
depth.sdn_parameter_name = 'Depth (spatial coordinate) relative to water surface in the water body'
depth.instrument = '' # [Mandatory - if there are instruments reported in the file that directly outputs the variable]
depth.calibration = '' # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]
depth.deployment = '' # [Mandatory - if deployment is unique to variable]
depth.sdn_uom_name = 'Metres'

depth[0,0:] = DEPTH # if depth is not known or the minimum and maximum sensor height is not equal, then set to zero

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
depthqc = rootgrp.createVariable('DEPTH_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57)
depthqc.long_name = 'SeaDataNet quality flag' 
depthqc.Conventions = 'SeaDataNet measurand qualifier flags' 
depthqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' 
depthqc.sdn_conventions_urn = 'SDN:L20::' 
depthqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1')
depthqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain'  # must use blank separated list
depthqc[0,0:] = DEPTH_QC




"""
Data variable(s)

DESCRIPTION: 
https://github.com/I-Ocean/common-metadata/blob/master/observedMeasurements.md
"""
# [Data variables are recommended] 
# [All attributes are mandatory if data variable created unless stated otherwise]
SEATEMP = rootgrp.createVariable('seatemp', 'f4', ('INSTANCE', 'MAXT'), fill_value=-9)
SEATEMP.long_name = 'sea surface temperature'
SEATEMP.coordinates = 'TIME DEPTH LATITUDE LONGITUDE'
SEATEMP.standard_name = 'sea_surface_temperature' # [Recommended]
SEATEMP.units = 'degC'
SEATEMP.valid_min = -3 # [Optional]
SEATEMP.valid_max = 35 # [Optional]
SEATEMP.ancillary_variables = 'TEMPHU01_SEADATANET_QC'
SEATEMP.sdn_parameter_urn = 'SDN:P01::TEMPHU01'
SEATEMP.sdn_uom_urn = 'SDN:P06::UPAA'
SEATEMP.sdn_parameter_name = 'Temperature of the water body by thermosalinograph hull sensor and NO verification against independent measurements'
SEATEMP.sdn_uom_name = 'Degrees Celsius'
SEATEMP.atlantosEVid = 'SDN:A05::EV_SEATEMP' # [optional]
SEATEMP.atlantosEVname = 'Temperature' # [optional]
SEATEMP.instrument = '/instruments/TOOL0022_2490' # [Mandatory - if there are instruments reported in the file that directly outputs the variable]
SEATEMP.calibration = '/calibrations/CAL_2435' # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]
SEATEMP.deployment = '' # [Mandatory - if deployment is unique to variable]
SEATEMP[0,0:] = SST

# [QC ancilliary variable mandatory if data variable created] 
# [All attributes are mandatory if ancilliary variable created]
SEATEMPQC = rootgrp.createVariable('seatemp_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57)
SEATEMPQC.long_name = 'SeaDataNet quality flag' 
SEATEMPQC.Conventions = 'SeaDataNet measurand qualifier flags' 
SEATEMPQC.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' 
SEATEMPQC.sdn_conventions_urn = 'SDN:L20::' 
SEATEMPQC.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1')
SEATEMPQC.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain'  # must use blank separated list
SEATEMPQC[0,0:] = SST_QC


"""
##########################################
GROUP - INSTRUMENTS [Mandatory]
##########################################

DESCRIPTION: Used to group instances of instruments that are used to generate the data.
"""

"""
Create group
"""
Inst = rootgrp.createGroup('instruments') # [Mandatory] 

"""
Group dimensions
DESCRITPION: A dimension with one column (cell)
"""
Inst.createDimension('NCOLUMNS', 1) # [Mandatory] 


"""
Group attributes
"""


"""
---------------------------------------------------------------------------------------------------------------------
SUB-GROUP - INSTRUMENT INSTANCE (/instruments/TOOL0022_2490) [MANDATORY - if group instruments is created]
---------------------------------------------------------------------------------------------------------------------

DESCRIPTION: Identifies each physical instrument used to generate the data in the file. The group identifier should be 
unique to the file. Ideally it should be unique to your systems. 

For more information see: https://github.com/I-Ocean/common-metadata/blob/master/instrumentProperties.md
"""

"""
Create group
"""
Inst1 = Inst.createGroup('TOOL0022_2490')  # [Mandatory] identifier is what ever you want as long as it is unique in the file. Ideally it ought to include the serial number


"""
Group attributes
"""
Inst1.date_valid_from = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Mandatory]
Inst1.date_valid_to = '' # [Recommended] 
Inst1.calibration = '/calibrations/CAL_2435' # [Mandatory - if there are calibrations reported in the file that are relevant to the instrument]
Inst1.installation = '/installations/INSTAL_00001' # [Mandatory - if there are instrument installations in file that are applicable to the instrument]
Inst1.metadata_link = 'https://linkedsystems.uk/system/instance/TOOL0022_2490/current/' # [Optional]
Inst1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX' # [Optional]


"""
Pass group variable data
"""
INSTRUMENTPID = np.array(['http://hdl.handle.net/21.T11998/0000-001A-3905-F']) 
UUID = np.array(['TOOL0022_2490'])
INSTRUMENTNAME = np.array(['SBE 37-IM MicroCAT s/n 2490'])
SERIALNUMBER = np.array(['2490'])
MODELID = np.array(['http://vocab.nerc.ac.uk/collection/L22/current/TOOL0022/'])



"""
Group metadata variables
"""
# [Recommended] - may not be available for all instruments
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentpid = Inst1.createVariable('instrument_pid', 'str', ('NCOLUMNS')) 
Instrumentpid.long_name = 'PIDINST PID'
Instrumentpid.sdn_variable_name = 'TBC'
Instrumentpid.sdn_variable_urn = 'TBC'
Instrumentpid[:] = INSTRUMENTPID

# [Recommended]
# [All attributes mandatory if variable created unless stated otherwise]
Uuid = Inst1.createVariable('uuid', 'str', ('NCOLUMNS'))
Uuid.long_name = 'UUID'
Uuid.sdn_variable_name = 'Universally Unique Identifier (UUID)'
Uuid.sdn_variable_urn = 'SDN:W07::IDEN0007'
Uuid[:] = UUID

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentname = Inst1.createVariable('instrument_name', 'str', ('NCOLUMNS'))
Instrumentname.long_name = 'Instrument name'
Instrumentname.sdn_variable_name = 'Long name'
Instrumentname.sdn_variable_urn = 'SDN:W07::IDEN0002'
Instrumentname[:] = INSTRUMENTNAME

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Serialnumber = Inst1.createVariable('serial_number', 'str', ('NCOLUMNS'))
Serialnumber.long_name = 'Instrument serial number'
Serialnumber.sdn_variable_name = 'Serial Number'
Serialnumber.sdn_variable_urn = 'SDN:W07::IDEN0005'
Serialnumber[:] = SERIALNUMBER

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Modelid = Inst1.createVariable('model_id', 'str', ('NCOLUMNS'))
Modelid.long_name = 'Instrument model identifier'
Modelid.sdn_variable_name = 'Model name'
Modelid.sdn_variable_urn = 'SDN:W07::IDEN0003'
Modelid[:] = MODELID

# [Optional] Other optional instrument information




"""
#####################################################################################
GROUP - CALIBRATIONS (/calibrations) [Recommended]
#####################################################################################

DESCRIPTION: Groups calibration instances, even if the calibration is not applied 
to the data or to the instrument firmware.
"""

"""
Create group
"""
Cals = rootgrp.createGroup('calibrations') # [Mandatory]

"""
Group dimensions
"""
Cals.createDimension('NCOLUMNS', 1) # [Mandatory] 

"""
Group attributes
"""


"""
------------------------------------------------------------------------------------------------------------------
SUB-GROUP - CALIBRATION INSTANCE (/calibrations/CAL_2435) [MANDATORY - if group calibrations created]
------------------------------------------------------------------------------------------------------------------

DESCRIPTION:
Identifies each calibration associated to instruments of data variables in the file. The group identifier should be 
unique to the file. Ideally it should be unique to your systems. 

For more information see: https://github.com/I-Ocean/common-metadata/blob/master/calibrationProperties.md
"""

"""
Create group
"""
Cal1 = Cals.createGroup('CAL_2435') # [Mandatory] 

"""
Group attributes
"""
Cal1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Mandatory]
Cal1.date_valid_to = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Optional]
Cal1.instrument_first_use = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Optional]
Cal1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXX' # [Optional]

"""
Pass group variable data
"""
CALFUNC = np.array(['{"(input - CWO) * SF"}']) 
CALCOEFFS = np.array(['{"SF":5.6,"CWO":0.01}']) 
INPUT = np.array(['Volts'])
INPUTID = np.array(['http://vocab.nerc.ac.uk/collection/P06/current/UVLT/'])
OUTPUT=  np.array(['Milligrams per cubic metre'])
OUTPUTID = np.array(['http://vocab.nerc.ac.uk/collection/P06/current/UMMC/'])


"""
Group metadata variables
"""
# [Optional]
# [All attributes mandatory if variable created unless stated otherwise]
Calibrationfunction = Cal1.createVariable('calibration_function','str',('NCOLUMNS'))
Calibrationfunction.long_name = 'Calibration function' 
Calibrationfunction.sdn_variable_name = 'TBC'
Calibrationfunction.sdn_variable_urn = 'TBC'
Calibrationfunction[:] = CALFUNC

# [Recommended]
# [All attributes mandatory if variable created unless stated otherwise]
Inputunits = Cal1.createVariable('input_units','str',('NCOLUMNS'))
Inputunits.long_name = 'Input units'
Inputunits.sdn_variable_name = 'TBC'
Inputunits.sdn_variable_urn = 'TBC'
Inputunits[:] = INPUT 

# [Recommended]
# [All attributes mandatory if variable created unless stated otherwise]
Inputunitsid = Cal1.createVariable('input_units_id','str',('NCOLUMNS'))
Inputunitsid.long_name = 'Input units identifier'
Inputunitsid.sdn_variable_name = 'TBC'
Inputunitsid.sdn_variable_urn = 'TBC'
Inputunitsid[:] = INPUTID 

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Outputunits = Cal1.createVariable('output_units','str',('NCOLUMNS'))
Outputunits.long_name = 'Output units'
Outputunits.sdn_variable_name = 'TBC'
Outputunits.sdn_variable_urn = 'TBC'
Outputunits[:] = OUTPUT

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Outputunitsid = Cal1.createVariable('output_units_id','str',('NCOLUMNS'))
Outputunitsid.long_name = 'Output units identifier'
Outputunitsid.sdn_variable_name = 'TBC'
Outputunitsid.sdn_variable_urn = 'TBC'
Outputunitsid[:] = OUTPUTID 

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Calibrationcoefficients = Cal1.createVariable('calibration_coefficients', 'str', ('NCOLUMNS')) 
Calibrationcoefficients.long_name = 'Calibration coefficients' 
Calibrationcoefficients.sdn_variable_name = 'TBC' 
Calibrationcoefficients.sdn_variable_urn = 'TBC' 
Calibrationcoefficients[:] = CALCOEFFS 

# [Optional] Other optional calibration information


"""
###############################################################################
GROUP - INSTRUMENT INSTALLATIONS (/installations) [Recommended]
###############################################################################

DESCRIPTION: Groups the instances of instrument installations (e.g. their positions, orientations and sampling depths). 
"""

"""
Create group
"""
Xyz = rootgrp.createGroup('installations') # [Mandatory] 

"""
Group dimensions
"""
Xyz.createDimension('NCOLUMNS', 1) # [Mandatory] 

"""
Group attributes
"""


"""
----------------------------------------------------------------------------------------------------------------------
SUB-GROUP - INSTALLATION INSTANCE (/installations/INSTAL_00001) [Mandatory - if group installations created]
----------------------------------------------------------------------------------------------------------------------

DESCRIPTION:
Identifies each installation instance associated to the instruments in the file. The group identifier should be 
unique to the file. Ideally it should be unique to your systems.

For more information see: https://github.com/I-Ocean/common-metadata/blob/master/instrumentInstallationProperties.md
"""

"""
Create group
"""
Xyz1 = Xyz.createGroup('INSTAL_00001') # [Mandatory] 


"""
Group attributes
"""
Xyz1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Mandatory]
Xyz1.date_valid_to = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Recommended]
Xyz1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': Installed in <niche>' # [Optional]


"""
Pass group variable data
"""
POSY =  np.array([21.4])
POSZ =  np.array([2.63]) 
POSX = np.array([10.1])  
POSDATUM = np.array(['Centre point of ship'])
ORIENTATION =  np.array([0])
ORIENTDATUM = np.array(['Bow of ship'])
SAMPLEDEPTH = np.array([5.5])
SAMPLEDATUM = np.array(['Sea level'])



"""
Group coordinate variables
"""
# [Mandatory - if X, Y or Z positions are reported]
# [All attributes mandatory if variable created unless stated otherwise]
Positiondatum = Xyz1.createVariable('position_datum','str')
Positiondatum.long_name = 'Instrument position datum'
Positiondatum.sdn_variable_name = 'TBC'
Positiondatum.sdn_variable_urn = 'TBC'
Positiondatum[:] = POSDATUM

# [Mandatory - if an instrument orientation is reported]
# [All attributes mandatory if variable created unless stated otherwise]
Orientdatum = Xyz1.createVariable('orientation_datum','str')
Orientdatum.long_name = 'Instrument orientation datum'
Orientdatum.sdn_variable_name = 'TBC'
Orientdatum.sdn_variable_urn = 'TBC'
Orientdatum[:] = ORIENTDATUM

# [Mandatory - if a sampling depth is reported]
# [All attributes mandatory if variable created unless stated otherwise]
Sampledatum = Xyz1.createVariable('sample_depth_datum','str')
Sampledatum.long_name = 'Sampling depth datum'
Sampledatum.sdn_variable_name = 'TBC'
Sampledatum.sdn_variable_urn = 'TBC'
Sampledatum[:] = SAMPLEDATUM


"""
Group metadata variables
"""
# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
X = Xyz1.createVariable('x', 'f4', ('NCOLUMNS')) 
X.long_name = 'x position (positive = forward)' 
X.sdn_variable_name = 'x'
X.sdn_variable_urn = 'SDN:W02::002' 
X.units = 'm'
X.sdn_uom_name = 'Metres'
X.sdn_uom_urn = 'SDN:P06::ULAA'
X.coordinates = 'position_datum'
X[:] = POSX

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]       
Y = Xyz1.createVariable('y', 'f4', ('NCOLUMNS'))
Y.long_name = 'y position (positive = up)'
Y.sdn_variable_name = 'y'
Y.sdn_variable_urn = 'SDN:W02::003'
Y.units = 'm'
Y.sdn_uom_name = 'Metres'
Y.sdn_uom_urn = 'SDN:P06::ULAA'
Y.coordinates = 'position_datum'
Y[:] = POSY             

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
Z = Xyz1.createVariable('z', 'f4', ('NCOLUMNS')) 
Z.long_name = 'z position (positive = starboard)' 
Z.sdn_variable_name = 'z'
Z.sdn_variable_urn = 'SDN:W02::004' 
Z.units = 'm'
Z.sdn_uom_name = 'Metres' 
Z.sdn_uom_urn = 'SDN:P06::ULAA'
Z.coordinates = 'position_datum'
Z[:] = POSZ        

# [Mandatory - if instrument has an orientation] 
# [All attributes mandatory if variable created unless stated otherwise]
Orientation = Xyz1.createVariable('orientation', 'f4', ('NCOLUMNS')) 
Orientation.long_name = 'Rotational orientation (clockwise) of instrument'
Orientation.sdn_variable_name = 'TBC'
Orientation.sdn_variable_urn = 'TBC'
Orientation.units = 'degrees'
Orientation.sdn_uom_name = 'degrees'
Orientation.sdn_uom_urn = 'SDN:P06::UAAA'
Orientation.coordinates = 'orientation_datum'
Orientation[:] = ORIENTATION

# [Recommended - if instrument has sample depth. The sample depth may be different to position (e.g. TSG sample intake)]     
# [All attributes mandatory if variable created unless stated otherwise]    
Sampledepth = Xyz1.createVariable('sample_depth', 'f4', ('NCOLUMNS'))  
Sampledepth.long_name = 'Depth of sampling point'
Sampledepth.sdn_variable_name = 'TBC'
Sampledepth.sdn_variable_urn = 'TBC'
Sampledepth.units = 'm'
Sampledepth.sdn_uom_name = 'Metres'
Sampledepth.sdn_uom_urn = 'SDN:P06::ULAA'
Sampledepth.coordinates = 'sample_depth_datum'
Sampledepth[:] = SAMPLEDEPTH



"""
#############################################
GROUP - PLATFORMS [Optional]
#############################################

DESCRIPTION: 
Groups the instances of platforms that are directly relevant to the instruments and data variables in the file.
"""

"""
Create group
"""
Plats = rootgrp.createGroup('platforms') # [Mandatory] 

"""
Group dimensions
"""
Plats.createDimension('NCOLUMNS', 1) # [Mandatory] 

"""
Group attributes
"""

"""
----------------------------------------------------------------------------------------------------------
SUB-GROUP - MOUNTING PLATFORM (/platforms/DISCOVERY) [Mandatory - if group platforms is created]
----------------------------------------------------------------------------------------------------------

DESCRIPTION:
Identifies each platform instance associated to the instruments or data in the file. The group identifier should be 
unique to the file. Ideally it should be unique to your systems.

For more information see: https://github.com/I-Ocean/common-metadata/blob/master/platformProperties.md
"""

"""
Create group
"""
Disco = Plats.createGroup('DISCOVERY') # [Mandatory] An identifier of your choice as long as it is unique to the file


"""
Group attributes
"""
Disco.date_valid_from = datetime(2007, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Recommended]
Disco.date_valid_to = datetime(2020, 10, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Optional]
Disco.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX' # [Optional]


"""
Pass group variable data
"""
PLATFORM = np.array(['RRS Discovery'])
PLATFORMMODELID = np.array(['TBC'])
ICESID = np.array(['http://vocab.nerc.ac.uk/collection/C17/current/74EQ/'])
IMOID = np.array(['9588029'])
CALLSIGN = np.array(['2FGX5']) 



"""
Group metadata variables
"""

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Platform = Disco.createVariable('platform_name', 'str', ('NCOLUMNS'))
Platform.long_name = 'Platform name'
Platform.sdn_variable_name = 'Long name' 
Platform.sdn_variable_urn = 'SDN:W07::IDEN0002'
Platform[:] = PLATFORM


# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Platmod_id = Disco.createVariable('platform_model_id','str', ('NCOLUMNS'))
Platmod_id.long_name = 'Model name identifier'
Platmod_id.sdn_variable_name = 'TBC'
Platmod_id.sdn_variable_urn = 'TBC'
Platmod_id[:] = PLATFORMMODELID

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
Ices_id = Disco.createVariable('platform_ices_id','str', ('NCOLUMNS'))
Ices_id.long_name = 'ICES platform code'
Ices_id.sdn_variable_name = 'ICES code'
Ices_id.sdn_variable_urn = 'SDN:W07::IDEN0001'
Ices_id[:] = ICESID

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
Platform_imo_id = Disco.createVariable('platform_imo_id', 'str', ('NCOLUMNS'))
Platform_imo_id.long_name = 'IMO number'
Platform_imo_id.sdn_variable_name = 'TBC'
Platform_imo_id.sdn_variable_urn = 'TBC'
Platform_imo_id[:] = IMOID

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Platform_callsign = Disco.createVariable('platform_callsign','str', ('NCOLUMNS'))
Platform_callsign.long_name = 'Call Sign'
Platform_callsign.sdn_variable_name = 'Call Sign'
Platform_callsign.sdn_variable_urn = 'SDN:W07::IDEN0010'
Platform_callsign[:] = CALLSIGN



# [Optional] Other static properties related to platforms


"""
###################################################
GROUP - DEPLOYMENTS [Optional] /deployments
###################################################

DESCRIPTION: 
Groups deployment instances associated to the data in the file.
"""

"""
Create group
"""
Deps = rootgrp.createGroup('deployments') # [Mandatory]

"""
Group dimensions
"""
Deps.createDimension('NCOLUMNS', 1) # [Mandatory]

"""
Group attributes
"""


"""
-------------------------------------------------------------------------------------
SUB-GROUP - DEPLOYMENT (/deployments/DY122) [Mandatory]
-------------------------------------------------------------------------------------

DESCRIPTION: 
Describes a deployment instance. It is also used to link sensors to platforms.

For more information see: https://github.com/I-Ocean/common-metadata/blob/master/deploymentProperties.md
"""

"""
Create group
"""
Dep1 = Deps.createGroup('DY122') # [Mandatory] An identifier of your choice as long as it unique to the file. Ideally the cruise ID


"""
Group attributes
"""
Dep1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Mandatory]
Dep1.date_valid_to = datetime(2019, 2, 11, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z') # [Recommeded]
Dep1.platform = '/platforms/DISCOVERY' # [Recommended - if platforms in the file are used in the deployment]
Dep1.instrument = '/instruments/TOOL0022_2490' # [Recommended - if instruments in file are used in the deployment]
Dep1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX' # [Optional]




"""
Pass group variable data
"""
DEPLOYMENT = np.array(['DY122'])
INSTITUTIONID = np.array(['http://vocab.nerc.ac.uk/collection/B75/current/ORG00003/']) 
CAMPAIGN = np.array(['OSMOSIS'])


"""
Group metadata variables
"""
# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Deployment_id = Dep1.createVariable('Deployment_id','str',('NCOLUMNS'))
Deployment_id.long_name = 'Deployment identifier'
Deployment_id.sdn_variable_name = 'TBC'
Deployment_id.sdn_variable_urn = 'TBC'
Deployment_id[:] = DEPLOYMENT

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Owner_id = Dep1.createVariable('owner_id', 'str', ('NCOLUMNS'))
Owner_id.long_name = 'Institution identifier'
Owner_id.sdn_variable_name = 'TBC'
Owner_id.sdn_variable_urn = 'TBC'
Owner_id[:] = INSTITUTIONID

# [Optional] 
# [All attributes mandatoB75ry if variable created unless stated otherwise]
Campaign_name = Dep1.createVariable('campaign_name', 'str', ('NCOLUMNS'))
Campaign_name.long_name = 'Campaign name'
Campaign_name.sdn_variable_name = 'TBC'
Campaign_name.sdn_variable_urn = 'TBC'
Campaign_name[:] = CAMPAIGN



"""
----------------------
CLOSE
----------------------
"""

rootgrp.close()


