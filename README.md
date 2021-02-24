# NCI Data Collection Intake Catalogue

## Usage

The catalogue is available in intake's default catalogue list in the CLEX Conda
environment

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
