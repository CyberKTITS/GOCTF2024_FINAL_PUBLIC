#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#define MAX 500


typedef struct chunk{;
  char id[8];
  char *info;
  void *func;
} chunk;

int getInt(int *x){
	int a;
	int check;
	char c = '\n';
	do{
	  check = scanf("%d", &a);
		if (check == EOF) return EOF;
		if (check != 1|| c != '\n') printf("Wrong.\nPlease, repeat.\n");
		if (c != '\n'){
			scanf("%*[^\n]%*c");
		}
	}while(check != 1 || c != '\n');
	*x = a;
	return check;
}

void chunk_read(chunk *ch);
void chunk_print(chunk *ch);
void chunk_free(chunk *ch);
void chunk_info(chunk *ch);
void print_info(chunk*ch);
void change_info(chunk*ch);
void execute(chunk *ch);


int main(){
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  chunk chu[1000];
  printf("Oops: %p\n", chu);
  int ind, stat;
  do{
    printf("Here is your menu\n");
    stat = getInt(&ind);
    if (stat == EOF)
      exit(0);
    switch (ind){
      case 1:
        chunk_read(chu);
        break;
      case 2:
        chunk_print(chu);
        break;
      case 3:
        chunk_info(chu);
        break;
      case 4:
        chunk_free(chu);
        break;
      case 5:
        print_info(chu);
        break;
      case 6:
        change_info(chu);
        break;
      case 7:
        execute(chu);
        break;
    }
  }while(ind != 0);
}

void placeholder(){
  printf("bugagaga\n");
}

void chunk_read(chunk *ch){
  printf("Where to write?\n");
  int ind;
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  printf("Now reading 0x10 byte\n");
  ch[ind].info = NULL;
  ch[ind].func = &placeholder;
  read(0, ch[ind].id, 0x10);
}

void chunk_print(chunk *ch){
  puts("What to read?");
  int ind, stat;
  stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  write(1, ch[ind].id, 0x10);
  puts("");
}

void chunk_free(chunk*ch){
  int ind;
  puts("What info to del?");
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  
  printf("%p\n", ch[ind].info); 
  free(ch[ind].info);
}

void chunk_info(chunk*ch){
  printf("Where to write?\n");
  int ind;
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  
  char *info = calloc(0x11, sizeof(char));
  printf("What indo to add?\n");
  read(0, info, 0x20);
  ch[ind].info = info;
}

void execute(chunk *ch){
  int ind;
  printf("executing\n");
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  void (*func_ptr)(void) = ch[ind].func;
  func_ptr();
}

void change_info(chunk*ch){
  int ind;
  printf("What index to change?\n");
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  read(0, ch[ind].info, 0x20);
}

void print_info(chunk*ch){
  int ind;
  printf("What to print?\n");
  int stat = getInt(&ind);
  if (ind < 0 || ind > MAX || stat == EOF){
    puts("GET OUT");
    exit(-100);
  }
  write(1, ch[ind].info, 0x20);
}

void win(){
  execve("/bin/sh", NULL, NULL);
}


