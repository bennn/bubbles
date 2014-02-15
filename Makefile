clean:
	find . -name '*.cmi' | xargs rm
	find . -name '*.cmo' | xargs rm
	find . -name '*.cma' | xargs rm

install:
	ocamlc -g -o serializer.cma -a serializer.ml
	echo `ocamlc -where` | xargs cp serializer.* 
	ocamlc -g -o assertions.cma -a assertions.ml
	echo `ocamlc -where` | xargs cp assertions.* 
	ln -s `pwd`/ocamltest /usr/local/bin/ocamltest

uninstall:
	echo `ocamlc -where`/serializer.* | xargs rm 
	echo `ocamlc -where`/assertions.* | xargs rm 
	rm /usr/local/bin/ocamltest
