# P.<a,pq_delta,r1,r2> = PolynomialRing(Zmod(n))

# p_a = c1*2^60+r1
# q_a = c2*2^60+r2
# f = (n+a*pq_delta+a^2)^2-p_a*q_a

# small_roots(f, (2^60,2^256,2^60,2^60))
# # (p-a)**2 = c1*2^60+r1
'''
Я не придумал красиого копперсмита. Подумал, поэтому решил повторить идею с goctf part1. Надеюсь, вы читали райтапы чтобы осознать ее :)
В общем, дело имеем с рса. Задача ясна: разложить N на множители, а затем расшифровать сообщение.
Мы знаем
(p-a)^2 = c1*2^60+r1 где 
r1<2^60
p<2^256
a<2^60 
Давайте попробуем запустить код у себя локально (т.е. со своими данными)
In [20]: isqrt(c1 * 2 ** 60), p - a
Out[20]:
(mpz(75039513464615431396182302446144249962893570653341415749729213981836223025873),
 75039513464615431396182302446144249962893570653341415749729213981836223025874)

Невероятно. Почему это работает? Видимо, из-за того что 60 из 512 бит вообще ничего особо не меняют.
В любом случае, получаем isqrt(c1 * 2 ** 60)+isqrt(c2 * 2 ** 60) ~= p+q
Осталось расшифровать рса.
для этого нужно вычислить phi= (p-1)*(q-1) = p*q -p -q +1 = n - (p+q) +1
Далее все дефолт
'''
from gmpy2 import isqrt
ct = 5234134987863748217592877691184516725977940101487778794796733456104242510413903246090244236404682775093122417367736777442508316870490720427292017665501232

n=6116131078371275318529012515763832266677276143683815012261888710578475234783502758794051107124185435820269715707990679785451837432636558688129186609169951
c1=6595556068879622741128868139856581329708569235648083382508082032293977372856462810797190054869755889414479816174159274840192227249081944
c2=4266803794170052314241790328379545437973054675865133422680632821157109480592840885162365685238878051028087079561332063070335610037977472

p_q = isqrt(c1 * 2 ** 60)+isqrt(c2 * 2 ** 60)
for i in range(-10,10+1):
    try:
        phi = n-(p_q+i)+1
        d = pow(0x10001,-1,phi)
        m = pow(ct,d,n)
        print(int(m).to_bytes(64,'little'))
    except:pass
# CTF{Nesposoben_byt_odin???}