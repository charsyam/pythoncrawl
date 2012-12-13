from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    hrefs = []

    def handle_starttag(self, tag, attrs):
        if( tag == "a" ):
            for attr in attrs:
                if( attr[0] == "href" ):
                    self.hrefs.append(attr[1])
