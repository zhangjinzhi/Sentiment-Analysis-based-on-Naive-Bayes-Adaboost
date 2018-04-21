import os
import tweepy
import tw_util
import tw_class

class MyWriter:

    nums_line = 0
    nums_file = 0
    save_path = "" #文件保存的路径，默认为执行该脚本的路径

    count_line = 0 #没有写完的文件里，写了多少行
    count_file = 0 #目前已经完整的文件数

    __latest_id = 0  # 最近插入的一条数据的id，为了尽可能使其从上次中断的地方继续爬取而不是完全重新爬取

    mode = None

    def __check_exit(self): 

        '''
        检查是否已经完成目标，若完成目标就终止进程
        '''

        if self.count_file == self.nums_file:
            exit()

    def __check_record(self):

        '''
        1. w+ 可读可写 如果文件存在 则覆盖整个文件不存在则创建 
        2. 每次初始化Writer， 检查之前是否有中断后留下的记录
        3. 若count.txt不存在则自动创建
        '''

        if os.path.exists(self.save_path+"/count.txt"):

            with open(self.save_path + "/count.txt", "r") as f_count:

                result_list = f_count.readline().split(",")
                print("之前的记录"+ str(result_list))
                if result_list:
                    self.count_line = int(result_list[0])
                    self.count_file = int(result_list[1])


    def __write_record(self):

        with open(self.save_path+"/count.txt", "w+") as f_count:

            f_count.write(str(self.count_line))
            f_count.write(",")
            f_count.write(str(self.count_file))

        if self.mode == "hist":

            with open(self.save_path+"/latest_id.txt", "w+") as f_id:

                f_id.write(self.__latest_id)

        self.__check_exit()

    def __init__(self, nums_line, nums_file, mode="unspecified", save_path=os.getcwd()+"/data"):
        self.nums_line = nums_line
        self.nums_file = nums_file
        self.save_path = save_path
        self.mode = mode

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        self.__check_record()

    

    def write_data(self, text, text_id=0):

        if self.count_file < self.nums_file:

            #tweet_file_name = 'tweets_' + str(count_file) + '.txt'

            tweet_file_name = "tweets_{}_{}.txt".format(self.mode, self.count_file+1)

            with open(self.save_path+"/"+tweet_file_name, "a+") as f_tweet:

                #a+ 可读可写 从文件顶部读取内容 从文件底部添加内容 不存在则创建
                # 每次追加完内容后，指针会被自动定位到文件底部
                f_tweet.seek(0, 0)  #必须手动将指针调到文件头才能读出东西
                if not f_tweet.readline():  #如果文件中没有内容，就将count_line设置为0
                    self.count_line = 0

                if self.count_line < self.nums_line:

                    f_tweet.write(text + "\n")

                    self.count_line += 1

                    if self.count_line == self.nums_line:
                        self.count_file += 1
                        self.count_line = 0

                    if self.mode == "hist":
                        self.__latest_id = text_id
                    self.__write_record()


                #self.__write_record()

class MyStreamListener(tweepy.StreamListener):


    writer = None

    def __init__(self, nums_line, nums_file, save_path=os.getcwd()):

        super(MyStreamListener,self).__init__()

        self.writer = tw_class.MyWriter(nums_line, nums_file, "stream")


    def on_status(self, status):

        try:
            tweet_text = status.extended_tweet["full_text"]
        except AttributeError:
            tweet_text = status.text

        tweet_text = tw_util.process_tweet_text(tweet_text)
        #print(tweet_text)
        self.writer.write_data(tweet_text)


class MyHistGetter:

    __writer = None
    __api = None
    __max_id = None

    __save_path = os.getcwd()+"/data"

    __tweets_cursor = None


    def __get_max_id(self):

        if os.path.exists(self.__save_path+"/latest_id.txt"):
            with open(self.__save_path+"/latest_id.txt", "r") as f_id:
                self.__max_id = f_id.readline()
                print("最近一次插入的id: " + self.__max_id)


    def __init__(self, api, nums_line, nums_file, until):
        self.__api = api

        self.__get_max_id()

        if self.__max_id:
            self.__tweets_cursor = tweepy.Cursor(self.__api.search,
                                                 q="trump", count=100, lang="en",
                                                 tweet_mode='extended',
                                                 result_type="recent", include_entities="false",
                                                 until=until, max_id=self.__max_id)
        else:
            self.__tweets_cursor = tweepy.Cursor(self.__api.search,
                                                 q="trump", count=100, lang="en",
                                                 tweet_mode='extended',
                                                 result_type="recent", include_entities="false",
                                                 until=until)


        self.__writer = MyWriter(nums_line, nums_file, "hist")

    def get_hist_tweet(self):
        while True:
            try:
                for tweet_info in self.__tweets_cursor.items():

                    """
                    if a tweet object is a retweeted tweet, the text in 'full_text' attribute will be truncated, 
                    -- i.e. it is incomplete and end up with "..."
                    -- e.g. "It is a go..." 
                    -- in this case, the full_text of the original tweet can be found in the "full_text" attribute of "retweeted_status" object.
                    -- check https://twittercommunity.com/t/retrieve-full-tweet-when-truncated-non-retweet/75542
                    """

                    if 'retweeted_status' in dir(tweet_info):  # if it is a retweeted tweet
                        tweet_text = tweet_info.retweeted_status.full_text
                    else:
                        tweet_text = tweet_info.full_text

                    if not tweet_text:
                        continue

                    # if tweet_text.find("Looks") == 0:
                    #     pass

                    tweet_text = tw_util.process_tweet_text(tweet_text)
                    # print(tweet_info.created_at)
                    self.__writer.write_data(tweet_text, tweet_info.id_str)

            except tweepy.TweepError as te:
                print(te)
                tw_util.handle_TweepError(self.__api)
                continue



