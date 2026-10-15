paragraph = input("Enter The Paragrraph : ")

unique = []
repeated = []

words = paragraph.split()

print("List : ",words)

print("Total Number Of Words : ",len(words))

for i in words:
    count = words.count(i)
    if not count > 1 and i not in unique:
        unique.append(i)

print("Total Unique Words : ",unique)
print("Total Unique Words : ",len(unique))

maxNum = words[0]
maximumWord = ""

for i in words:
    # print(len(i))
    if len(i) >= len(maxNum):
        maxNum = i
        maximumWord = maxNum

print("Longest Word : ",maximumWord)


minWord = words[0]
sortestsWord = ""
for j in words:
    if len(j) <= len(minWord):
        minWord = j
        sortestsWord = minWord

print("Sortest Word : ",sortestsWord)

for k in words:
    count = words.count(k)

    if count > 1 and k not in repeated:
        repeated.append(k)

print(repeated)
print("Repeated Word : ",len(repeated))