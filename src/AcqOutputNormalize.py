#!/usr/bin/python
"""
Appends source CADU file name and it's MD5 checksum to acquisition name

"""


import envoy
import os
import re
import sys


def check_input():
    if len(sys.argv) != 2:
        print("Missing destination folder. Only 1 argument please")
        exit(-1)


def find_md5sum(folder):
    cadu_file = envoy.run("%s %s %s" %
                                  ("find", folder, " -name '*_CADU_*RAW'"))
    md5sum = envoy.run("md5sum " + cadu_file.std_out)
    return md5sum.std_out


def find_source_cadu(report_file):
    source_cadu = envoy.run("grep <Source_CADU_File> "
                                 + global_report.std_out)
    # remove XML node and add to file name
    return source_cadu.std_out[22:-24]

check_input()

os.chdir(sys.argv[1])

for acq in sorted(os.listdir(".")):
    #only use unNormalized ACQ outputs
    if re.match("ACQ_[0-9]+T[0-9]+$", acq):
        file_name = acq + "_"
        global_report = envoy.run("%s %s %s" %
                              ("find", acq, " -name '*GLOBAL*XML'"))
        # empty string indicates no match found
        if global_report.std_out != "":
            file_name += find_source_cadu(global_report.std_out)
            file_name += find_md5sum(acq)
        else:
                file_name += "EMPTY"
        print "Renaming  " + acq + " : " + file_name
        #os.rename(acq, file_name)
