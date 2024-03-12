def f(num):
    sum = 0
    while num > 0:
        sum += num % 10
        num //= 10
    return sum

def partity(num):
    if num % 2 == 0:
        return "EVEN"
    else:
        return "ODD"

print(" *** Sum and ODD/EVEN ***")
text = input("Enter a number : ")
num = int(text)
print(f"Sum of each digits => {f(num)} => {partity(f(num))}")