import os
path = "H:\\2020BJ zili pei\\7.19-7.29"
row = 0
for a, b, c in os.walk(path):
	number = len(c)
	for i in range(int(number)):
		temp = c[i].split(".")
		if temp[-1] == "tif":
			names = "".join(c[i])
			names = str(a) + "\\" + str(names)
			print (names)