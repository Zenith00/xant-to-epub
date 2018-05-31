from bs4 import BeautifulSoup
import urllib.request
import re
import collections

url = "https://xantandminions.wordpress.com/kuma-kuma-kuma-bear/"
f = urllib.request.urlopen(url)
html = f.read()
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
# print("break\n"*4)
# print(soup.select("div.entry-content"))
entry_content = soup.find_all("div", class_="entry-content")[-1]
# print(entry_content)

linked = entry_content.find_all([re.compile("h\d"), "a"])
errors = collections.defaultdict(int)
error_log = []
def strip_unneeded(list_of_candidates):
    metadata =[]
    volume_list = collections.defaultdict(list)
    curr_volume = None
    for candidate in list_of_candidates:

print("\n".join(str(x) for x in linked))
