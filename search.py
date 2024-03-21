import sys
import utility

# GLOBALS
links = {}

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
        self.weight = 1

    def __str__(self):
        return f"URL: {self.url}, NUM_LINKS: {self.num_links}, NUM_WORDS: {self.num_words}, WEIGHT: {self.weight}"


def readinput(filename):
    with open(filename, 'r') as f:
        d = "URL: http"
        webpagestringarr = [d + i for i in " ".join(f.read().split("\n")).split("URL: http") if i]
        weblist = []
        addallinternallinks(webpagestringarr)
        for webpage in webpagestringarr:
            temppage = Webpage()
            tempnumlinks = 0
            tempnumwords = 0
            wordparsing = True
            wordlist = webpage.split(" ")
            temppage.url = wordlist[1]
            for i in range(3, len(wordlist)):
                if len(wordlist[i]) == 0:
                    continue
                elif wordparsing and wordlist[i] != "LINKS:":
                    tempnumwords += 1
                    temppage.words.append(wordlist[i])
                elif wordlist[i] == "LINKS:":
                    wordparsing = False
                else:
                    if wordlist[i] in links.keys():
                        tempnumlinks += 1
                        temppage.links.append(links.get(wordlist[i]))
            temppage.num_words = tempnumwords
            temppage.num_links = tempnumlinks
            weblist.append(temppage)
    return weblist

def index(weblist):
    words = []
    wordsdict = {}
    for page in weblist:
        for i in range(len(page.words)):
            if wordsdict.get(page.words[i]) is not None:
                words[wordsdict.get(page.words[i])][1].add(links.get(page.url))
                words[wordsdict.get(page.words[i])][2] += 1
            else:
                k = len(words)
                wordsdict.update({page.words[i]: k})
                tempset = set()
                tempset.add(links.get(page.url))
                words.append([page.words[i], tempset, 1])
    return words, wordsdict

def query(queryterm, pagelist, wordstuff):
    results = None
    if pagelist and wordstuff is not None:
        worddict = wordstuff[1]
        if worddict.get(queryterm) is not None:
            word = wordstuff[0][worddict.get(queryterm)]
            if word is not None:
                results = []
                for id in word[1]:
                    link = pagelist[id].url
                    snippet = getsnippet(id, word[0], pagelist)
                    weight = pagelist[id].weight
                    results.append((link, snippet, weight, word[0]))
            sortedlist = sorted(results, key=lambda x: x[2], reverse=True)
            last = min(sortedlist.index(sortedlist[-1]), 5)
            return sortedlist[:last]
    else:
        return [(None, "Test", None, None)]

def pagerank(pages):
    global pagelist
    if pagelist is not None:
        new_weight = None
        for i in range(50):
            new_weight = [0.1] * len(pages)
            for i in range(len(pages)):
                if pages[i].num_links > 0:
                    for j in range(len(pages[i].links)):
                        new_weight[pages[i].links[j]] += 0.9 * pages[i].weight/pages[i].num_links
                else:
                    new_weight[i] += pages[i].weight * 0.9
            for i in range(len(pages)):
                pages[i].weight = new_weight[i]
    return pages

def addallinternallinks(pages):
    j = 0
    for page in pages:
        wordlist = page.split(" ")
        links.update({wordlist[1]: j})
        j += 1

def getsnippet(id, word, pagelist):
    page = pagelist[id]
    index = page.words.index(word)
    elements = getsurroundingelements(page.words, index)
    elementstr = " ".join(elements)
    return elementstr

def getsurroundingelements(wordlist, index):
    start = max(0, index - 5)
    end = min(len(wordlist), index + 5 + 1)

    if end - start < 5:
        if start == 0:
            end = min(len(wordlist), start + 5)
        elif end == len(wordlist):
            start = max(0, end - 5)
    return wordlist[start:end]

def main():
    global wordstuff
    global pagelist
    wordstuff = None
    pagelist = None
    pagelist = readinput(sys.argv[1])
    wordstuff = index(pagelist)
    pagelist = pagerank(pagelist)
    utility.process_keystrokes(pagelist, wordstuff)


if __name__ == "__main__":
    main()
