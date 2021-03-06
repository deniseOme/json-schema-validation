
# JSON Schema Validation

## Table of contents

- [Introduction](#introduction)
- [Quick start](#quick-start)
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Copyright and license](#copyright-and-license)

## Introduction

Selected Open Targets projects from the Wellcome Trust Sanger Institute and the EMBL-EBI submits computationally generated, human curated and experimentally derived data
containing evidence linking genes to common and rare diseases. 
Submitted Open Targets Data must be validated against the JSON Schema that specifies how the information should be exchanged between providers and the Open Targets.

The json-schema-validation python package was developed to support the Open Targets data collection process.
An existing python project called [python_jsonschema_objects] (https://github.com/cwacek/python-jsonschema-objects) automatically binds classes to JSON schemas 
for use in python. This can be used to validate a specific JSON file on the fly. This will also create python classes on the fly that can be instanciated.

We have developed a similar python project except that the validation is customised to Open Targets requirements and the classes that bind to JSON schema objects are generated before
with custom validation procedures.

## Quick start

First, install tox with 'pip install tox' or 'easy_install tox'. Tox is a generic virtualenv management and test command line tool that 
Open Targets use for running tests and for continuous integration of the software components we develop.

The Open Targets validation package is generated by a python script called ```modelgenerator.py```
Run this program to generate the Open Targets classes representing the different types of evidence strings (e.g. genetics, drugs, literature, evidence, bioentities).

## Validating JSON files

Once the current version of the validation package is installed, you can test the validation of an existing Open Targets datasource by running the program called modelvalidator.py

```shell
gunzip -c <PATH TO FILE>/cttv018_ibd_gwas_20141128_formatted.json.gz | python modelvalidator.py
```

## Bugs and feature requests

Have a bug or a feature request?

## Author

Gautier Koscielny

## Copyright and license
Copyright 2014-2018 Biogen, Celgene Corporation, EMBL - European Bioinformatics Institute, GlaxoSmithKline, Takeda Pharmaceutical Company and Wellcome Sanger Institute

This software was developed as part of the Open Targets project. For more information please see: http://www.opentargets.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
