"""Docstring."""

import os
import sys
from html.parser import HTMLParser


class TwitchQuoteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_parsed = []

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag :", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag  :", tag)

    def handle_data(self, data):
        print("Encountered some data. Memefying.")
        self.data_parsed.append(data)

    def get_data_parsed(self):
        return self.data_parsed


def read_raw(filename):
    try:
        with open(filename, "r", encoding="utf8") as infile:
            return infile.read().replace("\n", "")
    except (IOError, FileNotFoundError):
        print("Dankness overload! Cannot read raw data from file!")


def write_results(filename, results):
    try:
        with open(filename, "a", encoding="utf8") as outfile:
            for r in results:
                outfile.write(r)
    except (IOError, FileNotFoundError):
        print("Dankness overload! Cannot write results to file!")


def scan_directory():
    filenames = [
        name for name in os.listdir(".") if name.endswith(".html")]
    return filenames


def main():
    parser = TwitchQuoteParser()
    output = "dankness.txt"

    print("Scanning directory for HTML files.")
    raw_files = scan_directory()
    print("Scan complete.\n")

    print("Parsing HTML files.")
    for file_ in raw_files:
        parser.feed(read_raw(file_))
    print("Parsing completed.\n")

    print("Writing results to file '{}'.".format(output))
    write_results(output, parser.get_data_parsed())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
