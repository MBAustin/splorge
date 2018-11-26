
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


@log_function
def foo():
    return beep()

@log_function
def beep():
    wow = Wow()
    wow.cool()
    return 3

@class_decorator(log_function)
class Wow:
    def cool(self):
        return 10