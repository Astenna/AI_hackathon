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
    database["predictions"] = [
   {
       "date": "09.08.2018",
       "prediction": {
           "increase": "0.6",
           "decrease": "0.4"
       }
   },
   {
       "date": "10.08.2018",
       "prediction": {
           "increase": "0.9",
           "decrease": "0.1"
       }
   },
   {
       "date": "11.08.2018",
       "prediction": {
           "increase": "0.6",
           "decrease": "0.4"
       }
   },
   {
       "date": "12.08.2018",
       "prediction": {
           "increase": "0.2",
           "decrease": "0.8"
       }
   },
   {
       "date": "13.08.2018",
       "prediction": {
           "increase": "0.3",
           "decrease": "0.7"
       }
   }
]

    env = Environment(
        loader=PackageLoader("templates-module", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    template = env.get_template("index.html")
    _generate_page(
        template,
         "./docs",
        "index.html",
        database=database,
    )
