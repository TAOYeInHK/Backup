__author__ = 'ty'

import os
import sys
import time
import threading
import re
import urllib2
import urllib

#url = 'http://m.sohu.com/'
#directory = '/Users/ty/Desktop/'

pattern_js = r'src="(.+?([\d\w_]+\.js))"'
pattern_img = r'(original|src)="(.+?([\d\w_]+\.jpg)|.+?([\d\w_]+\.png))"'
pattern_css = r'href="(.+?([\d\w_]+\.css))"'


def get_timestamp():
    return time.strftime("%Y%m%d%H%M", time.localtime())

def html_handler(content, dir_html):
    with open(dir_html, 'w') as index:
        index.write(content)

def img_handler(content, dir_img):
    img_src = re.findall(pattern_img, content)
    for item in img_src:
        if len(item[2]) == 0:
            dir_img_single = dir_img + item[3]
            urllib.urlretrieve(item[1], dir_img_single)
        else:
            dir_img_single = dir_img + item[2]
            urllib.urlretrieve(item[1], dir_img_single)

def js_handler(content, dir_js):
    js_src = re.findall(pattern_js, content)
    for item in js_src:
        dir_js_single = dir_js+item[1]
        urllib.urlretrieve(item[0], dir_js_single)

def css_handler(content, dir_css):
    css_src = re.findall(pattern_css, content)
    for item in css_src:
        dir_css_single = dir_css + item[1]
        urllib.urlretrieve(item[0], dir_css_single)


def backup(timestamp, url, directory):
    os.mkdir(directory+timestamp)
    os.makedirs(directory+timestamp+'/js')
    os.makedirs(directory+timestamp+'/images')
    os.makedirs(directory+timestamp+'/css')
    content = urllib2.urlopen(url).read()
    dir_html = directory+timestamp+'/index.html'
    dir_img = directory+timestamp+'/images/'
    dir_js = directory+timestamp+'/js/'
    dir_css = directory+timestamp+'/css/'

    thread1 = threading.Thread(target=html_handler(content, dir_html))
    thread2 = threading.Thread(target=img_handler(content, dir_img))
    thread3 = threading.Thread(target=js_handler(content, dir_js))
    thread4 = threading.Thread(target=css_handler(content, dir_css))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


def main(argv):
    while True:
        timestamp = get_timestamp()
        backup_thread = threading.Thread(target=backup(timestamp, argv[2], argv[3]))
        backup_thread.start()
        backup_thread.join()
        time.sleep(float(argv[1]))

if __name__ == '__main__':
    main(sys.argv)
