from builtin_env import default_env
from expressions import Atom, false, true
from main import parse_expression

import pytest


@pytest.fixture
def setup_env():
    return default_env


def test_constant_eval(setup_env):
    assert parse_expression("true", setup_env).eval(setup_env) is true


def test_boolean_logic(setup_env):
    assert (
        parse_expression(
            "(if (and true true false) false (or false true))", setup_env
        ).eval(setup_env)
        is true
    )


def test_define_constant(setup_env):
    parse_expression("(define TEST false)", setup_env).eval(setup_env)

    assert parse_expression("TEST", setup_env).eval(setup_env) is false


def test_builtin_math(setup_env):
    assert parse_expression("(+ 1 2)", setup_env).eval(setup_env) == Atom(3)
    assert parse_expression("(* 3 4)", setup_env).eval(setup_env) == Atom(12)
    assert parse_expression("(- 3 9)", setup_env).eval(setup_env) == Atom(-6)
    assert parse_expression("(/ 15 5)", setup_env).eval(setup_env) == Atom(3)


def test_define_lambda(setup_env):
    parse_expression("(define sqr (lambda (x) (* x x)))", setup_env).eval(setup_env)

    assert parse_expression("(sqr 2)", setup_env).eval(setup_env) == Atom(4)


def test_define_function(setup_env):
    parse_expression("(define (test a) (or true a))", setup_env).eval(setup_env)

    assert parse_expression("(test false)", setup_env).eval(setup_env) is true


def test_recursion(setup_env):
    parse_expression(
        "(define (fact n) (if (zero? n) 1 (* n (fact (- n 1)))))", setup_env
    ).eval(setup_env)

    assert parse_expression("(fact 5)", setup_env).eval(setup_env) == Atom(120)
