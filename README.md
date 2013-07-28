bubbles
=======
A simple unit testing framework for OCaml. It's slowly coming into its own.

Installation
------------
1. Clone the repository 
    `git clone https://github.com/bennn/bubbles.git`
2. Export the `ocamltest` executable to your path
    `export PATH=$PATH:<path-to-wherever-you-cloned-the-repo>`

Uninstallation
--------------
Just remove the repo and reset your path.

Usage
-----
1. Make a simple module. Let's pretend its called `mymodule.ml`. 
2. Make a test file `mymodule_test.ml`. The `_test` suffix is important!
   Test file should contain `unit -> unit` functions with the prefix `test_`. These are the test cases. Other functions and modules may be defined inside the test file, but those will not be executed as part of the suite.
3. Run `ocamltest mymodule` and hope for the best.

Example
-------
Let's make a tiny lists library and run some tests on it. First, we write the source code:
##### my_lists.ml #####
```
let length = function [] -> 0 | _::t -> 1 + length t
```

Cool cool. That's a good start. Next, we write a test for our new module:
##### my_lists_test.ml #####
```
module M = My_lists

module State = struct
  let xs = [1;2;3]
  let ys = [1;2;3;4]
end

let test_length1 () =
  assert (M.length [1;2] = 2)

let test_length2 () = 
  assert (M.length State.xs = 3)

let test_length3 () = 
  assert (M.length State.ys = 1 + M.length State.xs)

let helper xss = List.hd xss

let test_length4 () = 
  let mylist = [[1; 2]] in
  assert (M.length (helper mylist) > M.length mylist)
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

There no support for referencing external modules. The `State` module or its equivalents, if you choose to define them, __must__ exist within either the source code or the test file. (Issue #21 will address this)

Globbing
--------
You can supply ocamltest with a pattern instead of a module name. Say you have a directory with the following four files: `module1.ml`, `module2.ml`, `module1_test.ml`, `module2_test.ml`.

Running `ocamltest 'module*'` will execute the harnesses `module1_test.ml` and `module2_test.ml`. (The quotes might matter, depends on which shell you use.)
Actually, you can do even better. Leading and trailing asterisks are implicit, so the following patterns achieve the same results:

* `ocamltest module`
* `ocamltest mod`
* `ocamltest ule`
* `ocamltest 'od*l'`

You get the idea. Be careful getting too lazy if you have lots of test files around and don't want to run 'em all. Or don't be careful and just run all the tests all the time. 

2013-07-28, Ben Greenman (blg59)
