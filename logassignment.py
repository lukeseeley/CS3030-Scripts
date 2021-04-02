import sys, re

failedLoginUsers = {}
for i, arg in enumerate(sys.argv):
    if i != 0:
        print(i)
        print(arg)
        f = open(arg, "r")

        for line in f:
            if line.find("Failed password for") >= -1:
                # print(line)
                parts = line.split("Failed ")
                parts = parts[1].split(" ")
                user = ""
                if parts[2] == "invalid":
                    user = parts[4]
                else:
                    user =parts[2]

                #print(user)
                if not user in failedLoginUsers:
                    failedLoginUsers[user] = 1
                else:
                    failedLoginUsers[user] += 1
        f.close()

for user in failedLoginUsers:
    print("User: ", user, "Failed number of attempts: ", failedLoginUsers[user])