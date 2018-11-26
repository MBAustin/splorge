
import inspect as loggerInspect
def log_function(method):
    def log(*args, **kw):
        className = args[0].__class__.__name__ if loggerInspect.ismethod(method) else None
        methodName = ""
        if className is not None:
            methodName = className + "."
        methodName += method.__name__
        with open("out.txt", "a") as out_file:
            out_file.write("call " + methodName + "\n")
            result = method(*args, **kw)
            out_file.write("exit " + methodName + "\n")
        return result
    return log


def class_decorator(decorator):
    def dectheclass(cls):
        for name, m in loggerInspect.getmembers(cls, loggerInspect.ismethod):
            setattr(cls, name, decorator(m))
        return cls
    return dectheclass


import test1

@log_function
def faa():
    bar()
    test1.foo()
    bar()
    baz()

@log_function
def baz():
    bar()

@log_function
def bar():
    return 8

faa()
