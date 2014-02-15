from __future__ import print_function

import re, subprocess, sys, time, os

from util.termcolor import colored

class Log:
    """
        2013-07-27:
            Wrapper for printing color coded messages to the console
    """

    def debug(self, msg):
        print(msg)

    def header(self, msg):
        print(colored("--- %s ---" % msg, attrs=["bold","reverse"]))

    def error(self, msg):
        print(colored("Error: %s" % msg, "red"))
        exit(1)

    def failure(self, msg):
        print(colored(msg, "red"))

    def info(self, msg):
        print(colored(msg, "blue"))

    def nocompile(self, msg):
        print(colored("Compilation Failed:\n  %s" % msg, color="red"))
        print("**********************************************************************")
        print("* IF YOU WANT TO SUCCEED IN THIS CLASS YOUR CODE MUST COMPILE -mgn29 *")
        print("**********************************************************************")
        time.sleep(0.7)
    
    def pprint_failures(self, error_messages, duration):
        self.failure("FAILURE in %0.3f seconds" % duration)
        for (module_name, errors) in error_messages.iteritems():
            print(colored("%s.ml" % module_name, color="red", attrs=["bold"]))
            for fail_tuple in errors:
                self.failure("> %s - %s" % fail_tuple)
        self.failure("\n\"START TRAINING\nMAKE A COMEBACK!\"")

    def run(self, msg):
        print(colored(msg, "yellow"))

    def success(self, msg):
        print(colored(msg, "green"))

    def warn(self, msg):
        print(colored("Warning: %s" % msg, "magenta"))
        
    class Student:
        
        def __init__(self, filename, strip=True):
            # 2013-08-30: Initialize a postscript stream, track every printout the test generates
            if strip:
                self.student_name = filename.split("/")[-1]
            else:
                self.student_name = filepath

        def __enter__(self):
            print(colored("Testing student '%s'" % self.student_name, attrs=['bold']))

        def __exit__(self, *args):
            print("")

    class TestFile:
        """
            2013-08-28:
                Handle pretty-printing upon entering / exiting a test case
        """
        
        def __init__(self, filename):
            self.filename = filename
        
        def __enter__(self):
            print(colored("--- %s ---" % self.filename, attrs=["bold","reverse"]))

        def __exit__(self, *args):
            print("")

