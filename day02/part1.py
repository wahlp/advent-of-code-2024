with open('day02/input.txt') as f:
    data = f.readlines()

total = 0
for line in data:
    nums = [int(x) for x in line.split()]
    diffs = [nums[i+1] - nums[i] for i in range(len(nums) - 1)]

    safe = (
        (
            all(x > 0 for x in diffs) 
            or all(x < 0 for x in diffs)
        ) 
        and all(1 <= abs(x) <= 3 for x in diffs)
    )

    total += safe

print(total)
