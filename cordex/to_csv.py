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

# /g/data/rr3/publications/CORDEX/output/AUS-44i/CSIRO/CNRM-CERFACS-CNRM-CM5/historical/r1i1p1/CSIRO-CCAM-1704/v1/day/cll/files/d20201123/cll_AUS-44i_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_CSIRO-CCAM-1704_v1_day_19900101-19901231.nc
# directory_format_template_ = %(root)s/%(project)s/%(product)s/%(domain)s/%(institute)s/%(driving_model)s/%(experiment)s/%(ensemble)s/%(rcm_model)s/%(rcm_version)s/%(time_frequency)s/%(variable)s/%(version)s 
# filename_format_template = %(variable)s_%(domain)s_%(driving_model)s_%(experiment)s_%(ensemble)s_%(rcm_model)s_%(rcm_version)_%(time_frequency)s_%(date_range)s.nc

pattern = re.compile(
    r'^(?P<path>/g/data/(rr3/publications|al33/replicas)/'+
    r'(?P<project>[^/]+)/'+
    r'(?P<product>[^/]+)/'+
    r'(?P<domain>[^/]+)/'+
    r'(?P<institute>[^/]+)/'+
    r'(?P<driving_model>[^/]+)/'+
    r'(?P<experiment>[^/]+)/'+
    r'(?P<ensemble>[^/]+)/'+
    r'(?P<rcm_model>[^/]+)/'+
    r'(?P<rcm_version>[^/]+)/'+
    r'(?P<time_frequency>[^/]+)/'+
    r'(?P<variable>[^/]+)/'+
    r'(?P<version>[^/]+)/'+
    r'(?P=variable)_'+
    r'(?P=domain)_'+
    r'(?P=driving_model)_'+
    r'(?P=experiment)_'+
    r'(?P=ensemble)_'+
    r'([^/]+)_'+ # not rcm_model from the path
    r'([^/]+)_'+ # Not rcm_version from the path
    r'(?P=time_frequency)'+
    r'(_(?P<date_range>.*))?\.nc)$')
#    r'.*)$')


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

        # print(record)

        csv_w.writerow(record)

