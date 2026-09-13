
# include "fuzzy_math.h"
# include <stdio.h>

float interpolate(float input_x, const float input_x_array[], const float input_y_array[], uint16_t len_arrays)
{
    uint16_t i;
    uint16_t idx = -1;
    float result = 0;

    if (input_x < input_x_array[0]) return input_y_array[0];
    if (input_x > input_x_array[len_arrays-1]) return input_y_array[len_arrays-1];

    for (i=0; i< len_arrays; i++)
    {
        //printf("%f, %f, %d, %d\n", input_x , input_x_array[i], i, len_arrays);
        if (input_x > input_x_array[i]) continue;
        else if (input_x == input_x_array[i]) return input_y_array[i];

        idx = i-1;
        break;

    }
    //printf("idx: %d,i: %d, len: %d \n ",idx, i, len_arrays);
    if ((idx >= len_arrays) || idx==-1)
    {
        result = input_y_array[len_arrays-1];
        return result;
    }

    //yp = y0 + ((y1-y0)/(x1-x0)) * (xp - x0);
    float dx = input_x_array[idx+1] - input_x_array[idx];
    float dy = input_y_array[idx+1] - input_y_array[idx];
    float ln = input_x - input_x_array[idx];
    //printf("dx: %f, dy: %f, ln: %f \n", dx, dy, ln);
    result = input_y_array[idx] + dy/dx *ln;
    //printf("result: %f \n", result);

    return result;
}

float centre_of_gravity(float x_array[], float y_array[], uint16_t len)
{
    float sum_y = 0;
    float sum_weighted = 0;
    float result = 0;
    uint16_t i;
    for (i=0;i< len;i++) sum_y += y_array[i];

    if (sum_y == 0 ) return 0;

    for (i=0;i< len;i++) sum_weighted += y_array[i] * x_array[i];
    result = sum_weighted / sum_y;
    return result;
}

void min_array_value(float array1[], float value, float array_result[], uint16_t len)
{
    uint16_t i;
    for (i=0; i< len; i++)
    {
        if (array1[i] < value) array_result[i] = array1[i];
        else array_result[i] = value;
    }
}

void max_array_value(float array1[], float value, float array_result[], uint16_t len)
{
    uint16_t i;
    for (i=0; i< len; i++)
    {
        if (array1[i] > value) array_result[i] = array1[i];
        else array_result[i] = value;
    }
}

void min_array_array(float array1[], float array2[], float array_result[], uint16_t len)
{
    uint16_t i;
    for (i=0; i< len; i++)
    {
        if (array1[i] < array2[i]) array_result[i] = array1[i];
        else array_result[i] = array2[i];
    }
}

void max_array_array(float array1[], float array2[], float array_result[], uint16_t len)
{
    uint16_t i;
    for (i=0; i< len; i++)
    {
        if (array1[i] > array2[i]) array_result[i] = array1[i];
        else array_result[i] = array2[i];
    }
}

float min_array(float arrayf[], uint16_t len)
{
    float res = 0;
    uint16_t i;
    for (i=0; i< len; i++) if ((arrayf[i] < res) || (i == 0)) res = arrayf[i];
    return res;
}

float max_array(float arrayf[], uint16_t len)
{
    float res = 0;
    uint16_t i;
    for (i=0; i< len; i++) if ((arrayf[i] > res) || (i == 0)) res = arrayf[i];
    return res;
}

float minf(float val1, float val2)
{
    if (val1 > val2) return val2;
    return val1;
}

float maxf(float val1, float val2)
{
    if (val1 > val2) return val1;
    return val2;
}

