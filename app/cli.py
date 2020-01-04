import functools
import inspect
import re
import sys
import traceback


class CommandLineInterface:

    def __init__(self):
        self.functions = {}

    def command(self, f):
        self.functions[f.__name__] = f

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    def main(self):
        file_name = sys.argv[0]
        if len(sys.argv) < 2:
            self.__error(file_name)
        func_name, *args = sys.argv[1:]
        if not self.__is_function_exists(func_name):
            self.__error(file_name)
        kwargs = self.__get_arguments(func_name, *args)
        if not kwargs:
            self.__error(file_name)
        func = self.functions[func_name]
        try:
            func(**kwargs)
        except Exception as error:
            print(f'ERROR: {error}')
            print(traceback.format_exc())
            sys.exit(1)
        sys.exit(0)

    def __is_function_exists(self, func_name):
        return func_name in self.functions

    def __error(self, file_name):
        print(f'USAGE: python {file_name} <command> [<key>=<value>]*')
        sys.exit(1)

    def __get_arguments(self, func_name, *args):
        func = self.functions[func_name]
        func_args = inspect.getfullargspec(func).args
        if len(func_args) != len(args):
            return None
        kwargs = {}
        for arg in args:
            if not self.__is_kwarg_format(arg):
                return None
            key, value = arg.split("=")
            if key not in func_args:
                return None
            kwargs[key] = value
        return kwargs

    def __is_kwarg_format(self, arg):
        match = re.fullmatch(r"\S+=.+", arg)
        return match is not None
