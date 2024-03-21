from utility import process_keystrokes
import sys

class Webpage:
    """
    Webpage represents a given page found in the input
    """
    def __init__(self):
        self.url = None
        self.num_links = None
        self.num_words = None
        self.links = []
        self.words = []
        self.weight = 0

def readinput(filename):
    with open(filename, 'r') as f:
        webpagestringarr = f.read().split("URL: https://")
        weblist = []
        for webpage in webpagestringarr:
            temppage = Webpage()
            tempnumlinks = 0
            tempnumwords = 0
            wordparsing = True
            wordlist = webpage.split(" ")
            for i in range(3, len(wordlist)):
                if wordparsing and wordlist[i] != "LINKS:":
                    tempnumwords += 1
                    temppage.words.append(wordlist[i])
                elif wordparsing and wordlist[i] == "LINKS:":
                    wordparsing = False
                else:
                    tempnumlinks += 1
                    temppage.links.append(wordlist[i])
            weblist.append(temppage)


def main():
    # readinput(sys.argv[1])
    process_keystrokes()

if __name__ == "__main__":
    print(sys.argv)
    main()