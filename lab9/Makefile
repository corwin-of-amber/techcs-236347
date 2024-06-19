SKETCH_HOME ?= /usr/local/bin/sketch-1.7.5

default: compile run

all: sketch compile run


sketch: scanner.sk
	sketch $^ -fe-output-code


compile: scanner.h scanner.cpp
	g++ -o scanner scanner.cpp main.cpp -I /usr/include/sketch -I $(SKETCH_HOME)/sketch-frontend/runtime/include

run:
	./scanner
