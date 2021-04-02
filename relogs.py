import sys, re  

# line = "Let's trick ourselves into thinking that we can make alternative facts become a trending topic in social media"

# matches = re.match(r'.*trick (.*) into.* in (.*) media', line, re.M|re.I)

# if matches:
#     print("We found:", matches.group(1), "and", matches.group(2))
# else:
#     print("We did not find any match")

sessions = {}
for i, arg in enumerate(sys.argv):
    if i != 0:
        #print(i)
        #print(arg)
        f = open(arg, "r")

        for line in f:
            matches = re.match(r'.*sshd\[(.*)\]: (Failed|Accepted) (password for |none for )(invalid user)?(.*?) from.*', line, re.I)
            if matches:
                #print("We found: ", matches.group(1), ", ", matches.group(2), ", ", matches.group(5))
                sessionId = matches.group(1)
                if not sessionId in sessions:
                    sessions[sessionId] = [matches.group(5), matches.group(2)] #Username, failed/accepted, count
                else:
                    sessions[sessionId][1] = matches.group(2)
                    sessions[sessionId][2] += 1
            # else:
            #     print("No matches found")
        f.close()

for key in sessions:
    print("For session ID: ", key, "we have values: ", str(sessions[key]))