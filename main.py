import re
from typing import List, Union

from builtin_env import default_env
from environment import Environment
from expressions import (
    And,
    Atom,
    Cons,
    Definition,
    Expression,
    Function,
    FunctionCall,
    If,
    Or,
)


def parse_expression(line: str, env: Environment) -> Expression:
    def gen_list(tokens: List[str]) -> Union[str, List]:
        token = tokens.pop(0)
        if token == "(":
            rsf = []
            while tokens[0] != ")":
                rsf.append(gen_list(tokens))
            tokens.pop(0)
            return rsf
        else:
            return token

    def parse(exp_list: Union[str, List]) -> Expression:
        def atomize(param) -> Atom:
            if re.search(r"^\d+\.\d+$", param):
                return Atom(float(param))
            elif re.search(r"^\d+$", param):
                return Atom(int(param))
            else:
                return Atom(param)

        if isinstance(exp_list, str):
            return atomize(exp_list)
        else:
            exp = exp_list.pop(0)

            if exp == "lambda":
                return Function(parse(exp_list[1]), env, *exp_list[0])
            elif exp == "define":
                if isinstance(exp_list[0], str):
                    return Definition(exp_list[0], parse(exp_list[1]))
                elif isinstance(exp_list[0], list):
                    func_name = exp_list[0].pop(0)
                    return Definition(
                        func_name, Function(parse(exp_list[1]), env, *exp_list[0])
                    )

            args = list(map(parse, exp_list))

            if exp == "if":
                return If(*args)
            elif exp == "and":
                return And(*args)
            elif exp == "or":
                return Or(*args)
            elif exp == "cons":
                return Cons(*args)
            else:
                return FunctionCall(Atom(exp), *args)

    split_line = line.replace("(", " ( ").replace(")", " ) ").split()

    return parse(gen_list(split_line))


def repl(prompt="TSL> "):
    global_env = Environment(outer=default_env)
    while True:
        exp = input(prompt)
        if exp == "(exit)":
            break
        else:
            val = parse_expression(exp, global_env).eval(global_env)
            if val is not None:
                print(val)


if __name__ == "__main__":
    repl()
