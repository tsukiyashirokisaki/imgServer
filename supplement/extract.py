import os
import sys
def extractIP(name):
	os.system("ping -c 1 %s > extractIP.txt"%(name))
	f = open("out.txt","r")
	ip = f.read().split(" ")[2][1:-1]
	f.close()
	os.system("rm extractIP.txt")
	return ip
print(extractIP(sys.argv[1]))
