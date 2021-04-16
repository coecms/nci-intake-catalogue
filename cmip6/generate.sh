#!/bin/bash
#  Copyright 2021 Scott Wales
#
#  \author  Scott Wales <scott.wales@unimelb.edu.au>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

find /g/data/fs38/publications/CMIP6 -not -type d -not -path \*/files/\* -name \*.nc > listing.fs38
find /g/data/oi10/replicas/CMIP6 -not -type d -not -path \*/files/\* -name \*.nc > listing.oi10

cat listing.fs38 listing.oi10 | sort | ./to_csv.py
