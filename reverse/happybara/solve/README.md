`main` в иде стремный какой-то:
```c
  v18[67] = (void *)__readfsqword(0x28u);
  qmemcpy(v18, &dword_2020, 0x218uLL);
  v3 = (void **)operator new(0x218uLL);
  *v3 = v18[0];
  v3[66] = v18[66];
  qmemcpy(
    (void *)((unsigned __int64)(v3 + 1) & 0xFFFFFFFFFFFFFFF8LL),
    (const void *)((char *)v18 - ((char *)v3 - ((unsigned __int64)(v3 + 1) & 0xFFFFFFFFFFFFFFF8LL))),
    8LL * (((unsigned int)v3 - (((_DWORD)v3 + 8) & 0xFFFFFFF8) + 536) >> 3));
  v18[0] = &v18[2];
  v18[1] = 0LL;
  LOBYTE(v18[2]) = 0;
  std::operator>><char>(&std::cin, v18);
  v4 = (void **)v18[0];
  v5 = 0LL;
  while ( 1 )
  {
    v6 = *((char *)v18[0] + v5);
    v7 = v5 + 13337;
    v8 = 0;
    do
    {
      v9 = v8 - 1640531527;
      v10 = v8 + 1013904242;
      v11 = ((v7 + v9) ^ (dword_4284 + (v7 >> 5)) ^ (KEY + 16 * v7)) + v6;
      v12 = ((v9 + v11) ^ (dword_428C + (v11 >> 5)) ^ (dword_4288 + 16 * v11)) + v7;
      v13 = ((v12 + v10) ^ (dword_4284 + (v12 >> 5)) ^ (KEY + 16 * v12)) + v11;
      v14 = ((v10 + v13) ^ (dword_428C + (v13 >> 5)) ^ (dword_4288 + 16 * v13)) + v12;
      v15 = ((v14 + v9 + 1013904242) ^ (dword_4284 + (v14 >> 5)) ^ (KEY + 16 * v14)) + v13;
      v8 = v9 - 626627285;
      v16 = ((v9 + 1013904242 + v15) ^ (dword_428C + (v15 >> 5)) ^ (dword_4288 + 16 * v15)) + v14;
      v6 = ((v16 + v9 - 626627285) ^ (dword_4284 + (v16 >> 5)) ^ (KEY + 16 * v16)) + v15;
      v7 = ((v9 - 626627285 + v6) ^ (dword_428C + (v6 >> 5)) ^ (dword_4288 + 16 * v6)) + v16;
    }
    while ( v9 != -330774027 );
    if ( *((_DWORD *)v3 + v5) != _mm_crc32_u32(0xFFFFFFFF, v7) + _mm_crc32_u32(0xFFFFFFFF, v6) )
      break;
    if ( ++v5 == 134 )
      goto LABEL_6;
  }
  std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "CHECK FAILED", 12LL);
  v4 = (void **)v18[0];
LABEL_6:
  if ( v4 != &v18[2] )
    operator delete(v4, (unsigned __int64)v18[2] + 1);
  operator delete(v3, 0x218uLL);
```
Давайте заметим что мы вводим строку `v18`, а `v6` - символ этой строки.
```python
v8 = input()
v5 = 0
while 1:
	v6 = v8[v5]
	# do smth with v6
	v5+=1
	if v5==134:
		break
```
Если с условием выхода из цикла все ясно, то как мы можем попасть на `check failed`?
```c
qmemcpy(v18, &dword_2020, 0x218uLL);
v3 = (void **)operator new(0x218uLL);
*v3 = v18[0];
v3[66] = v18[66];
while (1){
	...
    if ( *((_DWORD *)v3 + v5) != _mm_crc32_u32(0xFFFFFFFF, v7) + _mm_crc32_u32(0xFFFFFFFF, v6) )
      break;
}
std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "CHECK FAILED", 12LL);
```
Если поиграться в дебаггере, то можно заметить, что каждый символ проверяется независимо от других. Поэтому можно просто перебрать каждый символ, и нам будет плевать на все это умное шифрование.
Остается сдампить массив `v3`:
```c
  qmemcpy(v18, &dword_2020, 0x218uLL);
  v3 = (void **)operator new(0x218uLL);
  *v3 = v18[0];
```
Скрипт для idapython:
```python
bs = idc.get_bytes(0x2020,0x218)
table = [int.from_bytes(bs[i:i+4],'little') for i in range(0,len(bs),4)]
```
потом результат шифрования символа (`_mm_crc32_u32(0xFFFFFFFF, v7) + _mm_crc32_u32(0xFFFFFFFF, v6) )` и тп): 
```asm
.text:0000000000001374 mov     esi, r14d
.text:0000000000001377 mov     eax, r14d
.text:000000000000137A crc32   esi, ecx
.text:000000000000137F crc32   eax, edx
.text:0000000000001384 add     eax, esi
.text:0000000000001386 cmp     [rbp+r12*4+0], eax # encrypt(symbol) находится в eax, так мы и сдампим символ
```
Но перебирать каждый символ последовательно очень долго. Давайте уберем `break`, чтобы убрать `check failed` после неверного символа
```c
    if ( *((_DWORD *)v3 + v5) != _mm_crc32_u32(0xFFFFFFFF, v7) + _mm_crc32_u32(0xFFFFFFFF, v6) )
      break;
```
Это можно сделать, поставив `nop` вместо `jnz`:

![](files/Pasted%20image%2020240528165839.png)

Теперь шлем в бинарь `aaaaaaaaaaaaaaa...`, `bbbbbbbbbbbb...` и тп и для каждой позиции сопоставляем нужное с v3.
Скрипт для gdb лежит в [solve/sol.py].

Важный момент: если у вас включен gef или другие плагины для гдб, то их следует отключить, т.к. они будут обновлять интерфейс, тем самым тормозя скрипт.
