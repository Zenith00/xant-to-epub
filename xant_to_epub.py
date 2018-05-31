import traceback

from bs4 import BeautifulSoup
import urllib.request
import re
import collections
from ebooklib import epub

url = "https://xantandminions.wordpress.com/kuma-kuma-kuma-bear/"
# url = "https://xantandminions.wordpress.com/yuusha-oshishou/"
# url = "https://xantandminions.wordpress.com/isekai-izakaya-nobu/"
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

def page_parser(url):
    f = urllib.request.urlopen(url)
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    entry_content = soup.find_all("div", class_="entry-content")[-1]
    # print(entry_content)
    for tagname in entry_content.select("div.sharedaddy") + entry_content.select("div.wpcnt"):
        tagname.decompose()
    index = entry_content.find_all(string="Index")
    for index_loc in index:
        try:
            index_loc.parent.parent.decompose()
        except:
            print(traceback.format_exc())
            print(str(index_loc))
            errors["warning"] += 1
            error_log.append("Failed to remove index at " + str(index))
    scripts = entry_content.find_all("script")
    for script in scripts:
        script.decompose()
    # print(entry_content)
    outputstr = entry_content.prettify()
    outputstr = "<html><body>" + outputstr + "</body></html>"
    return outputstr

# print(page_parser("https://xantandminions.wordpress.com/kuma-kuma-kuma-bear/art/"))
linked = strip_fluff(linked)

def create_epub():
    book = epub.EpubBook()
    book.set_identifier("wat")
    book.set_title("book title")
    book.set_language('en')
    book.add_author('xant')
    return book

name = "Volume 0"
volumes = collections.defaultdict(create_epub)
chapters = []
clean_uri = lambda string_in: ''.join([x for x in string_in if ord(x) < 128 and x != " "])
for link in linked:
    link.string = re.sub(r'[\\/*?:"<>|]', "", link.string)
    if link.name in ["h2", "h3", "h4", "h5", "h6"]:
        if len(chapters) > 0:
            volumes[name].toc = chapters
            volumes[name].add_item(epub.EpubNav())
            volumes[name].add_item(epub.EpubNcx())
            volumes[name].spine = chapters
            volumes[name].add_item(epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content='BODY { text-align: justify;}'))
            try:
                epub.write_epub(name + ".epub", volumes[name])
            except:
                print(traceback.format_exc())
        name = link.string
        chapters = []

    elif link.name == "a":
        if "chapter" in str(link.string).lower():
            # print(name + ": " + link.string)
            # print(link.attrs["href"])
            chapter = epub.EpubHtml(title=link.string, file_name=clean_uri(link.string) + ".xhtml", content=page_parser(link.attrs['href']),
                                    media_type="application/xhtml+xml")
            chapter.add_item(epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content='BODY { text-align: justify;}'))
            volumes[name].add_item(chapter)
            chapters.append(chapter)
    else:
        errors["warning"] += 1
        error_log.append("Unrecognized tag: " + str(link))
