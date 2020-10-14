import re

def convert(content):
    htmlCode = []

    start = True
    listing  = False
    lineBreaking = False

    for line in content.splitlines():
        if len(line) == 0:
            line = findLineBreak(line, lineBreaking)                

        else:
            lineBreaking = False

            line = findHeader(line, start)
            line = findList(line, listing)

            listing = listingCheck(listing, line, htmlCode)

            if noTags(line):
                line = addParagraph(line)

            line = findBoldText(line)
            line = findItalicText(line)
            line = findLinks(line)

            htmlCode.append(line)
            start = False

    if listing:
        endList(htmlCode)

    return htmlCode

def findLineBreak(line, lineBreaking):
    if not lineBreaking:
        lineBreaking = True
        line = "<br>"

    return line


def findHeader(line, start):
    tag = re.match("#+", line)

    if tag != None:
        header = True
        size = tag.end()

        if (start):
            line = f"<h{size}>{line[size:]}</h{size}><hr><br>"
        else:
            line = f"<br><h{size}>{line[size:]}</h{size}><hr><br>"

    return line


def findBoldText(line):
    tag = re.search("[*]{2}.+?[*]{2}", line)

    while tag != None:
        line = line[:tag.start()] + "<b>" + tag.group(0)[2:-2] + "</b>" + line[tag.end():]
        tag = re.search("[*]{2}.+?[*]{2}", line)

    return line

def findItalicText(line):
    tag = re.search("\*.+?\*|_.+?_", line)

    while tag != None:
        line = line[:tag.start()] + "<i>" + tag.group(0)[1:-1] + "</i>" + line[tag.end():]
        tag = re.search("\*.+?\*|_.+?_", line)

    return line


def findList(line, listing):
    tag = re.match("\- |\* ", line)

    if tag != None:
        if not listing :
            line = "<ul><li>" + line[2:] + "</li>"
        else:
            line = "<li>" + line[2:] + "</li>"

    return line


def listingCheck(listing, line, code):
    tag = re.match("<ul>|<li>", line)

    if tag != None:
        return True

    elif listing:
        endList(code)

    return False

import time

def findLinks(line):
    tag = re.search("\[.+?\]", line)

    while tag != None:
        linkLabel = tag.group(0)[1:-1]

        addrTag = re.search("\(.+?\)", line[tag.end():])
        address = addrTag.group(0)[1:-1]

        hyperlink = f'<a href="{address}">{linkLabel}</a>'

        line = line[:tag.start()] + hyperlink + line[tag.end() + addrTag.end():]
        tag = re.search("\[.+?\]", line)

    return line


def noTags(line):
    tag = re.match("<", line)

    if tag == None:
        return True

    return False


def addParagraph(line):
    return "<p>" + line + "</p>"


def endList(code):
    code[-1] += "</ul>"