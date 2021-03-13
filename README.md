# Feature reporter

"Feature reporter" comes from the need to provide MS Word reports to customer.

It aims to pretty print a set of plain text `.feature` files into one shareable document.

Optionally, it adds the last automated execution of these scenarios.

**Please note!** This package heavily relies on the [Behave package](https://behave.readthedocs.io/en/stable/) in order 
to process feature file and execution results format.

## Installation 

```
pip install eaiscenarioreporter
```

## Usage

### From a python shell

```python
from featurereporter import ExportUtilities

my_export = ExportUtilities()

my_export.feature_repository = "path/to/the/feature/files/folder"

my_export.create_application_documentation()

# Create the demo.docx document in the current folder.
```

### From the command line

#### GUI (experimental)

You can start the reporter's GUI using the following command :

```commandline
python3 -m featurereporter
```

#### CLI 

Feature reporter can be called directly from the command line.

```
# Display help
> python3 -m featurereporter -h

usage: featurereporter.py [-h] [--tag TAG] [--title TITLE] [--repository REPOSITORY] [--output OUTPUT] [--execution EXECUTION] [--license]

optional arguments:
  -h, --help            show this help message and exit
  --tag TAG             Invariant pointing to a user story
  --title TITLE         The document's title
  --repository REPOSITORY
                        The folder where the feature files are
  --output OUTPUT
  --execution EXECUTION
                        Behave plain test output in order to also print the last execution result
  --license             Display the license.

```
 
```commandline
python3 -m featurereporter --repository path/to/the/feature/files/folder
```

## Disclaimer

This tool is still under development. There is currently **no** arguments control nor formal tests.

I use it in my daily work to produce report.

Please contact me for any concern.