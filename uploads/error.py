def calculate_average(numbers):

    total = 0

    for i in range(len(numbers)):
        total += numbers[i]

    average = total / len(numbers)

    return average


numbers = []

result = calculate_average(numbers)

print("Average:", result)
