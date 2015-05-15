__author__ = 'Jason Yao'
# Import statements
from bin import User
import csv

# The number of days in advance that you'd like to reserve the rooms, default is 60
offsetDays = 60

# Floor number wanted:
floorNumber = 'LL1'

# Room number wanted:
roomNumber = '18'

# Event description name:
description = 'NYU Violets'

loginArray = []

# Start of automated User creation utilizing .csv file
##### NOTE: Make sure that you have a .userLogins.csv file in the same directory as this file.
loginArray = []
with open('userLogins.csv', newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    csvList = list(csvReader)
    totalRows = len(csvList)
    for i in range(1, totalRows):
        userName = csvList[i][1]
        password = csvList[i][2]

# IF YOU DON'T HAVE A .CSV FILE, AND WANT TO MAKE IT HARD ON YOURSELF, UNCOMMENT AND DO IT MANUALLY.
# AND COMMENT OUT THE AUTOMATED .CSV WAY.

# For each valid username/password combo, put below in the form loginArray.append(User('username','password'))
# NOTE: To book a room for 24 hours will require 12 valid people's login information
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 1
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 2
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 3
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 4
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 5
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 6
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 7
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 8
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 9
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 10
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 11
# loginArray.append(User.User('netid', 'examplePassword'))  # Person 12
