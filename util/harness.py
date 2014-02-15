import os, re

from util.invalidTestException import InvalidTestException
from util.log import Log
from util.noCompileException import NoCompileException
from util.stackOverflowException import StackOverflowException
from util.subprocessWrapper import SubprocessWrapper
from util.testCaseOutput import TestCaseOutput
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
    STD_LIBS = [
        "dump.cma",
        "ocamltest.cma",
    ]

    def __init__(self, module_name, sol_dir, stu_dir, include=[], timeout=5, debug=False, no_solution=False, compile_script=None):
        """
            2013-08-28:
                `module_name` should not have any suffix. 
                Send 'fun' instead of 'fun.ml'.

                Too many keywords? Fear not, you can always just work with the 
                corresponding setter methods.
        """
        self.compile_script = compile_script
        self.debug=debug
        self.log = Log()
        self.no_solution = no_solution
        # this is a pretty important string. It's passed directly to the compiler + runner.
        self.include = include
        self.subprocess = SubprocessWrapper()
        self.timeout = timeout

        self.module_name = module_name
        self.sol_dir = sol_dir
        self.stu_dir = stu_dir

        # Absolute paths to library files
        self.sol_ml = "%s/%s_sol.ml" % (sol_dir, self.module_name)
        self.test_ml = "%s/%s_test.ml" % (sol_dir, self.module_name)
        self.stu_ml = "%s/%s.ml" % (stu_dir, self.module_name)
        # Absolute path to modules
        self.sol_cma = "%s/%s_sol.cma" % (sol_dir, self.module_name)
        self.test_cma = "%s/%s_test.cma" % (sol_dir, self.module_name)
        self.stu_cma = "%s/%s.cma" % (stu_dir, self.module_name)

        self.failures = []
        self.successes = []
        self.all_output = []
        self.warnings = []

    def clean_all(self, directory):
        try :
            self.subprocess.execute("find %s -name '*.cm*' | xargs rm" % directory)
        except:
            pass

    def compile(self):
        """
            2013-08-23:
                Compile solution file to 'solution.cma'
                Compile student file to 'student.cma'
                (Failing that, 
                 try renaming the files into /tmp/harness311/src_name/student.ml
                 and compiling)
                Compile test file, generate interface
                
                Return directory to solution + student .cma and test.ml

                TODO support compilation via makefile
        """
        self.include.append("-I %s" % self.stu_dir)
        base_command = " ".join(["ocamlc"] + self.STD_LIBS + self.include + ["-a", "-o"])
        # Someday, simplify this. Don't compile so often. WAIT maybe ocaml already
        # skips compiling if there are no changes.
        self.log.info("Compiling solution files...")
        # compile_sol = "%s %s -g %s" % \
        #     (base_command, self.sol_cma, self.sol_ml)
        compile_stu_mli = "%s -g %si" % \
            (base_command, self.stu_ml)
        compile_stu = "%s %s -g %s" % \
            (base_command, self.stu_cma, self.stu_ml)
        compile_test = "%s %s -g -I %s -I %s %s" % \
        if self.compile_script is not None:
            # Break early! We have a quick script to run
            # Change into student's directory
            # read the script as a string, execute
            with open(self.compile_script, "r") as script_stream:
                script = script_stream.read()
                self.log.info("Running compile script:\n %s" % script) 
            script = "cd %s; %s" % (self.stu_dir, script)
            self.subprocess.execute(script, on_failure=self.compile_error)
            return []

        self.clean_all(self.stu_dir)
        base_command = " ".join(["ocamlc"] + self.STD_LIBS + self.include + ["-a", "-o"])
        # Someday, simplify this. Don't compile so often. WAIT maybe ocaml already
        # skips compiling if there are no changes.
        self.log.info("Compiling files...")
        commands = []
        # TODO
        if not self.no_solution:
            commands += self.compile_command(base_command, self.sol_cma, self.sol_ml)
        compile_stu = self.compile_command(base_command, self.stu_cma, self.stu_ml)
        # base_command = " ".join(["ocamlc"] + self.STD_LIBS + self.include + \
        #                             ["%s/eval.cma" % (), "-a", "-o"])
        compile_test = "%s %s -g -I %s -I '%s' '%s'" % \
            (base_command, self.test_cma, self.sol_dir, self.stu_dir, self.test_ml)
        # Extract the interface. This command does not produce library output
        gen_interface = "ocamlc -i %s -I %s -I '%s' '%s'" % \
            (" ".join(self.STD_LIBS + self.include), self.sol_dir, self.stu_dir, self.test_ml)
        commands += compile_stu
        commands.append(compile_test)
        commands.append(gen_interface)
        # Run all three compilation commands
        for command in [compile_stu_mli, compile_stu, compile_test]:
            print("COMMAND = %s" % command)
            # TODO catch compiler warnings
        for command in commands:
            # print("COMPILECOMMAND = %s" % command)
            output = self.subprocess.execute(command, on_failure=self.compile_error)
            # 2013-10-06: Ignore compiler output. 
            # if output:
            #     warn_msg = ("WARNING", output)
            #     self.all_output.append(warn_msg)
            #     self.warnings.append(warn_msg)
        # Generate the interface
        return self.subprocess.execute(gen_interface).split("\n")

    def compile_command(self, base_command, output_file, input_module):
        """
            2013-09-28:
                Generate a command (or series of commands) which will compile the named test.
                Searches for .mli files
        """
        command = []
        path = input_module.rsplit("/", 1)[0]
        fullname = input_module.rsplit(".",1)[0]
        # name = "%s/%s" % (path, name)
        # if os.path.exists("%s/build.sh" % path):
        #     command.append("cd %s; sh build.sh; cd -;" % path)
        # elif sol and os.path.exists("%s/Makefile" % path):
        #     command.append("cd %s; make; cd -;" % path)
        # # elif sol and os.path.exists("%s.mli" % fullname):
        # #     # First compile the mli, then compile the .ml using the .mli as reference
        # #     # Don't care where this outputs
        # #     command.append("%s a.out %s.mli" % \
        # #         (base_command, fullname))
        # #     command.append("%s %s %s.cmi %s" % \
        # #         (base_command, output_file, fullname, input_module))
        # else:
        #     # Compile the file without .mli
        #     command.append("%s %s -g %s.mli %s" % \
        #         (base_command, output_file, fullname, input_module))
        mli_file = "%si" % input_module
        if os.path.exists(mli_file):
            command.append("%s a.out '%s'" % \
                (base_command, mli_file))
            command.append("%s %s -I '%s' '%s'" % \
                (base_command, output_file, path, input_module))
        else:
            command.append("%s '%s' '%s'" % \
                (base_command, output_file, input_module))
        return command

    def compile_error(self, cpe):
        """
            2013-09-07:
                Behaviour on compile error. Exception is guaranteed to be
                an instance of `subprocess.CalledProcessError`
        """
        err_msg = cpe.output.strip()
        # 2013-08-23: Retrieve failing line from the file
        sourceError = self._regenerate_source(err_msg)
        # Put the OCaml exception + line from source into one string. 
        nocompile_msg = ("%s\n%s" % (err_msg, sourceError))
        # Replace vanilla newlines with indented newlines.
        nocompile_msg = nocompile_msg.replace("\n", "\n  ")
        self.log.nocompile(nocompile_msg)
        raise NoCompileException(nocompile_msg)
            
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
            # Change "my_test.ml" to the module "My"
            test_name = "%s_test" % (self.module_name.capitalize())
            return ( (case, self._toplevel_input(test_name, case))
                for case in test_cases )

    def run(self):
        """
            2013-08-23:
                Compile a test file, find the tests inside it, run each, record output
        """
        self._check_paths()
        with self.log.TestFile(self.module_name):
            # Compile the test + source files
            test_interface = self.compile()
            # Generate the test scripts
            self.log.info("Compilation succeeded! Generating test scripts...")
            test_scripts = self.generate_scripts(test_interface)
            if test_scripts is None:
                self.log.warn("No test cases in %s" % self.test_ml)
                return
            else:
                # Execute tests
                self.run_tests(test_scripts)

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
            "-I %s" % self.sol_dir,
            "-I %s" % self.stu_dir,
            ] + self.include 
            + self.STD_LIBS + [
            self.sol_cma,
            self.stu_cma, 
            self.test_cma,
        ])
        # print("TESTCOMMAND = %s" % run_test)
        with Timer() as t:
            try:
                output, err = TimedProcess(run_test).run(self.timeout)
                parsed = TestCaseOutput(output, err, self.debug)
                err_msg = parsed.serialize()
            except TimeoutException:
                err_msg = "TIMEOUT"
            except StackOverflowException:
                err_msg = "STACK OVERFLOW"
        if not err_msg:
            msg = "PASS in %0.3f seconds" % t.duration
            self.log.success(msg)
            return (msg, 0)
        else:
            msg = "FAIL with '%s' in %0.3f seconds" % (err_msg, t.duration)
            self.log.failure(msg)
            return (msg, 1)

    def run_tests(self, test_scripts):
        """
            2013-08-23:
                Given an association list of ("test_case_name", "toplevel script"),
                execute each test in an ocaml toplevel and record the output.
        """
        for (fn_name, script) in test_scripts:
            self.log.run("Running %s..." % fn_name)
            msg, err_status = self.run_test(script)
            output = (fn_name, msg)
            self.all_output.append(output)
            if err_status:
                self.failures.append(output)
            else:
                self.successes.append(output)

    def set_include(self, include):
        """
            2013-09-17:
                Accept a list (later passed to `ocaml`, on command line)
                specifying a few directory and library files to include. 
                
                This could be used to pass any compiler directive to the toplevel.
                Even --explode
        """
        self.include = include or []
        return True

    def set_timeout(self, timeout):
        self.timeout = timeout
        return True

    def _check_paths(self):
        """
            2013-08-23:
                Make sure the source and test files (still) exist.
        """
        raise NotImplementedError
        ### master vs. ps4. This is master
        # if not os.path.exists(self.stu_ml):
        #     self.log.warn("Source file '%s' not found. Skipping %s..." % (self.src_name, self.test_name))
        #     raise InvalidTestException(0)
        # if not os.path.exists(self.sol_ml):
        #     self.log.warn("Solution file '%s' not found. Skipping %s..." % (self.sol_name, self.test_name))
        #     raise InvalidTestException(0)
        # if not os.path.exists(self.test_ml):
        #     self.log.warn("Test file '%s' not found. Skipping it." % self.test_name)
        #     raise InvalidTestException(0)
        ### master vs. ps4. This is ps4
        # if (self.compile_script is None):
        #     if not os.path.exists(self.stu_ml):
        #         self.log.warn("Source file '%s' not found. Skipping %s..." % (self.src_name, self.test_name))
        #         raise InvalidTestException(0)
        #     if not os.path.exists(self.sol_ml):
        #         self.log.warn("Solution file '%s' not found. Skipping %s..." % (self.sol_ml, self.test_ml))
        #         raise InvalidTestException(0)
        #     if not os.path.exists(self.test_ml):
        #         self.log.warn("Test file '%s' not found. Skipping it." % self.test_ml)
        #         raise InvalidTestException(0)
        ### a new addition, according to git 
        # if not os.path.exists(self.stu_ml):
        #     self.log.warn("Source file '%s' not found. Skipping %s..." % (self.src_name, self.test_name))
        #     raise InvalidTestException(0)
        # if not os.path.exists(self.sol_ml):
        #     self.log.warn("Solution file '%s' not found. Skipping %s..." % (self.sol_name, self.test_name))
        #     raise InvalidTestException(0)
        # if not os.path.exists(self.test_ml):
        #     self.log.warn("Test file '%s' not found. Skipping it." % self.test_name)
        #     raise InvalidTestException(0)

    def _regenerate_source(self, errorMessage):
        """
            2013-08-23:
                Get the line number and source file that spawned `errorMessage`,
                extract that line of code from that source file.

                TODO try using ack to rebuild
        """
        match = re.search(r"File \"(.*?)\", line ([0-9]+),", errorMessage)
        if match is None:
            return ""
        else:
            fname = match.group(1)
            if self.compile_script is not None:
                #TODO make this less hacks
                fname = "%s/%s" % (self.stu_dir, fname)
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
