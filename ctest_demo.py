# coding: utf-8
# author: 88IO

import getopt
import os
import pandas as pd
import subprocess
import sys
import time


class CTest:
    def __init__(self):
        self.ex_files = [None]
        self.ex_data = []
        self.outputs = []
        self.test_app, self.trials, self.ex_files[0], ex_dir = self.get_option(sys.argv[1:])
        if self.test_app:
            if self.ex_files:
                with open(self.ex_files[0], "r") as f:
                    self.ex_data.append(f.read())
            if ex_dir:
                for dat_file in filter(self.pick_dat_file, os.listdir(ex_dir)):
                    with open(dat_file, "r") as f:
                        self.ex_file.append(dat_file)
                        self.ex_data.append(f.read())
            if not self.ex_data:
                sys.exit()
        else:
            sys.exit()

    def get_option(self, argv):
        test_app = None
        ex_file = None
        ex_dir = None
        num_trials = 5
        try:
            opts, args = getopt.getopt(argv, "i:t:f:d:hv", ["input=", "trials=", "--file", "--dir", "help", "version"])
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
                test_app = a if os.path.isfile(a) else None
            if o in ("-t", "--trials"):
                num_trials = int(a)
            if o in ("-f", "--file"):
                ex_file = a if os.path.isfile(a) else None
            if o in ("-d", "--dir"):
                ex_dir = a if os.path.isdir(a) else None

        if not test_app and not (ex_file or ex_dir):
            print(test_app, ex_dir, ex_file)
            print("Please set test_app or example_file.\n")
            usage()
            sys.exit()

        print(test_app, num_trials, ex_file, ex_dir)
        return test_app, num_trials, ex_file, ex_dir

    def pick_dat_file(self, f: str) -> bool:
        return os.path.splitext(f)[1] == ".dat"

    def run_app(self):
        for data in self.ex_data:
            self.outputs.append([self.get_output(data) for _ in range(self.trials)])

    def get_output(self, data):
        app_p = subprocess.Popen([self.test_app], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stime = time.time()
        output = app_p.communicate(data.encode())[0].decode()
        ftime = time.time()
        return output, ftime-stime

    def print_result(self):
        print("「アプリ」 -> {}".format(self.test_app))
        for ex_file, input, outputs in zip(self.ex_files, self.ex_data, self.outputs):
            print("  [テストファイル] -> {}".format(ex_file))
            print("    (入力) ↴\n{}".format(input))
            for t, output in enumerate(outputs):
                print(t)
                print("    (出力) ↴\n{}".format(output[0]))
                print("    (時間) -> {}s".format(output[1]))

    def make_data_frame(self):
        dict_data = {}
        for ex_file, ex_data, output in zip(self.ex_files, self.ex_data, self.outputs):
            dict_data[ex_file] = {"data": ex_data, "output": output[0][0], "time": output[0][1]}
        df = pd.DataFrame.from_dict(dict_data)
        df.to_html("test.html")
        df.to_clipboard()


def usage():
    pass


def version():
    pass


def main():
    tframe = CTest()
    tframe.run_app()
    tframe.print_result()
    tframe.make_data_frame()


if __name__ == "__main__":
    main()
