BITS 64 

.test
global _start


_start:
  call main
  mov rax,0x3c
  syscall
main:
  mov rax,0
  mov rdi,0
  mov rsi,rsp
  mov rdx,0x500
  syscall
  ret
