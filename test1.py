print(" *** Common Divisor Summation ***")
numbers = input("Enter n1 n2: ").split()

numbers = [int(num) for num in numbers]

num1, num2, num3 = numbers

divisors = []
for i in range(1, max(num1, num2, num3) + 1):
    if num1 % i == 0 and num2 % i == 0 and num3 % i == 0:
        divisors.append(i)

sum_of_divisors = sum(divisors)

print(*divisors)
print("Sum = ", sum_of_divisors)
print(" ===== End of program =====")
