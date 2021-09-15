#!/g/data/hh5/public/apps/nci_scripts/python-analysis3
# Copyright 2021 Paola Petrelli 
# author: Paola Petrelli <paola.petrelli@utas.edu.au>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas
import yaml
import json
import numpy as np


# Read current csv and fixed variables catalogue
df = pandas.read_csv("catalogue.csv.xz")
dffix = pandas.read_csv("cat_fix.csv")

# Concatenate the two tables
df = pandas.concat([df,dffix])

# Add experiment (forecast/analysis/land) and
# level (surface/pressure/model/potential vorticity and potential temperature) based on mode value
df['level'] = 'surface'
df['level'] = df['level'].where(df['mode'] != 'an-pl', 'pressure')
df['level'] = df['level'].where(df['mode'] != 'an-ml', 'model')
df['level'] = df['level'].where(df['mode'] != 'an-pt', 'potential temperature')
df['level'] = df['level'].where(df['mode'] != 'an-pv', 'potential vorticity')
df['product'] = 'analysis'
df['product'] = df['product'].where(df['mode'] != 'fc-sfc', 'forecast')
df['product'] = df['product'].where(df['mode'] != 'land', 'land')

# Read csv file of ECMWF parameters tables 128 and 162, and current catalogue
table = pandas.read_csv("ecmwf_param_table.csv", sep=":")

# Join two tables based on cmor_name column in ECMWF tanle
# NB not all the variables in tables have a cmor_name assigned, but all the ones for which we have data should
# If a valid CMOR name didn't exist for the variable the lowercase ECMWF name has been used, as variable name
# This will add the following columns to the catalogue:
#  standard_name, long_name, parameter (grib code), ecmwf_name, cell_methods

df  = df.join(table.set_index('cmor_name'), on='variable')

# Save updated catalogue.csv.xz
df = df.drop(['Unnamed: 0', 'index'], axis=1)
df.to_csv('catalogue.csv.xz', index=False)

# Update catalogue.json
with open('catalogue.json') as f:
    cat = json.load(f)
cat['aggregation_control']['groupby_attrs'].extend(['parameter', 'standard_name', 'ecmwf_name','level','product'])
cat['attributes'].extend([
     {
      "column_name": "standard_name"
    },
     {
      "column_name": "ecmwf_name"
    },
     {
      "column_name": "level"
    },
     {
      "column_name": "product"
    },
    {
      "column_name": "parameter"
    }])
with open('catalogue.json', 'wt') as f:
    json.dump(cat, f, indent=2)

