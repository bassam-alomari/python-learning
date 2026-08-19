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


# nested if 

drink = input ("What would you like to drink ? (coffee/tea) : ")

if drink == "coffee":
    sugar=input("Do u want it black or with sugar ? ")

    if sugar=="black":
        print("Black Coffee")
    elif sugar== "With sutgar":
        print("Nice Coffee With Sugar ")
    else:
        print("bad input")

elif drink =="tea":
    type_of_tea=input("Grean tea or Red tea : ")
    if(type_of_tea=="green"):
        print("green tea")
    elif type_of_tea=="red":
        print("red tea")
    else:
        print("bad input")

gender="female"
age=14

if gender=="male":
    print("gender : male ")
    if age<=21:
        print("he is young boy ")

elif gender=="female":
    print("gender : female")
    if age<=21:
        print("She is young girl")

# 17 if & and / or

userName = input("Enter Your userName : ")
password = input("Enter Your password : ")


if userName == "ahmed" and password=="1234":
    print("Login Successful ")
elif userName=="ahmed" or password=="1234":
    print("Almost Correct but one dof the details is wrong ")

else:
    print("wrong userName aand password ")

# | ----------------------------- |

has_invitation=input("Do u have an invitation ? (yes/no) : ")
is_formal=input("Are wearing formal ? (yes/no) : ")

if has_invitation =="yes" and is_formal=="yes":
    print("Welcome")
elif has_invitation=="yes" or is_formal=="yes":
    print("Okay we will let u in ")
else:
    print("Sorry")

# 18 list

# name1="Ahmaed" --> This is wrong
# name2="Ali"    --> This is wrong
# name3="eslam"  --> This is wrong

students = ["ahmed","Ali","Eslam","Mohamed"]

print(students)

grades = [80,20,50,12]
list1 = ["Ahmed",20,1.2]
print("list1 is ",list1)

print("0 index in list1 is ",list1[0])
print("1 index in list1 is ",list1[1])
print("2 index in list1 is ",list1[2])
print("-1 index in list1 is ",list1[-1])
print("-2 index in list1 is ",list1[-2])
print("-3 index in list1 is ",list1[-3])

# 19 Advanced list

# Change item in List

fruits = ["apple","banana","orange"]

print("before ", fruits)

fruits[0] = "Kiwi"

print("After ", fruits)

# fruits[3] = "Kiwi" ---> Error
# print(fruits)

# Tools can be use in list (append/insert/remove) This is functions // & del list

fruits.append("kiwi")

print("After 2 steps ", fruits)

fruits.insert(0,"kiwi") # insert before the index (shift right)

print("After 3 steps ", fruits)

fruits.insert(-1,"kiwi") # insert before the index (shift right)

print("After 4 steps ", fruits)

fruits.remove("kiwi")
print("After 5 steps ", fruits)

del fruits[0]
print("After 5 steps ", fruits)

# pop in lists
fruits.pop
print("After 6 steps ", fruits)

# 20 loops

# print("Hello")
# print("Hello")
# print("Hello")
# print("Hello")
# print("Hello") ------> This is bad Method for large Number of loops


# for in

for i in range(5):
    print(i," Hello")


for i in range(1,11):
    print(i)

word = "python"
for letter in word:
    print(letter)

# This is print 
# p
# y
# t
# h
# o
# n

total = 0

for i in range(1,11):
    total+=i

print("total = ",total)


# while
i=1
while i<=5:
    print("Hello")
    i+=1

print("welcome")

#loops : while
# 0 2 4 6 8 10 : while

i=0
while i<=10:
    print(i)
    i+=2


# for loop with list
names=["Ahmed","Ali","Eslam"]

for n in names:
    print(n)

# break & continue in for loop
for n in names:
    if n == "Ali":
        print("Break The Loop")
        break

for i in range(1,6):
    if i==3:
        continue
    print(i)

i=0
while i<10:
    i+=1
    if i==3:
        continue
    if i==7:
        break
    print("i = ",i)

# 21 Fauctions Part 1

def greet():
    print("Welcome")
    print("bassam")

greet()
greet()

# 21 Fauctions Part 2 : parameter
def sayHello(name,age):
    print("Hello", name)

sayHello("bassam",21)

# 21 Fauctions Part 3 : return

def display():
    print("bassam")
    return("bassam")

name = display()
print(name)

def add(x , y):
    return x+y

result= add(10,20)
print("Result is ",result)
print(result)


# What is the difference between `return` and `print`?

def mult(x,y):
    return x*y

def show(x,y):
    print(x*y)

result1 = mult(12,17) # ٍStore the result in result1

result2 = show(87,23) # ٍStore the None in result2

print("Result return ",result1)
print("Result print ",result2)


# | --------------------------------- |

def get_discount(price):
    return price*0.5

final_price = get_discount(1000)

print(final_price)