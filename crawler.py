#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, HTTPError

def crawlWebsite(url, main_arr = []):

    print '\n'

    def sendRequest(url):
        try:
            print ('Now crawl from: %s' % url)
            sys.stdout.write("\033[F")
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
            return urlopen(req).read()
        except HTTPError:
            return False

    def fulfillArray(ws, normalLink = False):
        global count
        soup = BeautifulSoup(ws, "html.parser")
        for link in soup.find_all('a'):
            link = link.get('href')
            if link != None:
                ext = ['.jpg', '.png', '.gif', '.pdf', '.doc', '.xlsx']
                finded_ext = ''
                for ex in ext:
                    try:
                        link.index(ex)
                        finded_ext = ex
                        break
                    except ValueError:
                        pass
                if finded_ext != '':
                    try:
                        link.index('?')
                    except ValueError:
                        continue

                has_protocols = 0
                protocols = ['http://', 'https://']
                for p in protocols:
                    try:
                        link.index(p)
                        if link.index(p) == 0:
                            try:
                                has_protocols  += 1
                                link.index(clear_url)
                                main_arr.append(link)
                            except ValueError:
                                pass
                    except ValueError:
                        if has_protocols == 0 and link[:8] != 'https://':
                            if link[:1] == '/':
                                link = url + link
                                has_protocols  += 1
                                main_arr.append(link)
                            else:
                                if url[-1:] != "/":
                                    link = url + "/" + link
                                else:
                                    link = url + link
                                has_protocols  += 1
                                main_arr.append(link)
        return list(set(main_arr))

    def crawl(arr, checked_arr):
        prev_length = len(arr)
        for a_url in arr:
            try:
                checked_arr.index(a_url)
                pass
            except ValueError:
                website = sendRequest(a_url)
                if website:
                    arr = fulfillArray(website)
                    post_length = len(arr)
                checked_arr.append(a_url)
                # sys.stdout.write('Number of crawled links: %d\r' % len(arr))
                # sys.stdout.flush()

        post_length = len(arr)

        if prev_length != post_length:
            return crawl(arr, checked_arr)
        else:
            print "\nT H E  E N D\n"
            print 'Array length: %d\n' % len(arr)
            return arr

    try:
        url.index('http://')
        httpUrl = True
    except ValueError:
        httpUrl = False
    try:
        url.index('https://')
        httpsUrl = True
    except ValueError:
        httpsUrl = False

    if httpsUrl or httpUrl:
        clear_url = url.split('http://')
        clear_url = url.split('https://')[1] if len(clear_url) == 1 else clear_url[1]
    else:
        clear_url = url
        url = 'http://' + url

    main_arr.append(url)

    print '\n'

    return crawl(main_arr, [])
