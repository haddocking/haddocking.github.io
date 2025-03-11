#!/usr/bin/env python

"""
Quick and dirty replacement for 'octopress new post'
"""

__author__ = 'J. Rodrigues'

import argparse
import os
import sys
import string # template
import time

news_template = """---
layout: news
title: $title
date: $date
excerpt:
tags: [HADDOCK, Utrecht University, Alexandre Bonvin, Docking]
image:
  feature:
---

"""

if __name__ == '__main__':
    # Parse arguments
    ap = argparse.ArgumentParser(description='Auto-generate new blank posts')
    ap.add_argument('title', help="Title of the post, e.g. 'A Random Post'", nargs='+')
    cmd = ap.parse_args()
    
    rtitle = cmd.title[0].split() # Raw title

    # Check if we are in the root dir of the website
    curdir = os.path.abspath(os.curdir)
    contents = set(os.listdir(curdir))
    if '_config.yml' not in contents:
        print("Run this script in the root folder of the website", file=sys.stderr)
        sys.exit(1)
    
    # Get data and make blank post
    curdate = time.strftime("%Y-%m-%d")
    title = ' '.join(rtitle)
    template = string.Template(news_template)
    post_content = template.substitute({'title': title, 'date': curdate})
    
    # Save file
    ftitle = '-'.join(rtitle) # For filename
    fname = curdate + '-' + ftitle + '.md'
    
    os.chdir('news/_posts')
    with open(fname, 'w') as handle:
        print(post_content, file=handle)

    print("New blank post created at {0}".format(os.path.join('news/_posts', fname)))
