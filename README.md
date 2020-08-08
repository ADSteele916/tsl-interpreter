# tsl-interpreter
A simple interpreter for TSL (Tiny Student Language, a sublanguage of Racket) written in Python

Concept based on a bonus lecture by Gregor Kiczales for CPSC 110: Computation, Programs, and Programming in the fall term of 2019 at the University of British Columbia, in which an interpreter for a similar language was written in Racket ([Starter](https://edx-course-spdx-kiczales.s3.amazonaws.com/HTC/lecture/lec24-eval-starter.rkt), [Solution](https://edx-course-spdx-kiczales.s3.amazonaws.com/HTC/lecture/lec24-eval-solution.rkt)).

# TSL Features
## Types
* Boolean
* Number

## Expressions
* Arithmetic operations (+, -, *, /, =, zero?)
* Logical operations (and, or, not)
* if
* cons
* car/first
* cdr/rest
* empty?
* define
* lambda

## Loops
* No.

## Recursion
* Yes.

## Higher-Order Functions
* Surprisingly, yes.

## Error Handling
* None whatsoever. If the inputted code is anything less than perfect, the interpreter will crash.