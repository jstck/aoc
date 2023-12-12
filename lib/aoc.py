import sys

def readinput(fp=sys.stdin) -> list[str]:
    #Input lines with surrounding whitespace removed. Use rstrip() if indentation matters.
    input: list[str] = [line.strip() for line in fp.readlines()]

    #Remove any trailing empty lines
    while len(input)>0 and len(input[-1])==0:
        input.pop()

    return input


def chunks(input: list[str]) -> list[list[str]]:
    chunk = []
    chunky = []
    for line in input:
        if len(line) == 0:
            chunky.append(chunk)
            chunk = []
        else:
            chunk.append(line)

    if len(chunk)>0:
        chunky.append(chunk)
    return chunky

