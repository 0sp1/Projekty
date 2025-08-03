numbers = [i for i in range(2,1001)]
prime = []
for number in numbers:
    for x in range(2, number+1):
        if number%x == 0:
            break
    prime.append(number)
        
print(prime)