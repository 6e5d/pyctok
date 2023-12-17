import sys
from . import Tokenizer

def test(prog):
	tok = Tokenizer()
	tok.tokenize(prog)
	for (ty, tok) in tok.toks:
		print(ty, tok, end = " ")
	print()

if len(sys.argv) >= 2:
	test(open(sys.argv[1]).read())
else:
	test("&a&=&&b&&&c&&&&d")
	test("a<<=b>>c>d")
	test("{a*b;a*=b;a**b;c=a*b}")
	test("--a")
	test("a+=0.0f")
	test("typedef int (*F)(int x);")
	test("\"123\"\n\"123\"")
