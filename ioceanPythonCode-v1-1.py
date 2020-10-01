
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
from datetime import datetime, timezone, date
from netCDF4 import num2date, date2num
import pandas as pd
import matplotlib.pyplot as plt

"""
#######################
# Description
#######################
"""
"""
IOcean-1.0
The format uses netcdf4 groups to describe instruments, instrument installations, calibrations, platforms, deployments and 
campaigns associated to the data. This way you can append multiple cruises or link a data channel to more than one instrument 
such as a data logger and fitted sensor. Much of the metadata is in variables. This is to enable the use of APIs (like ERDDAP)
and not to limit the number of properties that can be associated as long as it is defined by vocabularies.
It is anticipated the format can be used for other data types on ship (e.g. CTD). The format is based on SeaDataNet Climate 
Forecast NetCDF. 

Daily files should be created at 1 second and 1 min resolutions

All dates and times are ISO 8601. Ideally they should be UTC. 
"""

"""
#########################
ROOTGROUP - [Mandatory]
#########################
"""
"""
DESCRIPTION: Central group that contains the data variables
"""


"""
Create/open file
"""
rootgrp = nc.Dataset('iocean_example.nc','w',format='NETCDF4') ; # overwrite

"""
Global attributes
"""
rootgrp.deployment_id = '/deployments/DY122'; # [Mandatory] Cruise_id. Potentially same as campaign for ships. Can be global attribute or variable attribute if more than one deployment in file.
rootgrp.title = 'I/Ocean trajectory file Climate Forecast 1.8'; # [Mandatory]
rootgrp.Conventions = 'CF-1.8 SeaDataNet-1.0 ACDD-1.3 IOcean-1.0'; # [Mandatory]
rootgrp.source = 'Underway observations from RRS Discovery navigation, meteorology and sea surface hydrography sensor arrays'; # [Mandatory]
rootgrp.history =  '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': (NMF) File created'; # [Mandatory] Provides an audit trail for modifications to the original data. Where possible, append the timestamp of the modification, the name of the responsible entity or program and the parameters invoked. Use newline characters to break lines.
rootgrp.references = 'https://github.com/I-Ocean/netcdf-specification'; # [Recommended]
rootgrp.date_created = datetime(2020, 1, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory]
rootgrp.date_update = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'); # [Mandatory] Set to date-created time if creating the file for first time
rootgrp.processing_level = 'Raw instrument data'; # [Mandatory] 
rootgrp.standard_name_vocabulary = 'http://vocab.nerc.ac.uk/collection/P07/current/';
rootgrp.sdn_vocabulary = 'http://vocab.nerc.ac.uk/';
rootgrp.featureType = 'trajectory'; # [Mandatory] 
rootgrp.data_interval = '1Hz'; # [Mandatory] 
rootgrp.comment = '\n'+datetime(2020, 1, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')+': XXXXX'; # [Optional] Miscellaneous information about the data or methods used to produce it. Only create attribute if there are comments. Use newline characters to break lines if more than one comment.

"""
Dimensions
"""
rootgrp.createDimension('INSTANCE',None) ; # this allows more than one trajectory (e.g. with a second timestamp) in the file
rootgrp.createDimension('MAXT',6) ; # [Mandatory] 
rootgrp.createDimension('STRING80',80); # [Mandatory] 

"""
Pass variable data
"""
TRAJECTORYID = nc.stringtochar(np.array(['DY122_UWAY1'], 'S80'));
CRS = 0 ; # grid mapping coordinate always = 0;
TIME = np.array([2458079., 2458079.00069444, 2458079.00138889, 2458107.66250002, 2458107.66319442, 2458107.66388887],'f8');
TIME_QC = np.array([49, 49, 49, 49, 49, 49], 'i1');
LAT = np.array([-51.71759033, -51.71879196, -51.72002792, -54.596138  , -54.59526443, -54.59444046],'f8');
LON = np.array([-57.65376663, -57.65382767, -57.65382385, -58.36009979, -58.36487961, -58.3693428 ],'f8');
POS_QC = np.array([49, 49, 49, 49, 49, 49], 'i1');
DEPTH = np.array([0,0,0,0,0,0],'f4'); 
DEPTH_QC = np.array([49, 49, 49, 49, 49, 49], 'i1');
SST = np.array([7.4809, 7.4390, -9, 7.4030, 7.3647, 7.3497],'f4'); # note 3rd element = -9 (fill value)
SST_QC = np.array([49, 49, 57, 49, 49, 49], 'i1'); # note 3rd element of ancilliary data to SST = 57 (fill value)


"""
Coordinate variables
"""
"""
DESCRIPTION: See GitHUB page - 
"""
# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
Traj = rootgrp.createVariable('trajectory','S1',('INSTANCE','STRING80')); # ID needed per instance that is needed to be CF compliant. This can't be deployment as there may be more than one time stamp (instance) per deployment
Traj.long_name = 'Trajectory identifier';
Traj.cf_role = "trajectory_id" ;
Traj[:] = TRAJECTORYID;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
Crs = rootgrp.createVariable('crs','i4');
Crs.grid_mapping_name = 'latitude_longitude' ;
Crs.epsg_code = 'EPSG:4326' ;
Crs.semi_major_axis = 6378137. ;
Crs.inverse_flattening = 298.257223563 ;
Crs[:] = CRS;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise]  
time = rootgrp.createVariable('TIME', 'f8', ('INSTANCE', 'MAXT'), fill_value=-99999999999);
time.long_name = 'Chronological Julian Date';
time.standard_name = 'time';
time.units = 'days since -4713-01-01T00:00:00Z';
time.calendar = 'julian';
time.valid_min = 0;
time.valid_max = 2500000;
time.axis = 'T';
time.ancillary_variables = 'TIME_SEADATANET_QC';
time.sdn_parameter_urn = 'SDN:P01::CJDY1101';
time.sdn_uom_urn = 'SDN:P06::UTAA';
time.sdn_parameter_name = 'Julian Date (chronological)';
time.sdn_uom_name = 'Days';
time[0,0:] = TIME;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
timeqc = rootgrp.createVariable('TIME_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57);
timeqc.long_name = 'SeaDataNet quality flag' ;
timeqc.Conventions = 'SeaDataNet measurand qualifier flags' ;
timeqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' ;
timeqc.sdn_conventions_urn = 'SDN:L20::' ;
timeqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1');
timeqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain' ; # must use blank separated list
timeqc[0,0:] = TIME_QC;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise]  
latitude = rootgrp.createVariable('LATITUDE', 'f8', ('INSTANCE', 'MAXT'), fill_value=-99);
latitude.long_name = 'Latitude';
latitude.standard_name = 'latitude';
latitude.units = 'degrees_north';
latitude.valid_min = -90;
latitude.valid_max = 90;
latitude.axis = 'Y';
latitude.ancillary_variables = 'POSITION_SEADATANET_QC';
latitude.sdn_parameter_urn = 'SDN:P01::ALATGP01';
latitude.sdn_uom_urn = 'SDN:P06::DEGN';
latitude.sdn_parameter_name = 'Latitude north relative to WGS84 by unspecified GPS system';
latitude.sdn_uom_name = 'Degrees north';
latitude.grid_mapping = 'crs';
latitude.instrument = '/instruments/TOOL0349_4444444x56'; # [Mandatory - if there are instruments reported in the file that directly outputs the variable]. Use a blank, comma or newline separated lists if more than two instruments are assigned.
#latitude.calibration =''; # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
#latitude.deployment =''; # [Mandatory - if more than one deployment reported in the file otherwise use a global attribute]. Only add deployment identifiers that are directly applicable to the variable. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
latitude[0,0:] = LAT;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
longitude = rootgrp.createVariable('LONGITUDE', 'f8', ('INSTANCE', 'MAXT'), fill_value=-999);
longitude.long_name = 'Longitude';
longitude.standard_name = 'longitude';
longitude.units = 'degrees_east';
longitude.valid_min = -180;
longitude.valid_max = 180;
longitude.axis = 'X';
longitude.ancillary_variables = 'POSITION_SEADATANET_QC';
longitude.sdn_parameter_urn = 'SDN:P01::ALONGP01';
longitude.sdn_uom_urn = 'SDN:P06::DEGE';
longitude.sdn_parameter_name = 'Longitude east relative to WGS84 by unspecified GPS system';
longitude.sdn_uom_name = 'Degrees east';
longitude.grid_mapping = 'crs';
longitude.instrument = '/instruments/TOOL0349_4444444x56'; # [Mandatory - if there are instruments reported in the file that directly outputs the variable]. Use a blank, comma or newline separated lists if more than two instruments are assigned.
#longitude.calibration =''; # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
#longitude.deployment =''; # [Mandatory - if more than one deployment reported in the file otherwise use a global attribute]. Only add deployment identifiers that are directly applicable to the variable. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
longitude[0,0:] = LON;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
posqc = rootgrp.createVariable('POSITION_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57);
posqc.long_name = 'SeaDataNet quality flag' ;
posqc.Conventions = 'SeaDataNet measurand qualifier flags' ;
posqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' ;
posqc.sdn_conventions_urn = 'SDN:L20::' ;
posqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1');
posqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain' ; # must use blank separated list
posqc[0,0:] = POS_QC;

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
depth = rootgrp.createVariable('DEPTH', 'f4', ('INSTANCE', 'MAXT'), fill_value=-1);
depth.long_name = 'DepBelowSurf';
depth.standard_name = 'depth';
depth.units = 'm';
depth.valid_min = 0;
depth.valid_max = 9999;
depth.axis = 'Z';
depth.ancillary_variables = 'DEPTH_SEADATANET_QC';
depth.positive = 'down';
depth.sdn_parameter_urn = 'SDN:P01::ADEPZZ01';
depth.sdn_uom_urn = 'SDN:P06::ULAA';
depth.sdn_parameter_name = 'Depth (spatial coordinate) relative to water surface in the water body';
depth.sdn_uom_name = 'Metres';
depth[0,0:] = DEPTH; # set to zero

# [Variable mandatory] 
# [All attributes mandatory unless stated otherwise] 
depthqc = rootgrp.createVariable('DEPTH_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57);
depthqc.long_name = 'SeaDataNet quality flag' ;
depthqc.Conventions = 'SeaDataNet measurand qualifier flags' ;
depthqc.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' ;
depthqc.sdn_conventions_urn = 'SDN:L20::' ;
depthqc.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1');
depthqc.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain' ; # must use blank separated list
depthqc[0,0:] = DEPTH_QC;

"""
Data variable(s)
"""
# [Data variables are recommended] 
# [All attributes are mandatory if data variable created unless stated otherwise]
SEATEMP = rootgrp.createVariable('seatemp', 'f4', ('INSTANCE', 'MAXT'), fill_value=-9);
SEATEMP.long_name = 'sea surface temperature';
SEATEMP.coordinates = 'TIME DEPTH LATITUDE LONGITUDE';
SEATEMP.standard_name = 'sea_surface_temperature';
SEATEMP.units = 'degC';
SEATEMP.valid_min = -3; 
SEATEMP.valid_max = 35;
SEATEMP.ancillary_variables = 'TEMPHU01_SEADATANET_QC';
SEATEMP.sdn_parameter_urn = 'SDN:P01::TEMPHU01';
SEATEMP.sdn_uom_urn = 'SDN:P06::UPAA';
SEATEMP.sdn_parameter_name = 'Temperature of the water body by thermosalinograph hull sensor and NO verification against independent measurements';
SEATEMP.sdn_uom_name = 'Degrees Celsius';
SEATEMP.atlantosEVid = 'SDN:A05::EV_SEATEMP'; # [optional]
SEATEMP.atlantosEVname = 'Temperature'; # [optional]
SEATEMP.instrument = '/instruments/TOOL0022_2490'; # [Mandatory - if there are instruments reported in the file that directly outputs the variable]. Use a blank, comma or newline separated lists if more than two instruments are assigned.
SEATEMP.calibration = '/calibrations/CAL_2435'; # [Mandatory - if there are calibrations reported in the file that are directly applied to variable]. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
#SEATEMP.deployment = ''; # [Mandatory - if more than one deployment reported in the file otherwise use a global attribute]. Only add deployment identifiers that are directly applicable to the variable. Use a blank, comma or newline separated lists if more than two calibrations are assigned.
SEATEMP[0,0:] = SST;

# [QC ancilliary variable mandatory if data variable created] 
# [All attributes are mandatory if ancilliary variable created]
SEATEMPQC = rootgrp.createVariable('seatemp_SEADATANET_QC','i1',('INSTANCE', 'MAXT'), fill_value = 57);
SEATEMPQC.long_name = 'SeaDataNet quality flag' ;
SEATEMPQC.Conventions = 'SeaDataNet measurand qualifier flags' ;
SEATEMPQC.coordinates = 'TIME DEPTH LATITUDE LONGITUDE' ;
SEATEMPQC.sdn_conventions_urn = 'SDN:L20::' ;
SEATEMPQC.flag_values = np.array([48,49,50,51,52,53,54,55,56,57,65],'i1');
SEATEMPQC.flag_meanings = 'no_quality_control good_value probably_good_value probably_bad_value bad_value changed_value value_below_detection value_in_excess interpolated_value missing_value value_phenomenon_uncertain' ; # must use blank separated list
SEATEMPQC[0,0:] = SST_QC;

"""
##########################################
GROUP - INSTRUMENTS [Mandatory]
##########################################

DESCRIPTION: Reports instruments used to generate the data. Obligations are stated if a instrument group is created.
"""

"""
Create group
"""
Inst = rootgrp.createGroup('instruments'); # [Mandatory] 

"""
Group dimensions
DESCRITPION: A dimension with one column (cell)
"""
Inst.createDimension('NCOLUMNS', 1); # [Mandatory] 


"""
Group attributes
"""


"""
---------------------------------------------------------------------------------------------------------------------
SUB-GROUP - INSTRUMENT INSTANCE (/instruments/TOOL0022_2490) [MANDATORY - if group instruments is created]
---------------------------------------------------------------------------------------------------------------------
"""
"""
DESCRIPTION: Identifies each physical instrument used to generate the data in the file. Use any name you like as long as it
is universally unique to your systems. The example uses the UUID used by the BODC data curation centre.
Obligations are stated inline if group is created.
"""

"""
Create group
"""
Inst1 = Inst.createGroup('TOOL0022_2490') ; # [Mandatory] identifier is what ever you want as long as it is unique in the file. Ideally it ought to include the serial number

"""
Group dimensions

DESCRIPTION: Used to create dimensions of more than one row if more than one value in value array needed. 
Create NRECORDSX dimensions as needed where X is the number of rows needed (e.g. NRECORDS2 = 2 columns). 
Apply dimensions as ('NRECORDSX','NCOLUMNS') when using createVariable.
"""
    # inst1.createDimension('NRECORDSX', X); 


"""
Group attributes
"""
Inst1.date_valid_from = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory] Commision date
#Inst1.date_valid_to = ''; # [Recommended - if decommission date is known]. 
Inst1.first_use_date = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Optional] 
Inst1.metadata_link = 'https://linkedsystems.uk/system/instance/TOOL0022_2490/current/'; # [Optional]. A link to further metadata or provenance information about the physical instrument. 
Inst1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX'; # [Optional]  Miscellaneous information about the instrument. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments


