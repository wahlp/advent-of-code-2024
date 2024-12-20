with open('day01/input.txt') as f:
    data = f.read()

c1, c2 = [], []
for line in data.splitlines():
    n1, n2 = line.split()
    c1.append(int(n1))
    c2.append(int(n2))

total = 0
for num in c1:
    total += num * c2.count(num)

print(total)
