import os
import shutil
from functools import reduce
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
        self.dir_path = dir_path if dir_path == "" else dir_path + "/"  # technical/tools/

        self.title = self.name.replace("-", " ").title()  # Overview
        self.long_name = dir_path.replace("/", " ").title().replace(
            " ", " / ") + " / " + self.title  # Technical / Tools / Overview

    def is_doc(self) -> bool:
        return self.extension == ".md"


class DocSet():
    def __init__(self, dir_path: str, docs: [Doc]):
        self.dir_path = dir_path  # technical/tools
        self.docs = docs
        self.doc_count = len(self.docs)
        self.long_name = dir_path.replace("/", " ").title().replace(
            " ", " / ") + " / "  # Technical / Tools /


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


def generate_contents(doc_set: DocSet,
                      all_sets: [DocSet],
                      current_page: DocSet = None,
                      long_names: bool = False):
    # each doc in current set
    contents_docs = [{
        "title":
        doc.long_name if long_names else doc.title,
        "url":
        doc.dir_path + f"{doc.name}.html" if long_names else f"{doc.name}.html"
    } for doc in doc_set.docs if doc.is_doc() and doc != current_page]

    # index of root
    if doc_set.dir_path == "":
        root_index = ""
    else:
        root_index = "../" * len(doc_set.dir_path.split("/"))
    # don't add for root index page
    if current_page != None or doc_set.dir_path != "":
        contents_docs.append({
            "title": f"Root Index of /",
            "url": root_index + "index.html"
        })

    upstream, downstream = find_relative_docsets(doc_set, all_sets)

    # index up one level
    if upstream != None and doc_set.dir_path != "":
        up_one_index = {
            "title": f"Upstream: Index of {upstream.long_name}",
            "url": "../index.html"
        }
        contents_docs.append(up_one_index)

    # downstream sets
    for down_stream_set in downstream:
        contents_docs.append({
            "title":
            f"Downstream: Index of {down_stream_set.long_name}",
            "url":
            down_stream_set.dir_path.replace(doc_set.dir_path + "/", "") +
            "/index.html"
        })

    return render_template("contents", {"docs": contents_docs})


def find_relative_docsets(doc_set: DocSet,
                          all_sets: [DocSet]) -> (DocSet, [DocSet]):
    common_path = "" if doc_set.dir_path == "" else doc_set.dir_path + "/"
    downstream = [
        docset for docset in all_sets
        if docset.dir_path.startswith(doc_set.dir_path)  # share common path
        and docset.dir_path != doc_set.dir_path and  # not current set
        # only one level down
        len(docset.dir_path.replace(common_path, "").split("/")) <= 1
    ]

    if doc_set.dir_path == "":
        return (None, downstream)

    upstream_path = "/".join(doc_set.dir_path.split("/")[:-1])
    upstream_doc_set = next(
        docset for docset in all_sets if docset.dir_path == upstream_path)
    return (upstream_doc_set, downstream)


def walk_raw_docs() -> [DocSet]:
    docs_by_dir = []
    for (root, _, filenames) in os.walk(RAW_DIR):
        dir_docs = []
        dir_path = os.path.relpath(root, RAW_DIR)
        clean_dir_path = dir_path.replace(".", "").replace("\\", "/")

        for filename in filenames:
            raw_path = os.path.join(root, filename)

            doc = Doc(filename, raw_path, clean_dir_path)
            if doc.is_doc():
                with open(os.path.join(root, filename), 'r') as doc_file:
                    markdown = doc_file.read().strip()
                    doc.markdown = markdown

            dir_docs.append(doc)
        docs_by_dir.append(DocSet(clean_dir_path, dir_docs))

    return docs_by_dir


def create_all_doc(raw_docs: [DocSet]):
    all = [doc for doc_set in raw_docs for doc in doc_set.docs if doc.is_doc()]
    combined_content = "\n\n---\n\n".join(
        [f"# {doc.long_name}\n\n{doc.markdown}" for doc in all])
    all_doc = Doc("all.md", f"{RAW_DIR}/all.md", "")
    all_doc.markdown = combined_content

    # if no root doc set create one
    if raw_docs[0].dir_path == "":
        raw_docs[0].docs.insert(0, all_doc)
    else:
        raw_docs.insert(0, DocSet("", [all_doc]))


def generate_docs(doc_sets: [DocSet]):
    for doc_set in doc_sets:

        doc_dir_path = os.path.join(OUTPUT_DIR, doc_set.dir_path)
        if not os.path.exists(doc_dir_path):
            os.makedirs(doc_dir_path)

        for doc in doc_set.docs:
            if doc.is_doc():
                contents = generate_contents(
                    doc_set, doc_sets, current_page=doc)
                page = build_doc_page(contents, doc)

                doc_path = os.path.join(doc_dir_path, f"{doc.name}.html")

                with open(doc_path, 'w') as output_file:
                    output_file.write(page)
            else:
                # raw file copy
                src = doc.src_path
                target = os.path.join(doc_dir_path, doc.src_filename)
                shutil.copyfile(src, target)


def write_index(contents: str, doc_set: DocSet):
    output = render_template(
        "base", {
            "title": f"Index of {doc_set.long_name}",
            "styles": styles,
            "name": f"Index of {doc_set.long_name}",
            "contents": contents
        })

    index_path = os.path.join(OUTPUT_DIR, doc_set.dir_path, "index.html")
    with open(index_path, 'w') as output_file:
        output_file.write(output)


def generate_indexes(doc_sets: [DocSet]):
    for doc_set in doc_sets:
        contents = generate_contents(doc_set, doc_sets)
        write_index(contents, doc_set)

    all = [doc for doc_set in doc_sets for doc in doc_set.docs if doc.is_doc()]
    all_doc_set = DocSet("", all)
    contents = generate_contents(all_doc_set, [all_doc_set], long_names=True)
    write_index(contents, all_doc_set)


if __name__ == "__main__":

    styles = create_styles()

    cleanup()
    print("Cleaned up output directory")

    raw_docs = walk_raw_docs()
    if len(raw_docs) == 0:
        print("No docs found to generate")
        exit(1)

    create_all_doc(raw_docs)
    total = reduce(lambda x, y: x + len(y.docs), raw_docs, 0)
    print(f"Found {total} files to generate")

    generate_docs(raw_docs)
    generate_indexes(raw_docs)
    print("All documents generated")