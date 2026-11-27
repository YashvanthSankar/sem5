#include "types.h"
#include "stat.h"
#include "user.h"

int main(void) {
    printf(1,"PID = %d\n",process_info(1));
    printf(1,"PPID = %d\n",process_info(2));
    printf(1,"Difference = %d\n",process_info(3));
    exit();
}
