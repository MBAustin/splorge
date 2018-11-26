import sys
import os

import shutil
script_dir = os.path.dirname(os.path.abspath(__file__))
shutil.rmtree(os.path.join(script_dir, "out"))
shutil.copytree(os.path.join(script_dir, "in"), os.path.join(script_dir, "out"))

fileName = sys.argv[1]
abs_file_path = os.path.join(script_dir, fileName)

with open(abs_file_path, "r") as in_file:
    buf = in_file.readlines()


header = """
import inspect as loggerInspect

logLines = ""


def log_function(method):
    def log(*args, **kw):
        global logLines
        className = args[0].__class__.__name__ if loggerInspect.ismethod(method) else None
        methodName = ""
        if className is not None:
            methodName = className + "."
        methodName += method.__name__
        logLines += "call " + methodName + "\\n"
        result = method(*args, **kw)
        logLines += "exit " + methodName + "\\n"
        return result
    return log


def class_decorator(decorator):
    def dectheclass(cls):
        for name, m in loggerInspect.getmembers(cls, loggerInspect.ismethod):
            setattr(cls, name, decorator(m))
        return cls
    return dectheclass


"""

footer = """

with open("out.txt", "w") as out_file:
    out_file.write(logLines)"""


with open(abs_file_path, "w") as out_file:
    out_file.write(header)
    for line in buf:
        if line.startswith("def"):
            line = "@log_function\n" + line
        elif line.startswith("class"):
            line = "@class_decorator(log_function)\n" + line
        out_file.write(line)
    out_file.write(footer)
