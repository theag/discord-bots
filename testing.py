import re

patt = re.compile('^(?<=r)\d+$')

print(patt.search('r14'))