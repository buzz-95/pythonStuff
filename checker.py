import subprocess
import shlex
import os
import datetime
import threading
import time

executionCompleted = False
runThread = threading.Thread()
timeThread = threading.Thread()

def runningFor(timeLimit):
	global executionCompleted,runThread
	startTime = datetime.datetime.now()
	while True:
		if executionCompleted:
			return
		time.sleep(0.05)
		currTime = datetime.datetime.now()
		timeDiff = (currTime - startTime).total_seconds()
		print(timeDiff)
		if timeDiff > timeLimit:
			print("Time Limit Exceeded!")
			return

def processSolution(cmd):
	global executionCompleted
	programOutput = os.popen(cmd).read()
	print("programOutput : " + str(programOutput))
	executionCompleted = True
	return


def compileSolutionFail(fileName):
	#compilationOutput = os.popen("g++ " + fileName).read()
	cmd = "g++ " + fileName
	p = subprocess.Popen([cmd],shell = True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	compilationOutput = p.stdout.read()
	#print("OUTPUT : " + str(compilationOutput.decode()))
	compilationOutputStr = str(compilationOutput.decode())
	if "error" in compilationOutputStr:
		return True
	return False

def main():
	fileName = "soln.cpp"
	if compileSolutionFail(fileName):
		print("Compilation Error!")
		return
	print("Successfully Compiled!")
	timeLimit = 1 #second
	processSolutionCmd = "./a.out<input.txt"
	global execultionCompleted
	execultionCompleted = False
	timeThread = threading.Thread(target=runningFor,args=(1,))
	runThread = threading.Thread(target=processSolution,args=(processSolutionCmd,))
	runThread.start()
	timeThread.start()
	running = True
	while running:
		if timeThread.is_alive() == False:
			if runThread.is_alive():
				runThread.kill()
				running = False
			else:
				running = False
	print("Execution Completed!")

if __name__ == '__main__':
	main()
	
	