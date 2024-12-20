with open('day01/input.txt') as f:
    data = f.read()

c1, c2 = [], []
for line in data.splitlines():
    n1, n2 = line.split()
    c1.append(int(n1))
    c2.append(int(n2))

c1.sort()
c2.sort()

total = sum(abs(n1 - n2) for n1, n2 in zip(c1, c2))
print(total)
