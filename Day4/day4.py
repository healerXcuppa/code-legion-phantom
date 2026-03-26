"""Day 4: Boolean Variables and Comparison Operations"""

# Create boolean variables
is_sunny = True
is_raining = False

# Use comparison operators
hot_temp = 30
warm_temp = 20
cold_temp = 10

#printing results of comparisons
print("\nQuestion 1: \n     Is it sunny?\n Answer (Q1):", hot_temp > cold_temp)  # True
print("\nQuestion 2: \n     Is the weather warm?\n Answer (Q2):", warm_temp > cold_temp)  # True
print("\nQuestion 3: \n     Is the weather cold?\n Answer (Q3):", cold_temp < warm_temp)  # True
print("\nQuestion 4: \n     The weather is neither hot or cold\n Answer (Q4):", warm_temp >= cold_temp )  # True

# BONUS: Combine comparisons with and/or
print("\nQuestion 5: \n     Is it sunny and warm?\n Answer (Q5):", is_sunny and warm_temp > cold_temp)  # True
print("\nQuestion 6: \n     Is it raining or cold?\n Answer (Q6):", is_raining or cold_temp < warm_temp)  # True
print("\nQuestion 7: \n     Is it sunny and raining?\n Answer (Q7):", is_sunny and is_raining)  # False
print("\nQuestion 8: \n     Is it sunny or raining?\n Answer (Q8):", is_sunny or is_raining)  # True
print("\nQuestion 9: \n     Is it sunny and not raining?\n Answer (Q9):", is_sunny and not is_raining)  # True