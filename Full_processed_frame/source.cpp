#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>

typedef ap_uint<8> pixel_type;
typedef ap_int<8> pixel_type_s;
typedef ap_uint<96> u96b;
typedef ap_uint<32> word_32;
typedef ap_ufixed<8,0, AP_RND, AP_SAT> comp_type;
typedef ap_fixed<10,2, AP_RND, AP_SAT> coeff_type;

struct pixel_data {
	pixel_type blue;
	pixel_type green;
	pixel_type red;
};


void flap_detector(volatile uint32_t* in_hand, volatile uint32_t* in_game, volatile uint32_t* out_data, int* mean_height, bool* flap, bool* rise, int colour_threshold, int height_threshold){


#pragma HLS INTERFACE s_axilite port=return

#pragma HLS INTERFACE m_axi depth=2073600 port=in_hand offset=slave // This will NOT work for resolutions higher than 1080p
#pragma HLS INTERFACE m_axi depth=2073600 port=in_game offset=slave // This will NOT work for resolutions higher than 1080p

#pragma HLS INTERFACE m_axi depth=2073600 port=out_data offset=slave

	/*
	 * Different dimensions:
	 *
	 * Format: W x H
	 *
	 * Output frame (out_data): 1280x720
	 * HDMI_in (in_hand): 1280x720 (used region is top-left quarter 640x360)
	 * Detected hand: 640x360
	 * Game frame (in_frame):640x720
	 *
	 * Output distribution:
	 *
	 *//////////////////////////////////////
	  //		    //		      //
	  //    HDMI_in	    //		      //
	  //   (640x360)    //  	      //
	  //		    //	 Game Frame   //
	  ////////////////////	   	      //
	  //		    //	  (640x720)   //
	  //   Detection    //		      //
	  //   (640x360)    //		      //
	  //		    //		      //
	  //////////////////////////////////////


	////////////////////////////////////////////////////
	///////////////HAND POSITION DETECTION//////////////
	////////////////////////////////////////////////////

	int previous_mean_height = *mean_height;

	// w*h = 1280*720 =921600

	unroll:for(int i = 0; i < 921600; i++){

		int game_i = 0;
		int hand_i = 0;

		// three cases for the different output regions

		// if in the left side, it's the game

		if(i%1280 > 639){

			out_data[i] = in_game[i-640*((int)(i/1280))];

		}else{

			if(i<460799){

				unsigned int current = in_hand[i];

				out_data[i] = current;

				unsigned char in_r = current & 0xFF;
				unsigned char in_g = (current >> 8) & 0xFF;
				unsigned char in_b = (current >> 16) & 0xFF;

				unsigned char out_r = 0;
				unsigned char out_b = 0;
				unsigned char out_g = 0;

				if((in_g > (in_r + colour_threshold)) & (in_g > (in_b + colour_threshold))){

					total_height += (720-(int)(i/1280)); //i starts from the top, so the pixel height would be total height minus i;
					pixel_number ++;

					out_data[i+460799] = 0xFFFFFF;
				}

				else{
					out_data[i+460799] = 0;
				}
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
