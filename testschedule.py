test = 'test'
a = 'This worked!'

b = test + ', ' + a

file = 'C:\\Users\\rhowell\\Documents\\Python\\scheduletest.txt'

with open(file, 'a') as f:
    f.write(b)
