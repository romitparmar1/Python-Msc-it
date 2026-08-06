password = input("Enter The Password : ")

uppercase = False
lowercase = False
digit = False
special_character = False
repeated_characters = []

for char in password:
    if char >= 'A' and char <= 'Z':
        uppercase = True
    elif char >= 'a' and char <= 'z':
        lowercase = True
    elif char >= '0' and char <= '9':
        digit = True
    else:
        special_character = True

for i in password:

    pas = password.count(i)
    
    characters_rep = password.index(i)
  
    if pas > 1 and (password[characters_rep] == password[characters_rep + 1]):


        if i not in repeated_characters:

            repeated_characters.append(i)

if not uppercase:
    print("Password not contains uppercase letters.")

if not lowercase:
    print("Password not contains lowercase letters.")

if not digit:
    print("Password not contains digits.")

if not special_character:
    print("Password not contains special characters.")

if repeated_characters:
    print("Password contains repeated characters.", repeated_characters)