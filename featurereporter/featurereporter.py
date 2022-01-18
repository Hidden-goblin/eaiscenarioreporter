# -*- coding: utf-8 -*-
# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-
import logging
import argparse
import os
import sys
import tempfile
import tkinter as tk

from logging.handlers import RotatingFileHandler

from PIL import ImageTk, Image
from tkinter import filedialog, Toplevel, messagebox

from featurereporter import ExportUtilities

log = logging.getLogger(__name__)

LICENCE = """ ExportUtilities  Copyright (C) 2021  E.Aivayan
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it under certain conditions.

    Please see https://opensource.org/licenses/lGPL-3.0
    """


class Application:

    def __init__(self):
        self.__assets = os.path.dirname(os.path.realpath(__file__))
        self.__master = tk.Tk()
        self.__master.geometry("500x200")
        # Feature repository vars
        self.__repository_label = None
        self.__repository_select_button = None
        self.__repository_location = None
        self.__repository_status = None
        self.__picture_valid = None
        self.__picture_warning = None
        # Created document
        self.__document_name_label = None
        self.__document_name_input = None
        self.__document_filename_label = None
        self.__document_filename_input = None
        self.__us_tag_label = None
        self.__us_tag_input = None
        # Execution reference
        self.__execution_result_label = None
        self.__execution_result_status = None
        self.__execution_result_button = None
        self.__execution_result_reset = None
        self.__execution_location = None
        # Other UI thing
        self.__quit = None
        self.__readme_button = None
        self.__execute_button = None
        self.__legal_label = None
        # Reporter object
        self.__reporter = ExportUtilities()
        # Create
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        # Legal stuff
        self.__legal_label = tk.Label(self.__master, text="?", )
        self.__legal_label.bind("<Button-1>", self.__display_legal)
        # Picture stuff
        valid = Image.open(f"{self.__assets}/assets/valid.png")
        valid = valid.resize((20, 20), Image.ANTIALIAS)
        self.__picture_valid = ImageTk.PhotoImage(valid)
        warning = Image.open(f"{self.__assets}/assets/warning.png")
        warning = warning.resize((20, 20), Image.ANTIALIAS)
        self.__picture_warning = ImageTk.PhotoImage(warning)
        # Repository
        self.__repository_status = tk.Label(self.__master, image=self.__picture_warning)
        self.__repository_label = tk.Label(self.__master,
                                           text="Please select a feature file repository.",
                                           wraplength="250")
        self.__repository_select_button = tk.Button(self.__master,
                                                    text="Select repository",
                                                    command=self.__select_repository)
        # Document name
        self.__document_name_label = tk.Label(self.__master,
                                              text="Document name: ")
        self.__document_name_input = tk.Entry(self.__master)
        # Document filename
        self.__document_filename_label = tk.Label(self.__master,
                                                  text="Document filename: ")
        self.__document_filename_input = tk.Entry(self.__master)
        # US Tag
        self.__us_tag_label = tk.Label(self.__master,
                                       text="US Tag: ")
        self.__us_tag_input = tk.Entry(self.__master)
        # Execution location
        self.__execution_result_label = tk.Label(self.__master,
                                                 text="Execution results location: ")
        self.__execution_result_button = tk.Button(self.__master, text="Select execution",
                                                   command=self.__select_execution)
        self.__execution_result_reset = tk.Button(self.__master, text="Reset location",
                                                  command=self.__reset_execution)
        self.__execution_result_status = tk.Label(self.__master, text="")
        # Readme
        self.__readme_button = tk.Button(self.__master, text="README",
                                         command=self.__display_readme)

        # Execute
        self.__execute_button = tk.Button(self.__master, text="Create report",
                                          command=self.__create_report)

        # QUIT
        self.__quit = tk.Button(self.__master, text="QUIT", fg="red",
                                command=self.__master.destroy)

    def create_layout(self):
        self.__legal_label.grid(row=0, column=4)
        self.__repository_status.grid(row=1, column=0)
        self.__repository_label.grid(row=1, column=1)
        self.__repository_select_button.grid(row=1, column=3, columnspan=4)
        self.__document_name_label.grid(row=2, column=0)
        self.__document_name_input.grid(row=2, column=1)
        self.__document_filename_label.grid(row=3, column=0)
        self.__document_filename_input.grid(row=3, column=1)
        self.__us_tag_label.grid(row=4, column=0)
        self.__us_tag_input.grid(row=4, column=1)
        self.__execution_result_label.grid(row=5, column=0)
        self.__execution_result_status.grid(row=5, column=1)
        self.__execution_result_button.grid(row=5, column=3)
        self.__execution_result_reset.grid(row=5, column=4)
        self.__readme_button.grid(row=6, column=0)
        self.__execute_button.grid(row=6, column=3)
        self.__quit.grid(row=7, column=0, columnspan=5, sticky="E,W")

    @staticmethod
    def __display_readme():
        messagebox.showinfo("Quick manual",
                            """1- Select the folder where you store the feature files
 Optionally:
     2- Select the report title
     3- Select the report file name
     4- Select the tag linking to US
     5- Select the behave plain report file""")

    def __create_report(self):
        log.info("Start reporting")
        if self.__repository_location is not None and self.__repository_location:
            self.__reporter.feature_repository = self.__repository_location
            if self.__document_name_input.get():
                self.__reporter.report_title = self.__document_name_input.get()
            if self.__us_tag_input.get():
                self.__reporter.us_tag = self.__us_tag_input.get()
            param = {}
            if self.__document_filename_input.get():
                param["output_file_name"] = self.__document_filename_input.get()
            if self.__execution_location is not None and self.__execution_location:
                param["report_file"] = self.__execution_location
            print(param)
            self.__reporter.create_application_documentation(**param)
        else:
            log.error("Cannot create de report without a feature files repository.")
            messagebox.showerror("Report creation",
                                 "Cannot create de report without a feature files repository.\n "
                                 "Please select one.")

    def __display_legal(self, event):
        log.debug("Display legal")
        f_infos = Toplevel()  # Popup -> Toplevel()
        f_infos.title('Infos')
        text = tk.Text(f_infos, height=15, width=90)
        text.insert(tk.END,
                    f"""License
*******

{LICENCE}

Pictures disclaimer
*******************

Icon by Raj Dev (https://freeicons.io/profile/714) on https://freeicons.io""")
        text.grid(row=0, column=0)
        tk.Button(f_infos, text='Quitter', command=f_infos.destroy).grid(row=1, column=0)
        f_infos.transient(self.__master)  # Réduction popup impossible
        f_infos.grab_set()  # Interaction avec fenetre jeu impossible
        self.__master.wait_window(f_infos)  # Arrêt script principal

    def __select_repository(self):
        self.__repository_location = filedialog.askdirectory(parent=self.__master,
                                                             mustexist=True,
                                                             title="Select the feature repository")
        if self.__repository_location is not None and self.__repository_location:
            self.__repository_label["text"] = self.__repository_location
            self.__repository_status["image"] = self.__picture_valid
        else:
            self.__repository_label["text"] = "Please select a feature file repository."
            self.__repository_status["image"] = self.__picture_warning

    def __select_execution(self):
        self.__execution_location = filedialog.askopenfilename(parent=self.__master,
                                                               title="Select the test plain report",
                                                               filetypes=[("text files", "*.txt")])
        if self.__execution_location is not None and self.__execution_location:
            self.__execution_result_status["text"] = "Execution selected"
        else:
            self.__execution_result_status["text"] = ""

    def __reset_execution(self):
        self.__execution_result_status["text"] = ""
        self.__execution_location = None

    def run(self):
        self.__master.mainloop()


