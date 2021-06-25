---
title: "A Beautiful Piece of Code: lis.py"
date: 2021-06-17T17:52:48-03:00
draft: false
tags:
- Lisp
- interpreter
- beautiful code
---

This post is about [Peter Norvig](https://norvig.com/)'s beautiful
**[lis.py](https://norvig.com/lispy.html)** interpreter for **Scheme**,
written in 132 readable lines of **Python**.

## Ok. But why?

> The big revelation to me when I was in graduate school [was] when I finally
> understood that the half page of code on the bottom of page 13 of the Lisp 1.5 manual
> was Lisp in itself.
> These were “Maxwell’s Equations of Software!”
> This is the whole world of programming in a few lines that I can put my hand over.
>
> — [_A Conversation with Alan Kay_](https://queue.acm.org/detail.cfm?id=1039523)

**Lisp** has a simple core, but is powerful and malleable. Over the decades, several **Lisp** dialects emerged.

* **Scheme** is a cleaned up **Lisp**, dropping some bad ideas and adding _closures_.
There are [lots of implementations](http://community.schemewiki.org/?scheme-faq-standards#implementations) of **Scheme**.
* **Clojure** is a modern **Lisp** that compiles to **Java** bytecode and **JavaScript**.
It's the main programming language in a
[retail bank](https://building.nubank.com.br/working-with-clojure-at-nubank/)
with millions of clients.
* **Lispy** is Peter Norvig's subset of **Scheme** written in **Python**.

Learning how **Lisp** works is a sound investment of your time because
it makes some fundamentals of Computer Science more visible and accessible,
and those fundamentals apply to any programming language.

**Lisp** and **Fortran** are the only programming languages from the 1950's that are still widely used in 2021.
There are reasons for that.
**Lisp** stays relevant because it's one of the most flexible and extensible languages you will ever learn.

**Lisp** is so extensible that it can adopt programming paradigms from other languages.
For example:

* The [Common Lisp Object System](https://en.wikipedia.org/wiki/Common_Lisp_Object_System)
brought Object Oriented Programming to **Lisp** two years after C++ appeared (eight years before **Java**).
* Shortly after **Go** popularized [CSP-style](https://en.wikipedia.org/wiki/Communicating_sequential_processes)
concurrency with coroutines and channels, **Clojure**
[implemented the same idea](https://clojure.org/news/2013/06/28/clojure-clore-async-channels).

In both cases, the new paradigm would not work well in a less flexible language.

Studying **lis.py** is a quick dive into the elegance and power of **Lisp**,
exploring not only its basic syntax, but how it works deep down, as it is implemented in two pages of code.

Now let's see what the **Scheme** dialect looks like.

## Lots of Parenthesis

**Lisp** and its descendants share a syntax of expressions with operators and operands
embedded in parenthesis, called _s-expressions_.

Here is an example using the **lis.py** interactive console, where `lis.py>` is the prompt:

```
lis.py> (* 6 7)
42
```

More formally, an _s-expression_ consists of:

* An _atom_. Examples of atoms: `*`, `define`, `-3` or `3.141592653589793`;
* an expression of the form `(x)` where `x` is 0 or more _s-expressions_.

Yes that is a recursive definition. _Lispers_ 💜 recursion.

Atoms like `*` and `define` are called _symbols_.
An atom may be a symbol or a number.

Here is how to define a `max` function, then call it:

```
lis.py> (define (max a b) (if (>= a b) a b))
lis.py> (max 2 3)
3
```

In an editor, the same function definition may be written as:

```
(define (max a b)
    (if (>= a b)
        a
        b))
```

Things to note:

* The first element in an _s-expression_ defines what it does.
* The same syntax is used for operators (`*`, `>=`), function calls (`max`), and statements (`define`, `if`).

_Lispers_ prefer to say that `define` and `if` are _special forms_ instead of statements.
The are like the keywords that mark special syntax and semantics in other
languages—instructions that cannot be expressed as function calls.

## An expression evaluator

In the [post](https://norvig.com/lispy.html) where Peter Norvig presents **lis.py**,
he describes a **Lispy Calculator**, a tiny subset of Scheme
that allows computing arithmetic expressions and defining constants.

The code of `calc.py` has two major functions:

* function `parse(source: str) -> Expression`
* function `evaluate(exp: Expression) -> Any`

They are used like this:

```python
>>> from calc import parse, evaluate
>>> parse('(* 7 (+ 2 4))')
['*', 7, ['+', 2, 4]]
>>> evaluate(parse('(* 7 (+ 2 4))'))
42
```

`parse` takes source code as a string, and returns an `Expression`
built of Python objects:

* `int` and `float` numbers;
* `str` used as identifiers (_symbols_ in Lisp parlance);
* lists of numbers, symbols, and nested lists;

`evaluate` takes an `Expression` and returns its value,
which may be of the above types and other types,
such as function objects.

The `calc` function wraps `parse` and `evaluate`:

```python
>>> calc('+')
<built-in function add>
>>> calc('(* 111 111)')
12321
```

### The global environment

To evaluate symbols like `+` and `abs`,
the evaluator fetches values stored in
a `dict`, the `global_env`

```python
>>> global_env['-']
<built-in function sub>
```

The `define` special form takes a symbol and
an expression, evaluates the expression, and
binds the symbol to the expression in the
`global_env`.

```python
>>> calc('(define n 1729)')
>>> global_env['n']
1729
```

You can `calc.py` as a script, to use it interactively.
The `calc>` prompt evaluates expressions in the calculator language:

```
$ python3 calc.py
calc> (define $ 5.0901)
calc> (* $ 200)
1018.02
calc> (define phi (/ (+ 1 (sqrt 5)) 2))
calc> phi
1.618033988749895
calc> (* phi 5)
8.090169943749475
calc>

```

### The `evaluate` function

`evaluate` is the most interesting part of the `calc.py`.

In Python, `evaluate` is best expressed with a `match` statement (introduced in Python 3.10):

```python
def evaluate(exp: Expression) -> Any:
    "Evaluate an expression in an environment."
    match exp:
        case Symbol(var):                         # variable reference
            return global_env[var]
        case int(x) | float(x):                   # number literal
            return x
        case ['define', Symbol(var), value_exp]:  # (define var exp)
            global_env[var] = evaluate(value_exp)
        case [Symbol(op), *args]:                 # (proc arg...)
            proc = evaluate(op)
            values = (evaluate(arg) for arg in args)
            return proc(*values)
```

Without going into details, the code expresses the four rules
of evaluation for the calculator language with amazing clarity.

To evaluate an expression `exp`, match its pattern with the appropriate rule:

| pattern                                         | how to evaluate                   |
|-------------------------------------------------|-----------------------------------|
| `exp` is a `Symbol`                             | look up its value in the `global_env` |
| `exp` is an `int` or `float`                    | it's a number literal, the value is itself |
| `exp` is a 3-item list starting with `'define'` | evaluate the `value_exp` and store the result in `global_env[var]`|
| `exp` is a list starting with a `Symbol`, with 0 or more items   | evaluate the first item to get a function, evaluate each argument, apply function to argument values |



### Why `if` cannot be a function call

Consider a function named `inverse` which, given x, returns 1/x.

```
lis.py> (inverse 3)
0.3333333333333333
lis.py> (inverse 0)
inf
```

If the argument is `0`, our `inverse` returns the _symbol_ `inf` instead of raising an error.

This is possible definition of `inverse`:


```
(define (inverse x)
    (if (= x 0)
        (quote inf)
        (/ 1 x)))
```

As we've seen, the syntax of `if` is:

```
(if condition consequence alternative)
```

Using `if`, we expect that only `consequence` or `alternative` will be executed, never both.
This is crucial because the `alternative` expression `(/ 1 x)` raises an error if `x` is `0`.

In contrast, consider the next function call:

```
(sum (* 2 3) (+ 4 5) (/ 10 2))
```

In this case, we expect that the 3 expressions given as arguments are all computed _before_ the `sum` function is called.

So that's the key difference between a function call and a special form.
Given this expression...

```(x a b c)```

...when:

* `x` is a function, the arguments `a`, `b`, and `c` will be evaluated before `x` is applied to them.
* `x` is a special form, then `a`, `b`, and `c` may or may not be evaluated, depending on the implementation of `x`.

In particular, the special form `quote` prevents all arguments from being evaluated, returning them as they are:

```
lis.py> (quote (a b (/ 1 0) whatever *))
(a b (/ 1 0) whatever *)
```

### To be continued...

_LR_
