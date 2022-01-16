#########################
# IMPORTS
#########################

from tokenizer import Token, StartEndPos, NumberToken, NoneToken, ColonToken, KeywordToken, StringToken

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
		arrows = (' '*self.pos.start.col) + ('^'*(self.pos.end.col-self.pos.start.col + 1))
		currentLine = self.code.split('\n')[self.pos.start.line]
		print(f"{currentLine}\n{arrows}\n\n{self}")

class UnexpectedTokenError(Error):
	def __init__(self, pos: StartEndPos, expected: Token, got: Token, code: str) -> None:
		super().__init__(pos, f"Expected \"{str(expected)}\", but got \"{str(got)}\"", code)

class InvalidKeywordError(Error):
	def __init__(self, pos: StartEndPos, got: Token, code: str) -> None:
		super().__init__(pos, f"\"{str(got.value)}\" is not a valid keyword", code)

#########################
# COPMILER
#########################

class Compiler:
	def __init__(self, tokens: list[Token], file: str, sorce) -> None:
		self.tokens = tokens
		self.file = file
		self.tokenIndex = 0
		self.currentToken = self.tokens[self.tokenIndex]
		self.source = sorce
		self.openLoops = 0

	def compile(self) -> str | UnexpectedTokenError:
		out = ""
		while self.currentToken.type != "NoneToken":
			if self.currentToken.type == "KeywordToken":
				if self.currentToken.value == "FORWARD":
					self.advance()
					if self.currentToken.type != "NumberToken":
						return UnexpectedTokenError(self.currentToken.pos, "NumberToken", self.currentToken, self.source)
					out += ">"*int(self.currentToken.value)
				elif self.currentToken.value == "BACKWARD":
					self.advance()
					if self.currentToken.type != "NumberToken":
						return UnexpectedTokenError(self.currentToken.pos, "NumberToken", self.currentToken, self.source)
					out += "<"*int(self.currentToken.value)
				elif self.currentToken.value == "ADD":
					self.advance()
					if not self.currentToken.type in ["NumberToken", "StringToken"]:
						return UnexpectedTokenError(self.currentToken.pos, ["NumberToken", "StringToken"], self.currentToken, self.source)
					if self.currentToken.type == "NumberToken":
						out += "+"*int(self.currentToken.value)
					else:
						out += "+"*ord(str(self.currentToken.value))
				elif self.currentToken.value == "SUB":
					self.advance()
					if not self.currentToken.type in ["NumberToken", "StringToken"]:
						return UnexpectedTokenError(self.currentToken.pos, ["NumberToken", "StringToken"], self.currentToken, self.source)
					if self.currentToken.type == "NumberToken":
						out += "-"*int(self.currentToken.value)
					else:
						out += "-"*ord(str(self.currentToken.value))
				elif self.currentToken.value == "OUT":
					out += "."
				elif self.currentToken.value == "STORE":
					out += ","
				elif self.currentToken.value == "LOOP":
					self.advance()
					if self.currentToken.type != "ColonToken":
						return UnexpectedTokenError(self.currentToken.pos, "ColonToken", self.currentToken, self.source)
					out += "["
					self.openLoops += 1
				elif self.currentToken.value == "END":
					if self.openLoops < 1:
						return UnexpectedTokenError(self.currentToken.pos, "KeywordToken", self.currentToken, self.source)
					out += "]"
					self.openLoops -= 1
				else:
					return InvalidKeywordError(self.currentToken.pos, self.currentToken, self.source)
			else:
				return UnexpectedTokenError(self.currentToken.pos, "KeywordToken", self.currentToken, self.source)

			previousToken = self.currentToken

			self.advance()

			if self.currentToken.type != "SemicolonToken" and previousToken.type != "ColonToken":
				return UnexpectedTokenError(self.currentToken.pos, "SemicolonToken", self.currentToken, self.source)
			
			if previousToken.type != "ColonToken":
				self.advance()

		return out


	def advance(self):
		self.tokenIndex += 1
		if not len(self.tokens) - 1 < self.tokenIndex:
			self.currentToken = self.tokens[self.tokenIndex]
		else:
			self.currentToken = NoneToken(StartEndPos(self.currentToken.pos.start, file=self.currentToken.pos.file))
