students = []

for i in range(3):

    print("\nStudent", i + 1)

    name = input("Enter Name: ")

    subject1 = int(input("Enter Subject 1 Marks: "))
    subject2 = int(input("Enter Subject 2 Marks: "))
    subject3 = int(input("Enter Subject 3 Marks: "))


    total = subject1 + subject2 + subject3

    
    percentage = total / 3

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

    students.append([name, total, percentage, grade])



for i in range(3):
    for j in range(i + 1, 3):

        if students[i][1] < students[j][1]:

            temp = students[i]
            students[i] = students[j]
            students[j] = temp



for i in range(3):

    if i > 0 and students[i][1] == students[i - 1][1]:
        rank = students[i - 1][4]
    else:
        rank = i + 1

    students[i].append(rank)



print(f"{'Rank':<8}{'Name':<15}{'Total':<10}{'Percentage':<15}{'Grade'}")
print("-" * 65)

for student in students:
    print(f"{student[4]:<8}{student[0]:<15}{student[1]:<10}{student[2]:<15.2f}{student[3]}")