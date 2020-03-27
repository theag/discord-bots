import re

patt = re.compile('(\d+\+)?(\d+)[Dd](\d+)([HhLl]\d+)?(!\d+)?')
s = '3+4d5 3d6'
m = patt.search(s)

print(sum([1,2,3,4]))
while m is not None:
    print(m)
    print(m.group(0))
    print(m.groups())
    print(m.group(1))
    m = patt.search(s,m.end())

l = [1,2,3]
print('{}'.format(l))
print([l[i] for i in [1,2]])