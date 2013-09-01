import os, re, subprocess

from util.invalidTestException import InvalidTestException
from util.log import Log
from util.timer import Timer
from util.timedProcess import TimedProcess
from util.timeoutException import TimeoutException

class Harness:
    """
        2013-08-23:
            Execute all tests cases found inside a module. Specifically:
            - Accept the path to a test file as input (like "my_test.ml" or "worker_test.ml")
            - Compile the test case and the corresponding .ml file ("file.ml" + "file_test.ml")
            - Extract the inferred interface from the test file
            - Extract all test cases from the interface ("unit -> unit" functions beginning with "test_")
            - Execute each test case in a separate ocaml toplevel, record output
    """

    # In order of dependence
    LIBS = [
        "dump.cma",
        "ocamltest.cma",
    ]

    def __init__(self, test_file, timeout):
        self.log = Log()
        self.timeout = timeout
        
        self.test_file = test_file
        self.src_file = "%s.ml" % test_file[:-(len("_test.ml"))]
        self.test_name = self.test_file.split("/")[-1]
        self.src_name = self.src_file.split("/")[-1]

        self.failures = self.run()
        print("") # Separator

    def compile(self):
        """
            2013-08-23:
                Compile the source file + test file, generate the interface for 
                the test file. In detail:
                - Generate the ocamlc command to compile source + test in unison,
                  pulling in all necessary external libraries
                - Generate the ocamlc command to get the interface for the test,
                  using the .cmo file generated by compiling the source as a library
        """
        self.log.info("Compiling %s and %s" % (self.src_name, self.test_name))
        # Prepare compilation commands. 
        # 2013-08-23: Base command includes standard testing library
        base_command = " ".join(["ocamlc -c"] + self.LIBS)
        # 2013-08-23: Full compilations uses '-g' option to generate debug information
        compile_all = "%s -g %s %s" % (base_command, self.src_file, self.test_file)
        # Name of the .cmo file generated after compiling the source
        src_cmo = "%s.cmo" % self.src_file[:-(len(".ml"))]
        # 2013-08-23: Use '-i' option to just generate the interface for the function
        infer_interface = "%s -i %s %s" % (base_command, src_cmo, self.test_file)
        try:
            # Compile both files, then infer and return the interface
            subprocess.check_output(compile_all, shell=True, stderr=subprocess.STDOUT)
            # 2013-08-23: Reached this line without making a .cmo Dear diary, this was bad
            interface = subprocess.check_output(infer_interface, shell=True)
            return str(interface, encoding='utf-8').split("\n")
        except subprocess.CalledProcessError as cpe:
            # NO COMPILEEEEEEEE
            err_msg = cpe.output.strip()
            # 2013-08-23: Retrieve failing line from the file
            sourceError = self._source_of_exception(err_msg)
            # Put the OCaml exception + line from source into one string. 
            # Replace vanilla newlines with indented newlines.
            nocompile_msg = ("%s\n%s" % (err_msg, sourceError)).replace("\n", "\n  ")
            self.log.nocompile(nocompile_msg)
            raise InvalidTestException(1)

    def generate_scripts(self, test_interface):
        """
            2013-08-23:
                Given the interface of a test file, generate a toplevel script
                for each test case. For instance, if the test file had an interface
                like:
                    val test_one : unit -> unit
                    val helper : int -> string
                    val test_two : unit -> unit
                    val test_three : int -> unit
                Then this function would generate scripts for `test_one` and
                `test_two`, because they are `unit -> unit` functions that
                start with the magic prefix "test_"
        """
        test_cases = []
        for defined_name in ( x for x in test_interface if x.startswith("val test_") ):
            val_name, val_type = defined_name[4:].split(" : ", 1)
            if val_type != "unit -> unit":
                self.log.warn("skipping test case %s with type %s" % (val_name, val_type))
            else:
                test_cases.append(val_name)
        if test_cases == []:
            return None
        else:
            # Change "my_test.ml" to the module "My_test"
            test_name = self.test_name[:-(len(".ml"))].capitalize()
            return ( (case, self._toplevel_input(test_name, case))
                for case in test_cases )
        
    def run(self):
        """
            2013-08-23:
        """
        self._check_paths()
        # Get the directory containing the test file, move to it
        if "/" in self.test_file:
            testcase_dir = self.test_file[::-1].split("/", 1)[1][::-1]
            os.chdir(testcase_dir)
        # Compile the test + source files
        self.log.header("Testing %s" % self.src_name)
        test_interface = self.compile()
        # Generate the test scripts
        self.log.info("Compilation succeeded! Generating test scripts...")
        test_scripts = self.generate_scripts(test_interface)
        if test_scripts is None:
            self.log.warn("No test cases in %s" % self.test_name)
        else:
            # Execute tests
            return self.run_tests(test_scripts)

    def run_test(self, script):
        """
            2013-08-23:
                Execute a single test script in a toplevel environment.
                Start a toplevel with the module and test case object files loaded, 
                pipe in the test script as an argument.

                I'm not entirely happy with the piping because it means that subprocess
                fails to throw an error when the test fails. Maybe fix that later.
        """
        run_test = " ".join([
            "echo \"%s\" |" % script,
            "ocaml",
            ] + self.LIBS + [
            "%s.cmo" % self.src_file[:-(len(".ml"))],
            "%s.cmo" % self.test_file[:-(len(".ml"))]
        ])
        with Timer() as t:
            try:
                output, err = TimedProcess(run_test).run(self.timeout)
                err_msg = self._error_of_output(output) # Maybe None
            except TimeoutException:
                err_msg = "TIMEOUT"
        if not err_msg:
            self.log.success("PASS in %0.3f seconds" % t.duration)
        else:
            self.log.failure("FAIL with '%s' in %0.3f seconds" % (err_msg, t.duration))
        return err_msg

    def run_tests(self, test_scripts):
        """
            2013-08-23:
                Given an association list of ("test_case_name", "toplevel script"),
                execute each test in an ocaml toplevel and record the output.
        """
        errors = []
        for (fn_name, script) in test_scripts:
            self.log.run("Running %s..." % fn_name)
            err_msg = self.run_test(script)
            if err_msg:
                errors.append((fn_name, err_msg))
        return errors

    def _check_paths(self):
        """
            2013-08-23:
                Make sure the source and test files (still) exist.
        """
        if not os.path.exists(self.src_file):
            self.log.warn("Source file '%s' not found. Skipping %s..." % (self.src_name, self.test_name))
            raise InvalidTestException(0)
        if not os.path.exists(self.test_file):
            self.log.warn("Test file '%s' not found. Exiting..." % self.test_name)
            raise InvalidTestException(0)

    def _error_of_output(self, toplevel_output):
        """
            2013-08-04:
                Toplevel output is always echoed to subprocess, regardless of
                whether the tests passed. Manually check if the code raised an
                assertion error. 
                
                TODO this is not very rigorous! It assumes there will be an octothorp
                at the end of the output!
                This is a reasonable assumption but still it makes me nervous

            2013-08-23:
                Ignores input errors. If the code this file sends to the toplevel
                has a syntax error or whatever, things will break down seriously. 
                I think its safe to assume that'll never happen in a release.

            2013-08-24:
                Added logic to print the non-exception printouts
                You know, we could probably just check that the output's "- : unit"
        """
        toplevel_output = str(toplevel_output, encoding='utf-8')
        match = re.search(r"#.*?(Exception:[\s].*)\n#", toplevel_output, re.DOTALL)
        if match is not None:
            # Debug output will be octothorp to exception.
            debug_match = re.search(r"# (.*?)Exception:", toplevel_output, re.DOTALL)
            message = match.group(1).strip()
        else:
            # Debug output will be octothorp to return value
            debug_match = re.search(r"# (.*?)\n- :", toplevel_output, re.DOTALL)
            message = None
        # Print the debug output, if any
        if debug_match is not None and debug_match.group(1):
            print(debug_match.group(1).rstrip())
        return message

    def _source_of_exception(self, errorMessage):
        """
            2013-08-23:
                Get the line number and source file that spawned `errorMessage`,
                extract that line of code from that source file.
        """
        errorMessage = str(errorMessage, encoding='utf-8')
        match = re.search(r"File \"(.*?)\", line ([0-9]+),", errorMessage)
        if match is None:
            return ""
        else:
            fname = match.group(1)
            line_num = int(match.group(2))
            with open(fname, "r") as f:
                currentLine = 1
                message = ""
                while currentLine < line_num:
                    currentLine += 1
                    message = next(f)
                try:
                    if message:
                        return("     %s %s---> %s %s" % \
                            (line_num-1, message, line_num, next(f).rstrip()))
                    else:
                        return("---> %s %s" % (line_num, next(f).rstrip()))
                except StopIteration:
                    # File ended unexpectedly. Add an empty line and point to it
                    return("     %s %s---> %s <unexpected end of file>" \
                        % (line_num-1, message, line_num))

    def _toplevel_input(self, module_name, test_case):
        """
            2013-07-28:
                 Write a script for the toplevel. Call the right function
                 from the right module
        """
        return "%s.%s ();;" % (module_name.capitalize(), test_case)

