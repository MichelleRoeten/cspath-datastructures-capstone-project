from trie import RestaurantSearchEngine
from data import *
from welcome import *
#from hashmap import HashMap
from linkedlist import LinkedList

exit_character = "#"

type_of_food_prompt = """
What type of food would you like to eat?
Type the beginning of that food type and
press enter to see if it's here.  Enter
{0} to exit if you are all done searching.\n
""".format(exit_character)

types_located_message = """
We located the following types of food:
"""

type_selection_prompt = """
If you would like to display one of these,
please enter the number to the left of it.
Any other response will bring you back to
the beginning.\n
"""

not_found_message = """
We could not locate any food types starting
with {0}.  Please try something else.
"""

exit_message = """
Have a nice day, hope to see you again soon!
"""

#Printing the Welcome Message
print_welcome()

#Write code to insert food types into a data structure here. The data is in data.py
soho_restaurants = RestaurantSearchEngine()
for type in types:
    soho_restaurants.add_type(type)

#Write code to insert restaurant data into a data structure here. The data is in data.py
for restaurant in restaurant_data:
    soho_restaurants.add_restaurant(restaurant)

#Write code for user interaction here
while True:
    user_input = str(input(type_of_food_prompt)).lower()
    if user_input == exit_character:
        print(exit_message)
        break
    
    # Search for user_input in food types data structure here
    restaurant_types = soho_restaurants.get_words(user_input)
    option_number = 0
    selector = {}
    for restaurant in restaurant_types:
        option_number += 1
        if option_number < 10:
            padding = ' '
        else:
            padding = ''
        if option_number == 1:
            print(types_located_message)
        print('{0}{1} {2}'.format(padding, option_number, restaurant))
        selector[str(option_number)] = restaurant

    # After finding food type write code for retrieving restaurant data here
    if selector == {}:
        print(not_found_message.format(user_input))
    else:
        user_input = str(input(type_selection_prompt))

    selected_type = selector.get(user_input)
    if selected_type != None:
        soho_restaurants.display_restaurants(selected_type)

        

    











