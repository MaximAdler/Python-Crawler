#!/usr/bin/env python
import sys
from crawler import crawlWebsite

crawl = crawlWebsite(sys.argv[1])
print crawl
