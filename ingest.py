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

import yaml
import subprocess
import tempfile
import re
import lzma
import csv
import shlex
import json
import jsonschema

with open("ingest.yaml") as f:
    config = yaml.safe_load(f)

schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'title': {'type': 'string'},
        'description': {'type': 'string'},
        'find': {
            'type': 'object',
            'properties': {
                    'paths': {
                        'type': 'array',
                        'items': {'type': 'string'}
                        },
                    'options': {'type': 'string'}
                },
            'required': ['paths'],
            },
        'drs': {'type': 'string'},
        'assets': {'type': 'object'},
        'aggregation_control': {'type': 'object'},
        'rename': {
            'type': 'object',
            'patternProperties': {
                    '.*': {
                        'type': 'object',
                        'patternProperties': {
                            '.*': {'type': 'string'}
                            },
                        },
                    },
            },
        'postprocess': {'type': 'object'},
        },
    'required': ['id','description','find','drs'],
}

jsonschema.validate(config, schema)

drs_re = re.compile(config["drs"], re.VERBOSE)

find_command = [
    "/bin/find",
    *config["find"]["paths"],
    *shlex.split(config["find"].get("options", "")),
]
print(shlex.join(find_command))

with tempfile.TemporaryFile('w+') as f, tempfile.TemporaryFile('w+') as s, lzma.open(
    "catalogue.csv.xz", mode="wt", newline=""
) as out, lzma.open('errors.xz', mode='wt') as e:

    # Find files
    print("Finding Files...")
    find = subprocess.run(find_command, stdout=f)
    find.check_returncode()
    f.seek(0)

    # Sort the results
    print("Sorting Files...")
    sort = subprocess.run(["/bin/sort"], stdin=f, stdout=s)
    sort.check_returncode()
    s.seek(0)

    # Get the column names
    columns = None
    for path in s:
        match = drs_re.match(path)
        if match is None:
            continue
        columns = list(match.groupdict().keys())
        break
    s.seek(0)

    # Write catalogue.csv.xz
    print("Writing Catalogue...")
    csv_w = csv.DictWriter(out, columns, dialect='unix')
    csv_w.writeheader()
    for path in s:
        match = drs_re.match(path)
        if match is None:
            print('ERROR',path.strip())
            e.write(path)
            continue
        record = match.groupdict()

        for col, renames in config.get('rename', {}).items():
            if record.get(col, None) in renames:
                record[col] = renames[record[col]]

        csv_w.writerow(record)

# Setup catalogue.json
# Drop extra config items
config.pop('find')
config.pop('drs')
config.pop('rename', None)
config.pop('postprocess', None)

config['esmcat_version'] = '0.1.0'
config['catalog_file'] = 'catalogue.csv.xz'
config['attributes'] = [{'column_name': c} for c in columns if c != config['assets']['column_name']]

with open('catalogue.json', 'w') as f:
    json.dump(config,f,indent=2)
