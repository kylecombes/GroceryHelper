address = input("Address (street, city): ")
state = input("State:")
ingredients = input("List ingredients seperated by commas:")
food_list = ingredients.rsplit(',')
for s in food_list:
    s = s.rstrip(' ')
print(food_list)
