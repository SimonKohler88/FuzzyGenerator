#include "tst_prj_name.h"
static tst_prj_name_Input_0_t tst_prj_name_Input_0= {
	.linvars = {
		{
			.name = tst_prj_name_Input_0_LV_Low,
			.y = {1.00f,0.60f,0.00f,0.00f}

		},		{
			.name = tst_prj_name_Input_0_LV_Mid,
			.y = {0.00f,0.50f,1.00f,0.00f}

		},		{
			.name = tst_prj_name_Input_0_LV_High,
			.y = {0.00f,0.00f,0.00f,1.00f}

		},
	},
	.num_linvars = tst_prj_name_Input_0_NUM_LINVARS,
	.x = {0.0,25.0,50.0,100.0}
};
static tst_prj_name_Input_1_t tst_prj_name_Input_1= {
	.linvars = {
		{
			.name = tst_prj_name_Input_1_LV_Low,
			.y = {1.00f,0.00f,0.00f}

		},		{
			.name = tst_prj_name_Input_1_LV_Mid,
			.y = {0.00f,1.00f,0.00f}

		},		{
			.name = tst_prj_name_Input_1_LV_High,
			.y = {0.00f,0.00f,1.00f}

		},
	},
	.num_linvars = tst_prj_name_Input_1_NUM_LINVARS,
	.x = {0.0,50.0,100.0}
};
static tst_prj_name_New_Item_t tst_prj_name_New_Item= {
	.linvars = {
		{
			.name = tst_prj_name_New_Item_LV_Low,
			.y = {1.00f,0.00f,0.00f}

		},		{
			.name = tst_prj_name_New_Item_LV_Mid,
			.y = {0.00f,1.00f,0.00f}

		},		{
			.name = tst_prj_name_New_Item_LV_High,
			.y = {0.00f,0.00f,1.00f}

		},
	},
	.num_linvars = tst_prj_name_New_Item_NUM_LINVARS,
	.x = {0.0,50.0,100.0}
};
static tst_prj_name_Output_0_t tst_prj_name_Output_0= {
	.linvars = {
		{
			.name = tst_prj_name_Output_0_LV_Low,
			.y = {1.00f,0.00f,0.00f}

		},		{
			.name = tst_prj_name_Output_0_LV_Mid,
			.y = {0.00f,1.00f,0.00f}

		},		{
			.name = tst_prj_name_Output_0_LV_High,
			.y = {0.00f,0.00f,1.00f}

		},
	},
	.num_linvars = tst_prj_name_Output_0_NUM_LINVARS,
	.x = {0.0,50.0,100.0}
};
static tst_prj_name_FUZZY_LOGIC_ELEMENT_00_t tst_prj_name_FUZZY_LOGIC_ELEMENT_00 = {
	.in1_ptr = &tst_prj_name_Input_0,
	.in2_ptr = &tst_prj_name_Input_1,
	.out_ptr = &tst_prj_name_Output_0,
	.logic = {
		{tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_Mid,},
		{tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_Mid,tst_prj_name_Output_0_LV_Low,},
		{tst_prj_name_Output_0_LV_Mid,tst_prj_name_Output_0_LV_Low,tst_prj_name_Output_0_LV_Low,},
	},
	.logic_inference = {
		{INF_MAX,INF_MAX,INF_MAX,},
		{INF_MAX,INF_MAX,INF_MAX,},
		{INF_MAX,INF_MAX,INF_MAX,},
	},
	.inference = INF_MIN
};
static tst_prj_name_FUZZY_LOGIC_ELEMENT_01_t tst_prj_name_FUZZY_LOGIC_ELEMENT_01 = {
	.in1_ptr = &tst_prj_name_Input_0,
	.in2_ptr = &tst_prj_name_New_Item,
	.out_ptr = &tst_prj_name_Output_0,
	.logic = {
		{tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_Mid,},
		{tst_prj_name_Output_0_LV_High,tst_prj_name_Output_0_LV_Mid,tst_prj_name_Output_0_LV_Low,},
		{tst_prj_name_Output_0_LV_Mid,tst_prj_name_Output_0_LV_Low,tst_prj_name_Output_0_LV_Low,},
	},
	.logic_inference = {
		{INF_MAX,INF_MAX,INF_MAX,},
		{INF_MAX,INF_MAX,INF_MAX,},
		{INF_MAX,INF_MAX,INF_MAX,},
	},
	.inference = INF_MIN
};
static tst_prj_name_Output_0_ELEMENT_RESULTS_t tst_prj_name_Output_0_ELEMENT_RESULTS;
static void calculate_fuzzy_element00(void){
	uint8_t row, col;
	FLOAT out_Low = -1;
	FLOAT out_Mid = -1;
	FLOAT out_High = -1;
	FLOAT temp = 0;

	for (row = 0; row < tst_prj_name_Input_1_NUM_LINVARS; row++) {
		for (col = 0; col < tst_prj_name_Input_0_NUM_LINVARS; col++) {
			temp = 0;
			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.logic_inference[row][col] == INF_IGNORE) continue;
			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.logic_inference[row][col] == INF_MIN)
				temp = minf(tst_prj_name_Input_0.linvars[col].value, tst_prj_name_Input_1.linvars[row].value);
			else
				temp = maxf(tst_prj_name_Input_0.linvars[col].value, tst_prj_name_Input_1.linvars[row].value);

			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.logic[row][col] == tst_prj_name_Output_0_LV_Low){
				if (out_Low < 0) out_Low = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.inference == INF_MIN) out_Low = minf(temp, out_Low);
 				else out_Low = maxf(temp, out_Low);
			}
			else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.logic[row][col] == tst_prj_name_Output_0_LV_Mid){
				if (out_Mid < 0) out_Mid = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.inference == INF_MIN) out_Mid = minf(temp, out_Mid);
 				else out_Mid = maxf(temp, out_Mid);
			}
			else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.logic[row][col] == tst_prj_name_Output_0_LV_High){
				if (out_High < 0) out_High = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_00.inference == INF_MIN) out_High = minf(temp, out_High);
 				else out_High = maxf(temp, out_High);
			}
		}
	}
	if (out_Low <0) out_Low = 0;
	if (out_Mid <0) out_Mid = 0;
	if (out_High <0) out_High = 0;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Low[0] = out_Low;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Mid[0] = out_Mid;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_High[0] = out_High;
}
static void calculate_fuzzy_element01(void){
	uint8_t row, col;
	FLOAT out_Low = -1;
	FLOAT out_Mid = -1;
	FLOAT out_High = -1;
	FLOAT temp = 0;

	for (row = 0; row < tst_prj_name_New_Item_NUM_LINVARS; row++) {
		for (col = 0; col < tst_prj_name_Input_0_NUM_LINVARS; col++) {
			temp = 0;
			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.logic_inference[row][col] == INF_IGNORE) continue;
			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.logic_inference[row][col] == INF_MIN)
				temp = minf(tst_prj_name_Input_0.linvars[col].value, tst_prj_name_New_Item.linvars[row].value);
			else
				temp = maxf(tst_prj_name_Input_0.linvars[col].value, tst_prj_name_New_Item.linvars[row].value);

			if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.logic[row][col] == tst_prj_name_Output_0_LV_Low){
				if (out_Low < 0) out_Low = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.inference == INF_MIN) out_Low = minf(temp, out_Low);
				else out_Low = maxf(temp, out_Low);
			}
			else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.logic[row][col] == tst_prj_name_Output_0_LV_Mid){
				if (out_Mid < 0) out_Mid = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.inference == INF_MIN) out_Mid = minf(temp, out_Mid);
 				else out_Mid = maxf(temp, out_Mid);
			}
			else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.logic[row][col] == tst_prj_name_Output_0_LV_High){
				if (out_High < 0) out_High = temp;
				else if (tst_prj_name_FUZZY_LOGIC_ELEMENT_01.inference == INF_MIN) out_High = minf(temp, out_High);
 				else out_High = maxf(temp, out_High);
			}
		}
	}
	if (out_Low <0) out_Low = 0;
	if (out_Mid <0) out_Mid = 0;
	if (out_High <0) out_High = 0;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Low[1] = out_Low;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Mid[1] = out_Mid;
	tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_High[1] = out_High;
}
static FLOAT calculate_tst_prj_name_Output_0_ELEMENT_RESULTS(void){
	FLOAT cutoff_Low[tst_prj_name_Output_0_DATA_LEN] = {0};
	FLOAT cutoff_Mid[tst_prj_name_Output_0_DATA_LEN] = {0};
	FLOAT cutoff_High[tst_prj_name_Output_0_DATA_LEN] = {0};
	FLOAT area[tst_prj_name_Output_0_DATA_LEN] = {0};
	FLOAT result = 0;
	//output inference: Min
	tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Low].value = min_array(tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Low,tst_prj_name_Output_0_NUM_OUT_ELEMENTS);
	tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Mid].value = min_array(tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_Mid,tst_prj_name_Output_0_NUM_OUT_ELEMENTS);
	tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_High].value = min_array(tst_prj_name_Output_0_ELEMENT_RESULTS.linvar_High,tst_prj_name_Output_0_NUM_OUT_ELEMENTS);

	min_array_value(tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Low].y, tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Low].value, cutoff_Low,tst_prj_name_Output_0_DATA_LEN);
	min_array_value(tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Mid].y, tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_Mid].value, cutoff_Mid,tst_prj_name_Output_0_DATA_LEN);
	min_array_value(tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_High].y, tst_prj_name_Output_0.linvars[tst_prj_name_Output_0_LV_High].value, cutoff_High,tst_prj_name_Output_0_DATA_LEN);

	max_array_array(cutoff_Low, area,area ,tst_prj_name_Output_0_DATA_LEN);
	max_array_array(cutoff_Mid, area,area ,tst_prj_name_Output_0_DATA_LEN);
	max_array_array(cutoff_High, area,area ,tst_prj_name_Output_0_DATA_LEN);

	result = centre_of_gravity(tst_prj_name_Output_0.x, area, tst_prj_name_Output_0_DATA_LEN);
	return result;
}
/* calculation function */
uint8_t tst_prj_name_calculate_fuzzy(tst_prj_name_IO_STRUCT_t *io_struct) {
	tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_Low].value = interpolate(io_struct->tst_prj_name_Input_0, tst_prj_name_Input_0.x, tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_Low].y, tst_prj_name_Input_0_DATA_LEN);
	tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_Mid].value = interpolate(io_struct->tst_prj_name_Input_0, tst_prj_name_Input_0.x, tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_Mid].y, tst_prj_name_Input_0_DATA_LEN);
	tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_High].value = interpolate(io_struct->tst_prj_name_Input_0, tst_prj_name_Input_0.x, tst_prj_name_Input_0.linvars[tst_prj_name_Input_0_LV_High].y, tst_prj_name_Input_0_DATA_LEN);
	tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_Low].value = interpolate(io_struct->tst_prj_name_Input_1, tst_prj_name_Input_1.x, tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_Low].y, tst_prj_name_Input_1_DATA_LEN);
	tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_Mid].value = interpolate(io_struct->tst_prj_name_Input_1, tst_prj_name_Input_1.x, tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_Mid].y, tst_prj_name_Input_1_DATA_LEN);
	tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_High].value = interpolate(io_struct->tst_prj_name_Input_1, tst_prj_name_Input_1.x, tst_prj_name_Input_1.linvars[tst_prj_name_Input_1_LV_High].y, tst_prj_name_Input_1_DATA_LEN);
	tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_Low].value = interpolate(io_struct->tst_prj_name_New_Item, tst_prj_name_New_Item.x, tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_Low].y, tst_prj_name_New_Item_DATA_LEN);
	tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_Mid].value = interpolate(io_struct->tst_prj_name_New_Item, tst_prj_name_New_Item.x, tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_Mid].y, tst_prj_name_New_Item_DATA_LEN);
	tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_High].value = interpolate(io_struct->tst_prj_name_New_Item, tst_prj_name_New_Item.x, tst_prj_name_New_Item.linvars[tst_prj_name_New_Item_LV_High].y, tst_prj_name_New_Item_DATA_LEN);
	calculate_fuzzy_element00();
	calculate_fuzzy_element01();
	io_struct->tst_prj_name_Output_0 = calculate_tst_prj_name_Output_0_ELEMENT_RESULTS();
	return 0;
}