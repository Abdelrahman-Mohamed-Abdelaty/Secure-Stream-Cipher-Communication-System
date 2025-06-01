class LCG:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a 
        self.c = c  
        self.m = m 

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    def generate_keystream(self, length):
        stream = [self.next() % 256 for _ in range(length)]
        print(f"[LCG] Keystream generated: {stream}")
        return stream
