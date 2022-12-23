# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import csv
import re
import logging

from behave.formatter.base import Formatter
from behave.model import Status
from csv import DictWriter

log = logging.getLogger(__name__)


class EaiCsv(Formatter):
    name = "eaicsv"
    description = """Basic csv formatter for bulk insertion.
    Epic tag discrimination is controlled by userdata EaiCsv.epic (default 'epic=')
    Scenario id tag discrimination is controlled by userdata EaiCsv.scenario (default 'id=')
    """

    def __init__(self, stream_opener, config, **kwargs):
        super(EaiCsv, self).__init__(stream_opener, config)
        self.__result = []
        self.__current_feature = None
        self.__current_epic = None
        self.__current_scenario_name = None
        self.__current_scenario_id = None
        self.__current_status = None
        self.__outline_order = None
        # UserData
        if "userdata" in config.defaults and "EaiCsv.epic" in config.defaults["userdata"]:
            self.__epic = config.defaults["userdata"]["EaiCsv.epic"]
        else:
            self.__epic = "epic="

        if "userdata" in config.defaults and "EaiCsv.scenario" in config.defaults["userdata"]:
            self.__scenario_id = config.defaults["userdata"]["EaiCsv.scenario"]
        else:
            self.__scenario_id = "id="
        # -- ENSURE: Output stream is open.
        self.stream = self.open()

    def feature(self, feature):
        self.__current_feature = feature.name
        for tag in feature.tags:
            self.__current_epic = None
            if self.__epic in tag:
                self.__current_epic = tag.replace(self.__epic, "")
                break

    def scenario(self, scenario):
        if self.__current_status is not None:
            self.add_result()
        self.__current_status = Status.undefined
        if "Outline" not in scenario.keyword:
            self.__current_scenario_name = scenario.name
            self.__outline_order = None
        else:
            match = re.match(r'(?P<name>[\d\w\s]*) -- @(?P<order>\d+\.\d+) (?P<subname>.*)',
                             scenario.name)
            self.__current_scenario_name = f'{match["name"]}-{match["subname"]}'
            self.__outline_order = match["order"]
        for tag in scenario.tags:
            self.__current_scenario_id = None
            if self.__scenario_id in tag:
                self.__current_scenario_id = tag.replace(self.__scenario_id, "")
                if self.__outline_order is not None:
                    self.__current_scenario_id = (f"{self.__current_scenario_id}-"
                                                  f"{self.__outline_order}")
                break

    def add_result(self):
        log.info(f"Add scenario {self.__current_scenario_id} to result")
        self.__result.append({"epic": self.__current_epic,
                              "feature_name": self.__current_feature,
                              "scenario_id": self.__current_scenario_id,
                              "scenario_name": self.__current_scenario_name,
                              "status": self.__current_status,
                              "order": self.__outline_order})
        self.__current_status = None

    def result(self, step):
        converter = {f"{Status.failed}": "failed",
                     f"{Status.executing}": "executing",
                     f"{Status.passed}": "passed",
                     f"{Status.skipped}": "skipped",
                     f"{Status.undefined}": "undefined",
                     f"{Status.untested}": "untested"}
        self.__current_status = converter[str(step.status)]

    def eof(self):
        self.add_result()

    def close(self):
        self.stream.reconfigure(newline="")
        writer = DictWriter(self.stream, ["epic",
                                          "feature_name",
                                          "scenario_id",
                                          "scenario_name",
                                          "status",
                                          "order"],
                            quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(self.__result)


class EaiCsvFull(Formatter):
    name = "eaicsv"
    description = """Csv formatter for epic, feature, scenario bulk insertion.
    Use it on dry-run only.
    Epic tag discrimination is controlled by userdata EaiCsv.epic (default 'epic=')
    Scenario id tag discrimination is controlled by userdata EaiCsv.scenario (default 'id=')
    """

    def __init__(self, stream_opener, config, **kwargs):
        super(EaiCsvFull, self).__init__(stream_opener, config)
        self.__result = []
        self.__features = []
        self.__epics = set()
        self.__current_feature = None
        self.__current_epic = None
        self.__current_scenario_name = None
        self.__current_scenario_id = None
        self.__current_status = None
        self.__outline_order = None
        self.__current_feature_model = None
        self.__current_scenario_model = None
        # UserData
        if "userdata" in config.defaults and "EaiCsv.epic" in config.defaults["userdata"]:
            self.__epic = config.defaults["userdata"]["EaiCsv.epic"]
        else:
            self.__epic = "epic="

        if "userdata" in config.defaults and "EaiCsv.scenario" in config.defaults["userdata"]:
            self.__scenario_id = config.defaults["userdata"]["EaiCsv.scenario"]
        else:
            self.__scenario_id = "id="
        # -- ENSURE: Output stream is open.
        self.stream = self.open()

    def feature(self, feature):
        self.__current_feature = feature.name
        for tag in feature.tags:
            self.__current_epic = None
            if self.__epic in tag:
                self.__current_epic = tag.replace(self.__epic, "")
                break
        self.__current_feature_model = FeatureModel(feature.name,
                                                    feature.filename,
                                                    self.__current_epic,
                                                    feature.tags,
                                                    feature.description)
        self.__epics.add(self.__current_epic)
        self.__features.append(self.__current_feature_model.to_dict())

    def scenario(self, scenario):
        if self.__current_status is not None:
            self.add_result()
        self.__current_status = Status.undefined
        if "Outline" not in scenario.keyword:
            self.__current_scenario_name = scenario.name
            self.__outline_order = None
        else:
            match = re.match(r'(?P<name>[\d\w\s]*) -- @(?P<order>\d+\.\d+) (?P<subname>.*)',
                             scenario.name)
            self.__current_scenario_name = f'{match["name"]}-{match["subname"]}'
            self.__outline_order = match["order"]
        for tag in scenario.tags:
            self.__current_scenario_id = None
            if self.__scenario_id in tag:
                self.__current_scenario_id = tag.replace(self.__scenario_id, "")
                break
        if self.__outline_order:
            self.__current_scenario_model = ScenarioModel(
                f"{self.__current_scenario_id}-{self.__outline_order}",
                self.__current_scenario_name,
                self.__current_feature_model.filename,
                scenario.tags,
                scenario.description,
                True
            )
        else:
            self.__current_scenario_model = ScenarioModel(
                self.__current_scenario_id,
                self.__current_scenario_name,
                self.__current_feature_model.filename,
                scenario.tags,
                scenario.description,
                False)

    def add_result(self):
        log.info(f"Add scenario {self.__current_scenario_id} to result")
        self.__result.append(self.__current_scenario_model.to_dict())
        self.__current_status = None

    def step(self, step):
        self.__current_scenario_model.steps = f"{step.keyword} {step.name}"

    def result(self, step):
        converter = {f"{Status.failed}": "failed",
                     f"{Status.executing}": "executing",
                     f"{Status.passed}": "passed",
                     f"{Status.skipped}": "skipped",
                     f"{Status.undefined}": "undefined",
                     f"{Status.untested}": "untested"}
        self.__current_status = converter[str(step.status)]

    def eof(self):
        self.add_result()

    def close(self):
        self.stream.reconfigure(newline="")
        writer = DictWriter(self.stream, ["epic",
                                          "feature_filename",
                                          "feature_name",
                                          "feature_tags",
                                          "feature_description",
                                          "scenario_id",
                                          "scenario_name",
                                          "scenario_tags",
                                          "scenario_description",
                                          "scenario_is_outline",
                                          "scenario_steps"],
                            quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows([{"epic": item} for item in self.__epics])
        writer.writerows(self.__features)
        writer.writerows(self.__result)


class FeatureModel:
    def __init__(self, name, filename, epic, tags, description):
        self.name = name
        self.filename = re.sub(r'^(\.\./)*', '', filename)
        self.epic = epic
        self.tags = ", ".join(tags)
        self.description = description

    def to_dict(self):
        return {"feature_name": self.name,
                "feature_filename": self.filename,
                "epic": self.epic,
                "feature_tags": self.tags,
                "feature_description": self.description}


class ScenarioModel:
    def __init__(self, scenario_id, name, filename, tags, description, is_outline):
        self.scenario_id = scenario_id
        self.name = name
        self.filename = re.sub(r'^(\.\./)*', '', filename)
        self.tags = ", ".join(tags)
        self.description = description
        self.outline = is_outline
        self._steps = []

    @property
    def steps(self):
        return "\n".join(self._steps)

    @steps.setter
    def steps(self, step):
        self._steps.append(step)

    def to_dict(self):
        return {"feature_filename": self.filename,
                "scenario_id": self.scenario_id,
                "scenario_name": self.name,
                "scenario_tags": self.tags,
                "scenario_description": self.description,
                "scenario_is_outline": self.outline,
                "scenario_steps": self.steps}