import os
import sys
import subprocess

def run():
    for fname in subprocess.check_output("find . -name '* *'", shell=True).split("\n"):
        if fname:
            # print("SERVING %s" % fname)
            # print("mv '%s' %s" % (fname, fname.replace(" ", "")))
            os.system("mv '%s' %s" % (fname, fname.replace(" ", "")))


if __name__ == "__main__":
    run()#sys.argv[1])
