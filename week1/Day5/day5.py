"""Day 5: Lists and List Operations."""
#Creating List
randoms = ["Fruits","Ghana","Prime","Games","Pineapple"]
#Printing entire List
print(f"\nThe entire list is: {randoms}")
#Printing the first and last item
print(f"\nThe first item in the list is {randoms[0]} and the last item is {randoms[-1]}")
#Adding new item to the list
randoms.append("Brazil")
print(f"\nThis is the new list after adding a new item: {randoms}")
#Removing an item from the list
randoms.remove("Pineapple")
print(f"\nThis is the new list after removing an item: {randoms}")
#Looping through to print each item
for random in randoms:
    print(f"\n{random}")

#Bonus: Creating a nested list
nested_list = [["Fruits", "Ghana"], ["Prime", "Games"], ["Pineapple", "Brazil"]]
print(f"\nThis is the nested list: {nested_list}")