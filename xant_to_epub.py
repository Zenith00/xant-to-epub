import traceback

from bs4 import BeautifulSoup
import urllib.request
import re
import collections
import pypub

url = "https://xantandminions.wordpress.com/kuma-kuma-kuma-bear/"
url = "https://xantandminions.wordpress.com/yuusha-oshishou/"
url = "https://xantandminions.wordpress.com/isekai-izakaya-nobu/"
f = urllib.request.urlopen(url)
html = f.read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
# print("break\n"*4)
# print(soup.select("div.entry-content"))
entry_content = soup.find_all("div", class_="entry-content")[-1]
# print(entry_content)

linked = entry_content.find_all([re.compile("h\d"), "a"])
for link in linked:
    if link.name == "a":
        # print(link.attrs)
        pass
    else:
        pass
errors = collections.defaultdict(int)
error_log = []
def fluff(tag):
    if tag.name == "a":
        if "href" not in tag.attrs.keys():
            return False
        if "xantandminions.wordpress" not in tag.attrs["href"]:
            return False
    if "class" in tag.attrs.keys():
        for class_name in tag.attrs["class"]:
            if class_name in ["share-icon", "sd-title"]:
                return False

    return True


def strip_fluff(raw_list):
    stripped_list = []
    for item in raw_list:
        if fluff(item):
            stripped_list.append(item)
    return stripped_list




# print("\n".join(str(x) for x in strip_fluff(linked)))

url = "https://xantandminions.wordpress.com/2016/10/06/isekai-izakaya-nobu-chapter-5/"
f = urllib.request.urlopen(url)
html = f.read()
soup = BeautifulSoup(html, 'html.parser')
entry_content = soup.find_all("div", class_="entry-content")[-1]
for tagname in entry_content.select("div.sharedaddy") + entry_content.select("div.wpcnt"):
    tagname.decompose()
index = entry_content.find_all(string="Index")
for index_loc in index:
    index_loc.parent.parent.parent.decompose()
# print(index)
print(entry_content.prettify())