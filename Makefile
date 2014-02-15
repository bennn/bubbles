OCAMLC_HOME=`ocamlc -where`

clean:
	find . -name '*.cmi' | xargs rm
	find . -name '*.cmo' | xargs rm
	find . -name '*.cma' | xargs rm

install:
	ocamlc -g -o serializer.cma -a serializer.ml
	cp serializer.cma serializer.cmi serializer.cmo ${OCAMLC_HOME}
	ocamlc -g -o assertions.cma -a assertions.ml
	cp assertions.cma assertions.cmi assertions.cmo ${OCAMLC_HOME}
	ln -s `pwd`/ocamltest /usr/local/bin/ocamltest

uninstall:
	rm ${OCAMLC_HOME}/serializer.cma ${OCAMLC_HOME}/serializer.cmi ${OCAMLC_HOME}/serializer.cmo
	rm ${OCAMLC_HOME}/assertions.cma ${OCAMLC_HOME}/assertions.cmi ${OCAMLC_HOME}/assertions.cmo
	rm /usr/local/bin/ocamltest
