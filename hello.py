# printing statement cause this is the fundamental of python programming
# Activity 1 and Activity 2
print("==============================================")
print("Welcome here")
print("My first post!")
print("==============================================")

# create a variable and assign a value to it
username = "cool_creator"
bio = "I am a Python enthusiast and love to code!"
followers = 1500

print("Username:", username)
print("Bio:", bio)
print("Followers:", followers)

# Activity 3
# Follower Growth Tracker
followers += 50
print("Updated Followers day 1:", followers)

followers += 20
print("Updated Followers day 2:", followers)

followers -= 10
print("Updated Followers day 3:", followers)

# Activity 4 & 5
newusername = input("Enter your new username: ")
age = int(input("Enter your age: ")) #int() pass as int because age is a number and we need to compare it with 40yo
category = input("Enter Content Category: ")

print("==============================================")
print("\nProfile Summary:") #linebreak amazing lol
print("Username:", newusername)
print("Age:", age)
print("Content Category:", category)

if age > 40 and category.lower() == "fun": # also age needs to be in int because i like small case letters
    print("You are old what is fun for you??")
