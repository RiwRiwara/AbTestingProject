# wiboon 10 kanut 20 parinya 25
data = input("Enter name and age : ").split()
print(data)
result_dict = {}

for i in range(0, len(data), 2):
    name = data[i]
    age = int(data[i + 1])
    result_dict[name] = age
print(result_dict)

tuple_result = [(value, key) for key, value in result_dict.items()]
print(tuple_result)

tuple_result.sort(reverse=True)
print(tuple_result)

print("*** The Histogram of Age ***")
for age, name in tuple_result:
    print(f"{name[0:3]} : {'=' * age}")