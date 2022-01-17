# Brainfun

Brainfun is a programming language made in python that compiles to brainf**k

## Content

- [Brainfun](#brainfun)
	- [Content](#content)
	- [Setup](#setup)
	- [Terminal command](#terminal-command)
		- [Command](#command)
		- [Parameters](#parameters)
	- [Code](#code)
		- [Commands](#commands)
		- [Examples](#examples)
		- [Errors](#errors)
			- [Tokenizer](#tokenizer)
			- [Compiler](#compiler)
	- [Contribute](#contribute)

## Setup

How to download and setup the project.

1. [Download the main branch from this repository](https://github.com/brainfun/brainfun/archive/refs/heads/main.zip "Download the repo")
2. Unzip the downloaded file
3. Open the folder in the terminal
4. Run `./brainfun.sh examples/helloWorld.bfun` or `bash ./brainfun.sh examples/helloWorld.bfun` in the terminal
5. When its finnished running, run the `ls` command and you should see a file called `output.bf`. Thats the compiled code.

## Terminal command

How to use the terminal command

### Command

`./brainfun.sh <file> <outputFile>?`

### Parameters

* **File:**
The name/path to the file you want to compile to brainf**k
* **Output file:** (opitional)
  The name of the file to output the compiled code to. Defaults to `output.bf`

## Code

How to use the Brainfun programming language

### Commands

* #### FORWARD

  **`FORWARD <Amount: Number>;`**
  Move the pointer `<Amount>` times forward

  **Parameters:**

  * `<Number: Number>`

      The amount of times you want to move the ponter forwards

* #### BACKWARD

  **`BACKWARD <Amount: Number>;`**
  Move the pointer `<Amount>` times backwards

  **Parameters:**

  * `<Amount: Number>`

      The amount of times you want to move the ponter backwards

* #### ADD

  **`ADD <Amount: Number | String>;`**
  Add `Amount` to the pointers current location

  **Parameters:**

  * `<Amount: Number | String>`

      The amout you want to incroment the value at the pointers position with

* #### SUB

  **`SUB <Amount: Number | String>;`**
  Subtract `Amount` from the pointers current location

  **Parameters:**

  * `<Amount: Number | String>`

      The amout you want to subtract the value at the pointers position with

* #### OUT

  **`OUT;`**
  Output the value at the pointers current position

* #### STORE

  **`STORE;`**
  Store the value in the output at the pointers current position

* #### LOOP

  **`LOOP: ... END;`**
  A loop that run until the value at the pointers current location is `0`

### Examples

Examples can be found in the [/examples directory](/examples)

### Errors

#### Tokenizer

* ##### UnescapedStringError
  
  Errors when a string was never closed before a new line

* ##### IllegalCharacterError

  Errors when there is an invalid character in the code

* ##### StringMaxLengthError
  
  Errors when a string is longer then `1` character

#### Compiler

* ##### UnexpectedTokenError

  Errors when there is an unexpected token

* ##### InvalidKeywordError
  
  Errors when there is a unknown keyword

## Contribute

You can contribute by filing a [issue](https://github.com/brainfun/brainfun/issues) or opening a [pull request](https://github.com/brainfun/brainfun/pulls)