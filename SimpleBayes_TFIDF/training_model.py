import numpy as np
import process_data

def trainingNaiveBayes(trainMarkedWords, trainLabels):
    """
    load vocabulary of train data to calculate probability of negative：P（Wi|S）
    :param trainMarkedWords: marked data according to BOW, two-dimensional array
    :param trainLabels:
    :return proContentNeg : probability of content that is negative
            proContentPos : probability of content that is positive
            proNeg : negative rate of contents in file 
    """
    numTrainDoc = len(trainMarkedWords)
    numWords = len(trainMarkedWords[0])
    # Priori probability of negative contents: P(S)
    proNeg = sum(trainLabels) / float(numTrainDoc)

    # calcualte the number of words ( in BOW ) that occurs in file 
    wordsInSpamNum = np.ones(numWords)
    wordsInHealthNum = np.ones(numWords)
    spamWordsNum = 2.0
    healthWordsNum = 2.0
    for i in range(0, numTrainDoc):
        if trainLabels[i] == 1:  # if it is negative
            wordsInSpamNum += trainMarkedWords[i]
            spamWordsNum += sum(trainMarkedWords[i])  # calculate totoal times words occur that are from negative BOW
        else:
            wordsInHealthNum += trainMarkedWords[i]
            healthWordsNum += sum(trainMarkedWords[i])

    proContentNeg = np.log(wordsInSpamNum / spamWordsNum)
    proContentPos = np.log(wordsInHealthNum / healthWordsNum)

    return proContentNeg, proContentPos, proNeg




def classify(BOW, proContentNeg, proContentPos, proNeg, content,IDF_list):
    """
    calculate joint probability to classify
    :param BOW:
    :param proContentNeg:
    :param proContentPos:
    :param proNeg:
    :param contents:
    :return 1 or 0:
    """
    contentsCount = process_data.transferContentToVector(BOW, content)
    contentsMarkedArray = np.array(contentsCount)


    # vocabMarked_IDF = TFIDF.IDF(BOW, content)
    # contentsMarkedArray = TFIDF.TF_IDF(contentsMarkedArray,vocabMarked_IDF)

    TFIDF = contentsMarkedArray * IDF_list
    TFIDF = np.array(TFIDF)
    TFIDF = TFIDF / (np.sqrt(sum((list(map(lambda x: x**2, TFIDF))))))

    #calcualte P(Ci|W), W is vector. calculating P(Ci|W) just needs to calcualte P(W|Ci)P(Ci)
    p1 = sum(proContentNeg * TFIDF) + np.log(proNeg)
    p0 = sum(proContentPos * TFIDF) + np.log(1 - proNeg)
    # print 'p1 is ',p1,'p0 is ',p0
    if p1 > p0:
        return 1
    else:
        return 0
