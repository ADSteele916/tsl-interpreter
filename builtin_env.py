from typing import Union

from environment import Environment
from expressions import Atom, Cons, Expression, PyFunction, empty, false, true


def add(*args: Atom) -> Atom:
    rsf = 0
    for arg in args:
        rsf += arg.val
    return Atom(rsf)


def subtract(*args: Atom) -> Atom:
    rsf = args[0].val
    for arg in args[1:]:
        rsf -= arg.val
    return Atom(rsf)


def multiply(*args: Atom) -> Atom:
    rsf = 1
    for arg in args:
        rsf *= arg.val
    return Atom(rsf)


def divide(*args: Atom) -> Atom:
    rsf = args[0].val
    for arg in args[1:]:
        rsf /= arg.val
    return Atom(rsf)


def equals(*args: Atom) -> Atom:
    first = args[0].val
    for arg in args[1:]:
        if arg.val != first:
            return false
    return true


def zero_check(atom: Atom) -> Atom:
    if atom.val == 0:
        return true
    else:
        return false


def lnot(atom: Atom) -> Atom:
    if atom.val is false:
        return true
    else:
        return false


def car(cons: Cons) -> Expression:
    return cons.car


def cdr(cons: Cons) -> Union[Cons, Atom]:
    return cons.cdr


def empty_check(exp: Expression) -> Atom:
    if exp is empty:
        return true
    else:
        return false


default_env = Environment(
    {
        "true": true,
        "false": false,
        "empty": empty,
        "+": PyFunction(add),
        "-": PyFunction(subtract),
        "*": PyFunction(multiply),
        "/": PyFunction(divide),
        "=": PyFunction(equals),
        "zero?": PyFunction(zero_check),
        "not": PyFunction(lnot),
        "car": PyFunction(car),
        "cdr": PyFunction(cdr),
        "first": PyFunction(car),
        "rest": PyFunction(cdr),
        "empty?": PyFunction(empty_check),
    }
)
