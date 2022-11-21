"""
Flakey Roman K-23
var. 1 4 10
1 - 1-адреса | 1-й операнд завжди в акумуляторі, результат команди заноситься в акумулятор
4 - 18-бітні	
10 - Доповнення до числа у доповнюючому коді за умови що змінюваний операнд не менший за значення у: 
 •	вказаному регістрі для безстекової реалізації;
 •	верхівці стека в стековій реалізації розміщення операндів.
"""

import random;
import sys;
import os;


TACT_WORK = True;




class Processor:
    _BIT_LENGTH = 18;
    _RAM_SIZE = 16;

    @property
    def BIT_LENGTH(self):
        return self.__class__._BIT_LENGTH

    @property
    def RAM_SIZE(self):
        return self.__class__._RAM_SIZE


    @staticmethod
    def to_hex(value):
        return hex(value)[2:].zfill(2)


    @staticmethod
    def from_hex(value):
        return 

    def to_binary(self, value):
        val = abs(value)

        res = [0]*self.BIT_LENGTH
        for i in range(self.BIT_LENGTH-1, -1, -1):
            res[i] = val % 2;
            val //= 2;

        if value >= 0:
            return res

        else:
            return [int(not x) for x in res]

    @staticmethod
    def bin_add(*bin_nums: str) : 
        return bin(sum(int(x, 2) for x in bin_nums))[2:]


    def tact(self):
        if TACT_WORK:
            input("Press Enter to next tact...")


    def _prepare(self, command):
        self._CMD = command;
        self._Ins = [];
        self._PC += 1;
        self._TC = 1;


    def _command_parser(self):
        cmd = self._CMD.strip()

        if cmd.startswith("SET "):
            value = int(cmd[4:])
            self._Ins = ["SET_IN_R1", value]
        
        elif cmd.startswith("DUMP "):
            value = int(cmd[5:])
            self._Ins = ["DUMP_IN_MEM", value]

        elif cmd.startswith("LOAD "):
            value = int(cmd[5:])
            self._Ins = ["LOAD_FROM_MEM", value]
        
        elif cmd.startswith("COPY_MEM "):
            args = cmd[9:]
            addr1, addr2 = map(int, args.split(">", 1))
            self._Ins = ["COPY_MEM", addr1, addr2]

        elif cmd.startswith("COMP "):
            value = int(cmd[5:])
            self._Ins = ["COMPLEMENT", value]

        self._TC += 1
            

    
    def _executer(self):
        cmd = self._Ins[0]
        
        if cmd == "SET_IN_R1":
            self.set_in_register(self._Ins[1])

        elif cmd == "DUMP_IN_MEM":
            self.dump_in_memory(self._Ins[1])
        
        elif cmd == "LOAD_FROM_MEM":
            self.load_from_memory(self._Ins[1])

        elif cmd == "COPY_MEM":
            self.copy_memory(self._Ins[1], self._Ins[2])

        elif cmd == "COMPLEMENT":
            self.complement_operation(self._Ins[1])

        self._TC += 1


    def main_command_procedure(self, command):
        if command.strip() == "" or command.strip().startswith("#"):
            return;

        self._prepare(command);
        self.show();
        self.tact()

        self._command_parser();
        self.show();
        self.tact()

        self._executer();
        self.show();
        self.tact()


    def show(self):
        print("\nCommand:", self._CMD)
        print("\nR1:", "".join(map(str,self._R1)))
        print("Memory:", 
            ".".join(map(self.to_hex, self._RAM.values())),
            ".".join(str(k).zfill(2) for k in self._RAM.keys()), sep="\n    ")

        print("PS:", self._PS, " "*10, "INS:", " | ".join(map(str, self._Ins)))
        print("PC:", self._PC)
        print("TC:", self._TC)


    def set_in_register(self, value):
        self._R1 = self.to_binary(value);


    def dump_in_memory(self, address):
        self._RAM[address] = int(
            "".join(map(str, self._R1)),
            base=2);


    def load_from_memory(self, address):
        self._R1 = self.to_binary(self._RAM[address]);


    def copy_memory(self, address1, address2):
        self._RAM[address2] = self._RAM[address1]


    def complement_operation(self, address):
        A = int("".join(map(str, self._R1)))
        B = self._RAM[address]

        if A>=B:
            D = "".join([str(int(not x)) for x in self._R1])
            
            sum = self.bin_add(D, D).zfill(self.BIT_LENGTH)[-self.BIT_LENGTH:]
            self._R1 = [str(sum)[i] for i in range(self.BIT_LENGTH)]


    def __init__(self):
        self._R1 = random.choices(range(2),k=self.BIT_LENGTH)

        self._RAM = {k:0 for k in range(self.RAM_SIZE)}

        self._CMD = ""
        self._Ins = [];
        self._PS = 0;
        self._PC = 0;
        self._TC = 0;


class WorkProcessor(Processor):
    _BIT_LENGTH = 18;
    _RAM_SIZE = 20;



def main():
    global TACT_WORK
    program_file = None;

    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            program_file = sys.argv[1]
        
        if "-no-tact" in sys.argv:
            print("Tact stoping is off.")
            TACT_WORK = False

    if program_file is None:
        print("File not given. Used default program-file..")
        program_file = "program.txt"

    print("Load program file..")
    with open(program_file) as f:
        program_code = f.read().splitlines()
        f.close()

    print("Loaded program code:", *program_code, sep="\n ")

    print("Create simulation processor..")
    processor = WorkProcessor()
    print("Start program code on created simulation processor..")

    for line in program_code:
        processor.main_command_procedure(line)
    
    print("\nProgram finished.")



main()
