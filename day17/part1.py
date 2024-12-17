def parse_input(filename):
    with open(f'day17/{filename}') as f:
        data = f.read().splitlines()
    ra = int(data[0].split()[-1])
    rb = int(data[1].split()[-1])
    rc = int(data[2].split()[-1])
    instructions = list(map(int, data[4].split()[-1].split(',')))
    return ra, rb, rc, instructions

def main(filename):
    data = parse_input(filename)
    ra, rb, rc, instructions = data

    output = []
    ip = 0
    while ip < len(instructions):
        opcode = instructions[ip]
        operand = instructions[ip + 1]
        if operand == 4:
            operand_value = ra
        elif operand == 5:
            operand_value = rb
        elif operand == 6:
            operand_value = rc
        elif operand == 7:
            raise Exception
        else:
            operand_value = operand

        match opcode:
            case 0:
                ra = ra // (2 ** operand_value)
            case 1:
                rb = rb ^ operand
            case 2:
                rb = operand_value % 8
            case 3:
                if ra != 0:
                    ip = operand
                    continue
            case 4:
                rb = rb ^ rc
            case 5:
                output.append(operand_value % 8)
            case 6:
                rb = ra // (2 ** operand_value)
            case 7:
                rc = ra // (2 ** operand_value)
            case _:
                raise Exception('bruh')
        
        ip += 2
    
    return ','.join(str(x) for x in output)

assert main('sample.txt') == '4,6,3,5,6,3,5,2,1,0'
r = main('input.txt')
print(f'answer: {r}')