# Feature reporter

"Feature reporter" comes from the need to provide MS Word reports to customer.

It aims to pretty print a set of plain text `.feature` files into one shareable document.

Optionally, it adds the last automated execution of these scenarios.

**Please note!** This package heavily relies on the [Behave package](https://behave.readthedocs.io/en/stable/) in order 
to process feature file and execution results format.

Moreover, it provides a basic behave csv formatter. You can:

- have a csv result for each scenario.
- have a csv list of each scenario using the behave's dry run option.

In my feature file I usually add a tag for the epic's name (`@epic=`) and a scenario id (`@id=`).

The csv formatter use these tag by default. Please see below for more details on usage.

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

usage: featurereporter.py [-h] [--tag TAG] [--title TITLE] [--repository REPOSITORY] [--forewords FOREWORDS] [--output OUTPUT] [--execution EXECUTION] [--license]

optional arguments:
  -h, --help            show this help message and exit
  --tag TAG             Invariant pointing to a user story
  --title TITLE         The document's title
  --repository REPOSITORY
                        The folder where the feature files are
  --forewords FOREWORDS
                        The folder where forewords markdown files are. It is not a recursive discovery.
  --output OUTPUT       The filename the docu
  --execution EXECUTION
                        Behave plain test output in order to also print the last execution result
  --license             Display the license.


```
 
```commandline
python3 -m featurereporter --repository path/to/the/feature/files/folder
```

### Embedded features

#### Feature description

All descriptions can use Markdown syntax to enhance the report display in docx.

- The matching `[Bb]usiness [Rr]ules` will be replaced by a title with the correct depth `Business rules`
- The matching sequence `!!Worflow:\s*([\.\d\w\-\_\\\/]*)\s*` points out a puml diagram which will be generated on the fly. 
The puml file path is relative to the feature folder holder. For example `!!Workflow: ../business/workflow.puml` will generate the `workflow.puml` diagram in the `business` folder of the feature parent folder. 


#### Forewords inclusion

You can include markdown files as a "Forewords" section. They will be processed in alphabetical order.

- Picture inclusion will be resized to fit the document page.
- `!!Worflow:\s*([\.\d\w\-\_\\\/]*)\s*` does the same as for feature description. However, the base folder is the forewords' folder.

#### Result inclusion

You can include the full list of the documentation execution results. It's based on Behave's plain output reporter.

It generates a circular graph (*passed*, *failed*, *skipped*) and list each scenario result.

There is no control on the sections order nor ability to display only *failed* scenarios.

## Additional installation

Currently, all puml schema are processed using the GraphViz library. Your system needs [java](https://www.java.com/en/download/) and [GraphViz](https://graphviz.org/download/).

The plantuml's jar version is 1.2022.1. Please see [PlantUml page](https://plantuml.com/en/).


## Behave csv formatter

To use the default setting just use the following (`-d` is for dry-run)

```commandline
behave -d -f featurereporter.csvformatter:EaiCsv -o output.csv
```

Add in `behave.ini` the following to update the tag setting. You can have a `=` symbol in your tag definition.

```ini
[behave.userdata]
EaiCsv.epic = my_epic_tag
EaiCsv.scenario = my_scenario_id_tag
```


The csv output is 

```csv
epic, feature, scenario_id, scenario, status, order
"epic name fetched from the epic's tag", "feature name", "scenario id fetched from the id's tag", "scenario name", "execution status", "order for outline scenario"
```

The first line contains the csv header.


## Behave csv 'full' formatter

To use the default setting just use the following (`-d` is for dry-run).

**Please mind** this formatter is for dry-run only.

```commandline
behave -d -f featurereporter.csvformatter:EaiCsvFull -o output.csv
```

Add in `behave.ini` the following to update the tag setting. You can have a `=` symbol in your tag definition.

```ini
[behave.userdata]
EaiCsv.epic = my_epic_tag
EaiCsv.scenario = my_scenario_id_tag
```


The csv output is 

```csv
epic, feature_filename, feature_name, feature_tags, feature_description, scenario_id, scenario_name, scenario_tags, scenario_description, scenario_is_outline, scenario_steps
"epic name", "feature filename", "feature name (following the 'Feature:' element)", "feature tags", "feature description", "scenario id fetched from the id's tag", "scenario name", "scenario tags", "scenario description", "True if the scenario is an outline one", "scenario's steps without background"
```

The first line contains the csv header.

## Disclaimer

This tool is still under development. There is currently **no** arguments control nor formal tests.

I use it in my daily work to produce report.

Please contact me for any concern.