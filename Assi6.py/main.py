from student import get_students
from ranking import students_rank
from report import display

students = get_students()

students = students_rank(students)

display(students)