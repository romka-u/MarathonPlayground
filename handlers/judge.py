
import platform
from os.path import join
import subprocess, datetime
import random

test_jar_name = "SnowCleaningVis.jar"

def run_judging(filename):
	print "Judging " + filename + "..."
	try:
		# init strings
		if platform.system() == "Windows":
			outfile = join("testing", "solution.exe")
			script_name = "run_test_{0}.bat".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
			header = "@echo off\ncd testing"
			not_judged_str = "echo \"Not judged yet.\" > \"..\\logs\\{1}_seed_{0}.log\""
			run_jar_str = "java -jar {2} -novis -seed {0} -exec solution.exe >\"..\\logs\\{1}_seed_{0}.log\" 2>&1"
			del_str = "del"
			popen_list = [script_name]
		else:
			outfile = join("testing", "solution")
			script_name = "run_test_{}.sh".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
			header = "cd testing"
			not_judged_str = "echo \"Not judged yet.\" > \"../logs/{1}_seed_{0}.log\""
			run_jar_str = "bash -c \"time java -jar {2} -novis -seed {0} -exec './solution'\" >\"../logs/{1}_seed_{0}.log\" 2>&1"
			del_str = "rm"
			popen_list = ["bash", "-e", script_name]

		# main logic
		try:
			subprocess.check_call(["g++", join("submissions", filename), "-O2", "-o", outfile])
		except:
			return "Compilation error."

		with open(script_name, "w") as f:
			print >>f, header
			for seed in open("seeds.txt", "r"):
				if seed.strip():
					print >>f, not_judged_str.format(seed.strip(), filename)

			for seed in open("seeds.txt", "r"):
				if seed.strip():
					print >>f, run_jar_str.format(seed.strip(), filename, test_jar_name) + (" &" if random.random() < 0.3 else "")

			print >>f, "cd .."
			print >>f, del_str, script_name

		subprocess.Popen(popen_list)

		return "Solution was compiled successfully, testing in process (testing script: {0}).".format(script_name)
			
	except Exception, e:
		print e
		print "Fail to judge " + filename
