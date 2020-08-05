from typing import Callable, Optional, Union

from environment import Environment


class Expression:
    def eval(self, env: Environment):
        pass


class And(Expression):
    def __init__(self, *args: Expression):
        self.args = args

    def __str__(self):
        rsf = "(and"
        for arg in self.args:
            rsf += f" {arg}"
        rsf += ")"
        return rsf

    def eval(self, env: Environment):
        for arg in self.args:
            if arg.eval(env) is false:
                return false
        return true


class Or(Expression):
    def __init__(self, *args: Expression):
        self.args = args

    def __str__(self):
        rsf = "(or"
        for arg in self.args:
            rsf += f" {arg}"
        rsf += ")"
        return rsf

    def eval(self, env: Environment):
        for arg in self.args:
            if arg.eval(env) is true:
                return true
        return false


class If(Expression):
    def __init__(
        self, question: Expression, true_answer: Expression, false_answer: Expression
    ):
        self.question = question
        self.true_answer = true_answer
        self.false_answer = false_answer

    def __str__(self):
        return f"(if {self.question} {self.true_answer} {self.false_answer})"

    def eval(self, env: Environment):
        if self.question.eval(env) is true:
            return self.true_answer.eval(env)
        elif self.question.eval(env) is false:
            return self.false_answer.eval(env)


class Atom(Expression):
    def __init__(self, val: Optional[Union[bool, float, int]]):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __str__(self):
        if self.val is True:
            return "true"
        elif self.val is False:
            return "false"
        elif self.val is None:
            return "empty"
        else:
            return str(self.val)

    def eval(self, env: Environment):
        if isinstance(self.val, str):
            return env.find(self.val).eval(env)
        else:
            return self


true = Atom(True)
false = Atom(False)
empty = Atom(None)


class Definition(Expression):
    def __init__(self, key: str, value=Expression):
        self.key = key
        self.value = value

    def __str__(self):
        return f"(define {self.key} {self.value})"

    def eval(self, env: Environment):
        env.add(self.key, self.value)
        return None


class Function(Expression):
    """Essentially a lambda"""

    def __init__(self, body: Expression, env: Environment, *args: str):
        self.body = body
        self.env = env
        self.params = args

    def __str__(self):
        rsf = "(lambda ("
        for param in self.params:
            rsf += f" {param}"
        rsf += f") {self.body})"
        return rsf

    def eval(self, env: Environment):
        return self


class PyFunction(Expression):
    def __init__(self, func: Callable):
        self.func = func

    def eval(self, env: Environment):
        return self

    def call(self, env: Environment, *args: Expression):
        evaled_args = []
        for arg in args:
            evaled_args.append(arg.eval(env))
        return self.func(*evaled_args)


class FunctionCall(Expression):
    def __init__(self, func: Atom, *args: Expression):
        self.func = func
        self.args = args

    def __str__(self):
        rsf = f"({self.func}"
        for arg in self.args:
            rsf += f" {arg}"
        rsf += ")"
        return rsf

    def eval(self, env: Environment):
        function_object: Union[Function, PyFunction] = self.func.eval(env)
        if isinstance(function_object, PyFunction):
            return function_object.call(env, *self.args)
        else:
            new_keys = dict(
                zip(function_object.params, map(lambda arg: arg.eval(env), self.args))
            )
            local_env = Environment(new_keys, env)
            return function_object.body.eval(local_env)
