import re
import numpy as np

def cleanData(text):
    """
    filter the empty string and set the content in lower case
    :param text:
    :return words:
    """
    regEx = re.compile(r'[^a-zA-Z]|\d')  # use regular expression to find the target(leave the word)
    words = regEx.split(text)

    words = [word.lower() for word in words if len(word) > 0]
    return words


def createBOW(contents):
    """
    construct the BOW
    :param contents:
    :return BOW:
    """
    vocabularySet = set([])
    for words in contents:
        vocabularySet = vocabularySet | set(words)
    BOW = list(vocabularySet)
    return BOW


def transferContentToVector(BOW, content):
    """
    use input content to match the BOW, and do the counting
    :param BOW:
    :param content:
    :return vocabMarked:
    """
    vocabMarked = [0] * len(BOW)
    for Word in content:
        if Word in BOW:
            vocabMarked[BOW.index(Word)] += 1
    return np.array(vocabMarked)


def transferContentsToVector(BOW, contents):
    """
    do the counting for all the contents
    :param BOW:
    :param contents:
    :return vocabMarkedList:
    """
    vocabMarkedList = []
    for i in range(len(contents)):
        vocabMarked = transferContentToVector(BOW, contents[i])
        vocabMarkedList.append(vocabMarked)
    return vocabMarkedList
    

def IDF(BOW, contents_for_TFIDF):
    """
    calculate the idf of each word in contents
    :param BOW:
    :param contents:
    :return vocabMarked_IDF:
    """
    # num = 0
    vocabMarked = [0] * len(BOW)
    for content in contents_for_TFIDF:
        # num += 1
        # print "content" + str(num)
        for vocabulary in BOW:
            # print vocabulary
            if vocabulary in content:
                vocabMarked[BOW.index(vocabulary)] += 1

    vocabMarked = np.array(vocabMarked)

    vocabMarked_IDF = np.log(len(contents_for_TFIDF)*1.0/(vocabMarked+1) )

    return vocabMarked_IDF

def TF_IDF(vocabMarked,vocabMarked_IDF):
	#calculate and return the tf-idf
    TFIDF = vocabMarked * vocabMarked_IDF
    TFIDF = np.array(TFIDF)
    TFIDF = TFIDF / (np.sqrt(sum((list(map(lambda x: x**2, TFIDF))))))
    return TFIDF

