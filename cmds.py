# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
import subprocess

# Run ls command, get output, and print it
#decode() is necessary because check_output returns byte objects by default
#since we know we'll get ascii in this project decod() suffices to change to str
response = subprocess.check_output(['ls','-la']).decode()
print(response)






