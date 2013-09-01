Test Harness
===========

Install
-------
Run `make install` with root permissions.

Uninstall
---------
Run `make uninstall` with root permissions.

How to write a test harness
---------------------------
* Create solution files
  - Make a directory to hold the solutions. Call it whatever you like, but `solution` is a good name
  - Name all solutions with the `_test` suffix. For instance if you want to test the module `part1.ml`, the solution file should be named `part1_sol.ml`. This is pretty important
  - Write test cases. Make sure to name them with the `_sol` suffix. For instance `part1_test.ml` is the right name to test `part1.ml`.
    + See the section below on writing good test cases
* Make a directory to hold the students' submissions. `Submissions` is preferred because that's what CMS will give you automatically if you navigate to the 'groups' page for the assignment, select all students (use the 'All' button on top), and click the 'Files' button.
  - Make sure every student's files are in a new folder. The folder really really really should be named with the student's netid. Really.
  - Student files don't need a particular suffix, or even need to be located in a particular place. You can put `part1.ml` directly under the student's netid directory or 10 folders deep it doesn't matter.
* Run the harness with the `harness311` command. 
  - Assume we have folders `solution` and `Submissions`. Then you can run the harness via `harness311 solution Submissions/*`
    + The first argument to `harness311` must be the solutions directory. This directory should have the `_sol.ml` and `_test.ml` files.
    + The following arguments to `harness311` should be student directories to run the tests on. You can give as many arguments as you like. 
  - ALTERNATIVELY, run the command `harness311 solution @Submissions/netids`
    + The `@` character at the start of a student folder indicates that the argument is not a folder but rather a list of folders that should be run. Ideally, a list of netids. You can generate such a file real easy by:
      - Download the `Submissions` folder
      - `cd Submissions`
      - `ls -1 * > netids`
    + BOOM! Now you can `cd ..; harness311 solution @Submissions/netids`
* Set a timeout with the `-t` or `--timeout` options. Example: `harness311 -t 1 solution @Submissions/netids` runs the harness with a one-second timeout. The default timeout is 20 seconds.
* By default, `harness311` runs all the tests in the solutions directory. Instead, you can specify which tests to run by giving a pattern with the `-p` or `--pattern` options. Example: if there exist tests `solution/part1_test.ml`, `solution/part2_test.ml` and `solution/part3_test.ml`, running `harness311 -p part3 solution @Submissions/netids` will execute the test harness for `part3.ml` and NOT for `part1` or `part2`.

How to write a test case
------------------------
Here's an example simple test case `module_test.ml`:
```
open Ocamltest

let test_fun1 () =
  assert_equal (Module.fun1 ()) (Module_sol.fun1 ())
```
Notes:
* Opening `Ocamltest` is important. That gives you access to the assertions library `ocamltest.ml`. 
* Since the test is named `module_test.ml`, the solution file `module_sol.ml` and student file `module.ml` are linked during compilation. So you can call the solution and student modules no problem.

- - -

_Author_: Ben Greenman

_Last Updated_: 2013-09-01