def main():
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s -- %(filename)s.%(funcName)s-- %(levelname)s -- %(message)s")
    handler = RotatingFileHandler(f"{tempfile.gettempdir()}/test_log.log",
                                  encoding="utf-8",
                                  maxBytes=1000000,
                                  backupCount=2)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", help="Invariant pointing to a user story")
    parser.add_argument("--title", help="The document's title")
    parser.add_argument("--repository", help="The folder where the feature files are")
    parser.add_argument("--output", help="")
    parser.add_argument("--execution",
                        help="Behave plain test output in order to "
                             "also print the last execution result")
    parser.add_argument("--license",
                        help="Display the license.",
                        action="store_true")

    args = parser.parse_args()
    if (
        all(
            value is None
            for item, value in vars(args).items()
            if item != "license"
        )
        and not args.license
    ):
        app = Application()
        app.run()
    else:
        print(args.license)
        if args.license is not None and args.license:
            with open(os.path.realpath(
                    f"{os.path.dirname(os.path.realpath(__file__))}"
                    f"/assets/LICENSE.txt")) as my_license:
                print(my_license.read())
                sys.exit(0)
        if args.repository is None or not args.repository:
            parser.print_help()
        report = ExportUtilities()
        report.feature_repository = args.repository
        if args.title is not None and args.title:
            report.report_title = args.title
        if args.tag is not None and args.tag:
            report.us_tag = args.tag
        parameters = {}
        if args.execution is not None and args.execution:
            parameters["report_file"] = args.execution
        if args.output is not None and args.output:
            parameters["output_file_name"] = args.output
        print(f"""{LICENCE}
    Run with --license option to display the full licence""")
        report.create_application_documentation(**parameters)
    sys.exit(0)


if __name__ == '__main__':
    main()
