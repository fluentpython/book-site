---
title: "Beautiful Code"
date: 2021-06-17T17:52:48-03:00
draft: false
---

> The big revelation to me when I was in graduate school [was] when I finally understood that the half page of code on the bottom of page 13 of the Lisp 1.5 manual was Lisp in itself. These were “Maxwell’s Equations of Software!” This is the whole world of programming in a few lines that I can put my hand over.
>
> — [_A Conversation with Alan Kay_](https://queue.acm.org/detail.cfm?id=1039523)


**Lisp** and **Fortran** are the only programming languages from the 1950's that are still relevant in 2021. 

**Lisp** has a simple core, but is powerful and malleable. Over the decades, several **Lisp** dialects emerged.

* **Scheme** is a cleaned up **Lisp**, dropping some bad ideas and adding _closures_. There are [lots of implementations](http://community.schemewiki.org/?scheme-faq-standards#implementations) of **Scheme**.
* **Clojure** is a modern **Lisp** that compiles to **Java** bytecode and **JavaScript**. There's a [bank](https://building.nubank.com.br/working-with-clojure-at-nubank/) built with it.
* **lis.py** is Peter Norvig's interpreter for a subset of **Scheme** written in 130 lines of readable and maintainable **Python**.

This post is about **Scheme** and Norvig's beautiful code: **lis.py**.

## Lots of Parenthesis

**Lisp** and its descendants share a syntax of expressions with operators and operands embedded in parenthesis, called _s-expressions_.

Here is an example using the **lis.py** interactive console, where `lis.py>` is the prompt:

```
lis.py> (* 6 7)
42
```

And here is how to define a `max` function, then use it:

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





_LR_