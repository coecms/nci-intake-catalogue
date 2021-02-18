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

path_to_parameter = {
    "lai-hv": "lai_hv",
    "lai-lv": "lai_lv",
}

parameter_to_var = {
    "2d": "d2m", 
    "swh1": "p140121", 
    "mwd1": "p140122", 
    "mwp1": "p140123", 
    "swh2": "p140124", 
    "mwd2": "p140125", 
    "mwp2": "p140126", 
    "swh3": "p140127", 
    "mwd3": "p140128", 
    "mwp3": "p140129", 
    "wstar": "p140208", 
    "rhoao": "p140209", 
    "vima": "p53.162", 
    "vit": "p54.162", 
    "vike": "p59.162", 
    "vithe": "p60.162", 
    "vipie": "p61.162", 
    "vipile": "p62.162", 
    "vitoe": "p63.162", 
    "viec": "p64.162", 
    "vimae": "p65.162", 
    "viman": "p66.162", 
    "vikee": "p67.162", 
    "viken": "p68.162", 
    "vithee": "p69.162", 
    "vithen": "p70.162", 
    "viwve": "p71.162", 
    "viwvn": "p72.162", 
    "vige": "p73.162", 
    "vign": "p74.162", 
    "vitoee": "p75.162", 
    "vitoen": "p76.162", 
    "vioze": "p77.162", 
    "viozn": "p78.162", 
    "vilwd": "p79.162", 
    "viiwd": "p80.162", 
    "vimad": "p81.162", 
    "viked": "p82.162", 
    "vithed": "p83.162", 
    "viwvd": "p84.162", 
    "vigd": "p85.162", 
    "vitoed": "p86.162", 
    "viozd": "p87.162", 
    "vilwe": "p88.162", 
    "vilwn": "p89.162", 
    "viiwe": "p90.162", 
    "viiwn": "p91.162", 
    "vimat": "p92.162", 
    "10si": "si10", 
    "ci": "siconc", 
    "2t": "t2m", 
    "10u": "u10", 
    "100u": "u100", 
    "10v": "v10", 
    "100v": "v100",
}

with open('catalogue.json') as f:
    meta = json.load(f)
    fieldnames = [a['column_name'] for a in meta['attributes']]
    fieldnames.append(meta['assets']['column_name'])


with open('listing') as f_in, open('catalogue.csv', mode='w', newline='') as f_out:
    
    csv_w = csv.DictWriter(f_out, fieldnames, dialect='unix')
    csv_w.writeheader()

    for path in f_in:
        parts = path.split('/')

        try:
            record = {'path': path.strip()}

            record['sub_collection'] = parts[4]
            record['product_type'] = parts[5]
            record['parameter'] = path_to_parameter.get(parts[6], parts[6])
            record['year'] = parts[7]

            basename = parts[-1]
            record['startdate'] = basename.split('_')[-1][:8]
            record['month'] = int(record['startdate'][4:6])

            record['file_variable'] = parameter_to_var.get(record['parameter'], record['parameter'])

            csv_w.writerow(record)
        except Exception:
            print(path)



