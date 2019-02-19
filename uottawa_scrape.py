import requests
import bs4 as soup
import json
import re

_DOC_ID = -1
_EN_COURSE_PATTERN = re.compile(r"^CSI (\d[1,2,3,4]\d*).*$", re.M)

f = open("courses.txt", "w")


def parse(c):
    info = list(filter(bool, c))
    assert len(info) == 2, "Invalid."

    h, d = map(lambda x: x.text, info)
    h = h.replace(u'\xa0', ' ')
    d = d.replace("\n", '')

    if not bool(re.match(_EN_COURSE_PATTERN, h)):
        # f.write(h+"\n")
        # print(h)
        return None

    global _DOC_ID
    _DOC_ID += 1

    return dict(id=_DOC_ID, title=h, body=d)

def make_soup(html):
        return soup.BeautifulSoup(html, "lxml").find("body")

def scrape(url="https://catalogue.uottawa.ca/en/courses/csi/", html=None):
    if url and not html:
        r = requests.get(url)
        with open("data/uottawa.html", "w") as f:
                f.write(r.text)

        html = make_soup(r.text)

    else:
        html = make_soup(html)

    titles = html.findAll("p", {"class": "courseblocktitle noindent"})
    descs = html.findAll("p", {"class": "courseblockdesc noindent"})

    courses = list(zip(titles, descs))

    with open("data/catalogue-uottawa-ca.json", "w") as f:
        formatted = map(parse, courses)
        filtered = list(filter(bool, formatted))
        f.write(json.dumps(filtered, indent=2))


with open("data/uottawa.html") as f:
        html = f.read()

my_soup = make_soup(html)

scrape(html=html)