"""
Pass group variable data
"""
INSTRUMENTPID = np.array(['http://hdl.handle.net/21.T11998/0000-001A-3905-F']); 
UUID = np.array(['TOOL0022_2490']);
INSTRUMENTNAME = np.array(['SBE 37-IM MicroCAT s/n 2490']);
SERIALNUMBER = np.array(['2490']);
MODELNAME = np.array(['Sea-Bird SBE 37-IM MicroCAT C-T Sensor']);
MODELID = np.array(['http://vocab.nerc.ac.uk/collection/L22/current/TOOL0022/']);
INSTCAL = np.array(['/calibrations/CAL_2435']);
INSTPOS = np.array(['/installations/INSTAL_00001']);


"""
Group metadata variables
"""
# [Recommended] - may not be available for all instruments
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentpid = Inst1.createVariable('instrument_pid', 'str', ('NCOLUMNS')); 
Instrumentpid.long_name = 'PIDINST PID';
Instrumentpid.sdn_variable_name = 'TBC';
Instrumentpid.sdn_variable_url = 'TBC';
Instrumentpid[:] = INSTRUMENTPID;

# [Mandatory] - needed for BODC systems
# [All attributes mandatory if variable created unless stated otherwise]
Uuid = Inst1.createVariable('uuid', 'str', ('NCOLUMNS'));
Uuid.long_name = 'UUID';
Uuid.sdn_variable_name = 'Universally Unique Identifier (UUID)'
Uuid.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0007/';
Uuid[:] = UUID;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentname = Inst1.createVariable('instrument_name', 'str', ('NCOLUMNS'));
Instrumentname.long_name = 'Instrument name';
Instrumentname.sdn_variable_name = 'Long name';
Instrumentname.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0002/';
Instrumentname[:] = INSTRUMENTNAME;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Serialnumber = Inst1.createVariable('serial_number', 'str', ('NCOLUMNS'));
Serialnumber.long_name = 'Instrument serial number';
Serialnumber.sdn_variable_name = 'Serial Number';
Serialnumber.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0005/';
Serialnumber[:] = SERIALNUMBER;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Modelname = Inst1.createVariable('model_name', 'str', ('NCOLUMNS')) ;
Modelname.long_name = 'Instrument model name';
Modelname.sdn_variable_name = 'Model Name';
Modelname.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0003/';
Modelname[:] = MODELNAME;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Modelid = Inst1.createVariable('model_id', 'str', ('NCOLUMNS')) ;
Modelid.long_name = 'Model Name Identifier';
Modelid.sdn_variable_name = 'TBC';
Modelid.sdn_variable_url = 'TBC';
Modelid[:] = MODELID;

