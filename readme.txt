* unsupported operators: ++ -- ?: ,
* backslace multiline string unsupported, string concat not handled
* type cast is not handled in tokenizer

a greedy tokenizer is almost perfect at tokenizing c:
however, it has the case cannot handle

y = &&x is y=&(&x)

actually check previous symbol is sufficient.

* literal
	* number
	* string
	* char
* identifier
	* type
	* var
* operator
	* unary (+ - & ! ~)
	* binary (arith, bit, logical, relation)
	* deref or mul(*)
* parentheses
	* (
	* )
	* [
	* ]
	* {
	* }

The && is interpreted as "logical and" instead of double address,
iff the previous token is:

* literal
* identifier
* parentheses
	* )
	* ]
