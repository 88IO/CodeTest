# coding: utf-8
# author: 88IO

import getopt
import json
import os
import subprocess
import sys
import time
import toml


class DataBase:
    def __init__(self):
        self._ex_file = None
        self.ex_data = None
        self.trials = 0
        self.data_frame = {}

    '''
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
                self.ex_file = a if os.path.isfile(a) else None
    '''

    @property
    def ex_file(self):
        return self._ex_file

    @ex_file.setter
    def ex_file(self, value):
        self._ex_file = value

        with open(self._ex_file, "r") as f:
            _, ext = os.path.splitext(self.ex_file)
            if ext == ".json":
                self.ex_data = json.load(f)
            elif ext == ".toml":
                self.ex_data = toml.load(f)
            elif ext == ".yml":
                pass
            else:
                pass


class CodeTester:
    app_name = None

    def __init__(self, input_source, answer):
        self._data = {"input": None,
                      "output": None,
                      "time": 0,
                      "correct": False}
        self._data["input"] = input_source
        self._answer = answer

    def run_app(self) -> dict:
        stime = time.time()
        app_pipe = subprocess.Popen([self.app_name],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._data["output"] = app_pipe.communicate(self._data["input"].encode())[0].decode()
        self._data["time"] = time.time() - stime
        self._data["correct"] = (str(self._answer) == self._data["output"].replace("\r\n", ""))

        return self._data


def usage():
    pass


def version():
    pass


def get_option(argv=sys.argv[1:]):
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
            app_name = a if os.path.isfile(a) else None
        if o in ("-f", "--file"):
            ex_file = a if os.path.isfile(a) else None

        trials = int(a) if o in ("-t", "--trials") else 5

    return app_name, ex_file, trials


def main():
    db = DataBase()
    CodeTester.app_name, db.ex_file, db.trials = get_option()

    for ex_name, ex_prop in zip(db.ex_data.keys(), db.ex_data.values()):
        ct = CodeTester(input_source=ex_prop["input"],
                        answer=ex_prop["answer"])
        db.data_frame[ex_name] = {n: ct.run_app() for n in range(db.trials)}

    print(db.data_frame)


if __name__ == "__main__":
    main()
