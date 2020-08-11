import pytest

from builtin_env import Environment, default_env
from expressions import Atom, false, true
from main import parse_expression


@pytest.fixture
def basic_env():
    return Environment(outer=default_env)


@pytest.fixture
def list_env(basic_env):
    parse_expression(
        "(define 5to1 (cons 5 (cons 4 (cons 3 (cons 2 (cons 1 empty))))))", basic_env,
    ).eval(basic_env)
    return basic_env


def test_constant_eval(basic_env):
    assert parse_expression("true", basic_env).eval(basic_env) is true


def test_boolean_logic(basic_env):
    assert (
        parse_expression(
            "(if (and true true false) false (or false true))", basic_env
        ).eval(basic_env)
        is true
    )


def test_define_constant(basic_env):
    parse_expression("(define TEST false)", basic_env).eval(basic_env)

    assert parse_expression("TEST", basic_env).eval(basic_env) is false


def test_builtin_math(basic_env):
    assert parse_expression("(+ 1 2)", basic_env).eval(basic_env) == Atom(3)
    assert parse_expression("(* 3 4)", basic_env).eval(basic_env) == Atom(12)
    assert parse_expression("(- 3 9)", basic_env).eval(basic_env) == Atom(-6)
    assert parse_expression("(/ 15 5)", basic_env).eval(basic_env) == Atom(3)


def test_define_lambda(basic_env):
    parse_expression("(define sqr (lambda (x) (* x x)))", basic_env).eval(basic_env)

    assert parse_expression("(sqr 2)", basic_env).eval(basic_env) == Atom(4)


def test_define_function(basic_env):
    parse_expression("(define (test a) (or true a))", basic_env).eval(basic_env)

    assert parse_expression("(test false)", basic_env).eval(basic_env) is true


def test_recursion(basic_env):
    parse_expression(
        "(define (fact n) (if (zero? n) 1 (* n (fact (- n 1)))))", basic_env
    ).eval(basic_env)

    assert parse_expression("(fact 5)", basic_env).eval(basic_env) == Atom(120)


def test_list_recursion(list_env):
    parse_expression(
        "(define (sum lon) (if (empty? lon) 0 (+ (car lon) (sum (cdr lon)))))",
        list_env,
    ).eval(list_env)

    assert parse_expression("(sum 5to1)", list_env).eval(list_env) == Atom(15)


def test_higher_order(list_env):
    parse_expression(
        "(define (map f lox) (if (empty? lox) empty (cons (f (first lox)) (map f (rest lox)))))",
        list_env,
    ).eval(list_env)

    assert (
        str(
            parse_expression("(map (lambda (n) (+ n 1)) 5to1)", list_env).eval(list_env)
        )
        == "(cons 6 (cons 5 (cons 4 (cons 3 (cons 2 empty)))))"
    )
