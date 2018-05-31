import traceback

from bs4 import BeautifulSoup
import urllib.request
import re
import collections

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



def strip_unneeded(list_of_candidates):
    metadata =[]
    volume_list = collections.defaultdict(list)
    curr_volume = None
    for candidate in list_of_candidates:
        pass

print("\n".join(str(x) for x in strip_fluff(linked)))
