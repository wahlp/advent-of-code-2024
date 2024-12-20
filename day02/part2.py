def check(nums: list[int]):
    diffs = [nums[i+1] - nums[i] for i in range(len(nums) - 1)]

    return (
        (
            all(x > 0 for x in diffs) 
            or all(x < 0 for x in diffs)
        ) 
        and all(1 <= abs(x) <= 3 for x in diffs)
    )


with open('day02/input.txt') as f:
    data = f.readlines()

total = 0
for line in data:
    nums = [int(x) for x in line.split()]

    safe = check(nums)
    if not safe:
        # test removing every level
        alternatives = [
            [nums[j] for j in range(len(nums)) if j != i] 
            for i in range(len(nums))
        ]
        for alt in alternatives:
            alt_safe = check(alt)
            if alt_safe:
                safe = True
                break

    total += safe

print(total)

