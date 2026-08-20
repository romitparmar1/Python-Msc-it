def get_students():

    students = []

    n = int(input("Enter number of students: "))

    for i in range(n):

        roll = int(input("\n  Enter Roll No: "))
        name = input("Enter Name: ")

        marks = []

        for j in range(5):
            mark = int(input("Enter marks of Subject " + str(j + 1) + ": "))
            
            while mark < 0 or mark > 100:
                print("Marks should be between 0 and 100.")
                mark = int(input("Enter marks again: "))
                
            marks.append(mark)

        total = sum(marks)
        percentage = total / 5

        if percentage >= 90:
            grade = "A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"

        students.append([roll, name, total, percentage, grade ])

    return students