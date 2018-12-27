import os
import shutil
from markdown2 import Markdown
from pybars import Compiler

TEMPLATE_DIR = "template"
OUTPUT_DIR = "docs"
RAW_DIR = "raw"

markdowner = Markdown(extras=["tables", "fenced-code-blocks"])
compiler = Compiler()


class Document():
    src_filename: str  # overview.md
    src_path: str  # raw/technical/tools/overview.md
    name: str  # overview
    extension: str  # .md
    dir_path: str  # technical/tools
    markdown: str

    def __init__(self, src_filename, src_path, dir_path):
        self.src_filename = src_filename.strip()
        self.src_path = src_path.strip()
        (name, extension) = os.path.splitext(self.src_filename)
        self.name = name.replace(" ", "-").lower().strip()
        self.extension = extension.strip()
        self.dir_path = dir_path.strip()

    def is_doc(self) -> bool:
        return self.extension == ".md"

    def title(self) -> str:
        return self.name.replace("-", " ").title()


def read_base_template() -> str:
    with open(f"{TEMPLATE_DIR}/base.html", 'r') as template_file:
        template = template_file.read().strip()
        return compiler.compile(template)


def create_styles() -> str:
    styles = ""
    css_files = [f"{TEMPLATE_DIR}/styles.css", f"{TEMPLATE_DIR}/highlight.css"]
    for css in css_files:
        with open(css, 'r') as css_file:
            styles += css_file.read().strip()
    return styles


def cleanup():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)


def build_doc_page(base, styles, title, markdown) -> str:
    content = markdowner.convert(markdown)
    output = base({"title": title, "styles": styles, "content": content})
    return output


def walk_raw_docs() -> [[Document]]:
    docs_by_dir = []
    for (root, _, filenames) in os.walk(RAW_DIR):
        dir_docs = []
        for filename in filenames:
            dirpath = os.path.relpath(root, RAW_DIR).replace(".", "")
            raw_path = os.path.join(root, filename)

            doc = Document(filename, raw_path, dirpath)
            if doc.is_doc():
                with open(os.path.join(root, filename), 'r') as doc_file:
                    markdown = doc_file.read().strip()
                    doc.markdown = markdown

            dir_docs.append(doc)
        docs_by_dir.append(dir_docs)

    return docs_by_dir


def generate_docs(raw_docs):
    base = read_base_template()
    styles = create_styles()

    for directory in raw_docs:
        for doc in directory:
            doc_dir_path = os.path.join(OUTPUT_DIR, doc.dir_path)
            if not os.path.exists(doc_dir_path):
                os.makedirs(doc_dir_path)

            if doc.is_doc():
                page = build_doc_page(base, styles, doc.title(), doc.markdown)

                doc_path = os.path.join(doc_dir_path, f"{doc.name}.html")

                with open(doc_path, 'w') as output_file:
                    output_file.write(page)
            else:
                # raw file copy
                src = doc.src_path
                target = os.path.join(doc_dir_path, doc.src_filename)
                shutil.copyfile(src, target)


if __name__ == "__main__":

    cleanup()
    print("Cleaned up output directory")

    raw_docs = walk_raw_docs()
    print(f"Found {len(raw_docs)} files to generate")

    generate_docs(raw_docs)
    print("All documents generated")