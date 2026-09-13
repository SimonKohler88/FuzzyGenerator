//
// Created by skohl on 13.09.2026.
//

#ifndef FUZZY_C_FUZZY_CODE_H
#define FUZZY_C_FUZZY_CODE_H
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif



/* Common typedefs / global defines */
# define NUM_DATA_ARRAY 11
enum {
    INF_MIN = 0,
    INF_MAX,
    INF_IGNORE
}; typedef uint8_t INFERENCE_e;

enum {
    ERR_NONE = 0,
    ERR_YES,
}; typedef uint8_t ERROR_CODE_e;


/* Typedefs for Input 1 */
enum {
    INP01_LV_LOW = 0,
    INP01_LV_MID,
    INP01_LV_HIGH
}; typedef uint8_t INP01_LINVARS_e;

typedef struct {
    INP01_LINVARS_e name;
    float y[NUM_DATA_ARRAY];
    float value;
} INP01_LINVAR_t;

# define INP01_NUM_LINVARS 3
typedef struct {
    INP01_LINVAR_t linvars[INP01_NUM_LINVARS];
    const uint8_t num_linvars;
    float x[NUM_DATA_ARRAY];
} INPUT01_t;

/* Typedefs for Input 2 */
enum {
    INP02_LV_LOW = 0,
    INP02_LV_MID,
    INP02_LV_HIGH
}; typedef uint8_t INP02_LINVARS_e;

typedef struct {
    INP02_LINVARS_e name;
    float y[NUM_DATA_ARRAY];
    float value;
} INP02_LINVAR_t;

# define INP02_NUM_LINVARS 3
typedef struct {
    INP02_LINVAR_t linvars[INP02_NUM_LINVARS];
    const uint8_t num_linvars;
    float x[NUM_DATA_ARRAY];
} INPUT02_t;

/* Typedefs for Output */
enum {
    OUT01_LV_LOW = 0,
    OUT01_LV_MID,
    OUT01_LV_HIGH
}; typedef uint8_t OUT01_LINVARS_e;

typedef struct {
    OUT01_LINVARS_e name;
    float y[NUM_DATA_ARRAY];
    float value;
} OUT01_LINVAR_t;

# define OUT01_NUM_LINVARS 3
typedef struct {
    OUT01_LINVAR_t linvars[OUT01_NUM_LINVARS];
    const uint8_t num_linvars;
    float x[NUM_DATA_ARRAY];
} OUTPUT01_t;

/*Typedef for Logic elements*/
typedef struct {
//    const INPUT01_t * inp1;
//    const INPUT02_t * inp2;
//    const OUTPUT01_t * out;
    const OUT01_LINVARS_e logic[INP02_NUM_LINVARS][INP01_NUM_LINVARS];
    const INFERENCE_e logic_inference[INP02_NUM_LINVARS][INP01_NUM_LINVARS];
    const INFERENCE_e inference; // hardcode
}FUZZY_LOGIC_ELEMENT01_t;

#define NUM_OUTPUT01_ELEMENTS 1
typedef struct {
    float linvar_low[NUM_OUTPUT01_ELEMENTS];
    float linvar_mid[NUM_OUTPUT01_ELEMENTS];
    float linvar_high[NUM_OUTPUT01_ELEMENTS];
} OUTPUT01_ELEMENT_RESULTS_t;


#define NUM_INPUTS 2
#define NUM_OUTPUTS 1
typedef struct {
    const INFERENCE_e global_inference; // hardcode
    OUTPUT01_ELEMENT_RESULTS_t out01_results;
} FUZZY_CTRL_t;



// IO_STRUCT_t* get_io_struct_ref(void);
// uint8_t calculate_fuzzy(IO_STRUCT_t* input_struct);


#ifdef __cplusplus
}
#endif
#endif //FUZZY_C_FUZZY_CODE_H
