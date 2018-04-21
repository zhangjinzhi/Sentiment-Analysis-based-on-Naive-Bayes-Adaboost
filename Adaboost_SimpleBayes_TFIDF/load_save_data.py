import process_data
import numpy as np

def loadContentsLabels(fileName):
    """
    load data from txt file and split the line in two parts
    :param fileName:
    :return contents, labels:
    """
    f = open(fileName)
    labels = []  # the label for type，1 is for negtive content，0 is for positive content
    contents = []
    for line in f.readlines():
        linedatas = line.strip().split('\t')
        if linedatas[0] == 'pos':
            labels.append(0)
        elif linedatas[0] == 'neg':
            labels.append(1)
        # process the original data, filter useless string
        words = process_data.cleanData(linedatas[1])
        contents.append(words)
    return contents, labels


def loadContents_for_TFIDF(fileName):
    """
    load data from txt file and just collect the content
    :param fileName:
    :return contents:
    """
    f = open(fileName)
    contents = []
    for line in f.readlines():
        linedatas = line.strip().split('\t')

        content = linedatas[1]

        contents.append(content)

    return contents

def loadBOW(fileName):
    """
    load the BOW from the txt file
    :param fileName:
    :return BOW:
    """
    fr = open(fileName)
    BOW = fr.readline().strip().split('\t')
    fr.close()
    return BOW


def loadTrainedModelInfo():
    """
    load the information of the model from related txt files 
    :return BOW, proContentNeg, proContentPos, proNeg:
    """
    # loading the BOW
    BOW = loadBOW('BOW.txt')
    proContentPos = np.loadtxt('proContentPos.txt', delimiter='\t')
    proContentNeg = np.loadtxt('proContentNeg.txt', delimiter='\t')
    fr = open('proNeg.txt')
    proNeg = float(fr.readline().strip())
    fr.close()

    return BOW, proContentNeg, proContentPos, proNeg

def getTrainAdaboostInfo():
    """
    获取训练算法阶段的DS和minErrorRate信息
    :return:
    """
    trainDS = np.loadtxt('trainDS.txt', delimiter='\t')
    trainMinErrorRate = np.loadtxt('trainMinErrorRate.txt', delimiter='\t')
    BOW = loadBOW('BOW.txt')
    proContentNeg = np.loadtxt('proContentNeg.txt', delimiter='\t')
    proContentPos = np.loadtxt('proContentPos.txt', delimiter='\t')
    proNeg = np.loadtxt('proNeg.txt', delimiter='\t')
    return BOW, proContentNeg, proContentPos, proNeg, trainMinErrorRate, trainDS


def saveModelData(dsErrorRate):

    # 保存模型训练的信息
    np.savetxt('proContentNeg.txt', dsErrorRate['proContentNeg'], delimiter='\t')
    np.savetxt('proContentPos.txt', dsErrorRate['proContentPos'], delimiter='\t')
    np.savetxt('proNeg.txt', np.array([dsErrorRate['proNeg']]), delimiter='\t')
    np.savetxt('trainDS.txt', dsErrorRate['DS'], delimiter='\t')
    np.savetxt('trainMinErrorRate.txt', np.array([dsErrorRate['minErrorRate']]), delimiter='\t')
    vocabulary = dsErrorRate['BOW']
    fw = open('BOW.txt', 'w')
    for i in range(len(vocabulary)):
        fw.write(vocabulary[i] + '\t')
    fw.flush()
    fw.close()



