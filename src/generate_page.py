import os
import sys

from block_markdown import markdown_to_html_node
from extract_markdown import extract_title

template_path = "./template.html"


def generate_page(from_path, template_path, dest_path, base_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        contents = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_contents = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_contents)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)


def generate_pages_recursive(from_path, template_path, dest_path, base_path):
    list = os.listdir(from_path)
    for item in list:
        if os.path.isfile(os.path.join(from_path, item)):
            dest_file = item.replace(".md", ".html")
            generate_page(
                os.path.join(from_path, item),
                template_path,
                os.path.join(dest_path, dest_file),
                base_path,
            )
        else:
            generate_pages_recursive(
                os.path.join(from_path, item),
                template_path,
                os.path.join(dest_path, item),
                base_path,
            )
