class vm:

    OP_ADD = 1
    OP_MULT = 2
    OP_HALT = 99

    OP_UNKNOWN = -1

    def __init__(self, memory, debug=False):
        self.memory = [x for x in memory]
        self.pc = 0
        self.debug = debug

    def debug_print(self, *args):
        if self.debug:
            print(*args)


    def read_op(self):
        m = self.memory[self.pc]
        self.pc += 1
        return m

    def read(self, addr):
        return self.memory[addr]

    def write(self, addr, val):
        self.memory[addr] = val

    def step(self):
        opcode = self.read_op()

        if opcode == vm.OP_ADD:
            a = self.read_op()
            b = self.read_op()
            c = self.read_op()
            self.write(c, self.read(a)+self.read(b))
            self.debug_print("ADD", a, b, c)
        elif opcode == vm.OP_MULT:
            a = self.read_op()
            b = self.read_op()
            c = self.read_op()
            self.write(c, self.read(a)*self.read(b))
            self.debug_print("MULT", a, b, c)
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
