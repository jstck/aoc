from typing import Iterable
from queue import Queue
from collections import defaultdict

class IntCodeVM:

    OP_ADD  =  1
    OP_MULT =  2
    OP_IN   =  3
    OP_OUT  =  4
    OP_BNE  =  5
    OP_BEQ  =  6
    OP_LT   =  7
    OP_EQ   =  8
    OP_BASE =  9
    OP_HALT = 99

    opcodes = {
        OP_ADD  :  "ADD",
        OP_MULT :  "MULT",
        OP_IN   :  "IN",
        OP_OUT  :  "OUT",
        OP_BNE  :  "BNE",
        OP_BEQ  :  "BEQ",
        OP_LT   :  "LT",
        OP_EQ   :  "EQ",
        OP_BASE :  "BASE",
        OP_HALT :  "HALT",
    }

    
    STATE_HALT = OP_HALT        #Reached HALT instruction
    
    STATE_HALT_INPUT = 9903     #Waiting for input
    STATE_HALT_OUTPUT = 9904    #Paused after sending output signal

    STATE_INVALID = 9999        #Invalid instruction reached
    STATE_RUNNING = 1           #Systems are possibly go
    

    OP_UNKNOWN = -1

    #Max I/O buffer size
    BUF_SIZE = 10000

    def __init__(self, memory: Iterable[int], input = [], debug=False):
        self.memory: defaultdict[int,int] = defaultdict(lambda: 0)
        for addr, val in enumerate(memory):
            self.memory[addr] = val
        self.pc: int = 0
        self.flag_debug: bool = debug
        self.output_buffer: Queue[int] = Queue(self.BUF_SIZE)
        self.input_buffer: Queue[int] = Queue(self.BUF_SIZE)
        for i in input:
            self.input_buffer.put_nowait(i)
        self.state: int = IntCodeVM.STATE_RUNNING
        self.flag_halt_output: bool = False
        self.base: int = 0


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
        #if not self.flag_debug:
        #    return

        print("PC:", self.pc)
        print("Base:", self.base)
        print("State:", self.state)
        print("Input buffer:", ",".join(map(str,self.input_buffer.queue)))
        print("Output buffer:", ",".join(map(str,self.output_buffer.queue)))
        print("Memory:")
        for addr, val in self.memory.items():
            start, end = '', ''
            if addr == self.pc:
                start = '\033[96m'
                end   = '\033[0m <-PC'

            print("%s%03d: %d%s" % (start, addr, val, end))
        print()

    def read_op(self):
        assert self.pc >= 0, f"Invalid PC: {self.pc}"

        opcode = self.memory[self.pc]

        op = opcode%100
        mode1 = (opcode // 100) % 10
        mode2 = (opcode // 1000) % 10
        mode3 = (opcode // 10000) % 10
        assert op in IntCodeVM.opcodes, f"Unknown op: {op} (from {opcode} @ {self.pc})"

        self.pc += 1
        
        return (op, mode1, mode2, mode3)

    def read_arg(self, mode=0):
        a = self.memory[self.pc]
        self.pc += 1
        if mode == 0:
            #position mode
            return self.memory[a]
        elif mode == 1:
            #immediate mode
            return a
        elif mode == 2:
            #relative mode
            return self.memory[a+self.base]
        assert False, f"Invalid argument mode: {mode}"

    def read_addr(self, mode=0):
        a = self.memory[self.pc]
        self.pc += 1
        if mode == 0:
            #position mode
            #return self.memory[a]
            return a
        elif mode == 2:
            #relative mode
            return self.base+a
        assert False, f"Invalid address mode: {mode}"

    def read(self, addr):
        assert addr>=0, f"Invalid address: {addr}"
        return self.memory[addr]

    def write(self, addr, val):
        assert addr>=0, f"Invalid address: {addr}"
        self.memory[addr] = val

    def step(self):
        (opcode, mode1, mode2, mode3) = self.read_op()
        self.debug_print("OP: ", IntCodeVM.opcodes[opcode])

        if opcode == IntCodeVM.OP_ADD:
            #self.debug_print(self.memory[self.pc-1 : self.pc+3])
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr(mode3)
            self.write(c, a+b)
            self.debug_print("ADD (%d%d%d) %d+%d->%d" % (mode1, mode2, mode3, a, b, c))

        elif opcode == IntCodeVM.OP_MULT:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr(mode3)
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
            a = self.read_addr(mode1)
            self.write(a, val)

        elif opcode == IntCodeVM.OP_OUT:
            a = self.read_arg(mode1)
            self.debug_print("OUT: %d" % (a,))
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
            c = self.read_addr(mode3)
            if a < b:
                v = 1
            else:
                v = 0
            self.write(c, v)      
        elif opcode == IntCodeVM.OP_EQ:
            a = self.read_arg(mode1)
            b = self.read_arg(mode2)
            c = self.read_addr(mode3)
            if a == b:
                v = 1
            else:
                v = 0
            self.write(c, v)

        elif opcode == IntCodeVM.OP_BASE:
            a = self.read_arg(mode1)
            self.base += a
            self.debug_print("BASE (%d) %d -> %d" % (mode1, a, self.base))


        elif opcode == IntCodeVM.OP_HALT:
            self.debug_print("HALT")
            self.pc -= 1 #Don't step here
            self.state = IntCodeVM.STATE_HALT
            return self.state
        else:
            self.pc -= 1
            raise Exception("Unhandled opcode: %d, PC=%d" % (opcode, self.pc))
        
        if self.flag_debug:
            self.dump()
            print()

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
