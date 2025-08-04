numbers = [4]
prime = []

for number in numbers:
    if number < 2:
        continue  # Skip numbers less than 2 (not prime)
    is_prime = True
    for x in range(2, int(number ** 0.5) + 1):
        if number % x == 0:
            is_prime = False
            break
    if is_prime:
        prime.append(number)

print(prime)
