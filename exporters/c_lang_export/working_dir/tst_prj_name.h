
#ifndef TST_PRJ_NAME_H_INCLUDED
#define TST_PRJ_NAME_H_INCLUDED

# include "fuzzy_math.h"
# include "tst_prj_name_interface.h"

/* Common typedefs / global defines */
enum {
	INF_MIN = 0,
	INF_MAX,
	INF_IGNORE
}; typedef UINT8 INFERENCE_e;

/* Typedefs for tst_prj_name_Input_0 */
# define tst_prj_name_Input_0_NUM_LINVARS 3
# define tst_prj_name_Input_0_DATA_LEN 4
enum {
    tst_prj_name_Input_0_LV_Low,
    tst_prj_name_Input_0_LV_Mid,
    tst_prj_name_Input_0_LV_High,
}; typedef UINT8 tst_prj_name_Input_0_LINVARS_e;

typedef struct {
	tst_prj_name_Input_0_LINVARS_e name;
	FLOAT y[tst_prj_name_Input_0_DATA_LEN];
	FLOAT value;
}
tst_prj_name_Input_0_LINVAR_t;

typedef struct {
	tst_prj_name_Input_0_LINVAR_t linvars[tst_prj_name_Input_0_NUM_LINVARS];
	FLOAT x[tst_prj_name_Input_0_DATA_LEN];
	uint8_t num_linvars;

} tst_prj_name_Input_0_t;

/* Typedefs for tst_prj_name_Input_1 */
# define tst_prj_name_Input_1_NUM_LINVARS 3
# define tst_prj_name_Input_1_DATA_LEN 3
enum {
    tst_prj_name_Input_1_LV_Low,
    tst_prj_name_Input_1_LV_Mid,
    tst_prj_name_Input_1_LV_High,
}; typedef UINT8 tst_prj_name_Input_1_LINVARS_e;

typedef struct {
	tst_prj_name_Input_1_LINVARS_e name;
	FLOAT y[tst_prj_name_Input_1_DATA_LEN];
	FLOAT value;
}
tst_prj_name_Input_1_LINVAR_t;

typedef struct {
	tst_prj_name_Input_1_LINVAR_t linvars[tst_prj_name_Input_1_NUM_LINVARS];
	FLOAT x[tst_prj_name_Input_1_DATA_LEN];
	uint8_t num_linvars;

} tst_prj_name_Input_1_t;

/* Typedefs for tst_prj_name_New_Item */
# define tst_prj_name_New_Item_NUM_LINVARS 3
# define tst_prj_name_New_Item_DATA_LEN 3
enum {
    tst_prj_name_New_Item_LV_Low,
    tst_prj_name_New_Item_LV_Mid,
    tst_prj_name_New_Item_LV_High,
}; typedef UINT8 tst_prj_name_New_Item_LINVARS_e;

typedef struct {
	tst_prj_name_New_Item_LINVARS_e name;
	FLOAT y[tst_prj_name_New_Item_DATA_LEN];
	FLOAT value;
}
tst_prj_name_New_Item_LINVAR_t;

typedef struct {
	tst_prj_name_New_Item_LINVAR_t linvars[tst_prj_name_New_Item_NUM_LINVARS];
	FLOAT x[tst_prj_name_New_Item_DATA_LEN];
	uint8_t num_linvars;

} tst_prj_name_New_Item_t;

/* Typedefs for tst_prj_name_Output_0 */
# define tst_prj_name_Output_0_NUM_LINVARS 3
# define tst_prj_name_Output_0_DATA_LEN 3
enum {
    tst_prj_name_Output_0_LV_Low,
    tst_prj_name_Output_0_LV_Mid,
    tst_prj_name_Output_0_LV_High,
}; typedef UINT8 tst_prj_name_Output_0_LINVARS_e;

typedef struct {
	tst_prj_name_Output_0_LINVARS_e name;
	FLOAT y[tst_prj_name_Output_0_DATA_LEN];
	FLOAT value;
}
tst_prj_name_Output_0_LINVAR_t;

typedef struct {
	tst_prj_name_Output_0_LINVAR_t linvars[tst_prj_name_Output_0_NUM_LINVARS];
	FLOAT x[tst_prj_name_Output_0_DATA_LEN];
	uint8_t num_linvars;

} tst_prj_name_Output_0_t;

/* Typedef for Logic elements */
typedef struct {
	tst_prj_name_Input_0_t* in1_ptr;
	tst_prj_name_Input_1_t* in2_ptr;
	tst_prj_name_Output_0_t* out_ptr;
	const tst_prj_name_Output_0_LINVARS_e logic[tst_prj_name_Input_1_NUM_LINVARS][tst_prj_name_Input_0_NUM_LINVARS];
	const INFERENCE_e logic_inference[tst_prj_name_Input_1_NUM_LINVARS][tst_prj_name_Input_0_NUM_LINVARS];
	const INFERENCE_e inference;
} tst_prj_name_FUZZY_LOGIC_ELEMENT_00_t;

typedef struct {
	tst_prj_name_Input_0_t* in1_ptr;
	tst_prj_name_New_Item_t* in2_ptr;
	tst_prj_name_Output_0_t* out_ptr;
	const tst_prj_name_Output_0_LINVARS_e logic[tst_prj_name_New_Item_NUM_LINVARS][tst_prj_name_Input_0_NUM_LINVARS];
	const INFERENCE_e logic_inference[tst_prj_name_New_Item_NUM_LINVARS][tst_prj_name_Input_0_NUM_LINVARS];
	const INFERENCE_e inference;
} tst_prj_name_FUZZY_LOGIC_ELEMENT_01_t;

/* Typedef for Logic element results */
# define tst_prj_name_Output_0_NUM_OUT_ELEMENTS 2
typedef struct {
	FLOAT linvar_Low[tst_prj_name_Output_0_NUM_OUT_ELEMENTS];
	FLOAT linvar_Mid[tst_prj_name_Output_0_NUM_OUT_ELEMENTS];
	FLOAT linvar_High[tst_prj_name_Output_0_NUM_OUT_ELEMENTS];
} tst_prj_name_Output_0_ELEMENT_RESULTS_t;



# endif // TST_PRJ_NAME_H_INCLUDED