# [Mandatory - if applicable instrument calibrations in file] - I/Ocean linking variable
# [All attributes mandatory if variable created unless stated otherwise]
Instcals = Inst1.createVariable('calibrations','str',('NCOLUMNS')) ;
Instcals.long_name = 'calibrations';
Instcals[:] = INSTCAL;

# [Mandatory - if applicable instrument installations in file] - I/Ocean linking variable
# [All attributes mandatory if variable created unless stated otherwise]
Instpos = Inst1.createVariable('installations','str',('NCOLUMNS')) ;
Instpos.long_name = 'installations';
Instpos[:] = INSTPOS;

# [Optional] Other optional instrument information






"""
---------------------------------------------------------------------------------------------------------------------
SUB-GROUP - INSTRUMENT INSTANCE (/instruments/TOOL0349_4444444x56) [MANDATORY - if group instruments is created]
---------------------------------------------------------------------------------------------------------------------
"""
"""
DESCRIPTION: Identifies each physical instrument used to generate the data in the file. Use any name you like as long as it
is universally unique to your systems. The example uses the UUID used by the BODC data curation centre.
Obligations are stated inline if group is created.
"""

"""
Create group
"""
Inst2 = Inst.createGroup('TOOL0349_4444444x56') ; # [Mandatory] identifier is what ever you want as long as it is unique in the file. Ideally it ought to include the serial number

