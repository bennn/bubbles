clean:
	find . -name '*.cmi' | xargs rm
	find . -name '*.cmo' | xargs rm
	find . -name '*.cma' | xargs rm

install:
	ocamlc -g -o dump.cma -a dump.ml
	echo `ocamlc -where` | xargs cp dump.* 
	ocamlc -g -o ocamltest.cma -a ocamltest.ml
	echo `ocamlc -where` | xargs cp ocamltest.* 
	ln -s `pwd`/harness311 /usr/local/bin/harness311

uninstall:
	echo `ocamlc -where`/dump.* | xargs rm 
	echo `ocamlc -where`/ocamltest.* | xargs rm 
	rm /usr/local/bin/harness311
