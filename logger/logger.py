import sys
import os

fileName = sys.argv[1]
script_dir = os.path.dirname(os.path.abspath(__file__))
abs_file_path = os.path.join(script_dir, fileName)
out_dir = "out/" + os.path.basename(fileName)

with open(abs_file_path, "r") as in_file:
    buf = in_file.readlines()


header = """
logLines = ""


def log_function(method):
    def log(*args, **kw):
        global logLines
        logLines += "call " + method.__name__ + "\\n"
        result = method(*args, **kw)
        logLines += "exit " + method.__name__ + "\\n"
        return result
    return log


"""

footer = """with open("out.txt", "w") as out_file:
    out_file.write(logLines)"""

with open(out_dir, "w") as out_file:
    out_file.write(header)
    for line in buf:
        if line.startswith("def"):
            line = "@log_function\n" + line
        out_file.write(line)
    out_file.write(footer)


execfile(out_dir)
