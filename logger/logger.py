import sys
import os

import shutil
script_dir = os.path.dirname(os.path.abspath(__file__))
shutil.rmtree(os.path.join(script_dir, "out"))
shutil.copytree(os.path.join(script_dir, "in"), os.path.join(script_dir, "out"))

fileName = sys.argv[1]
abs_file_path = os.path.join(script_dir, fileName)





def addLogging(file_path):

    with open(file_path, "r") as in_file:
        buf = in_file.readlines()


    header = """
import inspect as loggerInspect
def log_function(method):
    def log(*args, **kw):
        className = args[0].__class__.__name__ if loggerInspect.ismethod(method) else None
        methodName = ""
        if className is not None:
            methodName = className + "."
        methodName += method.__name__
        with open("out.txt", "a") as out_file:
            out_file.write("call " + methodName + "\\n")
        result = method(*args, **kw)
        with open("out.txt", "a") as out_file:
            out_file.write("exit " + methodName + "\\n")
        return result
    return log


def class_decorator(decorator):
    def dectheclass(cls):
        for name, m in loggerInspect.getmembers(cls, loggerInspect.ismethod):
            setattr(cls, name, decorator(m))
        return cls
    return dectheclass


"""


    with open(file_path, "w") as out_file:
        out_file.write(header)
        for line in buf:
            if line.startswith("def"):
                line = "@log_function\n" + line
            elif line.startswith("class"):
                line = "@class_decorator(log_function)\n" + line
            out_file.write(line)


for dirpath, _, filenames in os.walk(abs_file_path):
    for f in filenames:
        print f
        filePath = os.path.join(dirpath, f)
        if ('/.git' not in filePath):
            if (filePath.endswith('.py')):
                addLogging(filePath)