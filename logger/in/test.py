def foo():
    bar()


def bar():
    print("Bar!")


def baz():
    foo()
    bar()
    bar()
    foo()


baz()
