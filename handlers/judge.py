import os
from os.path import join
import subprocess
from pool import ProcessPool

test_jar_name = "./testing/CollageMakerVis.jar"

def run_jar(filename, seed, executable):
    log = "logs/{1}_seed_{0}.log".format(seed, filename)
    subprocess.check_call(
        "{{ /bin/bash -c 'time java -jar {jar} -novis -seed {seed} \
                          -target ../300px -source ../100px \
                          -exec {executable} 2>&1 >{log}' ; }} 2>>{log}".format(
            log=log, executable=executable, seed=seed, jar=test_jar_name),
        shell=True
    )

def run_judging(filename):
    print "Judging " + filename + "..."
    try:
        executable = join("testing", "solution_{0}".format(filename.split("_")[0]))

        try:
            subprocess.check_call(["g++", "-std=c++0x", join("submissions", filename), "-O2", "-o", executable])
        except Exception, e:
            return "Compilation error: " + str(e)

        with open("seeds.txt") as seeds_file:
            seeds = filter(None, map(lambda s: s.strip(), seeds_file.readlines()))

        for seed in seeds:
            log = "logs/{1}_seed_{0}.log".format(seed, filename)
            os.path.exists(log) and os.remove(log)

        for seed in seeds:
            ProcessPool.get_pool().apply_async(
                run_jar, [filename, seed, executable])

        return "Solution was compiled successfully, testing in progress"

    except Exception, e:
        message = "Failed to judge " + filename + ": " + str(e)
        print message
        return message
