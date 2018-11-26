import sys
import os
import json
# Sample usage:
# python3 logToJson.py tetrisLog.txt 

class fxnCall(object):
	def __init__(self, name, time = 0):
		self.name = name
		self.time = time
		self.children = []

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=False, indent=4)


class JsonLog(object):
	def __init__(self, abs_file_path):
		self.program = fxnCall("Program")
		with open(abs_file_path, "r") as in_file:
			buf = in_file.readlines()
		self.parseInputLog(buf)
		self.printLog()


	def printLog(self):
		print("Printing log to " + out_dir)
		with open(out_dir, "w") as out_file:
			out_file.write(self.program.toJSON())
		
	def parseInputLog(self, buf):
		fxnStack = []
		for line in buf:
			lineArray = line.split()
			if (lineArray[0] == "call"):
				#make fxn
				if (len(lineArray) == 2):
					fxnName = lineArray[1]
					newFxn = fxnCall(fxnName)
				elif (len(lineArray) == 3):
					time = lineArray[2]
					fxnName = lineArray[1]
					newFxn = fxnCall(fxnName, time)
				else:
					print("Invalid log. Log has to many or to little values here: " + line)
				
				
				#add fxn to children of top of fxnStack, if fxnStack is empty add it to the program's children
				if (len(fxnStack) == 0):
					self.program.children.append(newFxn)
				else:
					fxnStack[len(fxnStack) - 1].children.append(newFxn)
				#add new fxn to fxnStack
				fxnStack.append(newFxn)
			elif (lineArray[0] == "exit"):
				if (len(fxnStack) == 0):
					print("Fatally Invalid log, exiting. Log exits at nothing here: " + line)
					exit()
				else:
					fxnStack.pop()
			else:
				print("Invalid log, doesn't start with exit or call here: " + line)

if __name__ == '__main__':
	fileName = sys.argv[1]
	log_dir = os.path.dirname(os.path.abspath(__file__))
	abs_file_path = os.path.join(log_dir, fileName)
	out_dir = os.path.basename(fileName).split(".")[0] + 'Out.json'

	JsonLog(abs_file_path)
