numbers_list = [] 

for n in range(1,6):
    numbers_list.append(int(input("Enter The Number : ")))

print(numbers_list)

for i in range(max(numbers_list) - 1):
    if i not in numbers_list:
        print(i)