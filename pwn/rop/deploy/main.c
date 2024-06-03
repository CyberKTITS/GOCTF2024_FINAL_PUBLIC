#include <stdio.h>
#include <fcntl.h>
#include <stdio.h> 
#include <string.h>
#include <unistd.h>

char encrypted[32]={
0x25 ,
0x2d ,
0x21 ,
0x36 ,
0x24 ,
0x39 ,
0x63 ,
0x36 ,
0x1d ,
0x35 ,
0x2 ,
0x31 ,
0x1d ,
0x23 ,
0x1d ,
0x30 ,
0x71 ,
0x2 ,
0x2e ,
0x2e ,
0x3b ,
0x1d ,
0x27 ,
0x2 ,
0x31 ,
0x3b ,
0x1d ,
0x30 ,
0x72 ,
0x32 ,
0x3f ,
0x42 ,
};


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
  return;

}

void helper(){

  asm("pop %r9\n"
    "ret\n");
  return;
}
