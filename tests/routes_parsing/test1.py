import re

t1 = 'Data !@[value1] and also !@[system:uptime] testing.'

print("Content: " + t1)

if re.search('!@\[[_a-zA-Z0-9:]*\]', t1):
    print("YES")
else:
    print("NO")

o = re.sub('!@\[[_a-zA-Z0-9:]*\]', '_B9yPrsE_\\g<0>_B9yPrsE_', t1)
o2 = o.split("_B9yPrsE_")

for i in o2:
    if i.startswith("!@["):
        i2 = re.sub('[^\w:]', "", i)
        print("Parse: " + str(i) + " " +str(i2))
    else:
        print("Plain: '" + str(i) + "'")
