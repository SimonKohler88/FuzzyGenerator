#ifndef FUZZY_INTERFACE_H_INCLUDED
#define FUZZY_INTERFACE_H_INCLUDED

# include <stdint.h>
# include "fuzzy_math.h"
// # include "fuzzy_interface.h"

/* Data definitions */
# define FLOAT float
# define UINT8 uint8_t
# define UINT16 uint16_t


typedef struct {
    float input01;
    float input02;
    float output01;
} IO_STRUCT_t;

/* Common typedefs / global defines */
// enum {
//     INF_MIN = 0,
//     INF_MAX,
//     INF_IGNORE
// }; typedef UINT8 INFERENCE_e;
//
// enum {
//     ERR_NONE = 0,
//     ERR_YES,
// }; typedef UINT8 ERROR_CODE_e;
//
//
uint8_t calculate_fuzzy(IO_STRUCT_t *io_struct);


#endif // FUZZY_INTERFACE_H_INCLUDED
