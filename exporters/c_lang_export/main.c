


#include <stdio.h>

#include "tst_prj_name_interface.h"

int main(void)
{
    tst_prj_name_IO_STRUCT_t io_struct = {90, 91, 0};

    tst_prj_name_calculate_fuzzy(&io_struct);

    printf("in1 %f\n", io_struct.tst_prj_name_Input_0);
    printf("in2 %f\n", io_struct.tst_prj_name_Input_1);
    printf("out1 %f\n", io_struct.tst_prj_name_Output_0);
    // output should give 31.37
}
