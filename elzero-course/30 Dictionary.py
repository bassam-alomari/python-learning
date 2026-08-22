# Dictionary
# ------------------------
# [1] Dict Items Are Enclosed in Curly Braces
# [2] Dict Items Are Contains Key : Value
# [3] Dict Key Need To Be Immutable => (Number, String, Tuple) List Not Allowed
# [4] Dist Value Can Have Any Data Types
# [5] Dict Key Need To Be Unique
# [6] Dict Is Not Ordered You Access Its Element With Key
# ------------------------

# Dictionary

user = {
   # Dict Key | Dist Value
    "name" : "Bassam",
    "age" : "21",
    "country" : "Joradn",
    # [1,2,3,4] : "Test", Error
    (1,2,3,4) : "Test",
    "skills" : ["HTML", "CSS", "JS"],
    "rating" : "1.5",
}

print(user)
print(user["country"])
print(user.get("country"))

print(user.keys())
print(user.values())

# Two-Dimensional Dictionary /Nested
languages = {
    "One": {
        "name" : "Html",
        "progress" : "80%"
    },
    "Two": {
        "name": "Css",
        "progress": "90%"
    },
    "Three": {
        "name": "Css",
        "progress": "90%"
    }
}
print(languages)
print(languages["One"])
print(languages["One"]["name"])
# Dictionary Length
print(len(languages))
print(len(languages["One"]))

# Create Dictionary From Variables

frameworkOne = {
    "name": "Vuejs",
    "progress": "80%"
}

frameworkTwo = {
    "name": "ReactJs",
    "progress": "80%"
}

frameworkThree = {
    "name": "Angular",
    "progress": "80%"
}

allFramework = {
    "one": frameworkOne,
    "two": frameworkTwo,
    "three": frameworkThree
}

print(allFramework)