"""
Group dimensions

DESCRIPTION: Used to create dimensions of more than one row if more than one value in value array needed. 
Create NRECORDSX dimensions as needed where X is the number of rows needed (e.g. NRECORDS2 = 2 columns). 
Apply dimensions as ('NRECORDSX','NCOLUMNS') when using createVariable.
"""
    # Inst2.createDimension('NRECORDSX', X); 


"""
Group attributes
"""
Inst2.date_valid_from = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory] Commision date
#Inst2.date_valid_to = ''; # [Recommended - if decommission date is known]. 
Inst2.first_use_date = datetime(2020, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Optional] 
# Inst2.metadata_link = 'https://linkedsystems.uk/system/instance/TOOL0022_2490/current/'; # [Optional]. A link to further metadata or provenance information about the physical instrument. 
Inst2.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX'; # [Optional]  Miscellaneous information about the instrument. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments


"""
Pass group variable data
"""
UUID = np.array(['TOOL0349_4444444x56']);
INSTRUMENTNAME = np.array(['CNAV GPS s/n 4444444x56']);
SERIALNUMBER = np.array(['4444444x56']);
MODELNAME = np.array(['C&C Technologies C-Nav3050 satellite positioning system receiver']);
MODELID = np.array(['http://vocab.nerc.ac.uk/collection/L22/current/TOOL0349/']);


