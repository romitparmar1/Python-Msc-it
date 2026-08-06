N = str(int(input("Enter The N : ")))

ls = []

for i in N:
    count = N.count(i)

    if count > 1 and i not in ls:
        ls.append(i)
    else:
        continue

print(ls)