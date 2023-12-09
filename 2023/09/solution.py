def extrapolate_after(x: list[int]) -> int:
    if allzeros(x):
        return 0
    
    return x[-1] + extrapolate_after(differentiate(x))

def extrapolate_before(x: list[int]) -> int:
    if allzeros(x):
        return 0
    
    return x[0] - extrapolate_before(differentiate(x))


def differentiate(x: list[int]) -> list[int]:
    y = []
    for i in range(len(x)-1):
        y.append(x[i+1]-x[i])
    return y

def allzeros(z: list[int]) -> bool:
    for x in z:
        if x != 0:
            return False
    return True

def part1(input: list[str]):
    sum = 0
    for line in input:
        nums = [int(x) for x in line.split()]
        x = extrapolate_after(nums)
        print(nums, x)
        print()
        sum += x
    return sum

def part2(input: list[str]):
    sum = 0
    for line in input:
        nums = [int(x) for x in line.split()]
        x = extrapolate_before(nums)
        print(nums, x)
        print()
        sum += x
    return sum
