//
// Created by skohl on 13.09.2026.
//


# include <stdio.h>
# include "fuzzy_math.h"
# include "fuzzy_code.h"
# include "fuzzy_interface.h"


static INPUT01_t in01 = {
    .linvars = {
        {
            .name = INP01_LV_LOW,
            .y = {1.00f, 0.80f, 0.60f, 0.40, 0.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00}
        },
        {
            .name = INP01_LV_MID,
            .y = {0.00, 0.20, 0.40, 0.60, 0.80, 1.00, 0.80, 0.60, 0.40, 0.20, 0.00}

        },
        {
            .name = INP01_LV_HIGH,
            .y = {0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.40, 0.60, 0.80, 1.00}
        }
    },
    .num_linvars = INP01_NUM_LINVARS,
    .x = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100},
};


static INPUT02_t in02 = {
    .linvars = {
        {
            .name = INP02_LV_LOW,
            .y = {1.00, 0.80, 0.60, 0.40, 0.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00}
        },
        {
            .name = INP02_LV_MID,
            .y = {0.00, 0.20, 0.40, 0.60, 0.80, 1.00, 0.80, 0.60, 0.40, 0.20, 0.00}

        },
        {
            .name = INP02_LV_HIGH,
            .y = {0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.40, 0.60, 0.80, 1.00}
        }
    },
    .num_linvars = INP02_NUM_LINVARS,
    .x = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100},
};

static OUTPUT01_t out01 = {
    .linvars = {
        {
            .name = OUT01_LV_LOW,
            .y = {1.00, 0.80, 0.60, 0.40, 0.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00}
        },
        {
            .name = OUT01_LV_MID,
            .y = {0.00, 0.20, 0.40, 0.60, 0.80, 1.00, 0.80, 0.60, 0.40, 0.20, 0.00}

        },
        {
            .name = OUT01_LV_HIGH,
            .y = {0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.40, 0.60, 0.80, 1.00}
        }
    },
    .num_linvars = OUT01_NUM_LINVARS,
    .x = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100},
};

static FUZZY_LOGIC_ELEMENT01_t fuzzy_logic01 = {
    .logic = {
        {OUT01_LV_HIGH, OUT01_LV_HIGH, OUT01_LV_MID},
        {OUT01_LV_HIGH, OUT01_LV_MID, OUT01_LV_LOW},
        {OUT01_LV_MID, OUT01_LV_LOW, OUT01_LV_LOW}
    },
    .logic_inference = {
        {INF_MIN, INF_MIN, INF_MIN},
        {INF_MIN, INF_MIN, INF_MIN},
        {INF_MIN, INF_MIN, INF_MIN}
    },
    .inference = INF_MAX,
};

FUZZY_CTRL_t fuzzy_ctrl = {INF_MIN};

/* Static Function definitions */
static void calculate_fuzzy_element01(void) {
    uint8_t row;
    uint8_t col;

    float out_low = -1;
    float out_mid = -1;
    float out_high = -1;
    float temp = 0;

    for (row = 0; row < INP02_NUM_LINVARS; row++) {
        for (col = 0; col < INP01_NUM_LINVARS; col++) {
            temp = 0;

            if (fuzzy_logic01.logic_inference[row][col] == INF_IGNORE) continue;
            else if (fuzzy_logic01.logic_inference[row][col] == INF_MIN) temp = minf(in01.linvars[col].value,
                                                                             in02.linvars[row].value);
            else if (fuzzy_logic01.logic_inference[row][col] == INF_MAX) temp = maxf(in01.linvars[col].value,
                                                                             in02.linvars[row].value);

            //printf("temp: %f, in1: %f, in2: %f\n", temp, in01.linvars[col].value, in02.linvars[row].value);
            if (fuzzy_logic01.logic[row][col] == OUT01_LV_LOW) {
                if (out_low < 0) out_low = temp;
                else if (fuzzy_logic01.inference == INF_MIN) out_low = minf(temp, out_low);
                else out_low = maxf(temp, out_low);
            } else if (fuzzy_logic01.logic[row][col] == OUT01_LV_MID) {
                if (out_mid < 0) out_mid = temp;
                else if (fuzzy_logic01.inference == INF_MIN) out_mid = minf(temp, out_mid);
                else out_mid = maxf(temp, out_mid);
            } else if (fuzzy_logic01.logic[row][col] == OUT01_LV_HIGH) {
                if (out_high < 0) out_high = temp;
                else if (fuzzy_logic01.inference == INF_MIN) out_high = minf(temp, out_high);
                else out_high = maxf(temp, out_high);
            }
        }
    }
    if (out_low < 0) out_low = 0;
    if (out_mid < 0) out_mid = 0;
    if (out_high < 0) out_high = 0;

    //printf("--------------linvars---------\n");
    //printf("low: %f\n", out_low);
    //printf("mid: %f\n", out_mid);
    //printf("high: %f\n", out_high);

    fuzzy_ctrl.out01_results.linvar_low[0] = out_low;
    fuzzy_ctrl.out01_results.linvar_mid[0] = out_mid;
    fuzzy_ctrl.out01_results.linvar_high[0] = out_high;
}


