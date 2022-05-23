import re

def log_reader(file):
    with open(file) as fd:
        for line in fd:
            if re.match("(.*)\.js", line):
                yield line.split()[6].split('/')[2]
my_reader = log_reader('*FILE*.txt')
paths = set(my_reader) # unique elements
sortt=sorted(paths)
for row in sortt:
    print(row)
