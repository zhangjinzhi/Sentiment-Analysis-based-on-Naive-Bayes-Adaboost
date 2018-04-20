from textblob import TextBlob


def changeData(original_fileName,new_fileName):

    with open(new_fileName, 'wt') as f_new:
         

        f_original = open(original_fileName)

        for line in f_original.readlines():
            text = line.strip()

            if len(text.split()) == 0:
                continue

            sentiment_polarity = get_sentiment(text)

            # if sentiment_polarity >= -0.01 and sentiment_polarity <= 0.01:
            #     continue

            if sentiment_polarity >= 0:
                sentiment = "pos"
            else:
                sentiment = "neg"


            context = sentiment +'\t'+text

            print(context, file=f_new)



def get_sentiment(text):

    testimonial = TextBlob(text)

    return testimonial.sentiment.polarity 


if __name__ == '__main__':

    original_fileName = '../data/TweetData_Transfered.txt'
    new_fileName = '../data/CleanedTweetData.txt'

    changeData(original_fileName,new_fileName)

 

    # from nltk.stem.lancaster import LancasterStemmer#Lancaster词干器

    # LancasterStem=LancasterStemmer()

    # print(LancasterStem.stem('studied'))















