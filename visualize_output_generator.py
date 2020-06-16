#!/usr/bin/env python3
import shutil
import glob
import argparse

def makeOutputFile(input_path):
    files = glob.glob(input_path + "/*.csv")

    for fle_name in files:
        new_fle_name = fle_name[-12:]
        shutil.copy(fle_name, new_fle_name)


parser = argparse.ArgumentParser()
parser.add_argument("--input_path", required="True")
args = parser.parse_args()
input_path = args.input_path

makeOutputFile(input_path)
