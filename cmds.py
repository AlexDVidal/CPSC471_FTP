# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
import subprocess

# Run ls command, get output, and print it
response = subprocess.check_output(['ls','-la'])
response = response.split(sep='\n')
print(response)





