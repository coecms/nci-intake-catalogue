# NCI Data Collection Intake Catalogue

## Usage

The catalogue is available in intake's default catalogue list in the CLEX Conda
environment
Two notebooks are provided in the docs folder showing how to access the ERA5 and CIP6 datasets.  

```python
import intake

print(list(intake.cat.nci))
```

Individual datasets are catalogued using intake-esm

## Admin

This catalogue exists on Gadi's filesystem under /g/data/hh5/public/apps/nci-intake-catalogue

Use `git pull` to download changes from Github

Catalogue csv listings themselves need to be generated, they are not in the
repository due to their size. This may be done by running `make` within the
directory

The intake data package is under the directory `package/`, it simply provides
an intake entry point pointing to the catalogue directory


## Contributing

If you would like to contribute you can clone the repository, create a new branch to work on. Once you added a new dataset push your new branch and create a amerge request.

## Adding a new dataset listing 

To add a new dataset you need:

* add the main dataset metadata to the catalogue.yaml file
* create a directory for the dataset
* add here a catalogue.csv.xz file listing all files or a code to generate one on the fly

The catalogue.yaml file lists the main metadata for each dataset:

```yaml
    erai:
        description: |
                Replica of ERA Interim reanalysis ... 

        Project: ub4
        Maintained By: CLEX
        Contact: cws_help@nci.org.au
        Documentation: http://climate-cms.wikis.unsw.edu.au/ERA_INTERIM
        License: https://creativecommons.org/licenses/by/4.0/
        References:
                -  https://apps.ecmwf.int/datasets/data/interim-full-daily/licence/
        driver: intake_esm.esm_datastore
        args:
            esmcol_obj: '{{CATALOG_DIR}}/erai/catalogue.json' 
```

The catalogue.csv.xz file is a compressed csv file that lists every file in the dataset and the corresponding values for each of attributes defined for the dataset.
As an example a snippet of the catalogue for the erai dataset:

```csv
path,frequency,realm,version,variable,mode,date_range,level,product,code,ecmwf_name,long_name,standard_name,cell_methods,parameter
/g/data/ub4/erai/netcdf/3hr/atmos/oper_fc_sfc/v01/blh/blh_3hrs_ERAI_historical_fc-sfc_19790101_19790131.nc,3hr,atmos,v01,blh,fc-sfc,19790101_19790131,surface,forecast,159,BLH,Boundary layer height [m],,,159.128
...
```

As mentioned above, you can provide this list but especially if you're dealing with big datasets or datasets that are regularly updated it is easier to provide a code to generate this on the fly.
all the code ingest.yaml, you can see examples in the existing dataset directories.

The ingest.yaml is composed of 4 main sections:
* The main dataset metadata, as added to the main catalogue.yaml
* `find` section where you define the main path and any "find" options

```yaml
find:
    paths:
        - /g/data/ub4/erai/netcdf/
    options: -not -type d -not -path */fx/* -name *.nc
```

* `drs` section where you can use Python regular expression to retrieve attributes from the directory structure and filenames
```yaml
drs: |
    ^(?P<path>
    /g/data/ub4/erai/netcdf
    /(?P<frequency>[^/]+)             # /3hr
    /(?P<realm>[^/]+)                 # /atmos
    ...
```
 
* `assets` section, here the `path` is added as an attribute column, all the others are automatically generated based on the DRS pattern. This is also where the attributes used to groupby and aggregate the data are defined.

```yaml
assets:
    column_name: path
    format: netcdf
aggregation_control:
    # Name of the variable in the file
    variable_column_name: variable
    # Grouping keys are made of these columns, joined by '.'
    groupby_attrs:
        - realm
        - frequency
        - variable
        - version
    aggregations:
        # Join along the existing time dimension
        - type: join_existing
          attribute_name: date_range
          options:
              dim: time
```

Sometimes you need to do some further processing of the attributes you can derived from the DRS in that case you can do that by coding in a postprocess.py script. You add this script and any input files that you might need in the dataset directory, this will be automatically run after the ingest.yaml. There are examples both in the cmip5 and erai datasets. 

More information is available in the official [intake-esm](https://intake-esm.readthedocs.io/en/latest/) documentation.
