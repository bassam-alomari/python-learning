# 1
print("Bassam Alomari") # must include "" or '' in ()
print('Bassam Alomari') # must include "" or '' in ()
print("Hello")

#  tricks
# space + print('Bassam Alomari') = Error

# 2
print('*') # Dont Use This    
print('**') # Dont Use This
print('***') # Dont Use This
print('****') # Dont Use This
print('*****') # Dont Use This

# 3
name = "Bassam Alomari" # This is str
name1 = 'Bassam Alomari' # This is str
print(type(name),type(name1))
print(name)

# print(name2) Error
# name = "ahmad"

# 4
name11 = "bassam"
print(name11)

# Var cant start with Num
# Var cant use spaces -> use only _

gradeOfStd = 1
print(gradeOfStd)

# 5
#int
age=3

print(age)

#float
gpa = 3.4
print(gpa)

#string
name = "bassam"

# 6
Name = "bassam"
age = 20
print("Hello " + Name) # Correct
# print("Hello " + age) Error because you cant sum str to int But You Can
print("Hello",age) # This is Correct

qoute = " \"bassam alomari\" " # or use ' ' 
print(qoute)

print("hello my name is bassam")
print("hello\n my name is bassam") # \n -> new line

my_int = 1
my_float = 1.1

print(my_int + my_float) # 1 + 1.1 = 2.1

# 7
# + - * /
print(20+1-2*17/2)
num1=20
num2= 30
sum = num1 + num2
print(sum)

# Modulus %

# same % same 
mod1 = 10%10
print(mod1)

# small % big = small
mod2 = 10%20
print(mod2)

# big % small = big-small many times
mod3 = 10%4
print(mod3)

# 8
age=21
print("my age is " + str(age)) # Correct
# str() Convert any vaar type to string

print(type(age)) # Show Var Type

# This is only apply on string
name = "basssam alomari"
print(name.upper()) # use this for convert lower case to upper case
print("bassam".upper()) # This is True
print(name)

nameU= "BASSAM ALOMARI"
print(name.lower()) # use this for convert upper case to lower case
print("bassam".lower()) # This is True

print(name.capitalize()) # this is make first char capital only in first word
print(name.title()) # this is make first char capital only in all words
print(name.title().lower()) # last is high proirty


# 9
name = input("enter your name : ") # this use for input
# any input type convert too str after 
print("Your name is: " + name)

age=int(input("enter your age : ")) # this use for input
# this is input is int
print(20 + age)


# 10 Calc App



# 11 Comparison operations

#bolean : True or False
# == 
result = (10==11)
print(result)
# != 
result = (10!=11)
print(result)

# < 
result = (10<11)
print(result)
# > 
result = (10>11)
print(result)

# <=
result = (10<=11)
print(result)
# >=
result = (10<=11)
print(result)

# 12 Shortcuts Comparison operations
x = 10
x+=10
x+=10
x+=20
x-=7
x*=7
x/=7
x%=7

# 13 Lgical Operators
# and or

# and : true
x=10
y=11
print(x<y and 0>1)
print(x<y or 0>1)
print(not True)
print(not(10<2))

# 14 if elif

name="bassam"
if name=="bassam": #Error if you dont use :
    print("your name is bassam")
elif name=="mohammad": #Error if you dont use :
    print("your name is mohammad")
else: #Error if you dont use :
    print("sorry")

# 15 Advanced Calculator App


# 16 nested if
# Idea: condition inside a condition - if inside if
# After the first condition is met, we check a second condition inside it

name = "bassam"
age = 21

if name == "bassam":      # First condition
    print("your name is bassam")
    if age >= 18:         # Nested if - second condition inside the first
        print("and you are adult")
    else:
        print("and you are under 18")
else:
    print("sorry")

# Note: Focus on indentation - it determines which code is inside which block

# -------------------------------
# Challenge 16: Write below this line
# Program asks for: name + age
# - If name is bassam and age >= 18 → print: welcome bassam
# - If name is bassam and age < 18 → print: you are underage
# - If name is not bassam → print: who are you?
# (Use input + int + nested if - write it yourself, then we check together)
# -------------------------------
name = input("Enter Your Name : ")
age = int(input("Enter Your Age : "))
if name == "bassam":
    if age>=18:
        print("Welcome Bassam")
    else:
        print("You Are Underage")
else:
    print("Who Are You ?")        