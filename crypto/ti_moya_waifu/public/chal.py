from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import generator_256, Public_key, Private_key
from random import randint

G = generator_256
q = G.order()

FLAG = b'CTF{?????????????}'.strip(b'CTF{}')
assert len(FLAG) == 13

def genKeyPair():
    d = randint(1,2**80)#randint(1,q-1)
    pubkey = Public_key(G, d*G)
    privkey = Private_key(pubkey, d)
    return pubkey, privkey

pubkey, privkey = genKeyPair()

k1 = randint(1,q-1)
m1 = b'?????????'
assert len(m1)==9
sig1 = privkey.sign(bytes_to_long(m1), k1)

k2 = k1*sig1.s %q
m2 = FLAG
sig2 = privkey.sign(bytes_to_long(m2), k2)

print('r1,s1=',hex(sig1.r),',', hex(sig1.s))
print('r2,s2=',hex(sig2.r),',', hex(sig2.s))

'''
r1,s1= 0x78fee26be76d003b65246a4ba15124efd604ac080a39ae85b30b9217410aedfd , 0xf3e8dfede69f669afd26b7ecba3f966741530e59a96d7b0b840ad1c4d89f4368
r2,s2= 0xbf616947bbc381c7661cefb2eba9c86b35a77a4b623313b9d48d157e6ce919ed , 0x50afd8bea25877cb3f76eefcb077f4ba680e3cf8a6c3e28c0aebac7b75aee789
'''