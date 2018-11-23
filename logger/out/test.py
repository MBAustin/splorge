
logLines = ""


def log_function(method):
    def log(*args, **kw):
        global logLines
        logLines += "call " + method.__name__ + "\n"
        result = method(*args, **kw)
        logLines += "exit " + method.__name__ + "\n"
        return result
    return log


@log_function
def foo():
    bar()


@log_function
def bar():
    print("Bar!")


@log_function
def baz():
    foo()
    bar()
    bar()
    foo()


baz()
with open("out.txt", "w") as out_file:
    out_file.write(logLines)