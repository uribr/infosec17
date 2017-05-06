import assemble
import string
import mmap

GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr):
        """
        Construct the GadgetSearch object.

        Input:
            dump_path: The path to the memory dump file created with GDB.
            start_addr: The starting memory address of this dump.
        """
        self.path = dump_path
        self.sa = start_addr

    def get_format_count(self, gadget_format):
        """
        Get how many different register placeholders are in the pattern.
        
        Examples:
            self.get_format_count('POP ebx')
            => 0
            self.get_format_count('POP {0}')
            => 1
            self.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
            => 2
        """
        # Hint: Use the string.Formatter().parse method:
        #   import string
        #   print string.Formatter().parse(gadget_format)
        found = []
        for _, field_name, _, _ in string.Formatter().parse(gadget_format):
            if field_name is not None and field_name not in found:
                found.append(field_name)
        return len(found)

    def get_register_combos(self, nregs, registers):
        """
        Return all the combinations of `registers` with `nregs` registers in
        each combination. Duplicates ARE allowed!

        Example:
            self.get_register_combos(2, ('eax', 'ebx'))
            => [['eax', 'eax'],
                ['eax', 'ebx'],
                ['ebx', 'eax'],
                ['ebx', 'ebx']]
        """
        combinations = list()
        indices = list([0]*nregs)
        number_of_combinations = len(registers) * nregs
        for i in range(number_of_combinations):
            combinations.append(list(['']*nregs))
            for j in range(nregs):
                print('i = ' + str(i) + ' j = ' + str(j))
                combinations[i][j] = registers[indices[j]]
                if j == 0:
                    indices[j] += 1 
                elif indices[j - 1] == nregs:
                    indices[j - 1] = 0
                    indices[j] += 1
        return combinations


            



    def format_all_gadgets(self, gadget_format, registers):
        """
        Format all the possible gadgets for this format with the given
        registers.

        Example:
            self.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
            => ['POP eax; ADD eax, eax',
                'POP eax; ADD eax, ecx',
                'POP ecx; ADD ecx, eax',
                'POP ecx; ADD ecx, ecx']
        """
        # Hints:
        # 1. Use the format function:
        #    'Hi {0}! I am {1}, you are {0}'.format('Luke', 'Vader')
        #    => 'Hi Luke! I am Vader, you are Luke'
        # 2. You can use an array instead of specifying each argument. Use the
        #    internet, the force is strong with StackOverflow.
        nregs = self.get_format_count(gadget_format)
        combinations = self.get_register_combos(nregs, registers)
        gadget_string = [gadget_format]*len(combinations)
        i = 0
        for combo in combinations:
            for regs in zip(*[iter(combo)]*nregs):
                gadget_string[i] = gadget_string[i].format(*regs)
                i += 1
        return gadget_string


    def find_all(self, gadget):
        """
        Return all the addresses of the gadget inside the memory dump.

        Example:
            self.find_all('POP eax')
            => < all ABSOLUTE addresses in memory of 'POP eax; RET' >
        """
        # Notes:
        # 1. Addresses are ABSOLUTE (for example, 0x08403214), NOT RELATIVE to the
        #    beginning of the file (for example, 12).
        # 2. Don't forget to add the 'RET'
        addresses = []
        gadget_opcodes = assemble.assemble_data(gadget+'; RET')
        with open(self.path, "rw+b") as lib_c:
            memmap = mmap.mmap(lib_c.fileno(),0)
            offset = memmap.find(gadget_opcodes)
            while(offset != -1):
                addresses.append(self.sa + offset)

        return addresses

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget) if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        """
        Similar to find_all - but return all the addresses of all
        possible gadgets that can be created with this format and registers.
        Every elemnt in the result will be a tuple of the gadget string and
        the address in which it appears.

        Example:
            self.find_all_formats('POP {0}; POP {1}')
            => [('POP eax; POP ebx', address1),
                ('POP ecx; POP esi', address2),
                ...]
        """
        gadgets = []
        for raw_gadget in format_all_gadgets(self, gadget_format, registers):
            gadgets.append(tuple(raw_gadget, find(raw_gadget)))
        return gadgets

    def find_format(self, gadget_format, registers=GENERAL_REGISTERS, condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr))
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)