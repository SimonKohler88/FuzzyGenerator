#ifndef FUZZY_MATH_H_INCLUDED
#define FUZZY_MATH_H_INCLUDED


# include <stdint.h>

float interpolate(float input_x, const float input_x_array[], const float input_y_array[], uint16_t len_arrays);
float maxf(float val1, float val2);
float minf(float val1, float val2);
float max_array(float arrayf[], uint16_t len);
float min_array(float arrayf[], uint16_t len);
void max_array_array(float array1[], float array2[], float array_result[], uint16_t len);
void min_array_array(float array1[], float array2[], float array_result[], uint16_t len);
void max_array_value(float array1[], float value, float array_result[], uint16_t len);
void min_array_value(float array1[], float value, float array_result[], uint16_t len);
float centre_of_gravity(float x_array[], float y_array[], uint16_t len);
#endif // FUZZY_MATH_H_INCLUDED
