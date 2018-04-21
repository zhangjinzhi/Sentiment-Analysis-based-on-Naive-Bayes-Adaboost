import numpy as np
import process_data
import load_save_data
import training_model
import random

def training():
    # load file
    filename = '../data/CleanedTweetData.txt'
    #get the text content and labels in file
    contents, labels = load_save_data.loadContentsLabels(filename)
    # print contents
    BOW = process_data.createBOW(contents)
    print("generate BOW")
    trainMarkedWords = process_data.transferContentsToVector(BOW, contents)
    print("marking the data is finished")
    # transfer ti list to np.array
    trainMarkedWords = np.array(trainMarkedWords)

    '''
    contents_for_TFIDF = load_save_data.loadContents_for_TFIDF(filename)
    print("loadContents_for_TFIDF is OK")
    vocabMarked_IDF = process_data.IDF(BOW, contents_for_TFIDF)
    print("calculating IDF is OK")

    trainMarkedWords = process_data.TF_IDF(trainMarkedWords,vocabMarked_IDF)
    print("calculating TF_IDF is OK")
    '''
    print("transfer data to matrix")
    proContentNeg, proContentPos, proNeg = training_model.trainingNaiveBayes(trainMarkedWords, labels)
    print('proNeg is:', proNeg)

    load_save_data.saveModelData(proContentNeg, proContentPos, proNeg, BOW)



def simpleTest():
    # load calculating of model that has been tained
    BOW, proContentNeg, proContentPos, proNeg = load_save_data.loadTrainedModelInfo()

    # load testing data
    filename = '../data/test.txt'
    contents, labels = load_save_data.loadContentsLabels(filename)
    contents_for_TFIDF = load_save_data.loadContents_for_TFIDF(filename)
    IDF_list = process_data.IDF(BOW, contents)
    # print(contents[0])
    # print(contents_for_TFIDF)
    # print(IDF_list)
    label = training_model.classify(BOW, proContentNeg,proContentPos, proNeg, contents[0],IDF_list)
    print(label)


def trainningErrorRate():
    """
    : test the error rate of classification
    : return errorCount and errorRate
    """
    filename = '../data/CleanedTweetData.txt'
    contents, labels = load_save_data.loadContentsLabels(filename)

    # Cross-validation
    testWords = []
    testWordsType = []

    testCount = 1000
    for i in range(testCount):
        randomIndex = int(random.uniform(0, len(contents)))
        testWordsType.append(labels[randomIndex])
        testWords.append(contents[randomIndex])
        del (contents[randomIndex])
        del (labels[randomIndex])

    BOW = process_data.createBOW(contents)
    print("generate BOW")
    trainMarkedWords = process_data.transferContentsToVector(BOW, contents)
    print("marking the data is finished")
    # transfer data to array
    trainMarkedWords = np.array(trainMarkedWords)
    print("transfer data to matrix")
    proContentNeg, proContentPos, proNeg = training_model.trainingNaiveBayes(trainMarkedWords, labels)

    errorCount = 0.0

    IDF_list = process_data.IDF(BOW, testWords)

    for i in range(testCount):
        
        label = training_model.classify(BOW, proContentNeg, proContentPos, proNeg, testWords[i], IDF_list)
        
        print('predictive class: ', label, 'actual class: ', testWordsType[i])

        if label != testWordsType[i]:
            errorCount += 1

    print('error count is: ', errorCount, 'error rate is: ', errorCount / testCount)


if __name__ == '__main__':
    training()
    trainningErrorRate()
    # simpleTest()
