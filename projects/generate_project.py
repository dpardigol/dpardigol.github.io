from collections import defaultdict
import json
from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

def generate_projects():
    # Load JSON data
    with (Path(__file__).parent.parent / "portfolio.json").open(encoding="utf-8") as f:
        index_data = json.load(f)

    project_data = defaultdict(dict)
    # Generate individual project pages
    for project_num, file in enumerate(Path(__file__).parent.glob("*.json")): 
        if file.suffix == ".json":
            with file.open(encoding="utf-8") as f:
                project_data = json.load(f)

                project_data['author'] = {'name': index_data.get('name', ''),
                                          'label': index_data.get('label', ''),
                                          'image_path': index_data.get('image_path', '')
                                        }

                slug = index_data['projects'][0].get("slug", f"project_{project_num}")
                
                # Set up Jinja environment
                env = Environment(loader=FileSystemLoader("./projects/"), autoescape=True)
                project_template = env.get_template("project_template.html")

                # Render the template with the data
                html_output = project_template.render(**project_data)

                # Write the output to an HTML file
                with (Path(__file__).parent / f"{slug}.html").open("w", encoding="utf-8") as f:
                    f.write(html_output)
