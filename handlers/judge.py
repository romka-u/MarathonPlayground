
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
				
			with open("run_test.bat", "w") as f:
				print >>f, "cd testing"
				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "echo \"Not judged yet.\" > \"..\\logs\\{1}_seed_{0}.log\"".format(seed.strip(), filename)

				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "java -jar SnowCleaningVis.jar -novis -seed {0} -exec 'solution.exe' > \"..\\logs\\{1}_seed_{0}.log\" 2>&1".format(seed.strip(), filename)

			subprocess.Popen(["run_test.sh.bat"])
			return "Solution was compiled successfully, testing in process."
		else:
			outfile = join("testing", "solution")
			try:
				subprocess.check_call(["g++", join("submissions", filename), "-O2", "-o", outfile])
			except:
				return "Compilation error."
				
			with open("run_test.sh", "w") as f:
				print >>f, "cd testing"
				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "echo \"Not judged yet.\" > \"../logs/{1}_seed_{0}.log\"".format(seed.strip(), filename)

				for seed in open("seeds.txt", "r"):
					if seed.strip():
						print >>f, "java -jar SnowCleaningVis.jar -novis -seed {0} -exec './solution' > \"../logs/{1}_seed_{0}.log\" 2>&1".format(seed.strip(), filename)

			subprocess.Popen(["bash", "-e", "run_test.sh"])
			return "Solution was compiled successfully, testing in process."
			
	except Exception, e:
		print e
		print "Fail to judge " + filename