"""
Group metadata variables
"""
# [Recommended] - may not be available for all instruments
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentpid = Inst2.createVariable('instrument_pid', 'str', ('NCOLUMNS')); 
Instrumentpid.long_name = 'PIDINST PID;
Instrumentpid.sdn_variable_name = 'TBC';
Instrumentpid.sdn_variable_url = 'TBC';
Instrumentpid[:] = INSTRUMENTPID;

# [Mandatory] - needed for BODC systems
# [All attributes mandatory if variable created unless stated otherwise]
Uuid = Inst2.createVariable('uuid', 'str', ('NCOLUMNS'));
Uuid.long_name = 'UUID';
Uuid.sdn_variable_name = 'Universally Unique Identifier (UUID)'
Uuid.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0007/';
Uuid[:] = UUID;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Instrumentname = Inst2.createVariable('instrument_name', 'str', ('NCOLUMNS'));
Instrumentname.long_name = 'Instrument name';
Instrumentname.sdn_variable_name = 'Long name';
Instrumentname.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0002/';
Instrumentname[:] = INSTRUMENTNAME;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Serialnumber = Inst2.createVariable('serial_number', 'str', ('NCOLUMNS'));
Serialnumber.long_name = 'Instrument serial number';
Serialnumber.sdn_variable_name = 'Serial Number';
Serialnumber.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0005/';
Serialnumber[:] = SERIALNUMBER;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Modelname = Inst2.createVariable('model_name', 'str', ('NCOLUMNS')) ;
Modelname.long_name = 'Instrument model name';
Modelname.sdn_variable_name = 'Model Name';
Modelname.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0003/';
Modelname[:] = MODELNAME;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Modelid = Inst2.createVariable('model_id', 'str', ('NCOLUMNS')) ;
Modelid.long_name = 'Model Name Identifier';
Modelid.sdn_variable_name = 'TBC';
Modelid.sdn_variable_url = 'TBC';
Modelid[:] = MODELID;

# [Mandatory - if applicable instrument calibrations in file] - I/Ocean linking variable
# [All attributes mandatory if variable created unless stated otherwise]
Instcals = Inst2.createVariable('calibrations','str',('NCOLUMNS')) ;
Instcals.long_name = 'calibrations';
Instcals[:] = INSTCAL;

# [Mandatory - if applicable instrument installations in file] - I/Ocean linking variable
# [All attributes mandatory if variable created unless stated otherwise]
Instpos = Inst2.createVariable('instrument_installations','str',('NCOLUMNS')) ;
Instpos.long_name = 'installations';
Instpos[:] = INSTPOS;

# [Optional] Other optional instrument information





"""
#####################################################################################
GROUP - CALIBRATIONS (/calibrations) [Recommended]
#####################################################################################
"""
"""
DESCRIPTION: Contains groups for each instrument calibration, even if the instrument calibration is not applied 
to the data or to the instrument firmware. It also contains calibrations against independent samples that may be 
applied after data collection. Obligations are stated if a calibration group is created.
"""

"""
Create group
"""
Cals = rootgrp.createGroup('calibrations'); # [Mandatory]

"""
Group dimensions
"""
Cals.createDimension('NCOLUMNS', 1); # [Mandatory] 

"""
Group attributes
"""


"""
------------------------------------------------------------------------------------------------------------------
SUB-GROUP - CALIBRATION INSTANCE (/calibrations/CAL_2435) [MANDATORY - if group calibrations created]
------------------------------------------------------------------------------------------------------------------
"""
"""
DESCRIPTION: One calibration instance per calibration (e.g the calibrations for temp and salinity 
for a TSG are separate instances). If the calibration is applied to a data channel, use the path to 
populate variable attribute (e.g. Sst.calibration). Ideally incorporate your database id into the 
calibration name. Obligations are stated inline if group is created.
"""

"""
Create group
"""
Cal1 = Cals.createGroup('CAL_2435'); # [Mandatory] 

"""
Group attributes
"""
Cal1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory] Calibration active from/start date (e.g. manufacturer calibration date or start date of independent calibration)
Cal1.date_valid_to = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Optional] Calibration expiration/end date
Cal1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXX'; # [Optional]  Miscellaneous information about the calibration. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments

"""
Pass group variable data
"""
CALFUNC = np.array(['{"Chla":"A+B -C"}']); 
CALCOEFFS = np.array(['{"SF":{"units":"V/ug/L","value":5.6},"CWO":{"units":"V","value":"0.01"}}']); 
INPUT = np.array(['Volts']);
INPUTID = np.array(['http://vocab.nerc.ac.uk/collection/P06/current/UVLT/']);
OUTPUT=  np.array(['Milligrams per cubic metre']);
OUTPUTID = np.array(['http://vocab.nerc.ac.uk/collection/P06/current/UMMC/']);


