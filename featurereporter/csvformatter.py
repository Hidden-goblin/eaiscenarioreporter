# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
from behave.formatter.base import Formatter
from behave.model import Status
from csv import DictWriter
import re



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

    def add_result(self):
        self.__result.append({"epic": self.__current_epic,
                              "feature": self.__current_feature,
                              "scenario_id": self.__current_scenario_id,
                              "scenario": self.__current_scenario_name,
                              "status": self.__current_status,
                              "order": self.__outline_order})
        self.__current_status = None

    def scenario(self, scenario):
        if self.__current_status is not None:
            self.add_result()
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
                                          "feature",
                                          "scenario_id",
                                          "scenario",
                                          "status",
                                          "order"])
        writer.writeheader()
        writer.writerows(self.__result)
