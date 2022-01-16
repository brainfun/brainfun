import tokenizer
import compiler
import argparse
import os
import time

start_time = time.time()

command = argparse.ArgumentParser(description="Compile a .bfun file")

command.add_argument(
	"file",
	type=str,
	help="The file to compile"
)

command.add_argument(
	"-o",
	"--output_file",
	type=str,
	help="The file to output the compiled code in. Default: output.bf"
)

args = command.parse_args()

print("○ Reading from file", end="\r")

try:
	with open(args.file, "r") as f:
		code = f.read()
except FileNotFoundError as err:
	print(f"✘ ERROR while reading file: '{args.file}' dose not exist")
	exit()
except Exception as err:
	print(f"✘ ERROR while reading from file: {err}")
	exit()

print("✔ Reading from file")

print("○ Tokenizing code", end="\r")

t = tokenizer.Tokenizer(code, os.path.basename(args.file))
tokens = t.tokenize()

if issubclass(type(tokens), tokenizer.Error):
	print(f"✘ ERROR while tokenizing code: ")
	tokens.error()
	exit()

print("✔ Tokenizing code")

print("○ Compiling code", end="\r")

c = compiler.Compiler(tokens, os.path.basename(args.file), code)
output = c.compile()

if issubclass(type(output), compiler.Error):
	print(f"✘ ERROR while compiling code: ")
	output.error()
	exit()

print("✔ Compiling code")

print("○ Writing to file", end="\r")

outFile = "output.bf" if not args.output_file else args.output_file

if os.path.exists(outFile):
	print("○ Writing to file")
	i = input("  ? File already exist, do you want to overwrite it? (y) ")
	if not i or i.lower() in ["y", "yes"]:
		pass
	else:
		print(f"✘ EXITING didn't overwrite file")
		exit()


try:
	with open(outFile, "w") as f:
		code = f.write(output)
except Exception as err:
	print(f"✘ ERROR while reading from file: {err}")
	exit()

print("✔ Writing to file")

print(f"✔ DONE in {str(round(time.time() - start_time, 3))}s")