import fnmatch
import os
import re
from collections import defaultdict
from math import log10

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer

dct = defaultdict(list)

# Modify as per the system
docDirectory = './crawled-data/'
totalDocs = 1000
K = 20
stopWordList = []


# Parsing stop word list
def create_stop_word():
    global stopWordList
    url = "http://www.lextek.com/manuals/onix/stopwords1.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    list_of_words = []
    for blockqoute_word in soup.findAll('blockquote'):
        list_of_words.append(blockqoute_word)
        stopWordList = str(list_of_words[0]).split()
    stopWordList = stopWordList[77:503]


def is_stop_word(term):
    term1 = term.lower()
    if term1.isdigit() or len(term1) <= 2 or term1 in stopWordList:
        return True
    else:
        return False


def calculate_avg_gap(lst):
    for index in range(K - 1):
        total = 0
        word = lst[index][1]
        posting_list = dct[word]
        posting_list = list(set(posting_list))  # To retrieve unique docIds
        for posting_list_index in range(0, len(posting_list) - 1):
            total = total + abs(posting_list[posting_list_index] - posting_list[posting_list_index + 1])
        print(str(word) + ": " + str(float(total) / float(len(posting_list) - 1)))


def statistical_analysis():
    arr = []
    for key, value in dct.items():
        arr.append((len(set(value)), key))

    # Sorting the list based on the its document-frequency
    arr.sort()
    element_count = len(arr)

    # Least Frequent
    freq = []
    for item in range(K):
        freq.append(arr[item])
    print("\nLeast Frequent Words:\n" + str(freq))
    calculate_avg_gap(freq)

    # Most Frequent
    freq = []
    for item in range(element_count - 1, element_count - 1 - K, -1):
        freq.append(arr[item])
    print("\nMost Frequent Words:\n" + str(freq))
    calculate_avg_gap(freq)

    # Median Frequent
    freq = []
    for item in range(int(element_count / 2 - K / 2), int(element_count / 2 + K / 2)):
        freq.append(arr[item])
    print("\nMedian Frequent Words:\n" + str(freq))
    calculate_avg_gap(freq)


def stemming(term):
    try:
        stemmed = SnowballStemmer("english").stem(term)
        return str(stemmed)
    except:
        return term


def calculate_index_char(index_name, dictionary):
    dct_len = len(dictionary)
    max = 0
    min = 9999999
    total_len = 0
    for word, list in dictionary.items():
        list_len = len(list)
        if max < list_len:
            max = list_len
        if min > list_len:
            min = list_len
            total_len = total_len + list_len
    print("\nCharacteristics of Index " + str(index_name) + ":")
    print("Number of Terms: " + str(dct_len))
    print("Maximum length of Postings List: " + str(max))
    print("Minimum length of Postings List: " + str(min))
    print("Average length of Postings List: " + str(total_len / dct_len))
    print("Size of file: " + str(float(os.path.getsize(index_name + ".txt")) / float(1024)) + " KB\n")


def make_inverted_index(index_name, dictionary):
    with open(index_name + ".txt", "w") as file:

        for key, list in dictionary.items():
            op_str = key + " "
            for doc_id in list:
                op_str = op_str + str(doc_id) + ","
            file.write(op_str[:-1] + "\n")
    file.close()
    calculate_index_char(index_name, dictionary)


def make_i1(dct_old):
    # Original Index
    make_inverted_index("I1", dct_old)


def make_i2(dct_old):
    # Stop Word Removal
    dct_new = defaultdict(list)
    for word in dct_old:
        if not is_stop_word(word):
            dct_new[word] = dct_old[word]
    make_inverted_index("I2", dct_new)
    return dct_new


def make_i3(dct_old):
    # Stemming
    dct_new = defaultdict(list)
    for word in dct_old:
        stemmed_word = stemming(word)
        if word != stemmed_word:
            for docIds in dct_old[word]:
                dct_new[stemmed_word].append(docIds)
        else:
            dct_new[word] = dct_old[word]
    make_inverted_index("I3", dct_new)
    return dct_new


def make_i4(dct_old):
    # Do not consider terms which are occurring in < 2% of  the documents
    dct_new = defaultdict(list)
    for word, item in dct_old.items():
        # To remove repetitions
        item = list(set(item))
        if len(item) >= (0.02 * totalDocs):
            dct_new[word] = dct_old[word]

    make_inverted_index("I4", dct_new)
    return dct_new


def create_graph(graph_list, x_label, y_label, plot_name):
    x_axis = []
    y_axis = []
    for item in graphList:
        x_axis.append(item[0])
        y_axis.append(item[1])

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.scatter(x_axis, y_axis)
    plt.plot(x_axis, y_axis)
    try:  # Remove file, if already exists
        os.remove(plot_name + ".png")
    except:
        pass
    plt.savefig(plot_name + ".png")
    plt.close()


# Procedure Init
if __name__ == "__main__":
    date = []
    pattern = re.compile(r'.\\+x[a-zA-Z0-9]{1,4}.', 0)
    for i in [1, 31]:
        date.append(str(i))
    for docNum in range(1, totalDocs + 1):
        with open(docDirectory + str(docNum) + ".txt") as file:
            for line in file:
                # Considering only lowercase characters
                line = str(line.lower())
                # Concatenating all Date Formats
                date = re.findall(
                    r'(\s)+((\d*){1,4}(\s*)(?:january|february|march|april|may|june|july|august|september|october|november|december)(\s+)(\d+){1,4}(x*\d*){1,4})\s',
                    line)
                if date:
                    mod = date[0][1].replace(' ', '')
                    line = re.sub(date[0][1], mod, line)
                for word in re.split(' ', line):
                    # for removing fullstops, commas and other not useful data
                    if not fnmatch.fnmatch(word, "*:"):
                        if fnmatch.fnmatch(word, "http*") or fnmatch.fnmatch(word, "*-*-*"):
                            pass
                        else:
                            word = re.sub(r'[^\w]', '', word)
                        if word != '' and word != 'doc':
                            word = re.sub(r'\n', '', word)
                            dct[word].append(docNum)

    # Stop Word Filtering and Stemming
    create_stop_word()
    make_i1(dct)  # Original Index
    dct = make_i2(dct)  # Stop Word removal
    dct = make_i3(dct)  # Stemming
    dct = make_i4(dct)  # Remove less frequent words

    # Statistical Analysis
    statistical_analysis()

    # Create Log Graph - I
    topCollect = []
    termsFreq = [(word, len(items)) for word, items in dct.items()]
    termsFreq = sorted(termsFreq, key=lambda x: x[1], reverse=True)
    topCollect = [word for (word, freq) in termsFreq if len(topCollect) < 1000]
    topFreq = [freq for (word, freq) in termsFreq if len(topCollect) < 1000]

    graphList = []
    for i in range(1, len(topFreq)):
        graphList.append((log10(i), log10(topFreq[i])))

    create_graph(graphList, "log(Rank of the Term)", "log(Collection Frequency of the Term)", "logRankCollectionFreq")

    # Create Log Graph - II
    graphList = []
    vocabularyObs = []
    tokenCount = 0
    for docId in range(1, totalDocs + 1):
        for key, listOfWords in dct.items():
            occurrences = listOfWords.count(docId)
            tokenCount = tokenCount + occurrences
            if occurrences and key not in vocabularyObs:
                vocabularyObs.append(key)  # Add to vocabulary
        graphList.append((log10(tokenCount), log10(len(vocabularyObs))))

    create_graph(graphList, "log(#Tokens observed)", "log(#Vocabulory observed)", "logTokenVocabulary")
