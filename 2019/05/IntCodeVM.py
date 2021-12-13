class vm:

    OP_ADD  =  1
    OP_MULT =  2
    OP_IN   =  3
    OP_OUT  =  4
    OP_BNE  =  5
    OP_BEQ  =  6
    OP_LT   =  7
    OP_EQ   =  8
    OP_HALT = 99

    OP_UNKNOWN = -1

    def __init__(self, memory, input = [], debug=False):
        self.memory = [x for x in memory]
        self.pc = 0
        self.debug = debug
        self.output_buffer = []
        self.input_buffer = input

    def debug_print(self, *args):
        if self.debug:
            print(*args)

    def dump(self):
        if not self.debug:
            return

        for i in range(0, len(self.memory)):
            start, end = '', ''
            if i == self.pc:
                start = '\033[96m'
                end   = '\033[0m'

            print("%s%03d: %d%s" % (start, i, self.memory[i], end))
        print()


    def read_op(self):
        op = self.memory[self.pc]
        self.pc += 1

        mode1 = (op // 100) % 10
        mode2 = (op // 1000) % 10
        mode3 = (op // 10000) % 10
        return (op%100, mode1, mode2, mode3)

    def read_arg(self, mode=0):
        a = self.memory[self.pc]
        self.pc += 1
        if mode == 0:
            #position mode
            return self.memory[a]
        else:
            #immediate mode
            return a

    def read_addr(self):
        a = self.memory[self.pc]
        self.pc += 1
        return a

    def read(self, addr):
        return self.memory[addr]

    def write(self, addr, val):
        self.memory[addr] = val

    def step(self):
        (opcode, mode1, mode2, mode3) = self.read_op()

        if opcode == vm.OP_ADD:
            self.debug_print(self.memory[self.pc-1 : self.pc+3])
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            self.write(c, a+b)
            self.debug_print("ADD (%d%d%d) %d+%d->%d" % (mode1, mode2, mode3, a, b, c))

        elif opcode == vm.OP_MULT:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            self.write(c, a*b)
            self.debug_print("MULT (%d%d%d) %d+%d->%d" % (mode1, mode2, mode3, a, b, c))

        elif opcode == vm.OP_IN:
            val = self.input_buffer.pop(0)
            a = self.read_addr()
            self.write(a, val)
        elif opcode == vm.OP_OUT:
            a = self.read_arg(mode1)
            self.output_buffer.append(a)

        elif opcode == vm.OP_BNE:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            if(a != 0):
                self.pc = b
        elif opcode == vm.OP_BEQ:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            if(a == 0):
                self.pc = b
        elif opcode == vm.OP_LT:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            if a < b:
                v = 1
            else:
                v = 0
            self.write(c, v)      
        elif opcode == vm.OP_EQ:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            if a == b:
                v = 1
            else:
                v = 0
            self.write(c, v)

        elif opcode == vm.OP_HALT:
            self.debug_print("HALT")
            self.pc -= 1 #Don't step further
        else:
            self.pc -= 1
            raise Exception("Unknown opcode: %d, PC=%d" % (opcode, self.pc))

        return opcode

    def run(self):
        last_op = 0
        while last_op != vm.OP_HALT:
            last_op = self.step()
