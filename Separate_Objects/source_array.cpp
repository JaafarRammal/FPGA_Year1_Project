#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>
#include <vector>


void flap_detector(volatile uint32_t* in_hand, uint8_t colour_threshold){

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

	bool detection[360][640];

	detect_loop:for(int i = 0; i < 460800; i++){

			if(i%1280 < 640){

				unsigned int current = in_hand[i];

				unsigned char in_r = current & 0xFF;
				unsigned char in_g = (current >> 8) & 0xFF;
				unsigned char in_b = (current >> 16) & 0xFF;

				if((in_g > (in_r + colour_threshold)) & (in_g > (in_b + colour_threshold))){
					detection[i/1280][i%640]= 1;
				}

				else{
					in_hand[i+460800] = 0;
				}
			}

		}
		uint16_t queue_arr[115200];
		unsigned int colors[] = {
				0x0000FF, 0x00FF00, 0xFF0000,
				0x00FFFF, 0xFF00FF, 0xFFFF00,
				0xFFFFFF};
		uint8_t color_i = 0;
		i_loop: for (uint16_t i = 0; i < 360; ++i){
			j_loop: for (uint16_t j = 0; j < 640; ++j){
				if (detection[i][j]){

					int add_pt = 0;
					int read_pt = 0;

					queue_arr[add_pt++%115200] = j;
					queue_arr[add_pt++%115200] = i;

					color:while (read_pt != add_pt){
						// get current pixel
						uint16_t x = queue_arr[read_pt++%115200];
						uint16_t y = queue_arr[read_pt++%115200];

						// validate or skip
						if(detection[y][x] && x>0 && x!=640 && y>0 && y!=360){

							in_hand[y*1280+x+460800] = colors[color_i];
							detection[y][x] = 0;

							queue_arr[add_pt++%115200] = x+1;
							queue_arr[add_pt++%115200] = y;

							queue_arr[add_pt++%115200] = x;
							queue_arr[add_pt++%115200] = y+1;

							queue_arr[add_pt++%115200] = x-1;
							queue_arr[add_pt++%115200] = y;

							queue_arr[add_pt++%115200] = x;
							queue_arr[add_pt++%115200] = y-1;


						}

					}
					color_i = color_i+1;
					color_i = color_i%7;
				}
			}
		}

}
