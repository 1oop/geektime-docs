from pathlib import Path
from lxml import etree
import sys # Import sys module for stderr

##给页面添加一个meta标签禁止加载图片时发送referer
def add_meta_tag(tree):
    meta = etree.Element("meta")
    meta.set("name", "referrer")
    meta.set("content", "no-referrer")
    head = tree.find(".//head")
    if head is not None:
        # Check if the meta tag already exists
        existing_meta = head.xpath('.//meta[@name="referrer" and @content="no-referrer"]')
        if not existing_meta:
            head.append(meta)
    else:
        # If there is no <head> tag, create one and append it to the <html> tag
        html = tree.find(".//html")
        if html is not None:
            head = etree.Element("head")
            html.insert(0, head)
            head.append(meta)
    return tree


if __name__ == "__main__":
    htmls = Path(".").glob("**/*.html")
    # Use HTMLParser which is more lenient
    parser = etree.HTMLParser(encoding='utf-8') # Specify encoding if known, otherwise let lxml detect
    for html in htmls:
        try:
            # Parse using the HTML parser
            tree = etree.parse(str(html), parser) # Pass parser instance
            tree = add_meta_tag(tree)
            # Use etree.tostring with method='html' for proper HTML output
            with open(html, "wb") as f:
                f.write(etree.tostring(tree, method='html', pretty_print=True, encoding="utf-8", xml_declaration=False, doctype="<!DOCTYPE html>")) # Adjust output options for HTML
            print(f"Processed {html}")
        except etree.XMLSyntaxError as e:
            # Catch parsing errors and print a message
            print(f"Error parsing {html}: {e}", file=sys.stderr)
        except Exception as e:
            # Catch other potential errors during processing
            print(f"An unexpected error occurred processing {html}: {e}", file=sys.stderr)
