import time

from termcolor import colored

class Log:
    """
        2013-07-27:
            Wrapper for printing color coded messages to the console

            TODO add backgrounds
    """

    def error(self, msg):
        print(colored("Error: %s" % msg, "red"))

    def failure(self, msg):
        print(colored(msg, "red"))

    def header(self, msg):
        print(colored("--- %s ---" % msg, attrs=["bold","reverse"]))

    def info(self, msg):
        print(colored(msg, "blue"))

    def nocompile(self, msg):
        print(colored("Compilation Failed:\n  %s" % msg.strip().replace("\n", "\n  "), color="red"))
        print("**********************************************************************")
        print("* IF YOU WANT TO SUCCEED IN THIS CLASS YOUR CODE MUST COMPILE -mgn29 *")
        print("**********************************************************************")
        time.sleep(0.7)

    def pprint_failures(self, error_messages, duration):
        self.failure("FAILURE in %0.3f seconds" % duration)
        for (module_name, errors) in error_messages.iteritems():
            print(colored("%s_test.ml" % module_name, color="red", attrs=["bold"]))
            for (fn_name, err_msg) in errors:
                self.failure("> %s - %s" % (fn_name, err_msg))
        self.failure("\nBETTER LUCK NEXT TIME")

    def run(self, msg):
        print(colored(msg, "yellow"))

    def success(self, msg):
        print(colored(msg, "green"))

    def warn(self, msg):
        print(colored("Warning: %s" % msg, "magenta"))
