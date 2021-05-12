from jinja2 import Environment, FileSystemLoader



def page_render(template_name, folder='web_pages', **kwargs):

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)

    """
    path = os.path.join(folder, template_name)

    with open(path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
    """