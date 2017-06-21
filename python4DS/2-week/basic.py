# list compehension syntax
list_one = [i+1 for i in range(0,5)]
list_two = [i**2 for i in range(0,10)]

print(list_one)
print(list_two)

# dictionary comprehension 
alpha_dict = {i : chr(i) for i in range(65,91)}
print(alpha_dict)
