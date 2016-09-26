# ANTLR 3
The ANTLR 3 lib is used to generate a lexer and parser for FCL, in Python.

## Requirements

To make things simpler, the ANTLR lib can be run inside a docker container. So you'll only need to install **Docker** and **docker-compose**

After installing both, you'll need to build the docker image used to run ANTLR:

```sh
$ cd tools/antlr3
```

Then:

```sh
$ sudo docker-compose build
```


## Changing the Lexer and Parser

If possible don't change the python code in the files `FclLexer.py` nor `FclParser.py`, instead change the file `tools/antlr3/Fcl.g` to meet what you want, and then re-generate the Lexer and Parser file as described bellow.

## (Re)Generating the FclLexer and FclParser

Navigate to the directory `tools/antlr3`:

```sh
$ cd tools/antlr3
```

Once inside it, run docker-compose:

```sh
$ sudo docker-compose run --rm antrl3
```

This will generate the files `FclLexer.py`, `FclParser.py` and `Fcl.tokens`.

After this you can copy the **Lexer** and **Parser** files into the project (the `Fcl.tokens` can be ignored)