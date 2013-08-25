install:
	ocamlc -g -o dump.cma -a dump.ml
	echo `ocamlc -where` | xargs cp dump.* 
	ocamlc -g -o ocamltest.cma -a ocamltest.ml
	echo `ocamlc -where` | xargs cp ocamltest.* 

uninstall:
	echo `ocamlc -where`/dump.* | xargs rm 
	echo `ocamlc -where`/ocamltest.* | xargs rm 
