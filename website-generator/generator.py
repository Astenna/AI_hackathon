import csv
import json
import os

from collections import OrderedDict
from datetime import datetime
from jinja2 import Environment, PackageLoader, select_autoescape


def _generate_page(template, output_dir, name, **template_args):
    page = template.render(template_args)

    # Save static page to file
    with open(os.path.join(output_dir, name), "w") as f:
        f.write(page)


if __name__ == "__main__":
    # Website
    # Create Jinja2 templates environment
    database = OrderedDict()
    with open("predictions/prediction.json", "r") as prediction_file:
        database["predictions"] = json.load(prediction_file)
        database["predictions"] = database["predictions"][-15:]

    env = Environment(
        loader=PackageLoader("templates-module", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    template = env.get_template("index.html")
    _generate_page(template, "./docs", "index.html", database=database)
