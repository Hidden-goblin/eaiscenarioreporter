# -*- Product under GNU GPL v3 -*-
# -*- Author: E.Aivayan -*-

import re
from markdown_it import MarkdownIt
from htmldocx import HtmlToDocx


def insert_text(document, text):
    my_parser = HtmlToDocx()
    md = MarkdownIt()
    md.enable('table')
    my_parser.add_html_to_document(md.render(text), document)


def _repl(matchobj):
    print(f"Generate graph {matchobj.group(2)}")
    return f"![Schema](New path for {matchobj.group(2)})\n{matchobj.group(1)} {matchobj.group(2)}"


def extract_generate_workflow(text):
    return re.sub(r'(!!Workflow:)(.*)', _repl, text)