"""
Group metadata variables
"""
# [Optional]
# [All attributes mandatory if variable created unless stated otherwise]
Calibrationfunction = Cal1.createVariable('calibration_function','str',('NCOLUMNS'));
Calibrationfunction.long_name = 'Calibration function';
Calibrationfunction.sdn_variable_name = 'TBC';
Calibrationfunction.sdn_variable_url = 'TBC';
Calibrationfunction[:] = CALFUNC;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Inputunits = Cal1.createVariable('input_units','str',('NCOLUMNS'));
Inputunits.long_name = 'Input units';
Inputunits.sdn_variable_name = 'TBC';
Inputunits.sdn_variable_url = 'TBC';
Inputunits[:] = INPUT; 

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Inputunitsid = Cal1.createVariable('input_units_id','str',('NCOLUMNS'));
Inputunitsid.long_name = 'Input units identifier'
Inputunitsid.sdn_variable_name = 'TBC';
Inputunitsid.sdn_variable_url = 'TBC';
Inputunitsid[:] = INPUTID; 

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Outputunits = Cal1.createVariable('output_units','str',('NCOLUMNS'));
Outputunits.long_name = 'Output units';
Outputunits.sdn_variable_name = 'TBC';
Outputunits.sdn_variable_url = 'TBC';
Outputunits[:] = OUTPUT;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Outputunitsid = Cal1.createVariable('output_units_id','str',('NCOLUMNS'));
Outputunitsid.long_name = 'Output units identifier';
Outputunitsid.sdn_variable_name = 'TBC';
Outputunitsid.sdn_variable_url = 'TBC';
Outputunitsid[:] = OUTPUTID; 

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Calibrationcoefficients = Cal1.createVariable('calibration_coefficients', 'str', ('NCOLUMNS')) ;
Calibrationcoefficients.long_name = 'Calibration coefficients' ;
Calibrationcoefficients.sdn_variable_name = 'TBC' ;
Calibrationcoefficients.sdn_variable_url = 'TBC' ;
Calibrationcoefficients[:] = CALCOEFFS; 

# [Optional] Other optional calibration information


"""
###############################################################################
GROUP - INSTRUMENT INSTALLATIONS (/installations) [Recommended]
###############################################################################
"""
"""
DESCRIPTION: Describes the instrument installations, positions, orientations and sampling depths. 
Obligations are stated if an installation group is created
"""

"""
Create group
"""
Xyz = rootgrp.createGroup('installations'); # [Mandatory] 

"""
Group dimensions
"""
Xyz.createDimension('NCOLUMNS', 1); # [Mandatory] 

"""
Group attributes
"""


"""
----------------------------------------------------------------------------------------------------------------------
SUB-GROUP - INSTALLATION INSTANCE (/installations/INSTAL_00001) [Mandatory - if group installations created]
----------------------------------------------------------------------------------------------------------------------
"""
"""
One instance per installation. Ideally incorporate your database id into the instance name.
"""

"""
Create group
"""
Xyz1 = Xyz.createGroup('INSTAL_00001'); # [Mandatory] 


"""
Group attributes
"""
Xyz1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory] Date instrument installed
Xyz1.date_valid_to = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Optional]  Date instrument uninstalled
Xyz1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': Installed in <niche>'; # [Optional]  Miscellaneous information about the instrument installation. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments


"""
Pass group variable data
"""
POSY =  np.array([21.4]);
POSZ =  np.array([2.63]); 
POSX = np.array([10.1]);  
POSDATUM = 'Centre point of ship';
ORIENTATION =  np.array([0]);
ORIENTDATUM = 'Bow of ship';
SAMPLEDEPTH = np.array([5.5]);
SAMPLEDATUM = 'Sea level'



"""
Group coordinate variables
"""
# [Mandatory - if X, Y or Z positions are reported]
# [All attributes mandatory if variable created unless stated otherwise]
Positiondatum = Xyz1.createVariable('position_datum','str');
Positiondatum.long_name = 'Instrument position datum';
Positiondatum.sdn_variable_name = 'TBC';
Positiondatum.sdn_variable_url = 'TBC';
Positiondatum[0] = POSDATUM;

# [Mandatory - if an instrument orinetation is reported]
# [All attributes mandatory if variable created unless stated otherwise]
Orientdatum = Xyz1.createVariable('orientation_datum','str');
Orientdatum.long_name = 'Instrument orientation datum';
Orientdatum.sdn_variable_name = 'TBC';
Orientdatum.sdn_variable_url = 'TBC';
Orientdatum[0] = ORIENTDATUM;

# [Mandatory - if a sampling depth is reported]
# [All attributes mandatory if variable created unless stated otherwise]
Sampledatum = Xyz1.createVariable('sample_depth_datum','str');
Sampledatum.long_name = 'Sampling depth datum';
Sampledatum.sdn_variable_name = 'TBC';
Sampledatum.sdn_variable_url = 'TBC';
Sampledatum[0] = SAMPLEDATUM;


"""
Group metadata variables
"""
# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
X = Xyz1.createVariable('x', 'f4', ('NCOLUMNS')) ;
X.long_name = 'x position (positive = forward)' ;
X.sdn_variable_name = 'x'
X.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W02/current/002/' ;
X.units = 'm';
X.sdn_uom_name = 'metres';
X.sdn_uom_url = 'http://vocab.nerc.ac.uk/collection/P06/current/ULAA/';
X.coordinates = 'position_datum';
X[:] = POSX;

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]       
Y = Xyz1.createVariable('y', 'f4', ('NCOLUMNS')) ;
Y.long_name = 'y position (positive = up)' ;
Y.sdn_variable_name = 'y'
Y.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W02/current/003/' ;
Y.units = 'm';
Y.sdn_uom_name = 'metres';
Y.sdn_uom_url = 'http://vocab.nerc.ac.uk/collection/P06/current/ULAA/';
Y.coordinates = 'position_datum';
Y[:] = POSY;             

