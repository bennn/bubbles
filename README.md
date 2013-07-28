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

2013-07-28, Ben Greenman (blg59)
