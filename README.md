# 8085 Microprocessor Opcode Generator

This program takes a 8085 assembly program as input and prints the opcodes and Address Mapping of each of the instructions.

## Sample Input and Output

Assembly code can be provided to the program as shown in the examples in the `samples` directory. For instance, consider the following program which divides 2 numbers:

```asm
LDA 2501H
MOV B, A
LDA 2500H
MVI C, 00H
LOOP;CMP B
JC REMAINDER
SUB B
INR C
JMP LOOP
REMAINDER;STA 2503H
MOV A, C
STA 2502H
HLT
```
Here, division is performed by repeated subtraction method. The dividend is stored in 2500H, quotient is generated in 2502H, and remainder is generated in 2503H.

For the above program, output provided by this program would be:

| Address | Mnemonics  | Opcodes  |
|---------|----------- |--------- |
| 2000H   | LDA 2501H  | 3A 01 25 |
| 2003H   | MOV B, A   | 47       |
| 2004H   | LDA 2500H  | 3A 00 25 |
| 2007H   | MVI C, 00H | 0E 00    |
| 2009H   | CMP B      | B8       |
| 200AH   | JC 2012H   | DA 12 20 |
| 200DH   | SUB B      | 90       |
| 200EH   | INR C      | 0C       |
| 200FH   | JMP 2009H  | C3 09 20 |
| 2012H   | STA 2503H  | 32 03 25 |
| 2015H   | MOV A, C   | 79       |
| 2016H   | STA 2502H  | 32 02 25 |
| 2019H   | HLT        | 76       |

Some points to note are as follows:

* The mnemonics and the addresses are written in the assembly code with a space in between each token.
* If a mnemonic takes two arguments (such as MOV commands), a comma can be placed after the first argument as show in the example.
* All the addresses specified in the code (such as in STA commands) have to be in hexadecimal and has to be appended by the symbol `H`.
* Labels can be provided in the code for better understandability and for looping constructs as shown in the example (like `LOOP` in the code) but they have to be followed by a semi-colon.
* Blank lines can be inserted in the code for better readability.
* TODO: Adding support for comments in the assembly code.

## Usage and Options

First install the required library to run the program.
```shell
pip install tabulate
```

The [generate.py](./generate.py) is the main self-contained unit. It takes 2 arguments:

1. Path to the assembly code file (has to be an ASCII file).
2. Hardware kit (optional)

By default, it generates address from `2000H`.
```shell
python generate.py ./samples/FibonacciCount.txt
```

It supports two hardware kits - NVIS and Dynalog. If this information is provided as an argument, then it generates addresses compatible with the corresponding hardware kit.
```shell
python generate.py ./samples/FibonacciCount.txt NVIS
```

The [generate_db.py](./generate_db.py) performs essentially the same thing, but it incorporates a database in the picture. In this case, `Oracle` is used. The mnemonics, opcodes and the address length of each instruction need to be saved in the database.

The table should be named `Opcodes8085` and it should have 3 columns, namely, `Mnemonics`, `Opcodes` and `Length`. The structure of the table (partial) is shown as follows:

| Mnemonics | Opcodes | Length |
|-----------|---------|--------|
| ACI Data  | CE      | 2      |
| ADC A     | 8F      | 1      |

The entire list of all the instructions are available in the [generate.py](./generate.py).

TODO: An SQL file performing all the steps can be included.

To connect to the database from python, we need to install the following module:
```shell
pip install cx-Oracle
```

Additionally, the username and password also needs to be provided in the [generate_db.py](./generate_db.py) in the connection part.

It has been tested with `Oracle 18C`.

Usage is the same as that of the self-contained one.

Note: Implementation using the Oracle database is kind of useless because the data is static. It does not change. So it can be setup in a single file and thus, it becomes very portable. Inclusion of databases adds a lot of external dependencies and overheads. It has been done just for educational purposes and is not recommended for use.
