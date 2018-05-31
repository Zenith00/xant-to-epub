from bs4 import BeautifulSoup
import urllib.request

url = "https://xantandminions.wordpress.com/kuma-kuma-kuma-bear/"
f = urllib.request.urlopen(url)
html = f.read()
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())
print("break\n"*4)
# print(soup.select("div.entry-content"))
entry_content = soup.find_all("div", class_="entry-content")[-1]
