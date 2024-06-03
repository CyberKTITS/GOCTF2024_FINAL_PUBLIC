
# Решение | JYTHON | Medium | Reverse

1) Откроем через jd-gui. Нас будет интересовать два класса Base64Decoder.class и Lib/entrypoint.py:

<image src="images/1.jpg">
<image src="images/1.jpg">

2) Чтобы достать entrypoint.py надо разархивировать jar и прочитать файл.

<image src="images/3.jpg">

3) Функции используются из класса Base64Decoder. (пример расшифровки: https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Regex','string':'@'%7D,'%20',true,false,true,false)From_Decimal('Space',false)XOR(%7B'option':'UTF8','string':'StRaNgE_JyThOn%7DsecretTecretPockerOPAJSDNWQOUN!@*%26%23*T*FGVE@UNK@EBYGYDSF'%7D,'Standard',false)From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=MzBAMzBAMzRAMjRANDJAMzNAN0A1MkA0MUA3NUA2M0AxOEA0M0A1NEAxN0AyNEA2M0AxNEA1OUAzMUA1N0A2MkAyQDQwQDYzQDMxQDRAOTlAMzRANTlAMEA0NkA2MEAxMUAzMkA1MUAzMEA5NkA1QDUyQDUzQDU5QDZAOTdAMjNAOTFANDBAODBANzFAMTAwQDcwQDE3QDExNUAyM0A1NUAyOEA4QDI0QDUwQDU0QDVANEAzMUA1NkAyM0A0NUAyMEAxMTJANTRAMkA1MkAxM0AyOUA1NEA3QDgyQDExQDlAMTFANzI)

После расшифрования строки можно получить:
2:rtPdsi3uydfb328
3:w1y
4:kOp3n28c8shiDa
I1x146s638x829b95P5

Анализируя python код можно получить следующий порядок действий, чтобы получить первую часть флага: https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)XOR(%7B'option':'UTF8','string':'rtPdsi3uydfb328'%7D,'Standard',false)Find_/_Replace(%7B'option':'Regex','string':'w1y'%7D,'',true,false,true,false)XOR(%7B'option':'UTF8','string':'kOp3n28c8shiDa'%7D,'Standard',false)&input=QlVVcGFGTjZkSDB3RWpVRkNqc0hWMG9MWlRJREFoRWtWU2RP&oeol=FF 


