import glob
import os
import subprocess

def run():
  here = os.getcwd()
  for fname in glob.glob("Submissions/*"):
    os.chdir(fname)
    results = (x for x in subprocess.check_output("find . -name '.zip'", shell=True).split("\n") if x)
    if results:
        for zipfile in results:
          print("unzipping %s" % zipfile)
          path, name = zipfile.rsplit("/", 1)
          os.chdir(path)
          os.system("unzip %s" % name)
    else:
      print("Nothing for %s" % fname)
    os.chdir(here)

if __name__ == "__main__":
  run()
