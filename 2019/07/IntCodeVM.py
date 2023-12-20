from typing import Iterable
from queue import Queue

class IntCodeVM:

    OP_ADD  =  1
    OP_MULT =  2
    OP_IN   =  3
    OP_OUT  =  4
    OP_BNE  =  5
    OP_BEQ  =  6
    OP_LT   =  7
    OP_EQ   =  8
    OP_HALT = 99

    
    STATE_HALT = OP_HALT        #Reached HALT instruction
    
    STATE_HALT_INPUT = 9903     #Waiting for input
    STATE_HALT_OUTPUT = 9904    #Paused after sending output signal

    STATE_INVALID = 9999        #Invalid opcode reached
    STATE_RUNNING = 1           #Systems are possibly go
    

    OP_UNKNOWN = -1

    #Max I/O buffer size
    BUF_SIZE = 10000

    def __init__(self, memory: Iterable[int], input = [], debug=False):
        self.memory: list[int] = [x for x in memory]
        self.pc: int = 0
        self.flag_debug: bool = debug
        self.output_buffer: Queue[int] = Queue(self.BUF_SIZE)
        self.input_buffer: Queue[int] = Queue(self.BUF_SIZE)
        for i in input:
            self.input_buffer.put_nowait(i)
        self.state: int = IntCodeVM.STATE_RUNNING
        self.flag_halt_output: bool = False


    def has_output(self):
        return not self.output_buffer.empty()
    
    def get_output(self):
        return self.output_buffer.get_nowait()
    
    def halt_output(self, halt):
        self.flag_halt_output = halt


    def debug_print(self, *args):
        if self.flag_debug:
            print(*args)

    def dump(self):
        if not self.flag_debug:
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

        if opcode == IntCodeVM.OP_ADD:
            self.debug_print(self.memory[self.pc-1 : self.pc+3])
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            self.write(c, a+b)
            self.debug_print("ADD (%d%d%d) %d+%d->%d" % (mode1, mode2, mode3, a, b, c))

        elif opcode == IntCodeVM.OP_MULT:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            self.write(c, a*b)
            self.debug_print("MULT (%d%d%d) %d+%d->%d" % (mode1, mode2, mode3, a, b, c))

        elif opcode == IntCodeVM.OP_IN:
            self.debug_print("IN () buf: %s" % (self.input_buffer.qsize()))
            if self.input_buffer.empty():
                #Back up PC to maintain "proper state"
                self.pc -= 1

                self.state = IntCodeVM.STATE_HALT_INPUT

                return self.state

            val = self.input_buffer.get_nowait()
            a = self.read_addr()
            self.write(a, val)

        elif opcode == IntCodeVM.OP_OUT:
            a = self.read_arg(mode1)
            self.output_buffer.put_nowait(a)
            if self.flag_halt_output:
                self.state = self.STATE_HALT_OUTPUT

        elif opcode == IntCodeVM.OP_BNE:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            if(a != 0):
                self.pc = b
        elif opcode == IntCodeVM.OP_BEQ:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            if(a == 0):
                self.pc = b
        elif opcode == IntCodeVM.OP_LT:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            if a < b:
                v = 1
            else:
                v = 0
            self.write(c, v)      
        elif opcode == IntCodeVM.OP_EQ:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr()
            if a == b:
                v = 1
            else:
                v = 0
            self.write(c, v)

        elif opcode == IntCodeVM.OP_HALT:
            self.debug_print("HALT")
            self.pc -= 1 #Don't step here
            self.state = IntCodeVM.STATE_HALT
            return self.state
        else:
            self.pc -= 1
            raise Exception("Unknown opcode: %d, PC=%d" % (opcode, self.pc))

        return opcode

    def add_input(self, x: int):
        self.input_buffer.put_nowait(x)

    def run(self) -> int:
        last_op = 0
        if self.state == IntCodeVM.STATE_HALT_INPUT:
            self.state = IntCodeVM.STATE_RUNNING
        elif self.state == IntCodeVM.STATE_HALT_OUTPUT:
            self.state = IntCodeVM.STATE_RUNNING
            
        while self.state == IntCodeVM.STATE_RUNNING:
            last_op = self.step()

        return self.state
