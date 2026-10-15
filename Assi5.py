students = []

for i in range(4):

    print("\nStudent", i + 1)

    Roll = input("Enter Rollno. = ")

    name = input("Enter Name: ")

    sub1 = int(input("Enter subject 1 marks= "))
    sub2 = int(input("Enter subject 2 marks= "))
    sub3 = int(input("Enter subject 3 marks= "))
    sub4 = int(input("Enter subject 4 marks= "))
    sub5 = int(input("Enter subject 5 marks= "))

    total = sub1+sub2+sub3+sub4+sub5

    percentage = total / 5

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    students.append([Roll, name, total, percentage, grade])



for i in range(4):
    for j in range(i + 1, 4):

       if students[i][2] < students[j][2]:

            temp = students[i]
            students[i] = students[j]
            students[j] = temp



for i in range(4):

    if i > 0 and students[i][2] == students[i - 1][2]:
        rank = students[i - 1][5]
    else:
        rank = i + 1

    students[i].append(rank)



print(f"{'Roll':<7}{'Name':<15}{'Total':<10}{'Percentage':<15}{'Grade':<8}{'Rank'}")
print("-" * 63)

for student in students:
    print(f"{student[0]:<7}{student[1]:<15}{student[2]:<10}{student[3]:<15.2f}{student[4]:<8}{student[5]}")