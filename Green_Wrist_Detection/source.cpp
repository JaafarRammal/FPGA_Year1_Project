#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>

void flap_detector(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int* mean_height, bool* flap, bool* rise, int colour_threshold, int height_threshold){

	#pragma HLS INTERFACE s_axilite port=return

	////////////////////////////////////////////////////
	///////////////HAND POSITION DETECTION//////////////
	////////////////////////////////////////////////////
	int total_height = 0;
	int pixel_number = 0;

	int previous_mean_height = *mean_height;

	for (int i = 0; i < h; ++i) {

		for (int j = 0; j < w; ++j) {
			
			unsigned int current = *in_data++;

			unsigned char in_r = current & 0xFF;
			unsigned char in_g = (current >> 8) & 0xFF;
			unsigned char in_b = (current >> 16) & 0xFF;

			unsigned char out_r = 0;
			unsigned char out_b = 0;
			unsigned char out_g = 0;

			if((in_g > (in_r + colour_threshold)) & (in_g > (in_b + colour_threshold))){

				total_height += (h-i); //i starts from the top, so the pixel height would be total height minus i;
				pixel_number ++;

				*out_data++ = 0xFFFFFF;
			}

			else{
				*out_data++ = 0;
			}
		}
	}

	*mean_height = total_height / pixel_number;

	////////////////////////////////////////////////////
	///////////////////FLAP DETECTION///////////////////
	////////////////////////////////////////////////////

	if((previous_mean_height > (*mean_height + height_threshold)) & (*rise == true)){

		*flap = true;
		*rise = false;
	}
		
	if((*mean_height > (previous_mean_height + height_threshold)) & (*rise == false)){

		*rise = false;
	}
}
