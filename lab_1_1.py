# Задача 1.1
print('Введите три числа: ')
a = int(input())
b = int(input())
c = int(input())
print('Минимальное число:', min(a, b, c))

# Задача 1.2
print('Введите 3 числа: ')
x = int(input())
y = int(input())
z = int(input())
if 1 <= x <= 50: print('Попало под интервал число -', x)
else: print(x, 'не попало под интервал')
if 1 <= y <= 50: print('Попало под интервал число -', y)
else: print(y, 'не попало под интервал')
if 1 <= z <= 50: print('Попало под интервал число -', z)
else: print(z, 'не попало под интервал')

# Задача 1.3
m = float(input('Введите вещественное число m: '))
for x in range(1, 11): print(x*m)

# Задача 1.4
numbers = []  # создаем пустой список для хранения чисел последовательности
num = input("Введите число: ")
while num != "":
    numbers.append(int(num))  # добавляем число в список
    num = input("Введите число: ")

# вычисляем сумму всех чисел в последовательности
sum = 0
i = 0
while i < len(numbers):
    sum += numbers[i]
    i += 1

# вычисляем количество чисел в последовательности
count = len(numbers)

# выводим результаты
print("Сумма всех чисел последовательности: ", sum)
print("Количество чисел в последовательности: ", count)