import psutil
import os
import time
import sys


class PsMonitor:

    __pid = 0
    __cmd = ""
    __time_internal = 60

    def __init__(self, pid, cmd, time_internal=60):
        self.__pid = int(pid)
        self.__cmd = cmd
        self.__time_internal = int(time_internal)


    def __get_pid(self):
        with open("run.pid", "r") as f_pid:
            self.__pid = int(f_pid.readline())

    def monitor_ps(self):

        while True:

            try:
                print("monitoring pid at: " + str(self.__pid))
                p = psutil.Process(self.__pid)

            except psutil.NoSuchProcess as nsp:
                print("pid {} got killed. Trying to restart it...".format(self.__pid))
                self.__restart_ps()

            time.sleep(self.__time_internal)


    def __restart_ps(self):

        os.system(self.__cmd)

        print(self.__cmd)

        sys.stdout.flush()
        sys.stderr.flush()

        time.sleep(5)

        old_pid = self.__pid

        self.__get_pid()  # extract new pid from file

        if self.__pid and (old_pid != self.__pid):
            self.monitor_ps()
        else:
            print("Cannot find pid")
            exit()




if __name__ == "__main__":

    # pid = "5810"
    # cmd = "python3 -u get_tweets.py pengyuxia hist 1250000 3 >out.log 2>&1 &"
    # time_interval = ""

    # pid = sys.argv[1]
    # cmd = sys.argv[2]
    # time_interval = ""

    cmd = sys.argv[1]

    with open("run.pid", "r") as f_pid:
        pid = f_pid.readline()

    # if len(sys.argv) > 3:
    #     time_interval = sys.argv[3]
    #
    #
    #
    # if time_interval:
    #     psMonitor = PsMonitor(pid, cmd, time_interval)
    # else:
    #     psMonitor = PsMonitor(pid, cmd)

    psMonitor = PsMonitor(pid, cmd)
    psMonitor.monitor_ps()

