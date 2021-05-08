from jinja2 import Template
import os


def page_render(template_name, folder='web_pages', **kwargs):
    path = os.path.join(folder, template_name)

    with open(path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
