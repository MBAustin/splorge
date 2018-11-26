import test1

def faa():
    bar()
    test1.foo()
    bar()
    baz()

def baz():
    bar()

def bar():
    return 8

faa()
