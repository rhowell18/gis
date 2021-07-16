####This is just a test for scheduling a python script to run on a schedule. The script works, just change the file path
#Use Windows Scheduler
#https://datatofish.com/python-script-windows-scheduler/

test = 'test'
a = 'This worked!'

b = test + ', ' + a

file = 'C:\\Users\\rhowell\\Documents\\Python\\scheduletest.txt'

with open(file, 'a') as f:
    f.write(b)
