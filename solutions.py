from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import random
import math
import re

##############################################################################################################################
############################################## SECTION FETCHING AND ORGANIZING DATA ##########################################
##############################################################################################################################

URL = ".\\website\\python_class_question.html"
data_dictionary = {}
dict_items = []
n = 1

with open(URL, 'r') as content:
    page = ''.join(content.readlines())

soup = BeautifulSoup(page, "html.parser")
data = soup.find_all("td")  # Extract the information of interest from the website

for item in enumerate(data):
    if item[0] % 2 == 0:
        dict_items.append([item[1].text])
    else:
        string = item[1].text
        string_list = pattern = re.compile(r'[A-Z]+').findall(string) # Use of egular expression requirement
        dict_items[item[0]-n].append(string_list)
    n += 1

data_dictionary = dict(dict_items)
data_frame = pd.DataFrame(data_dictionary) # Using pandas for better data representation

print("\n")
print(data_frame)
print("\n")
input("Press enter to continue to mean...")

##############################################################################################################################
################################################### SECTION FOR FINDING MEAN #################################################
##############################################################################################################################
def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

sum_of_numeric_weights = 0

data_frame_numeric = data_frame.copy()
unique = set()
for head in data_frame_numeric.head():
    for color in data_frame_numeric[head]:
        unique.add(color)
unique = list(unique) # Stores the unique colors in a list so that we can represent them by numeric values which will be (index position + 1). This numerical value will enable us to perform mathematical operations on the data such as mean

for head in data_frame_numeric.head():
    new_column = []
    for color in data_frame_numeric[head]:
        new_column.append(unique.index(color) + 1)  
    data_frame_numeric[head] = new_column    # replace the colors in the data frame with their numeric values for easy computation

print("\n","---"*50)
print("NUMERIC REPRESENTATION OF COLORS USED FOR CALCULATING MEAN\n")
for i in unique:
    print(f"TAKING {i} as {unique.index(i)+1}", end=" | ") # Display the numeric value that has been assigned to each color
    sum_of_numeric_weights += unique.index(i)+1
print("\n","---"*50)
print("\n\n")

print("---"*50)
for head in data_frame_numeric.head():
    add = 0
    for i in data_frame_numeric[head].unique():
        add += i*countX(data_frame_numeric[head], i) # Σfx
    print(f"MEAN OF COLORS WORN ON {head} IS: {unique[round(add/len(data_frame_numeric[head])) - 1]}")         # Σfx/Σf
print("\n")
print("---"*50, "\n")

input("Press enter to continue to mode...")
##############################################################################################################################
################################################### SECTION FOR FINDING MODE #################################################
##############################################################################################################################
print("\n", "---"*50, "\n")
print(f"The color worn mostly throughout the week is:\n")
print(data_frame.mode())

input("Press enter to continue to median...")

##############################################################################################################################
################################################### SECTION FOR FINDING MEDIAN ###############################################
##############################################################################################################################
print("\n", "---"*50, "\n")
print(f"The median color is:\n")
median = round(data_frame_numeric.median())-1
for head in data_frame_numeric.head():
    print(head,"is", unique[round(median[head])-1])

input("Press enter to continue to variance...")

##############################################################################################################################
################################################### SECTION FOR FINDING variance ###############################################
##############################################################################################################################
print("\n", "---"*50, "\n")
print(f"The variance is:\n")
print(data_frame_numeric.var())

input("Press enter to continue to probablility...")

##############################################################################################################################
################################################### SECTION FOR FINDING PROBABILITY ############################################
##############################################################################################################################
red_count = 0
for head in data_frame.head():
    red_count += countX(data_frame[head], "RED")
print("\nThe probability of obtaining a red is: {:.2f} or {:.2f}%".format(red_count/data_frame.size, (red_count/data_frame.size)*100))

##############################################################################################################################
########################################### SECTION FOR INSERTING FREQUENCIES INTO DATABASE ##################################
##############################################################################################################################
frequencies = {}
for head in data_frame.head():
    for color in data_frame[head]:
        if color in frequencies:
            frequencies[color] += 1
        else:
            frequencies[color] = 1

connection = psycopg2.connect(
    database="bincom",
    user="postgres",
    password="test8910",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

for color in frequencies:
    cursor.execute(f"INSERT INTO details(colours,frequencies)values({color},{frequencies[color]})")
connection.commit()

print("\nCOLOURS AND FREQUENCIES SAVED IN DATABASE")

##############################################################################################################################
########################################### SECTION FOR RECURSIVE SEARCHING ALGORITHM ######################################
##############################################################################################################################

def binary_search(numbers, search_value, start_index, end_index):
    if start_index > end_index:
        return f"{search_value} is NOT present in the list"
    else:
        mid_index = (start_index + end_index)//2
        mid_value = numbers[mid_index]
        if mid_value == search_value:
            return f"{search_value} is present in the list"
        elif mid_value > search_value:
            return binary_search(numbers, search_value, start_index, mid_index-1)
        else:
            return binary_search(numbers, search_value, mid_index+1, end_index)

print("\n", "---"*50, "\n")
numbers = input("Enter a series of numbers separated by comma [e.g 2,3,5,6]: ").split(",")
search_value = int(input("Enter the number you are searching for: "))

numbers_integer = []
for i in numbers:
    numbers_integer.append(int(i))

print("LIST", numbers)
print(binary_search(numbers_integer, search_value, 0, len(numbers_integer)-1))
print("---"*50, "\n")
input("\nPress enter to continue to base conversion...")


##############################################################################################################################
########################################### SECTION FOR CONVERTING TO BASE 10 ###############################################
############################################################################################################################## 
add = 0
binary = ""
position = 3
for i in range(4):
    number = random.randint(0,1)
    binary += str(number)
    add += number*(2**position)
    position -=1

print("\n", "---"*50, "\n")
print(f"\nBINARY FORM: {binary}")
print(f"DECIMAL FORM {add}")
print("\n", "---"*50, "\n")

input("Press enter to continue to fibonacci sequence...\n")

##############################################################################################################################
########################################### SECTION FOR CONVERTING TO BASE 10 ###############################################
######################################################################################################################


a, b = 0, 1
count = 0
add = 0
while count < 50:
    add += a
    c = a + b
    a = b
    b = c
    count += 1
print("---"*50, "\n")
print(f"The sum of the first 50 fibonacci sequence is: {add}")
print("\n", "---"*50, "\n")