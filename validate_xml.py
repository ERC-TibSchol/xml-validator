import sys
from lxml import etree
from collections import defaultdict
import os
from datetime import datetime


def create_error_report(error_dict, report_filename):
    SORTED_ERRORS = {k: error_dict[k] for k in sorted(error_dict)}
    with open(report_filename, "a") as report:
        for f, e in SORTED_ERRORS.items():
            report.write(f"\nError in file: {os.path.basename(f)}\n")
            print(f"{os.path.basename(f)}\n")
            for ei in e:
                report.write(f"\tLine {ei[0]:4d}, Pos {ei[1]:4d}: {ei[2]}\n")
                print(f"\tLine {ei[0]:4d}, Pos {ei[1]:4d}: {ei[2]}\n")


def validate_xml(tei_filename):
    # Create a parser with error logging
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    try:
        tree = etree.parse(tei_filename, parser=parser)
    except etree.XMLSyntaxError as e:
        # Handle XML syntax errors that occur before parsing
        print(f"Error parsing {tei_filename}: {e}")
        return

    errors = defaultdict(list)
    ncname_errors = defaultdict(list)
    if parser.error_log:
        for err in parser.error_log:
            if "is not an NCName" in err.message:
                ncname_errors[err.filename].append((err.line, err.column, err.message))
            else:
                errors[err.filename].append((err.line, err.column, err.message))

    create_error_report(errors, "reports/validation_report.md")
    create_error_report(ncname_errors, "reports/ncname_report.md")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_xml.py <tei_filename>")
        sys.exit(1)

    tei_filename = sys.argv[1]
    validate_xml(tei_filename)
