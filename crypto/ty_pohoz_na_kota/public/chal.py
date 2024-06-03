from Crypto.Random.random import getrandbits

class LFSR:
    def __init__(self, key, taps):
        d = max(taps)
        assert len(key) == d, "Error: key of wrong size."
        self._s = key
        self._t = [d - t for t in taps]

    def _sum(self, L):
        s = 0
        for x in L:
            s ^= x
        return s

    def _clock(self):
        b = self._s[0]
        self._s = self._s[1:] + [self._sum(self._s[p] for p in self._t)]
        return b

    def bit(self):
        return self._clock()

    def byte(self):
        x = 0
        for i in range(7,-1,-1):
            x^=self.bit()<<i
        return x

key = getrandbits(33)
key = [(key>>i)&1 for i in range(33)]
lfsr = LFSR(key, [33, 32, 30, 27])
flag = "CTF{???}".strip('CTF{}')
assert flag.isascii()

print(bytes(i^lfsr.byte() for i in flag.encode()).hex())
# d1d6b4c617bddb28ab4405a0d8dd801d9b3d6fde58adf49150e6fd3aec5e6bc404