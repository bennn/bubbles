bubbles
=======
A simple unit testing framework for OCaml. At the moment it's a _very_ simple testing framework.

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
2. Make a test case `mymodule_test.ml`. The `_test` suffix is important!
3. Run `ocamltest mymodule` and hope for the best.

Globbing
--------
You can supply ocamltest with a pattern instead of a module name. Say you have a directory with the following four files:

<table><tr>
    <td>module1.ml</td><td>module2.ml</td><td>module1_test.ml</td><td>module2_test.ml</td>
</tr></table>

Running `ocamltest 'module*'` will execute the harnesses `module1_test.ml` and `module2_test.ml`. (The quotes might matter, depends on which shell you use.)
Actually, you can do even better. Leading and trailing asterisks are implicit, so the following patters achieve the same results:

* `ocamltest module`
* `ocamltest mod`
* `ocamltest ule`
* `ocamltest 'od*l'`

You get the idea. Be careful getting too lazy if you have lots of test files around and don't want to run 'em all. Or don't be careful and just run all the tests all the time. 

2013-07-28, Ben Greenman (blg59)
