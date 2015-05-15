__author__ = 'Jason Yao'
# Import statements
from bin import User

# The number of days in advance that you'd like to reserve the rooms, default is 60
offsetDays = 60

# Floor number wanted:
floorNumber = 'LL1'

# Room number wanted:
roomNumber = '18'

# Event description name:
description = 'NYU Violets'

loginArray = []
# For each valid username/password combo, put below in the form loginArray.append(User('username','password'))
# NOTE: To book a room for 24 hours will require 12 valid people's login information
loginArray.append(User.User('netid', 'examplePassword'))  # Person 1

# Note: Just uncomment the ones below to match the number of people
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

