// CS24I1029
// YASHVANTH S

#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main(int argc, char *argv[]){
  if(argc!=4){
    printf("Usage: %s <num1> <operator> <num2>\n", argv[0]);
    return 1;
    }
    
  float num1=atof(argv[1]);
  float num2=atof(argv[3]);
  char op=argv[2][0];
  float result;
  
  switch(op){
    case '+':
      result=num1+num2;
      break;
    case '-':
      result=num1-num2;
      break;
    case '*':
      result=num1*num2;
      break;
    case '/':
    if(num2==0){
      printf("Cannot divide by zero\n");
      return 1;
    }
      result=num1/num2;
      break;
    default:
      printf("Invalid Operator\n");
      return 1;
    }
    
    printf("Result: %.2f\n", result);
}
