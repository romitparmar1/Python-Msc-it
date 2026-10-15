password = input("Enter The Password : ")

for char in password:
    if char >= 'A' and char <= 'Z':
        uppercase = True
    elif char >= 'a' and char <= 'z':
        lowercase = True
    elif char >= '0' and char <= '9':
        digit = True
    else:
        special_character = True

uppercase = False
lowercase = False
digit = False
special_character = False
repeat_characters = []

for i in password:

    pas = password.count(i)

    characters_rep = password.index(i)
  
    if pas > 1 and (password[characters_rep] == password[characters_rep + 1]):


        if i not in repeat_characters:

            repeat_characters.append(i)

if not uppercase:
    print("Please enter uppercase letters.")

if not lowercase:
    print("Please enter lowercase letters.")

if not digit:
    print("Please enter digits.")

if not special_character:
    print("Please enter special characters.")

if repeat_characters:
    print("You enter repeated characters.", repeat_characters)