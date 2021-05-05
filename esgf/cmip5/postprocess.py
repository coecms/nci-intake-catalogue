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

import pandas
import requests
import yaml
import json

with open("ingest.yaml") as f:
    config = yaml.safe_load(f)
    config_post = config.get('postprocess',{})

df = pandas.read_csv("catalogue.csv.xz")

def rename(x, col):
    return config_post['rename'][col].get(x, x)

if config_post['esgf_project'] == 'CMIP5':
    df['model'] = df['model_id'].apply(rename, col='model')
    df['institute'] = df['institute_id'].apply(rename, col='institute')

df.to_csv("catalogue.csv.xz", index=False)

# Validate facets
project = config_post['esgf_project']
exclude = config_post['esgf_exclude']
columns = [c for c in df.columns if c not in exclude]

def esgf_facets(column):
    params = {}
    params["project"] = project
    params["facets"] = column
    params["limit"] = 0
    params["format"] = "application/solr+json"

    r = requests.get('https://esgf.nci.org.au/esg-search/search', params=params)
    r.raise_for_status()

    return r.json()['facet_counts']['facet_fields'][column][::2]

diffs = {}
for c in columns:
    esgf = set(esgf_facets(c))
    local = set(df[c].unique())

    diff = local - esgf
    if len(diff) > 0:
        diffs[c] = diff

if len(diffs) > 0:
    print("Renames needed in ingest.yaml:")
    print("---")
    print("rename:")
    for c, diff in diffs.items():
        print(f'    {c}:')
        for v in sorted(diff):
            print(f'        {v}: none')
    print("---")


# Create catalogue_latest.csv.xz
columns = [c for c in df.columns if c not in ['version', 'path']]
latest = df.groupby(columns).last().reset_index()
latest.to_csv('catalogue_latest.csv.xz', index=False)

# Create catalogue_latest.json
with open('catalogue.json') as f:
    cat = json.load(f)
cat['id'] = config_post['latest']['id']
cat['description'] = config_post['latest']['description']
cat['catalog_file'] = 'catalogue_latest.csv.xz'
with open('catalogue_latest.json', 'wt') as f:
    json.dump(cat, f, indent=2)

# Update the catalogue one level up
try:
    with open('../catalogue.yaml') as f:
        cat = yaml.safe_load(f)
except FileNotFoundError:
    cat = {'metadata': {'version': 1}, 'sources': {}}

cat['sources'][config['id']] = {
        'description': config['title']+'\n\n'+config['description'],
        'driver': 'intake_esm.esm_datastore',
        'args': {'esmcol_obj': '{{CATALOG_DIR}}/'+config_post['latest']['id']+'/catalogue.json'}
    }
cat['sources'][config_post['latest']['id']] = {
        'description': config_post['latest']['title']+'\n\n'+config_post['latest']['description'],
        'driver': 'intake_esm.esm_datastore',
        'args': {'esmcol_obj': '{{CATALOG_DIR}}/'+config_post['latest']['id']+'/catalogue_latest.json'}
    }

with open('../catalogue.yaml','wt') as f:
    yaml.dump(cat, f)

