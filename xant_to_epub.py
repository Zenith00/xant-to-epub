import traceback
import argparse
from bs4 import BeautifulSoup
import urllib.request
import re
import collections
from ebooklib import epub

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

def create_epub():
    book = epub.EpubBook()
    book.set_identifier("wat")
    book.set_title("book title")
    book.set_language('en')
    book.add_author('xant')
    return book

def write_epub(epub_obj, series_name, volume_name, chapters, output_dir):
    epub_obj.toc = chapters
    epub_obj.add_item(epub.EpubNav())
    epub_obj.add_item(epub.EpubNcx())
    epub_obj.spine = chapters
    epub_obj.add_item(
        epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content='BODY { text-align: justify;}'))
    try:
        epub.write_epub(f"{output_dir}[{series_name}] {volume_name}.epub", epub_obj)
    except:
        print(traceback.format_exc())

def epubize_link(url, output_dir):
    f = urllib.request.urlopen(url)
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(class_="entry-title").string
    print("Epubizing: " + title)
    # print(title)
    entry_content = soup.find_all("div", class_="entry-content")[-1]
    # print(entry_content)

    linked = strip_fluff(entry_content.find_all([re.compile("h\d"), "a"]))
    name = "Volumeless"
    volumes = collections.defaultdict(create_epub)
    chapters = []
    clean_uri = lambda string_in: ''.join([x for x in string_in if ord(x) < 128 and x != " "])
    for link in linked:
        # print(link.string)
        try:
            link.string = re.sub(r'[\\/*?:"<>|]', "", " ".join(link.strings))
        except:
            print(link.attrs)
            input()
            continue
        if link.name in ["h2", "h3", "h4", "h5", "h6"]:
            print("Recognized Volume " + name)
            if len(chapters) > 0:
                write_epub(volumes[name], title, name, chapters, output_dir)
            name = link.string
            chapters = []
        elif link.name == "a":
            if any(x in str(link.string).lower() for x in ["chapter", "Track"]):
                print("Chapter Found: " + link.string)
                # print(name + ": " + link.string)
                # print(link.attrs["href"])
                chapter = epub.EpubHtml(title=link.string, file_name=clean_uri(link.string) + ".xhtml", content=page_parser(link.attrs['href']),
                                        media_type="application/xhtml+xml")
                chapter.add_item(
                    epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content='BODY { text-align: justify;}'))
                volumes[name].add_item(chapter)
                chapters.append(chapter)
        else:
            errors["warning"] += 1
            error_log.append("Unrecognized tag: " + str(link))
    write_epub(volumes[name], title, name, chapters, output_dir)

epubize_link("https://xantandminions.wordpress.com/the-angel-does-not-desire-the-sky/", "")
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('output')
#     args = parser.parse_args()
#     print(args)
#     f = urllib.request.urlopen("https://xantandminions.wordpress.com/")
#     html = f.read()
#     soup = BeautifulSoup(html, 'html.parser')
#     # print(soup)
#     soup = soup.find(id="primary-menu")
#     # print(soup)
#     soup = soup.find(href="https://xantandminions.wordpress.com/series/", string="Series").parent
#     links = soup.find_all("a")
#     for link in links:
#         if link.string not in ["Series", "Active","Slow","Dropped/Hiatus"]:
#             print("epubizing... " + link.attrs["href"])
#             epubize_link(link.attrs["href"], args.output)
