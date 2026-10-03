
#ifndef TST_PRJ_NAME_INTERFACE_H_INCLUDED
#define TST_PRJ_NAME_INTERFACE_H_INCLUDED

# include "stdint.h"

/* Data definitions */
# define FLOAT float
# define UINT8 uint8_t
# define UINT16 uint16_t

typedef struct {
	FLOAT tst_prj_name_Input_0;
	FLOAT tst_prj_name_Input_1;
	FLOAT tst_prj_name_New_Item;
	FLOAT tst_prj_name_Output_0;
} tst_prj_name_IO_STRUCT_t;

uint8_t tst_prj_name_calculate_fuzzy(tst_prj_name_IO_STRUCT_t* io_struct);


# endif // TST_PRJ_NAME_INTERFACE_H_INCLUDED
