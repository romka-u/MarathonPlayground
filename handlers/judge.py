
import platform
from os.path import join
import subprocess, datetime

def run_judging(filename):
	print "Judging " + filename + "..."
	try:
		if platform.system() == "Windows":
			outfile = join("testing", "solution.exe")
			try:
				subprocess.check_call(["g++", join("submissions", filename), "-O2", "-o", outfile])
			except:
				return "Compilation error."
				
			script_name = "run_test_{}.bat".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
			with open(script_name, "w") as f:
				print >>f, "@echo off"
				print >>f, "cd testing"
				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "echo \"Not judged yet.\" > \"..\\logs\\{1}_seed_{0}.log\"".format(seed.strip(), filename)

				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "java -jar SnowCleaningVis.jar -novis -seed {0} -exec solution.exe > \"..\\logs\\{1}_seed_{0}.log\" 2>&1".format(seed.strip(), filename)

				print >>f, "cd .."
				print >>f, "del", script_name

			subprocess.Popen([script_name])
		else:
			outfile = join("testing", "solution")
			try:
				subprocess.check_call(["g++", join("submissions", filename), "-O2", "-o", outfile])
			except:
				return "Compilation error."
				
			script_name = "run_test_{}.sh".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
			with open(script_name, "w") as f:
				print >>f, "cd testing"
				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "echo \"Not judged yet.\" > \"../logs/{1}_seed_{0}.log\"".format(seed.strip(), filename)

				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "java -jar SnowCleaningVis.jar -novis -seed {0} -exec './solution' > \"../logs/{1}_seed_{0}.log\" 2>&1".format(seed.strip(), filename)

				print >>f, "cd .."
				print >>f, "rm", script_name

			subprocess.Popen(["bash", "-e", script_name])

		return "Solution was compiled successfully, testing in process ({}).".format(script_name)
			
	except Exception, e:
		print e
		print "Fail to judge " + filename
