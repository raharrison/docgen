from markdown2 import Markdown

TEMPLATE_DIR = "template"


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


def build_doc_page(base, styles, content):
    page = base.replace("{{ styles }}", styles)
    page = page.replace("{{ content }}", content)
    return page


def convert_markdown(markdown):
    markdowner = Markdown(extras=["tables", "fenced-code-blocks"])
    html = markdowner.convert(markdown)
    return html


def write_page(path, html):
    with open(path, 'w') as content_file:
        content_file.write(html)


if __name__ == "__main__":
    base = read_base_template()
    styles = create_styles()

    with open("docs.md", 'r') as content_file:
        markdown = content_file.read().strip()

    doc_content = convert_markdown(markdown)

    page = build_doc_page(base, styles, doc_content)

    write_page("docs.html", page)