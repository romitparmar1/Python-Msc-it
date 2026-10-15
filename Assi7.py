class Course:
    def __init__(self, code, day, start, end):
        self.code = code
        self.day = day
        self.start = start
        self.end = end

    def display(self):
        return f"{self.code} | {self.day} | {self.start} - {self.end}"


class Student:
    def __init__(self, sid, name):
        self.sid = sid
        self.name = name
        self.course_list = []

    def register_course(self, course):
        self.course_list.append(course)

    def show_details(self):
        print("Student ID:", self.sid)
        print("Student Name:", self.name)

        for item in self.course_list:
            print(item.display())

    def find_conflicts(self):
        has_conflict = False
        total = len(self.course_list)

        for x in range(total):
            for y in range(x + 1, total):
                first = self.course_list[x]
                second = self.course_list[y]

                if first.day.lower() == second.day.lower():
                    if (first.start < second.end and
                            second.start < first.end):
                        print(
                            f"Conflict detected: {first.code} "
                            f"and {second.code}"
                        )
                        has_conflict = True

        return has_conflict


def convert_to_minutes(time_value):
    hours, minutes = map(int, time_value.split(":"))
    return hours * 60 + minutes


try:
    total_students = int(input("How many students? "))
    student_records = []

    for number in range(1, total_students + 1):
        print(f"\n--- Student {number} Details ---")

        sid = input("Student ID: ")
        name = input("Student Name: ")

        current_student = Student(sid, name)
        total_courses = int(input("Number of courses: "))

        for index in range(total_courses):
            print(f"\nCourse {index + 1}")

            code = input("Course Code: ")
            day = input("Day: ")
            start = input("Start Time (HH:MM): ")
            end = input("End Time (HH:MM): ")

            start_value = convert_to_minutes(start)
            end_value = convert_to_minutes(end)

            if start_value >= end_value:
                raise ValueError(
                    "The ending time must be later than the starting time."
                )

            new_course = Course(code, day, start, end)
            current_student.register_course(new_course)

        student_records.append(current_student)

    for record in student_records:
        print("\n========== STUDENT REPORT ==========")

        print("Registered Courses:", len(record.course_list))
        print("\nChecking timetable...")

        if record.find_conflicts():
            print("Timetable Status: Invalid")
        else:
            print("No overlapping courses found.")
            print("Timetable Status: Valid")

        print("\nStudent Information:")
        record.show_details()

except ValueError as error:
    print("Input Error:", error)

except Exception as error:
    print("Unexpected Error:", error)