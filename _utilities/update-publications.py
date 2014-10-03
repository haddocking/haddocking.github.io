#!/usr/bin/env python

"""
Downloads Alexandre's pub list from his website. Converts the HTML to markdown.
"""

import urllib2
import re

year_re = re.compile('\(\d\d\d\d\)')
BOSS_URL = 'http://www.nmr.chem.uu.nl/~abonvin/publications.html'

# boss_page = urllib2.urlopen(BOSS_URL)
boss_page = open('bonvin-pubs.html')
boss_info = boss_page.readlines()

citations = []
parse = False

while boss_info:
    line = boss_info.pop(0).strip().replace('<BR>', '<br>')
    if line.strip().lower().startswith('<ol'):
        parse = True
    elif line.strip().lower().startswith('</ol>'):
        break
    elif parse:
        # Read multiple lines until <P> is found. 
        # Effectively, whole citation
        while '</li>' not in line.lower():
            line += " " + boss_info.pop(0).strip().replace('<BR>', '<br>')

        # Do not trust HTML.. messy
        # Follow boss conventions
        # Titles are always between double quotes
        # everything before is author list
        # everything after is journal / volume / etc
        # journal names might come between EM, volumes in <strong>.
        
        record = line.split('<br>')

        # 1st line, authors
        authors = ''
        for line in record:
            if line.strip()[0] == '"' or 'href' in line.lower():
                break
            authors += line.strip() + ' '

        ori_authors = authors
        authors = authors[4:].strip()
        authors = authors.replace('*', '\*').replace('<font color="#333333"><b>', '**')
        authors = authors.replace('</b></font>', '**')

        # 2nd line, title/url
        title_url = record[1].strip()

        if title_url.lower().startswith('"<a href='): # has url
            sta_pos = title_url.lower().rindex('"<a href="') + 10
            sto_pos = title_url.rindex('">')
            url = title_url[sta_pos:sto_pos]
            title = title_url[sto_pos+2:-5]
        else:
            url = None
            title = title_url[1:-1]

        # 3rd line, Journal, etc
        citation = ' '.join(record[2:]).replace('</li>', '').strip()
        citation = citation.replace('<em>', '_').replace('</em>', '_') 
        citation = citation.replace('*', '\*').replace('<strong>', '*').replace('</strong>', '*') 

        # Year is in citation, between parenthesis
        year = year_re.search(citation)
        if year:
            year = year.group(0)[1:-1]


        citations.append({})
        citations[-1]['authors'] = authors
        citations[-1]['title'] = title
        citations[-1]['url'] = url
        citations[-1]['citation'] = citation
        citations[-1]['year'] = year

# Output markdown style
prev_y = None
for i, entry in enumerate(citations):
    if entry['year']:
        if prev_y != entry['year']:
            print "\n## {0}\n<hr />\n".format(entry['year'])
            prev_y = entry['year']
    print "* {1}".format(str(i+1), entry['authors'])
    if entry['url']:
        print "[{0}]({1})".format(entry['title'], entry['url'])
    else:
        print entry['title']
    print entry['citation']
    print
    