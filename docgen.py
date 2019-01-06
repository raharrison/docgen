import os
import shutil
from markdown2 import Markdown
import pystache

TEMPLATE_DIR = "template"
OUTPUT_DIR = "docs"
RAW_DIR = "raw"

markdowner = Markdown(extras=["tables", "fenced-code-blocks"])

templates = {}  # cache for templates


class Doc():
    def __init__(self, src_filename, src_path, dir_path):
        self.src_filename = src_filename.strip()  # overview.md
        self.src_path = src_path.strip()  # raw/technical/tools/overview.md
        (name, extension) = os.path.splitext(self.src_filename)
        self.name = name.replace(" ", "-").lower().strip()  # overview
        self.extension = extension.strip()  # .md
        self.dir_path = dir_path.replace("\\", "/").strip()  # technical/tools

        self.title = self.name.replace("-", " ").title()  # Overview
        self.long_name = self.dir_path.replace("/", " ").title().replace(
            " ", " / ") + " / " + self.title  # Technical / Tools / Overview

    def is_doc(self) -> bool:
        return self.extension == ".md"


class DocSet():
    def __init__(self, dir_path: str, docs: [Doc]):
        self.dir_path = dir_path
        self.docs = docs
        self.doc_count = len(self.docs)

    def to_url(self):
        if self.dir_path != "":
            return self.dir_path + "/"
        return self.dir_path


def render_template(template, params) -> str:
    if not template in templates:
        with open(f"{TEMPLATE_DIR}/{template}.html", 'r') as template_file:
            templates[template] = template_file.read().strip()

    return pystache.render(templates[template], params)


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


def build_doc_page(contents: str, doc: Doc) -> str:
    content = markdowner.convert(doc.markdown)
    return render_template(
        "base", {
            "title": doc.title,
            "styles": styles,
            "name": doc.long_name,
            "contents": contents,
            "content": content
        })


def generate_contents(doc_set: DocSet):
    contents_docs = [{
        "title": doc.title,
        "url": f"{doc.name}.html"
    } for doc in doc_set.docs if doc.is_doc()]
    return render_template("contents", {"docs": contents_docs})


def walk_raw_docs() -> [DocSet]:
    docs_by_dir = []
    for (root, _, filenames) in os.walk(RAW_DIR):
        dir_docs = []
        dir_path = os.path.relpath(root, RAW_DIR).replace(".", "")
        for filename in filenames:
            raw_path = os.path.join(root, filename)

            doc = Doc(filename, raw_path, dir_path)
            if doc.is_doc():
                with open(os.path.join(root, filename), 'r') as doc_file:
                    markdown = doc_file.read().strip()
                    doc.markdown = markdown

            dir_docs.append(doc)
        docs_by_dir.append(DocSet(dir_path, dir_docs))

    return docs_by_dir


def generate_docs(doc_sets: [DocSet]):
    for doc_set in doc_sets:
        contents = generate_contents(doc_set)
        for doc in doc_set.docs:
            doc_dir_path = os.path.join(OUTPUT_DIR, doc.dir_path)
            if not os.path.exists(doc_dir_path):
                os.makedirs(doc_dir_path)

            if doc.is_doc():
                page = build_doc_page(contents, doc)

                doc_path = os.path.join(doc_dir_path, f"{doc.name}.html")

                with open(doc_path, 'w') as output_file:
                    output_file.write(page)
            else:
                # raw file copy
                src = doc.src_path
                target = os.path.join(doc_dir_path, doc.src_filename)
                shutil.copyfile(src, target)


def generate_index(doc_sets: [DocSet]):
    pages = []
    for doc_set in doc_sets:
        pages.extend([{
            "title": doc.long_name,
            "url": doc_set.to_url() + f"{doc.name}.html"
        } for doc in doc_set.docs if doc.is_doc()])

    index = render_template("contents", {"docs": pages})

    output = render_template("base", {
        "title": "Index",
        "styles": styles,
        "name": "Index",
        "content": index
    })

    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w') as output_file:
        output_file.write(output)


if __name__ == "__main__":

    styles = create_styles()

    cleanup()
    print("Cleaned up output directory")

    raw_docs = walk_raw_docs()
    print(f"Found {len(raw_docs)} files to generate")

    generate_docs(raw_docs)
    generate_index(raw_docs)
    print("All documents generated")