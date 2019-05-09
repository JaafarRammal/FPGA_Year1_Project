#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>


void flap_detector(volatile uint32_t* in_hand, uint16_t* mean_height, uint8_t colour_threshold){

#pragma HLS INTERFACE s_axilite port=returns
#pragma HLS INTERFACE m_axi depth=921600 port=in_hand offset=slave

	/*
	 * Different dimensions:
	 *
	 * Format: W x H
	 *
	 * HDMI_in (in_hand): 1280x720 (used region is top-left quarter 640x360)
	 * Detected hand: 640x360
	 * Output: 1280x720
	 */

	unsigned int total_height = 0;
	unsigned int pixel_number = 0;

	loop:for(int i = 0; i < 460799; i++){

			#pragma HLS PIPELINE II=2

			if(i%1280 < 640){

				unsigned int current = in_hand[i];

				unsigned char in_r = current & 0xFF;
				unsigned char in_g = (current >> 8) & 0xFF;
				unsigned char in_b = (current >> 16) & 0xFF;

				if((in_g > (in_r + colour_threshold)) & (in_g > (in_b + colour_threshold))){

					total_height += i/1280;
					pixel_number ++;

					in_hand[i+460799] = 0xFFFFFF;
				}

				else{
					in_hand[i+460799] = 0;
				}
			}


		}

	*mean_height = total_height / pixel_number;

}
