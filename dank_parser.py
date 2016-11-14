import re
import sys
import urllib.request
from html.parser import HTMLParser


class TwitchQuoteParser(HTMLParser):
    def __init__(self):
        super(TwitchQuoteParser, self).__init__()
        self.data = []
        self.recording = 0
        # The data we want is inside tags of following pattern:
        # <span id="quote_clipboard_copy_content_X">
        self.pattern = re.compile("quote_clipboard_copy_content_\.*")

    def handle_starttag(self, tag, attrs):
        if tag != "span":
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attrs:
            if name == "id" and self.pattern.match(value):
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == "span" and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)
            self.data.append(".\n")


def write_results(filename, results):
    try:
        with open(filename, "w", encoding="utf8") as outfile:
            for r in results:
                outfile.write(r)
    except (IOError, FileNotFoundError):
        print("Dankness overload! Cannot write results to file!")


def strip_nlcr(string):
    string = string.replace("\t", "")
    string = string.replace("\r", "")
    string = string.replace("\n", "")
    return string


def get_twitchquotes_urls():
    """Forgive me for this function. Returns a list of twitchquotes urls."""
    
    urls = []
    base = "http://www.twitchquotes.com/copypastas?page=XXX&popular=true"
    for i in range(1, 114):
        rep = "XXX"
        urls.append(base.replace(rep, str(i)))
    return urls


def main():
    parser = TwitchQuoteParser()
    outfile = "dankness.txt"

    print("Haxoring twitchquotes.com")
    urls = get_twitchquotes_urls()
    print("Done. Beware of the FBI.\n")

    print("Parsing HTML.")
    for url in urls:
        print("{}".format(url))
        parser.feed(
            strip_nlcr(urllib.request.urlopen(url).read().decode("utf-8")))
    print("Parsing done.\n")

    print("Writing results to file '{}'.".format(outfile))
    write_results(outfile, parser.data)
    print("Done.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
