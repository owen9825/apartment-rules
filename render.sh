#!/bin/bash
HASH=$(git rev-parse --short HEAD)
echo "\\newcommand{\\githash}{$HASH}" > githash.tex
echo "\\newcommand{\\giturl}{https://github.com/owen9825/apartment-rules/commit/$HASH}" >> githash.tex
pdflatex-dev main.tex
