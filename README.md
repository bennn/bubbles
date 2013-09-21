bubbles
=======
A simple unit testing framework for OCaml.
It's slowly coming into its own.

Very slowly, unfortunately. 
Development is at a virtual standstill.
Sort of.
I am not maintaining _this_ project, but am working on a testing framework for <a href="https://github.com/organizations/cs3110">CS3110</a> at Cornell. 
That's a framework for testing student code against a master set of solutions.
I've been extending this framework and revising it in that context, and I plan to some day do a big update drawing in all the changes from there over here.
What stopped me so far is that I haven't thought of a nice way of integrating the two usages: master vs. dev and unit testing. 

Disclaimer
----------
* This project requires <a href="http://www.gnu.org/software/make/">gnumake</a>
* This project requires Python 2.7
* This project requires OCaml. It has been developed with 4.00 but probably works with 3.12.
* This project does not currently support the testing of files with dependancies. That's coming soon, I promise you, but it's not here today.
* This project does not work on Windows. Sorry.
* This project is not currently maintained. 

Core Philosophy
---------------
Writing unit tests should be easy.
Extremely easy.
A simple test script should be as easy to write as a simple module; there should be a minimum of boilerplate involved.
Once I've written a module, I want to be able to write a few unit tests run them all with a few keystrokes.

How does it work?
-----------------
The `ocamltest` executable searches for modules ending with `_test.ml`.
Within those files, it searches for `unit -> unit` functions that begin with the prefix `test_` and then runs each testcase in a separate environment.
That's all you need to start testing: a script and a `_test.ml` script.

Installation
------------
1. Clone the repository 
    `git clone https://github.com/bennn/bubbles.git`
2. Run `make install`. You will likely need root permissions
3. (Optional) Set the `OCAMLTEST_HOME` environment variable to the root folder of whatever project you want to run tests in.

Uninstallation
--------------
Run `make uninstall` with root permissions.

Usage
-----
1. Make a simple module. Let's pretend its called `mymodule.ml`. 
2. Make a test file `mymodule_test.ml`. The `_test` suffix is important!
   Test file should contain `unit -> unit` functions with the prefix `test_`. These are the test cases. Other functions and modules may be defined inside the test file, but those will not be executed as part of the suite.
3. Run `ocamltest mymodule` and hope for the best.

Example
-------
The simplest possible test suite can be made as follows:
```
touch fun.ml
echo "let test\_one () = assert true" | fun_test.ml
```

A slightly more useful version of `fun_test.ml` would import `fun.ml` and the standard testing library, `ocamltest.cma`:
```
open Fun
open Ocamltest

let test\_one () = assert_true true
```

But these aren't too instructive.
Let's make a tiny lists library and run some tests on it.
First, we write the source code:
##### my_lists.ml #####
```
let length = function [] -> 0 | _::t -> 1 + length t
```

Cool cool. That's a good start. Next, we write a test for our new module:
##### my_lists_test.ml #####
```
open Ocamltest

module M = My_lists

module State = struct
  let xs = [1;2;3]
  let ys = [1;2;3;4]
end

let test_length1 () =
  assert_less (M.length [1;2]) 3

let test_length2 () = 
  assert_greater 3 (M.length [1;2])

let test_length3 () = 
  assert_equal (M.length State.ys) (1 + M.length State.xs)

let helper xss = List.hd xss

let test_length4 () = 
  let mylist = [[1; 2]] in
  assert_greater (M.length (helper mylist))  (M.length mylist)
```

Now we can run the tests:

`ocamltest my_lists`

and party. "ALL TESTS PASS"

Explanation
-----------
There's a bit going on in `my_lists_test.ml`, so let's break that down:
* The first line, `module M = My_lists`, imports the source code into the local namespace. It permits us to call the functions we want to test.
* The module starting at the second line, `module State = struct` creates shared state for the test cases. Lists `xs` and `ys` are defined once, here, and can be used in any number of tests later in the file. This is __by convention__. See the section on __Shared State__ for an explanation.
* Functions `test_length1` through `test_length4` are the test cases. Those get run. Their output decides wheter the suite passed or failed.
* `helper` is an auxillary function, defined for convenience right smack in the middle of the file. It is ignored by the harness, but `test_length4` uses it. Note that this function may not be called by test 1 through 3, because it (`helper`) was not in scope when they (tests 1 - 3) were defined.

Shared State
------------
If you'd like to define variables for the test cases to access, just declare them before you declare the test case. Test modules are compiled just like any other, from top to bottom. Preferred convention is to keep all your helpers and variables inside a module defined at the very top of the test file. This way, the variables are easy to locate within a test file and _all_ test test cases can access them.

There no support for referencing external modules. The `State` module or its equivalents, if you choose to define them, __must__ exist within either the source code or the test file.

Globbing
--------
You can supply ocamltest with a pattern instead of a module name. Say you have a directory with the following four files: `module1.ml`, `module2.ml`, `module1_test.ml`, `module2_test.ml`.

Running `ocamltest 'module*'` inside this directory will execute the harnesses `module1_test.ml` and `module2_test.ml`. (The quotes might matter, depends on which shell you use.)
Actually, you can do even better. Leading and trailing asterisks are implicit, so the following patterns achieve the same results:

* `ocamltest module`
* `ocamltest mod`
* `ocamltest ule`
* `ocamltest 'od*l'`

You get the idea. Be careful getting too lazy if you have lots of test files around and don't want to run 'em all. Or don't be careful and just run all the tests all the time.
This pattern matching is maybe a bit too eager. Let me know if you hate it.

Finding Test Files
------------------

By default, `ocamltest mymodule` searches for files matching the pattern "mymodule" in the current working directory and its containing folders. You can change this behavior. 
`ocamltest -d <dirname> mymodule` starts the search in the directory `dirname`, instead of the current directory. The `--directory` option does the same thing. Also, you can set the environment variable `OCAMLTEST_HOME`, which causes the harness to search from that directory instead of the current one. It's like running `ocamltest -d $OCAMLTEST_HOME mymodule`, just with less typing.

- - -

_Author_: Ben Greenman

_Last Updated_: 2013-08-26
