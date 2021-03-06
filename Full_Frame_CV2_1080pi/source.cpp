#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>


void flap_detector(volatile uint32_t* in_hand, volatile uint32_t* out_data, uint16_t* mean_height, bool* flap, bool* rise, uint8_t colour_threshold, uint8_t height_threshold){


#pragma HLS INTERFACE s_axilite port=returns

#pragma HLS INTERFACE m_axi depth=2073600 port=in_hand offset=slave // This will NOT work for resolutions higher than 1080p

#pragma HLS INTERFACE m_axi depth=2073600 port=out_data offset=slave

	/*
	 * Different dimensions:
	 *
	 * Format: W x H
	 *
	 * Output frame (out_data): 1920x1080
	 * HDMI_in (in_hand): 1920x1080 (used region is top-left quarter 960x540)
	 * Detected hand: 960x540
	 */

	////////////////////////////////////////////////////
	///////////////HAND POSITION DETECTION//////////////
	////////////////////////////////////////////////////
	int total_height = 0;
	int pixel_number = 0;

	int previous_mean_height = *mean_height;

	// scan top-left quarter only

	for(int i = 0; i < 518400; i++){

		unsigned int index = i + 960*(int)(i/960);

		unsigned int current = in_hand[index];

		out_data[index] = current;

		unsigned char in_r = current & 0xFF;
		unsigned char in_g = (current >> 8) & 0xFF;
		unsigned char in_b = (current >> 16) & 0xFF;

		unsigned char out_r = 0;
		unsigned char out_b = 0;
		unsigned char out_g = 0;

		if((in_g > (in_r + colour_threshold)) & (in_g > (in_b + colour_threshold))){

			total_height += (1080-(int)(i/1920)); //i starts from the top, so the pixel height would be total height minus i;
			pixel_number ++;

			out_data[index] = 0xFFFFFF;
		}

		else{
			out_data[index] = 0;
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
