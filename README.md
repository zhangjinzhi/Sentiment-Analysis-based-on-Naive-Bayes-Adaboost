# Sentiment Analysis based on Naive Bayes & Adaboost

This topic aims at improving Naives Bayes algorithm by using feature-correlation-based weighting and improving the performance of Bayes classifier by using Adaboost.

## Getting Started

These instructions will let you apply the project demo and running on your machine for development and testing purposes. 

### Prerequisites

Following tools and packages are required to run this project demo.

#### Programming Language
```
Python 3
```

#### Import Packages
```
numpy
random
re
nltk
textblob
time
tweepy
os
sys
```

### Installing on Windows 10

#### Python Installation
1. Open the <https://www.python.org/downloads/windows/>
2. Download the correct installation package(32 or 64 bits) for Python 3 (Latest Python 3 Release is OK)
3. Execute the installation package and finish the installation (remember to select the item "Add Python x.x to PATH")

#### Package Installation
For the *re* and *random* are included in original Python, we only need to install the *Numpy*, *NLTK* and *TextBlob*.

##### Numpy
1. Open the <http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy>
2. Download the correct *Numpy* wheel for your Python version
3. Go the path of the wheel in cmd and perform the installtion
```
>pip3 install numpy-x.xx.x+mkl-cpxx-cpxxm-win(32 or 64 bits).whl
```
##### NLTK
```
>pip3 install nltk
```
##### TextBlob
```
>pip3 install textblob
```

### Installing on Mac OS X

#### Python Installation
If there is no HomeBrew in your Mac, just install it in termianl.
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
You can use the Homebrew to search and install Python 3 in terminal.
```
$ brew search python
$ brew install python3
```

#### Package Installation
For the *re* and *random* are included in original Python, we only need to install the *Numpy*, *NLTK* and *TextBlob*.

##### Numpy
```
$ pip3 install numpy
```
##### NLTK
```
$ pip3 install nltk
```
##### TextBlob
```
$ pip3 install textblob
```

## Data Source (No need to run again in this demo)

For more details about twitter data crawling api, please refer to [Twitter Developer Docs](https://developer.twitter.com/en/docs/tweets/search/overview)

###  Windows 10 

``` 
>python get_tweets [user] [datatype] [nums_line] [nums_file] 
```

`e.g. >python get_tweets Tom hist 100 3`

which means use the auth key of **Tom** to get **historical** data, then write these data to the **3** files with **100** lines per file.

###  Mac OS X 
``` 
$ python3 get_tweets [user] [datatype] [nums_line] [nums_file] 
```

`e.g. $ python3 get_tweets Tom hist 100 3`

which means use the auth key of **Tom** to get **historical** data, then write these data to the **3** files with **100** lines per file.

As the data has been prepared in the folder 'data', this step can be skip in this demo.

## Data Preprocess (No need to run again in this demo)

### Windows 10 
``` 
>python data_transfer.py 
>python give_label.py 
```
### Mac OS X 
``` 
$ python3 data_transfer.py 
$ python3 give_label.py 
```
Please note the name and path of files in data_transfer.py. ( in Mac)
```
f_old = open('../data/TweetData_Original.txt','r')
f_new = open('../data/TweetData_Transfered.txt', 'w+')
```
Please note the name and path of files in give_label.py. (in Mac)
```
original_fileName = '../data/TweetData_Transfered.txt'
new_fileName = '../data/CleanedTweetData.txt'
changeData(original_fileName,new_fileName)
```
## Running the Demo

1. The project uses 4 spaces per indent instead of tab.
2. Pay attention to the label, which should match your training set and testing set. 

​       As for CleanedTweetData.txt, they are 'pos' and 'neg'. 

​       As for SMS.txt,  they are 'ham' and 'spam'

```
def loadContentsLabels(fileName):
    f = open(fileName)
    labels = []  # the label for type，1 is for negtive content，0 is for positive content
    contents = []
    for line in f.readlines():
        linedatas = line.strip().split('\t')
        if linedatas[0] == 'pos':  # 'ham'
            labels.append(0)
        elif linedatas[0] == 'neg': # 'spam'
            labels.append(1)
        # process the original data, filter useless string
        words = process_data.cleanData(linedatas[1])
        contents.append(words)
    return contents, labels
```
### Running the Simple Bayes Model
You can perform the model by going the path of the folder *SimpleBayes_TFIDF* in terminal and running the main.py.
#### Windows 10

```
>cd X:\xxx\xxx\SimpleBayes_TFIDF
>python main.py
```
#### Mac OS X
```
$ cd /Users/xxx/xxx/SimpleBayes_TFIDF
$ python3 main.py
```
For the count of test set, you can change it by the variable *testCount* in *trainningErrorRate* function in main.py in Mac.
```
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

	......
```
For the source of test set, you can change it by the variable filename in main.py. Take SMS.txt for an example in Mac.
```
def training():
    filename = '../data/SMS.txt'
    ...

def trainningErrorRate():
    filename = '../data/SMS.txt'
    ...
```
### Running the AdaBoost Version Bayes Model

You can perform the model by going the path of the folder *Adaboost_SimpleBayes_TFIDF* in terminal and running the main.py.
#### Windows 10

```
>cd X:\xxx\xxx\Adaboost_SimpleBayes_TFIDF
>python main.py
```
#### Mac OS X
```
$ cd /Users/xxx/xxx/Adaboost_SimpleBayes_TFIDF
$ python3 main.py
```
For the count of test set, you can change it by the variable *testCount* in *AdaboostTrainingWithDS* function in main.py in Mac
```
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

	......
```
For the iteration times of the model, you can change it by the variable *iterateNum* in main function in main.py
```
if __name__ == '__main__':
    AdaboostTrainingWithDS(iterateNum = 40)
```

For the source of test set, you can change it by the variable *filename* in main.py. Take SMS.txt for an example in Mac.

```
def AdaboostTrainingWithDS(iterateNum):
    filename = '../data/SMS.txt'
```

<div align="center">
<img src="https://raw.githubusercontent.com/zhangjinzhi/Sentiment-Analysis-based-on-Naive-Bayes-Adaboost/master/images/Github.jpg" height="30%" width="30%">
<img src="https://raw.githubusercontent.com/zhangjinzhi/Sentiment-Analysis-based-on-Naive-Bayes-Adaboost/master/images/Youtube.jpg" height="30%" width="30%">
<img src="https://raw.githubusercontent.com/zhangjinzhi/Sentiment-Analysis-based-on-Naive-Bayes-Adaboost/master/images/Demo%20Video.png" height="29%" width="29%">
</div>

[Github](https://github.com/zhangjinzhi/Sentiment-Analysis-based-on-Naive-Bayes-Adaboost)

[Youtube](https://www.youtube.com/watch?v=ZWTm23z2cxc)

[Demo Video](https://drive.google.com/drive/folders/1QuY5c65LM5mtMW9iWpW0mscyIRZV53rk?usp=sharing)