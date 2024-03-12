print(" *** Find 2-smallest even integers ***")
numbers = input("Enter a sequence of integers: ").split()

numbers = [int(num) for num in numbers]

even_numbers = [num for num in numbers if num % 2 == 0]

even_numbers.sort()

if len(even_numbers) < 2:
    print("Insufficient input data")
else:
    print("The smallest even integer is", even_numbers[0])
    print("The second-smallest even integer is", even_numbers[1])


print("===== End of program =====")