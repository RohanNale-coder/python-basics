# Combined Input and Output Program

# Taking input from user
name = input("Enter your name: ")
age = int(input("Enter your age: "))
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

# Displaying user details
print("\n--- User Details ---")
print("Name:", name)
print("Age:", age)

# Performing calculations
print("\n--- Calculations ---")
print("Addition:", num1 + num2)
print("Subtraction:", num1 - num2)
print("Multiplication:", num1 * num2)

# Division check
if num2 != 0:
    print("Division:", num1 / num2)
else:
    print("Division: Not possible (cannot divide by zero)")

# Showing data types
print("\n--- Data Types ---")
print("Type of name:", type(name))
print("Type of age:", type(age))
print("Type of num1:", type(num1))
