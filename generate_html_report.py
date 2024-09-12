import sys
from pathlib import Path


def generate_html_report(input_file, output_file):
    errors = {}
    with open(input_file, "r") as file:
        filename = ""
        for line in file:
            if line.startswith("Error in file"):
                filename = line.split(":")[1].strip()
                errors[filename] = []
            else:
                errors[filename].append(line.strip())

    errors = {k: errors[k] for k in sorted(errors)}
    html_content = "<html><head><title>XML Validation Report</title></head><body>"
    html_content += "<h1>XML Validation Report</h1>"
    for filename, error_list in errors.items():
        html_content += f"<div><h2>{filename}</h2>"
        html_content += "<details><summary>View Errors</summary><ul>"
        for error in error_list:
            html_content += f"<li>{error}</li>"
        html_content += "</ul></details></div>"
    html_content += "</body></html>"

    Path(output_file).write_text(html_content)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate_html_report(input_file, output_file)
