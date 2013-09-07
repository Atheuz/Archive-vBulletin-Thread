import lxml.html
import sys

html_escape_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
    '"': "&quot;"
}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def print_r(s):
    sys.stdout.write("%s \r" % (" " * 50))
    sys.stdout.write("%s \r" % s)
    sys.stdout.flush()
    
def get_html(session, url):
    return lxml.html.fromstring(session.get(url).text)