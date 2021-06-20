---
title: "A Beautiful Piece of Code"
date: 2021-06-17T17:52:48-03:00
draft: false
tags:
- Lisp
- interpreter
---

> The big revelation to me when I was in graduate school [was] when I finally understood that the half page of code on the bottom of page 13 of the Lisp 1.5 manual was Lisp in itself. These were “Maxwell’s Equations of Software!” This is the whole world of programming in a few lines that I can put my hand over.
>
> — [_A Conversation with Alan Kay_](https://queue.acm.org/detail.cfm?id=1039523)


**Lisp** and **Fortran** are the only programming languages from the 1950's that are still widely used in 2021. 

**Lisp** has a simple core, but is powerful and malleable. Over the decades, several **Lisp** dialects emerged.

* **Scheme** is a cleaned up **Lisp**, dropping some bad ideas and adding _closures_. There are [lots of implementations](http://community.schemewiki.org/?scheme-faq-standards#implementations) of **Scheme**.
* **Clojure** is a modern **Lisp** that compiles to **Java** bytecode and **JavaScript**. There's a [bank](https://building.nubank.com.br/working-with-clojure-at-nubank/) built with it.
* **Lispy** is Peter Norvig's subset of **Scheme** written in 130 lines of readable and maintainable **Python**.

This post is about **Scheme** and Norvig's beautiful code: the **lis.py** interpreter for **Lispy**.

## Lots of Parenthesis

**Lisp** and its descendants share a syntax of expressions with operators and operands
embedded in parenthesis, called _s-expressions_.

Here is an example using the **lis.py** interactive console, where `lis.py>` is the prompt:

```
lis.py> (* 6 7)
42
```

More formally, an _s-expression_ consists of:

* An _atom_. Four examples of atoms: `*`, `define`, `-3` or `3.141592653589793`;
* an expression of the form `(…)` where `…` is 0 or more _s-expressions.

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

The `calc` function wraps `parse` and `evaluate`::

```python
>>> calc('+')
<built-in function add>
>>> calc('(* 111 111)')
12321
```

### The global environment

and one data structure:
* dictionary `global_environment`






_LR_