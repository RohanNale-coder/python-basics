
# Input and Output in Python

# Program 1: Greeting Program
name = input("Enter your name: ")
print(f"Hello, {name}! Welcome to Python.")



# Program 2: Add Two Numbers
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
sum = num1 + num2
print(f"Sum of {num1} and {num2} is {sum}")



# Program 3: Calculate Percentage
marks1 = int(input("Enter marks of subject 1: "))
marks2 = int(input("Enter marks of subject 2: "))
marks3 = int(input("Enter marks of subject 3: "))

total = marks1 + marks2 + marks3
percentage = (total / 300) * 100

print(f"Total Marks: {total}")
print(f"Percentage: {percentage}%")


# Program 4: Voting Eligibility
age = int(input("Enter your age: "))

if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")


# Program 5: Area of Rectangle
length = float(input("Enter length: "))
breadth = float(input("Enter breadth: "))

area = length * breadth
print(f"Area of Rectangle: {area}")
