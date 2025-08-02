numbers = [i for i in range(2,1001)]
prime = []
for number in numbers:
    for x in range(1, number):
        if number%x == 0:
            prime.append(number)
        
print(prime)