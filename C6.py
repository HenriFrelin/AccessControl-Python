# script that automatically tests and times the parsing and processing of 5 test policies (test1-5 csv files)
import csv
import time

permissions = []
groups = []

def parser(file):
	startImport = time.time()

	with open(file) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    line_count = 0
	    for row in csv_reader:
	        if row[0] == "p": # policy instruction
	            permissions.append([row[0].lstrip(),row[1].lstrip(),row[2].lstrip(),row[3].lstrip()])
	            line_count += 1
	        else: # group delegation
	        	groups.append([row[0].lstrip(),row[1].lstrip(),row[2].lstrip()])
	        	line_count += 1

	    print(f'Processed {line_count} lines.')

	endImport = time.time()
	return print("parse time",(endImport - startImport)*100000)

def enforcer(sub, obj, act):
	start = time.time()

	if ["p",sub,obj,act] in permissions:
	    return print("query time =",(time.time() - start)*100000)
	elif any(n[1] == sub for n in groups): # if in a group
		for group in groups:
			if group[1] == sub:
				if ["p",group[2],obj,act] in permissions: # if a user's group has the permission...
					return print("query time =",(time.time() - start)*100000)
				elif any(n[1] == group[2] for n in groups): # if user's group is a subsection of another group
					for g in groups:
						if g[1] == group[2]:
							if ["p",g[2],obj,act] in permissions: # if a user's group has the permission...
								return print("query time =",(time.time() - start)*100000)							
							else:
								return print("query time =",(time.time() - start)*100000)
				else:
					return print("query time =",(time.time() - start)*100000)
	else:
	    return print("query time =",(time.time() - start)*100000)
	
print("test1")
parser("test1.csv")
enforcer("alice","users1", "read")
enforcer("bob","users2", "write")
print("\n")

print("test2")
parser("test2.csv")
enforcer("alice","users", "read")
enforcer("bob","users", "read")
print("\n")

print("test3")
parser("test3.csv")
enforcer("james","data0", "read")
enforcer("james","data2", "write")
print("\n")

print("test4")
parser("test4.csv")
enforcer("elise","db1", "read")
enforcer("alex","db2", "write")
print("\n")

print("test5")
parser("test5.csv")
enforcer("abbey","db1", "write")
enforcer("molly","db3", "write")

