def transpose(lst: list[list[str]]):
    return [''.join(x) for x in zip(*lst)]


def mirror(lst: list[list[str]]):
    return [''.join(reversed(x)) for x in lst] 


def get_45deg_2d_list(lst: list[list[str]]):
    unused_char = ' '
    new_lst = []
    for i, row in enumerate(lst):
        new_row = ''.join([
            *[unused_char for _ in range(i)],
            row,
            *[unused_char for _ in range(len(lst) - i)]
        ])
        new_lst.append(new_row)
    
    new_lst = [row.replace(unused_char, '') for row in transpose(new_lst)]
    return new_lst


with open('day4/input.txt') as f:
    data = f.read().splitlines()

# strategy: reorient the data into every permutation of angle to check
data_rotated_90 = [''.join(x) for x in zip(*data)]
data_rotated_45 = get_45deg_2d_list(data)
data_rotated_45_mirrored = get_45deg_2d_list(mirror(data))
angles = [
    data,
    mirror(data),
    data_rotated_90,
    mirror(data_rotated_90),
    data_rotated_45,
    mirror(data_rotated_45),
    data_rotated_45_mirrored,
    mirror(data_rotated_45_mirrored)
]

total = 0
for grid in angles:
    count = sum(row.count('XMAS') for row in grid)
    total += count
print(total)