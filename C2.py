import csv

permissions = []
groups = []

with open('policy.csv') as csv_file:
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


while True: # user input loop
	print("Input the User, File, and read/write to check privilege!")

	#promt user for input
	sub = input("User: ")
	obj = input("File: ")
	act = input("read/write: ")

	# if user has permission to read/write object 
	if ["p",sub,obj,act] in permissions:
	    print(sub, "has",act, "privilege for",obj)
	elif any(n[1] == sub for n in groups): # if in a group
		for group in groups:
			if group[1] == sub:
				if ["p",group[2],obj,act] in permissions: # if a user's group has the permission...
					print(sub, "has",act, "privilege for",obj,"via",group[2])
				elif any(n[1] == group[2] for n in groups): # if user's group is a subsection of another group
					for g in groups:
						if g[1] == group[2]:
							if ["p",g[2],obj,act] in permissions: # if a user's group has the permission...
								print(sub, "has",act, "privilege for",obj,"via",g[1],"->",g[2])								
							else:
								print(sub, "doen't have",act, "privilege for",obj)
				else:
					print(sub, "doen't have",act, "privilege for",obj)
	else:
	    print(sub, "doen't have",act, "privilege for",obj)

	if input("Continue? (yes/no) ") == "no":
		break 
