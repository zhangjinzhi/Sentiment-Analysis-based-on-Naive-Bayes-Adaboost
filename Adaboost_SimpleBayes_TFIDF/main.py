#!/usr/bin/python2.7
# _*_ coding: utf-8 _*_
import numpy as np
import process_data
import load_save_data
import training_model
import random


def AdaboostTrainingWithDS(iterateNum):
    """
    testing error rate of classification
    :param iterateNum:
    :return:
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
    print("construct BOW")
    trainMarkedWords = process_data.transferContentsToVector(BOW, contents)
    print("marking the data is finished")
    # trasnfer to numpy array
    trainMarkedWords = np.array(trainMarkedWords)

    
    vocabMarked_IDF = process_data.IDF(BOW, testWords)

    print("IDF is OK")
    '''
    trainMarkedWords = process_data.TF_IDF(trainMarkedWords,vocabMarked_IDF)
    print("TF_IDF is OK")
    '''

    print("transfer data to matrix")
    proContentNeg, proContentPos, proNeg = training_model.trainingNaiveBayes(trainMarkedWords, labels)

    DS = np.ones(len(BOW))

    ds_errorRate = {}
    minErrorRate = np.inf
    for i in range(iterateNum):
        errorCount = 0.0
        for j in range(testCount):
            testWordsCount = process_data.transferContentToVector(BOW, testWords[j])
            ps, ph, label = training_model.classify(proContentNeg, proContentPos,
                                                       DS, proNeg, testWordsCount,vocabMarked_IDF)

            if label != testWordsType[j]:
                errorCount += 1
                # alpha = (ph - ps) / ps
                alpha = ps - ph
                # print('alpha is ', alpha)
                if alpha > 0: # actual class label is positive，prediction is negative
                    DS[testWordsCount != 0] = np.abs(
                            (DS[testWordsCount != 0] - np.exp(alpha)) / DS[testWordsCount != 0])
                
                else:  # actual class label is negative，prediction is positive
                    DS[testWordsCount != 0] = (DS[testWordsCount != 0] + np.exp(alpha)) / DS[testWordsCount != 0]
        print('DS:', DS)
        errorRate = errorCount / testCount
        if errorRate < minErrorRate:
            minErrorRate = errorRate
            ds_errorRate['minErrorRate'] = minErrorRate
            ds_errorRate['DS'] = DS
        print(' %d iteration, errorCount is %d ,errorRate is %f' % (i, errorCount, errorRate))
        if errorRate == 0.0:
            break
    ds_errorRate['BOW'] = BOW
    ds_errorRate['proContentNeg'] = proContentNeg
    ds_errorRate['proContentPos'] = proContentPos
    ds_errorRate['proNeg'] = proNeg

    load_save_data.saveModelData(ds_errorRate)


def simpleTest():
    # load calculating of model that has been tained
    BOW, proContentNeg, proContentPos, proNeg, trainMinErrorRate, trainDS = load_save_data.getTrainAdaboostInfo()

    # load testing data
    filename = '../data/test.txt'
    contents, labels = load_save_data.loadContentsLabels(filename)
    testWordsMarkedArray = process_data.transferContentToVector(BOW, contents[0])
    IDF_list = process_data.IDF(BOW, contents)
    ps, ph, label = training_model.classify(proContentNeg, proContentPos, trainDS, proNeg, testWordsMarkedArray,IDF_list)
    print(label)


if __name__ == '__main__':
    AdaboostTrainingWithDS(iterateNum = 40)
    # simpleTest()

