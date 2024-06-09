import urllib.request
import re
from datetime import datetime
from html import unescape
from time import sleep
import ssl

#To do:
#-Private posts

user = input("Enter your Quotev URL: ")
url = 'https://www.quotev.com/{}/activity?vt=pages'.format(user)
fname = user[:10] + '_activity.txt'
#password = input('Please enter your password, or press enter to skip. Without it, the scraper can only access public posts from the last year. Your password will not be stored: ')
ssl._create_default_https_context = ssl._create_unverified_context
print("Working...")

pageOffset = ''
count = 0

outfile = open(fname,'w',encoding='utf-8')
outfile.write("{} activity crawled on {}".format(user,datetime.now()))
outfile = open(fname,'a',encoding='utf-8')

while True:
    sleep(.1)
    page = urllib.request.urlopen(url + pageOffset)
    raw = page.read().decode('utf-8')

    times = re.findall(r'(?<=datetime=")[^"]+',raw)
    posts = re.findall(r'(?<=<div class="msg">).+?(?=</div>)',raw)
    likes = re.findall(r'(?<=data-count=")\d+',raw)

    count += len(posts)
    for i in range(len(posts)):
        text = unescape(posts[i])
        text = text.replace('<br>','\n')
        text = re.sub(r'<.+?>','',text)
        outfile.write('\n\n{}\t| {}\n{}'.format(times[i],likes[i],text))

    try:
        pageOffset = re.search(r'\&last=\d+\.\d+',raw).group()
    except AttributeError:
        print("Scraped {} activities posted since {}".format(count,times[-1]))
        print("Saved to " + fname)
        print("Last page:",url + pageOffset)
        break

outfile.close()
