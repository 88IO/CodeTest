# coding: utf-8
# author: 88IO

import getopt
import json
import os
import subprocess
import sys
import time


class TaskMgr:
    trials = 5

    def __init__(self):
        self.ex_file = None
        self.ex_data = None
        self.data_frame = {}

    def get_option(self, argv=sys.argv[1:]):
        try:
            opts, args = getopt.getopt(argv, "i:t:f:hv",
                                       ["input=", "trials=", "--file", "help", "version"])
        except getopt.GetoptError:
            usage()
            sys.exit()

        for o, a in opts:
            if o in ("-v", "--version"):
                version()
                sys.exit()
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-i", "--input"):
                CodeTester.app_name = a if os.path.isfile(a) else None
            if o in ("-t", "--trials"):
                self.trials = int(a)
            if o in ("-f", "--file"):
                self.ex_file = a if (os.path.isfile(a) and a[-4:] == "json") else None

    def analyze_json(self):
        with open(self.ex_file, "r") as f:
            self.ex_data = json.load(f)

    def test_code(self):
        for ex_name in self.ex_data:
            ct = CodeTester(input_source=self.ex_data[ex_name]["input"],
                            answer=self.ex_data[ex_name]["answer"])
            self.data_frame[ex_name] = {n: ct.run_app() for n in range(self.trials)}


class CodeTester:
    app_name = None

    def __init__(self, input_source, answer):
        self.data = {"input": None,
                     "output": None,
                     "time": 0,
                     "correct": False}
        self.data["input"] = input_source
        self.answer = answer

    def run_app(self) -> dict:
        stime = time.time()
        app_pipe = subprocess.Popen([self.app_name],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.data["output"] = app_pipe.communicate(self.data["input"].encode())[0].decode()
        self.data["time"] = time.time() - stime
        self.data["correct"] = (self.answer == self.data["output"].replace("\r\n", ""))

        return self.data


def usage():
    pass


def version():
    pass


def main():
    tm = TaskMgr()
    tm.get_option()
    tm.analyze_json()
    tm.test_code()
    print(tm.data_frame)


if __name__ == "__main__":
    main()
