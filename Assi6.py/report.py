def display(students):

    print("\n" + "=" * 65)
    print("                    STUDENT RESULT")
    print("=" * 65)

    print(f"{'Roll':<7}{'Name':<15}{'Total':<10}{'Percentage':<15}{'Grade':<8}{'Rank'}")
    print("-" * 65)

    for s in students:
        print(f"{s[0]:<7}{s[1]:<15}{s[2]:<10}{s[3]:<15.2f}{s[4]:<8}{s[5]}")