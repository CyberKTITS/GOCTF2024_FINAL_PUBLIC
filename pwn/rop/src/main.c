#include <stdio.h>
#include <fcntl.h>
#include <stdio.h> 
#include <string.h>
#include <unistd.h>

char encrypted[32]={
0x0 ,
0x1 ,
0x2 ,
0x3 ,
0x4 ,
0x5 ,
0x6 ,
0x7 ,
0x8 ,
0x9 ,
0xa ,
0xb ,
0xc ,
0xd ,
0xe ,
0xf ,
0x10 ,
0x11 ,
0x12 ,
0x13 ,
0x14 ,
0x15 ,
0x16 ,
0x17 ,
0x18 ,
0x19 ,
0x1a ,
0x1b ,
0x1c ,
0x1d ,
0x1e ,
0x1f};


void win_round2(int c, int d, unsigned e){
    if (c == 0x4d1d0001){
      if (d == 0x4269){
        if (e == -1){
          puts((char*)encrypted);
          fflush(stdout);
        }
      }
    
  }
}

void win_round1(long long a, int b, int c, int d, unsigned e, long f, long long h){
  printf("WELCOME!\n");
  if (a == 0x19e24dbf4f16b6){
    for (int i = 0; i<32;i++){
      encrypted[i] = encrypted[i] ^ 0x42;
    }
    if (b == 0x1337){
      if (f == -1)
    if (h == 0xdeadbeefbadecafe){
        win_round2(c, d, e);     
    }
    }
  }
}

void leak(){
    char b[0x1000];
  int a = open("/proc/self/maps",0);
  memset(b,0,0x1000);
  read(a,b,0x1000);
  puts(b);
}

void logic(){
  char a[0x10];
  read(0, a, 0x100);
  return;
}

int main(){
  setvbuf(stdin,0,2,0);
  setvbuf(stdout,0,2,0);
  fprintf(stdout, "HELLO\n");
  leak();
  logic();
  printf("a\n");
  return 0;
}

void helper(){

  asm("pop %r9\n"
    "ret\n");
  return;
}
