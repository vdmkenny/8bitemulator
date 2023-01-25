class Z80:
    def __init__(self):
        # Create internal registers as properties
        self.A = 0x00
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00
        self.PC = 0x0000
        self.SP = 0x0000
        self.F = 0x00
        
    def ld_a_n(self, n):
        self.A = n
        
    def ld_a_b(self):
        self.A = self.B
        
    def add_a_n(self, n):
        self.A += n
        
    def add_a_b(self):
        self.A += self.B
        
    # Implement other opcodes as methods
    
    # ...
