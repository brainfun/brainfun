#########################
# IMPORTS
#########################

from typing import Type
from enum import Enum

#########################
# CONSTANTS
#########################

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"

UNDERSCORE = "_"
DOT = "."
SPACE = " "

ALL = LOWERCASE + UPERCASE + NUMBERS + UNDERSCORE + DOT

STRING = "\""
COLON = ":"
SEMICOLON = ";"

#########################
# POS CLASS
#########################

class Pos:
	def __init__(self, col: int, line: int, file: str = None) -> None:
		self.line = line
		self.col = col
		self.file = file

class StartEndPos:
	def __init__(self, start: Pos, end: Pos = None, file: str = None) -> None:
		self.start = start
		if not end:
			self.end = Pos(self.start.col, self.start.line, self.start.file)
		else:
			self.end = end
		self.file = file
		
#########################
# ERRORS
#########################

class Error:
	def __init__(self, pos: StartEndPos, description: str, code: str) -> None:
		self.pos = pos
		self.description = description
		self.code = code

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}: \"{self.description}\""

	def error(self) -> None:
		if self.pos.start.line != self.pos.end.line:
			arrows = (' '*self.pos.start.col) + ('^'*(len(self.code) - self.pos.start.col + 1))
		else:
			arrows = (' '*self.pos.start.col) + ('^'*(self.pos.end.col-self.pos.start.col + 1))
		print(f"{self.code}\n{arrows}\n\n{self}")

class UnescapedStringError(Error):
	def __init__(self, pos: StartEndPos, code: str) -> None:
		super().__init__(pos, "String was never escaped", code)

class IllegalCharacterError(Error):
	def __init__(self, pos: StartEndPos, char: str, code: str) -> None:
		super().__init__(pos, f"Unexpected char: \"{char}\"", code)

class StringMaxLengthError(Error):
	def __init__(self, pos: StartEndPos, code: str) -> None:
		super().__init__(pos, "Strings have a max length of 1 character", code)

#########################
# TOKEN CLASS
#########################

class Token:
	def __init__(self, value: str, pos: StartEndPos) -> None:
		self.value = value
		self.pos = pos
		self.type = self.__class__.__name__
	
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}: {self.value}>"

class KeywordToken(Token):
	def __init__(self, value: str, pos: StartEndPos) -> None:
		super().__init__(value, pos)

class StringToken(Token):
	def __init__(self, value: str, pos: StartEndPos) -> None:
		super().__init__(value, pos)

class NumberToken(Token):
	def __init__(self, value: str, pos: StartEndPos) -> None:
		super().__init__(value, pos)

class ColonToken(Token):
	def __init__(self, pos: StartEndPos) -> None:
		super().__init__(None, pos)

class NewLineToken(Token):
	def __init__(self, pos: StartEndPos) -> None:
		super().__init__(None, pos)

class NoneToken(Token):
	def __init__(self, pos: StartEndPos) -> None:
		super().__init__(None, pos)

class SemicolonToken(Token):
	def __init__(self, pos: StartEndPos) -> None:
		super().__init__(None, pos)

#########################
# TOKENIZER
#########################

class Tokenizer:
	def __init__(self, source: str, file: str = None) -> None:
		self.col = -1
		self.line = 0
		self.source = source
		self.file = file
		self.lineSource = self.source.split("\n")[0]
		self.currentChar = True
		self.tokens = []

		self.advance()


	def tokenize(self) -> list[Token] | Error:
		while self.currentChar:
			
			if not self.currentChar:
				break
			newToken = None
			if self.currentChar == "\n":
				self.advance()
			elif self.currentChar == STRING:
				newToken = self.makeString()
			elif self.currentChar in NUMBERS:
				newToken = self.makeNumber()
			elif self.currentChar in SPACE + "\t":
				self.advance()	
			elif self.currentChar in LOWERCASE + UPERCASE + UNDERSCORE:
				newToken = self.makeKeyword()
			elif self.currentChar == COLON:
				newToken = ColonToken(StartEndPos(Pos(self.col, self.line, self.file)))
				self.advance()
			elif self.currentChar == SEMICOLON:
				newToken = SemicolonToken(StartEndPos(Pos(self.col, self.line, self.file)))
				self.advance()
			else:
				newToken = IllegalCharacterError(StartEndPos(Pos(self.col, self.line, self.file), file=self.file), self.currentChar, self.lineSource)

			if newToken and issubclass(type(newToken), Error):
				return newToken
			
			if newToken:
				self.tokens.append(newToken)	

		return self.tokens

	def makeKeyword(self) -> KeywordToken:
		value = str(self.currentChar)
		start = Pos(self.col, self.line, self.file)
		self.advance()
		while self.currentChar and self.currentChar in ALL:
			value += self.currentChar
			self.advance()
		
		return KeywordToken(value, StartEndPos(start, Pos(self.col, self.line, self.file), self.file))

	def makeNumber(self) -> NumberToken:
		value = str(self.currentChar)
		start = Pos(self.col, self.line, self.file)
		self.advance()
		while self.currentChar and self.currentChar in NUMBERS:
			value += self.currentChar
			self.advance()

		return NumberToken(value, StartEndPos(start, Pos(self.col, self.line, self.file), self.file))
		

	def makeString(self) -> StringToken | UnescapedStringError | IllegalCharacterError | StringMaxLengthError:
		value = ""
		start = Pos(self.col, self.line, self.file)
		self.advance()
		while self.currentChar and self.currentChar in ALL + SPACE:
			value += self.currentChar
			self.advance()
		if self.currentChar == STRING:
			if len(value) > 1:
				return StringMaxLengthError(StartEndPos(start, Pos(self.col, self.line, self.file)), self.source.split("\n")[start.line])

			token = StringToken(value, StartEndPos(start, Pos(self.col, self.line), self.file))
			self.advance()
			return token

		if self.currentChar == "\n":
			return UnescapedStringError(StartEndPos(start, Pos(self.col, self.line, self.file)), self.source.split("\n")[start.line])
		
		return IllegalCharacterError(StartEndPos(Pos(self.col, self.line, self.file)), self.currentChar, self.source.split("\n")[start.line])
		

	def advance(self) -> None:
		self.col += 1
		if len(self.lineSource) - 1 < self.col:
			self.col = 0
			self.line += 1
			# self.tokens.append(NewLineToken(StartEndPos(Pos(self.col, self.line, self.file))))
			if len(self.source.split("\n")) - 1 < self.line:
				self.currentChar = None
				self.lineSource = None
				return
			self.lineSource = self.source.split("\n")[self.line]

		if len(self.lineSource) and self.currentChar != "\n":
			self.currentChar = self.lineSource[self.col]
		else:
			self.currentChar = "\n"

	def unadvance(self) -> None:
		self.col -= 1
		if self.col < 0:
			self.line -= 1
			if self.line < 0:
				self.line = 0
			self.lineSource = self.source.split("\n")[self.line]
			
		self.currentChar = self.lineSource[self.col]