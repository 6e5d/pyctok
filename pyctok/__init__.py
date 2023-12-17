from importer import importer
importer("../../pycdb/pycdb", __file__)

import itertools
from pycdb import binop, prefixop

ps = {"(": 41, ")": 42, "[": 43, "]": 44, "{": 45, "}": 46, ";": 47}

class Tokenizer():
	def __init__(self):
		self.current = 0
		self.toks = []
		self.pending = []
		self.escape = False
	def flush(self):
		if self.pending:
			s = "".join(self.pending)
			self.toks.append((self.current, s))
			self.pending = []
		self.current = 0
	def peek(self, s):
		if len(s) >= 2:
			return s[1]
		else:
			return None
	def prev(self, x):
		if x > len(self.toks):
			return 0
		return self.toks[-x][0]
	def testbin(self, s):
		ch = s[0]
		# the asterisk ambiguity is circumvented by disallowing
		# multiplication at beginning of a statement
		# corner cases handled: a *= b, a ** b
		if ch == "*":
			p2 = self.prev(2)
			if p2 == 45 or p2 == 47:
				self.current = 31
				self.flush()
			else:
				self.current = 32
				self.flush()
		p1 = self.prev(1)
		if p1 in [42, 44] or p1 >= 10 and p1 < 30:
			self.current = 32
		else:
			self.current = 31
			self.flush()
	def go(self, s):
		ch = s[0]
		if self.current in [12, 13]:
			# no quote resolve here
			if self.escape:
				self.escape = False
				self.pending.append(ch)
				return
			if ch == '"' and self.current == 12:
				self.flush()
				return
			if ch == "'" and self.current == 13:
				self.flush()
				return
			self.pending.append(ch)
			if ch == "\\":
				self.escape = True
		elif ch == '"':
			self.flush()
			self.current = 12
		elif ch == "'":
			self.flush()
			self.current = 13
		elif ch.isspace():
			if self.current == 0:
				return
			self.flush()
		elif ch == ".":
			if self.current != 11:
				self.flush()
				self.pending.append(ch)
				self.current = 32
				self.flush()
			self.pending.append(ch)
		elif ch.isalnum() or ch in "_":
			if self.current >= 10 and self.current < 30:
				self.pending.append(ch)
				return
			self.flush()
			if ch.isdigit():
				self.current = 11
			else:
				self.current = 21
			self.pending.append(ch)
		elif ch in ps:
			self.flush()
			self.current = ps[ch]
			self.pending.append(ch)
			self.flush()
		elif self.current > 30 and self.current < 40:
			self.pending.append(ch)
			if ch == "<" or ch == ">":
				p = self.peek(s)
				if p == "=":
					self.current = 32
					return
			self.flush()
		else:
			self.flush()
			self.pending.append(ch)
			p = self.peek(s)
			if p != None and f"{ch}{p}" in binop:
				self.current = 32
				return
			self.testbin(s)
	def tokenize(self, s):
		s = list(s)
		for idx in range(len(s)):
			self.go(s[idx:])
		self.flush()
