import re

PATTERN_MENTION = re.compile(r'(?:\<@)(\d+)(?:\>)')

s = "Daneel: <@479619027631734787> there is already a session started in this channel"

mat = PATTERN_MENTION.search(s)

print(mat.group())
print(mat.groups())
print(mat.group(1))