TEXINPUTS := .:./config:./common:./deps:./content:./examples:
export TEXINPUTS
PATH := deps/dot2tex/bin:${PATH}
export PATH
XELATEX_JOB_NAME=document
XELATEX_OUTPUT_DIR=dist
XELATEX_ARGS=-shell-escape \
						 -output-directory=${XELATEX_OUTPUT_DIR} \
						 -jobname=${XELATEX_JOB_NAME} \
						 "\input{$*.tex}"
XELATEX_COMMAND=xelatex ${XELATEX_ARGS}

all: config/main.pdf

%.pdf: %.tex
	echo ${TEXINPUTS} ${PATH}
	$(XELATEX_COMMAND)
	bibtex "${XELATEX_OUTPUT_DIR}/${XELATEX_JOB_NAME}"
	$(XELATEX_COMMAND)

show:
	xdg-open "${XELATEX_OUTPUT_DIR}/${XELATEX_JOB_NAME}.pdf" 2> /dev/null
