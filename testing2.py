import re

patt = re.compile('(\d*)d(\d+)(\+\d+)?')
s = 'd5'
m = patt.search(s)

while m is not None:
    print(m)
    print(m.group(0))
    print(m.groups())
    m = patt.search(s,m.end())

d = [1,2,3]
print(" ".join(map(str,d)))