class Monkey:

    def __init__(self, chunkymonkey):
        self.monkeynum = int(chunkymonkey[0].split()[1][:-1])
        self.items = [int(x.strip()) for x in chunkymonkey[1].split(":")[1].split(",")]
        self.op = " ".join(chunkymonkey[2].split(":")[1].strip().split()[2:])
        self.divisor = int(chunkymonkey[3].split(":")[1].split()[-1])
        self.throwtrue = int(chunkymonkey[4].split(":")[1].split()[-1])
        self.throwfalse = int(chunkymonkey[5].split(":")[1].split()[-1])

        self.inspected = 0
        self.modulus = 0

    
    def __str__(self):
        return f"""Monkey {self.monkeynum}:
  Items: {", ".join([str(x) for x in self.items])}
  Operation: {self.op}
  Test: div by {self.divisor}
    True: throw to {self.throwtrue}
    False: throw to {self.throwfalse}"""

    def getItem(self, item):
        self.items.append(item)

    def throwShit(self, monkeys):
        for item in self.items:
            self.inspected += 1
            old = item

            new = eval(self.op)

            if self.modulus == 0:
                new = new // 3
            else:
                new = new % self.modulus
            
            if new % self.divisor == 0:
                target = self.throwtrue
            else:
                target = self.throwfalse
            
            monkeys[target].getItem(new)

        self.items = []
