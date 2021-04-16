#!/g/data/hh5/public/apps/nci_scripts/python-analysis3
# Copyright 2021 Scott Wales
# author: Scott Wales <scott.wales@unimelb.edu.au>
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

import csv
import json
import re
import sys
import lzma

# /g/data/fs38/publications/CMIP6/C4MIP/CSIRO/ACCESS-ESM1-5/1pctCO2-bgc/r1i1p1f1/Emon/nLitter/gn/v20191118/nLitter_Emon_ACCESS-ESM1-5_1pctCO2-bgc_r1i1p1f1_gn_010101-025012.nc
#   C4MIP           - activity_id
#   CSIRO           - institution_id
#   ACCESS-ESM1-5   - source_id
#   1pctCO2-bgc     - experiment_id
#   r1i1p1f1        - member_id
#   Emon            - table_id
#   nLitter         - variable_id
#   gn              - grid_label
#   v20191118       - version
#   nLitter         - variable_id
#   Emon            - table_id
#   ACCESS-ESM1-5   - source_id
#   1pctCO2-bgc     - experiment_id
#   r1i1p1f1        - member_id
#   gn              - grid_label
#   010101-025012   - date_range

pattern = re.compile(
    r'^(?P<path>/g/data/(fs38/publications|oi10/replicas)/CMIP6/'+
    r'(?P<activity_id>[^/]+)/'+
    r'(?P<institution_id>[^/]+)/'+
    r'(?P<source_id>[^/]+)/'+
    r'(?P<experiment_id>[^/]+)/'+
    r'(?P<member_id>[^/]+)/'+
    r'(?P<table_id>[^/]+)/'+
    r'(?P<variable_id>[^/]+)/'+
    r'(?P<grid_label>[^/]+)/'+
    r'(?P<version>[^/]+)/'+
    r'(?P=variable_id)_'+
    r'(?P=table_id)_'+
    r'(?P=source_id)_'+
    r'(?P=experiment_id)_'+
    r'(?P=member_id)_'+
    r'(?P=grid_label)'+
    r'(_(?P<date_range>.*))?\.nc)$')


with open('catalogue.json') as f:
    meta = json.load(f)
    fieldnames = [a['column_name'] for a in meta['attributes']]
    fieldnames.append(meta['assets']['column_name'])


with lzma.open('catalogue_all.csv.xz', mode='wt', newline='') as f_out:
    csv_w = csv.DictWriter(f_out, fieldnames, dialect='unix')
    csv_w.writeheader()

    for path in sys.stdin:
        match = pattern.match(path)

        if match is None:
            print('ERROR',path)
            continue

        record = match.groupdict()

        csv_w.writerow(record)

