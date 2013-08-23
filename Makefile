install:
	ocamlc -g -o ocamltest.cma -a ocamltest.ml
	echo `ocamlc -where` | xargs cp ocamltest.* 

uninstall:
	echo `ocamlc -where`/ocamltest.* | xargs rm 
