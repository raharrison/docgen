import os
import shutil
from markdown2 import Markdown

TEMPLATE_DIR = "template"
OUTPUT_DIR = "docs"
RAW_DIR = "raw"

markdowner = Markdown(extras=["tables", "fenced-code-blocks"])


class Document():
    src_file: str  # overview.md
    name: str  # overview
    extension: str  # .md
    path: str  # technical/tools
    markdown: str

    def __init__(self, src_file, path, markdown=""):
        self.src_file = src_file
        (name, extension) = os.path.splitext(src_file)
        self.name = name.replace(" ", "-").lower()
        self.extension = extension
        self.path = path
        self.markdown = markdown

    def is_doc(self) -> bool:
        return self.extension == ".md"


def read_base_template() -> str:
    with open(f"{TEMPLATE_DIR}/base.html", 'r') as template:
        return template.read().strip()


def create_styles() -> str:
    styles = ""
    css_files = [f"{TEMPLATE_DIR}/styles.css", f"{TEMPLATE_DIR}/highlight.css"]
    for css in css_files:
        with open(css, 'r') as css_file:
            styles += css_file.read().strip()
    return styles


def cleanup():
    shutil.rmtree(OUTPUT_DIR)


# TODO: Replace <title> with content filename
def build_doc_page(base, styles, markdown) -> str:
    withStyles = base.replace("{{ styles }}", styles)
    content = markdowner.convert(markdown)
    withContent = withStyles.replace("{{ content }}", content)
    return withContent


def walk_raw_docs() -> [Document]:
    docs = []
    for (root, _, filenames) in os.walk(RAW_DIR):
        for filename in filenames:
            dirpath = os.path.relpath(root, RAW_DIR).replace(".", "")

            doc = Document(filename, dirpath)
            if doc.is_doc():
                with open(os.path.join(root, filename), 'r') as doc_file:
                    markdown = doc_file.read().strip()
                    doc.markdown = markdown

            docs.append(doc)

    return docs


def generate_docs(raw_docs):
    base = read_base_template()
    styles = create_styles()

    for doc in raw_docs:
        page = build_doc_page(base, styles, doc.markdown)
        doc_dir_path = os.path.join(OUTPUT_DIR, doc.path)
        doc_path = os.path.join(doc_dir_path, f"{doc.name}.html")

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