static void print_array(float arr[], uint16_t len) {
    int index;
    for (index = 0; index < len; index++) {
        printf("%f, ", arr[index]);
    }
    printf("\n");
}

static float calculate_output_01(void) {
    float cutoff_low[NUM_DATA_ARRAY] = {0};
    float cutoff_mid[NUM_DATA_ARRAY] = {0};
    float cutoff_high[NUM_DATA_ARRAY] = {0};
    float area[NUM_DATA_ARRAY] = {0};
    float result = 0;
    if (fuzzy_ctrl.global_inference == INF_MIN) {
        out01.linvars[OUT01_LV_LOW].value = min_array(fuzzy_ctrl.out01_results.linvar_low, NUM_OUTPUT01_ELEMENTS);
        out01.linvars[OUT01_LV_MID].value = min_array(fuzzy_ctrl.out01_results.linvar_mid, NUM_OUTPUT01_ELEMENTS);
        out01.linvars[OUT01_LV_HIGH].value = min_array(fuzzy_ctrl.out01_results.linvar_high, NUM_OUTPUT01_ELEMENTS);
    } else {
        out01.linvars[OUT01_LV_LOW].value = max_array(fuzzy_ctrl.out01_results.linvar_low, NUM_OUTPUT01_ELEMENTS);
        out01.linvars[OUT01_LV_MID].value = max_array(fuzzy_ctrl.out01_results.linvar_mid, NUM_OUTPUT01_ELEMENTS);
        out01.linvars[OUT01_LV_HIGH].value = max_array(fuzzy_ctrl.out01_results.linvar_high, NUM_OUTPUT01_ELEMENTS);
    }

    min_array_value(out01.linvars[OUT01_LV_LOW].y, out01.linvars[OUT01_LV_LOW].value, cutoff_low, NUM_DATA_ARRAY);
    min_array_value(out01.linvars[OUT01_LV_MID].y, out01.linvars[OUT01_LV_MID].value, cutoff_mid, NUM_DATA_ARRAY);
    min_array_value(out01.linvars[OUT01_LV_HIGH].y, out01.linvars[OUT01_LV_HIGH].value, cutoff_high, NUM_DATA_ARRAY);

    max_array_array(cutoff_low, area, area, NUM_DATA_ARRAY);
    max_array_array(cutoff_mid, area, area, NUM_DATA_ARRAY);
    max_array_array(cutoff_high, area, area, NUM_DATA_ARRAY);

    //print_array(area, NUM_DATA_ARRAY);
    result = centre_of_gravity(out01.x, area, NUM_DATA_ARRAY);
    return result;
}

/* calculation function */
uint8_t calculate_fuzzy(IO_STRUCT_t *io_struct) {
    ERROR_CODE_e err = ERR_NONE;
    //printf("Inputs given: in1: %f, in2: %f\n", io_struct->input01, io_struct->input02);
    /* calculate linguistic vars for in 1 */
    in01.linvars[INP01_LV_LOW].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_LOW].y,
                                                   NUM_DATA_ARRAY);
    in01.linvars[INP01_LV_MID].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_MID].y,
                                                   NUM_DATA_ARRAY);
    in01.linvars[INP01_LV_HIGH].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_HIGH].y,
                                                    NUM_DATA_ARRAY);

    /* calculate linguistic vars for in 2 */
    in02.linvars[INP02_LV_LOW].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_LOW].y,
                                                   NUM_DATA_ARRAY);
    in02.linvars[INP02_LV_MID].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_MID].y,
                                                   NUM_DATA_ARRAY);
    in02.linvars[INP02_LV_HIGH].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_HIGH].y,
                                                    NUM_DATA_ARRAY);

    //printf("in1_low: %f, in1_mid: %f, in1_high: %f\n", in01.linvars[INP01_LV_LOW].value, in01.linvars[INP01_LV_MID].value, in01.linvars[INP01_LV_HIGH].value);
    //printf("in2_low: %f, in2_mid: %f, in2_high: %f\n", in02.linvars[INP02_LV_LOW].value, in02.linvars[INP02_LV_MID].value, in02.linvars[INP02_LV_HIGH].value);
    calculate_fuzzy_element01();

    io_struct->output01 = calculate_output_01();

    return err;
}
