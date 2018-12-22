import os
import shutil
from markdown2 import Markdown

TEMPLATE_DIR = "template"
OUTPUT_DIR = "docs"
RAW_DIR = "raw"

markdowner = Markdown(extras=["tables", "fenced-code-blocks"])


def read_base_template():
    with open(f"{TEMPLATE_DIR}/base.html", 'r') as template:
        return template.read().strip()


def create_styles():
    styles = ""
    css_files = [f"{TEMPLATE_DIR}/styles.css", f"{TEMPLATE_DIR}/highlight.css"]
    for css in css_files:
        with open(css, 'r') as css_file:
            styles += css_file.read().strip()
    return styles


def cleanup():
    shutil.rmtree(OUTPUT_DIR)


# TODO: Replace <title> with content filename
def build_doc_page(base, styles, markdown):
    withStyles = base.replace("{{ styles }}", styles)
    content = markdowner.convert(markdown)
    withContent = withStyles.replace("{{ content }}", content)
    return withContent


def walk_raw_docs():
    docs = []
    for (root, _, filenames) in os.walk(RAW_DIR):
        for filename in filenames:

            with open(os.path.join(root, filename), 'r') as doc_file:
                markdown = doc_file.read().strip()

            dirpath = os.path.relpath(root, RAW_DIR).replace(".", "")
            name = os.path.splitext(filename)[0].replace(" ", "-").lower()
            docs.append({"path": dirpath, "name": name, "markdown": markdown})
    return docs


def generate_docs(raw_docs):
    base = read_base_template()
    styles = create_styles()

    for doc in raw_docs:
        page = build_doc_page(base, styles, doc["markdown"])
        doc_dir_path = os.path.join(OUTPUT_DIR, doc["path"])
        doc_path = os.path.join(doc_dir_path, f"{doc['name']}.html")

        if not os.path.exists(doc_dir_path):
            os.makedirs(doc_dir_path)

        with open(doc_path, 'w') as output_file:
            output_file.write(page)


if __name__ == "__main__":

    cleanup()
    print("Cleaned up output directory")

    raw_docs = walk_raw_docs()
    print(f"Found {len(raw_docs)} files to generate")

    generate_docs(raw_docs)
    print("Generated documents")