# [Optional] 
# [All attributes mandatory if variable created unless stated otherwise]
Z = Xyz1.createVariable('z', 'f4', ('NCOLUMNS')) ;
Z.long_name = 'z position (positive = starboard)' ;
Z.sdn_variable_name = 'z'
Z.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W02/current/004/' ;
Z.units = 'm';
Z.sdn_uom_name = 'metres' ;
Z.sdn_uom_url = 'http://vocab.nerc.ac.uk/collection/P06/current/ULAA/';
Z.coordinates = 'position_datum';
Z[:] = POSZ;        

# [Mandatory - if instrument has an orientation] 
# [All attributes mandatory if variable created unless stated otherwise]
Orientation = Xyz1.createVariable('orientation', 'f4', ('NCOLUMNS')) ;
Orientation.long_name = 'Rotational orientation (clockwise) of instrument' ;
Orientation.sdn_variable_name = 'TBC';
Orientation.sdn_variable_url = 'TBC';
Orientation.units = 'degrees';
Orientation.sdn_uom_name = 'degrees';
Orientation.sdn_uom_url = 'http://vocab.nerc.ac.uk/collection/P06/current/UAAA/';
Orientation.coordinates = 'orientation_datum';
Orientation[:] = ORIENTATION;

# [Recommended - if instrument has an orientation]     
# [All attributes mandatory if variable created unless stated otherwise]    
Sampledepth = Xyz1.createVariable('sample_depth', 'f4', ('NCOLUMNS')) ; # sampling depth (e.g. TSG sample intake)
Sampledepth.long_name = 'Depth of sampling point';
Sampledepth.sdn_variable_name = 'TBC';
Sampledepth.sdn_variable_url = 'TBC';
Sampledepth.units = 'm';
Sampledepth.sdn_uom_name = 'metres';
Sampledepth.sdn_uom_url = 'http://vocab.nerc.ac.uk/collection/P06/current/ULAA/';
Sampledepth.coordinates = 'sample_depth_datum';
Sampledepth[:] = SAMPLEDEPTH;



"""
#############################################
GROUP - PLATFORMS [Mandatory]
#############################################
"""

"""
DESCRIPTION: Contains information about the platform(s). Platforms will be linked to deployments. 
Obligations are stated if group is created.
"""

"""
Create group
"""
Plats = rootgrp.createGroup('platforms'); # [Mandatory] 

"""
Group dimensions
"""
Plats.createDimension('NCOLUMNS', 1); # [Mandatory] 

"""
Group attributes
"""

"""
----------------------------------------------------------------------------------------------------------
SUB-GROUP - MOUNTING PLATFORM (/platforms/DISCOVERY) [Mandatory - if group platforms is created]
----------------------------------------------------------------------------------------------------------
"""

"""
Create group
"""
Disco = Plats.createGroup('DISCOVERY'); # [Mandatory] An identifier of your choice as long as it is unique to the file



"""
Group dimensions

DESCRIPTION: Used to create dimensions of more than one row if more than one value in value array needed. 
Create NRECORDSX dimensions as needed where X is the number of rows (e.g. NRECORDS2 = 2 columns). 
This can be done using a loop when creating each variable that firsts checks the length of the array, 
then checks if the dimension exists. Dimensions are ('NRECORDSX','NCOLUMNS') using createVariable.
"""
    # Disco.createDimension('NRECORDSX', X); 


"""
Group attributes
"""
Disco.date_valid_from = datetime(2007, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Recommended] Commission date
Disco.date_valid_to = datetime(2020, 10, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Optional] Decommision date
Disco.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX'; # [Optional]  Miscellaneous information about the platform. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments


"""
Pass group variable data
"""
PLATFORM = np.array(['RRS Discovery']);
PLATFORMMODEL = np.array(['Discovery research vessel']);
PLATFORMMODELID = np.array(['TBC']);
ICESID = np.array(['http://vocab.nerc.ac.uk/collection/C17/current/74EQ/']);
IMOID = np.array(['9588029']);
CALLSIGN = np.array(['2FGX5']); 



"""
Group metadata variables
"""

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Platform = Disco.createVariable('platform_name', 'str', ('NCOLUMNS'));
Platform.long_name = 'Platform name';
Platform.sdn_variable_name = 'Long name' ;
Platform.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0002/';
Platform[:] = PLATFORM;

# [Mandatory] 
# [All attributes mandatory if variable created unless stated otherwise]
Platmod = Disco.createVariable('platform_model_name' ,'str', ('NCOLUMNS'));
Platmod.long_name = 'Model name';
Platmod.sdn_variable_name = 'Model name'; 
Platmod.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0003/';
Platmod[:] = PLATFORMMODEL;

# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Platmod_id = Disco.createVariable('platform_model_id','str', ('NCOLUMNS'));
Platmod_id.long_name = 'Model name identifier';
Platmod_id.sdn_variable_name = 'TBC';
Platmod_id.sdn_variable_url = 'TBC';
Platmod_id[:] = PLATFORMMODELID;

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Ices_id = Disco.createVariable('platform_ices_id','str', ('NCOLUMNS'));
Ices_id.long_name = 'ICES platform code';
Ices_id.sdn_variable_name = 'ICES code';
Ices_id.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0001/';
Ices_id[:] = ICESID;

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Platform_imo_id = Disco.createVariable('platform_imo_id', 'str', ('NCOLUMNS'));
Platform_imo_id.long_name = 'IMO number';
Platform_imo_id.sdn_variable_name = 'TBC';
Platform_imo_id.sdn_variable_url = 'TBC';
Platform_imo_id[:] = IMOID;

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Platform_callsign = Disco.createVariable('platform_callsign','str', ('NCOLUMNS'));
Platform_callsign.long_name = 'Call Sign';
Platform_callsign.sdn_variable_name = 'Call Sign';
Platform_callsign.sdn_variable_url = 'http://vocab.nerc.ac.uk/collection/W07/current/IDEN0010/';
Platform_callsign[:] = CALLSIGN;



# [Optional] Other static properties related to platforms


"""
###################################################
GROUP - DEPLOYMENTS [Mandatory] /deployments
###################################################
"""
"""
DESCRIPTION: Contains information about the Deployment (e.g. cruise). Links platforms and sensors. Obligations are stated.
"""

"""
Create group
"""
Deps = rootgrp.createGroup('deployments'); # [Mandatory]

"""
Group dimensions
"""
Deps.createDimension('NCOLUMNS', 1); # [Mandatory]

"""
Group attributes
"""


"""
-------------------------------------------------------------------------------------
SUB-GROUP - DEPLOYMENT (/deployments/DY122) [Mandatory]
-------------------------------------------------------------------------------------
"""
"""
DESCRIPTION: A deployment of the platform within the deployment group (for example, a cruise)
"""

"""
Create group
"""
Dep1 = Deps.createGroup('DY122'); # [Mandatory] An identifier of your choice as long as it unique to the file. Ideally the cruise ID


"""
Group dimensions

DESCRIPTION: Used to create dimensions of more than one column if more than one value in value array needed. 
Create NRECORDSX dimensions as needed where X is the number of columns (e.g. NRECORDS2 = 2 columns). 
This can be done using a loop when creating each variable that firsts checks the length of the array, 
then checks if the dimension exists. Dimensions are ('NRECORDSX','NCOLUMNS') when using createVariable
"""
Dep1.createDimension('NRECORDS2', 2); 



"""
Group attributes
"""
Dep1.date_valid_from = datetime(2019, 1, 31, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory] Deployment/cruise start date
Dep1.date_valid_to = datetime(2019, 2, 11, 0, 0, 0, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z'); # [Mandatory - if deployment end date known]
Dep1.comment = '\n'+datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')+': XXXXX'; # [Optional]  Miscellaneous information about the deployment. Use newline characters to break comments. Append date of each comment. Only add attribute if there are comments




"""
Pass group variable data
"""
DEPLOYMENT = np.array(['DY122']); 
INSTITUTION = np.array(['National Oceanography Centre, Liverpool']) ;
INSTITUTIONID = np.array(['http://vocab.nerc.ac.uk/collection/B75/current/ORG00003/']) ;
CAMPAIGN = np.array(['OSMOSIS']);
PLATS = np.array(['/platforms/DISCOVERY']);
INSTS = np.array(['/instruments/TOOL0022_2490','/instruments/TOOL0349_4444444x56']);

"""
Group metadata variables
"""
# [Mandatory]
# [All attributes mandatory if variable created unless stated otherwise]
Deployment_id = Dep1.createVariable('Deployment_id','str',('NCOLUMNS'));
Deployment_id.long_name = 'Deployment identifier'
Deployment_id.sdn_variable_name = 'TBC';
Deployment_id.sdn_variable_url = 'TBC'
Deployment_id[:] = DEPLOYMENT;

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Owner = Dep1.createVariable('owner', 'str', ('NCOLUMNS'));
Owner.long_name = 'Institution name';
Owner.sdn_variable_name = 'Owner';
Owner.sdn_variable_url = 'TBC';
Owner[:] = INSTITUTION;

# [Recommended] 
# [All attributes mandatory if variable created unless stated otherwise]
Owner_id = Dep1.createVariable('owner_id', 'str', ('NCOLUMNS'));
Owner_id.long_name = 'Institution identifier';
Owner_id.sdn_variable_name = 'TBC';
Owner_id.sdn_variable_url = 'TBC';
Owner_id[:] = INSTITUTIONID;

# [Optional] 
# [All attributes mandatoB75ry if variable created unless stated otherwise]
Campaign_name = Dep1.createVariable('campaign_name', 'str', ('NCOLUMNS'));
Campaign_name.long_name = 'Campaign name';
Campaign_name.sdn_variable_name = 'TBC';
Campaign_name.sdn_variable_url = 'TBC';
Campaign_name[:] = CAMPAIGN;

# [Mandatory] 
# [All attributes mandatory if variable created unless stated otherwise]
Platforms = Dep1.createVariable('platforms', 'str', ('NCOLUMNS'));
Platforms.long_name = 'platforms';
Platforms[:] = PLATS;

# [Mandatory] 
# [All attributes mandatory if variable created unless stated otherwise]
Instruments = Dep1.createVariable('instruments', 'str', ('NRECORDS2','NCOLUMNS'));
Instruments.long_name = 'instruments';
Instruments[:] = INSTS;


"""
----------------------
CLOSE
----------------------
"""

rootgrp.close();


