

# include "main.h"

#include <stdio.h>

#include "fuzzy_interface.h"

int main(void)
{
    IO_STRUCT_t io_struct = {90, 91, 0};

    calculate_fuzzy(&io_struct);

    printf("in1 %f\n", io_struct.input01);
    printf("in2 %f\n", io_struct.input02);
    printf("out1 %f\n", io_struct.output01);
    /*is: 27.87, should: 31.37*/

}
