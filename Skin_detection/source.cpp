#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>

void flap_detector(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int mean_hue, int mean_lightness, int mean_saturation, int hue_threshold, int lightness_threshold, int saturation_threshold){

	#pragma HLS INTERFACE s_axilite port=return

	////////////////////////////////////////////////////
	///////////////HAND POSITION DETECTION//////////////
	////////////////////////////////////////////////////

	for (int i = 0; i < h; ++i) {

		for (int j = 0; j < w; ++j) {

			unsigned int current = *in_data++;

			unsigned char in_r = current & 0xFF;
			unsigned char in_g = (current >> 8) & 0xFF;
			unsigned char in_b = (current >> 16) & 0xFF;

			unsigned char out_r = 0;
			unsigned char out_b = 0;
			unsigned char out_g = 0;

			//Cmax

			int Cmax;

			if (in_r >= in_g && in_r >= in_b){
				Cmax = in_r;
			}

			else if (in_b >= in_r && in_b >= in_g){
				Cmax = in_b;
			}

			else if (in_g >= in_r && in_g >= in_b){
				Cmax = in_g;
			}

			//Cmin

			int Cmin;

			if (in_r <= in_g && in_r <= in_b){
				Cmin = in_r;
			}

			else if (in_b <= in_r && in_b <= in_g){
				Cmin = in_b;
			}

			else if (in_g <= in_r && in_g <= in_b){
				Cmin = in_g;
			}

			// delta

			int delta = abs(Cmax - Cmin);

			//lightness

			int lightness = (Cmax + Cmin) / 2;

			//hue

			int hue;

			if (delta == 0){
				hue = 0;
			}

			else if (Cmax == in_r){
				hue = (((in_g - in_b)/delta)%6)* 60;
			}

			else if (Cmax == in_g){
				hue = (((in_b - in_r)/delta)+2)* 60;
			}

			else if (Cmax == in_b){
				hue = (((in_r - in_g)/delta)+4)* 60;
			} else{
				std::cout<<"ERROR HUE"<<std::endl;
			}

			//saturation
			int saturation;
			if(lightness != 0){
				saturation = (100*  delta) / (Cmax + Cmin);
			}else{
				saturation = 0;
			}



			//checking the value fits

			if ((saturation <= (mean_saturation + saturation_threshold)) && (saturation >= (mean_saturation - saturation_threshold))){
				if (hue <= (mean_hue + hue_threshold) && hue >= (mean_hue - hue_threshold)){
					if (lightness <= (mean_lightness + lightness_threshold) || lightness >= (mean_lightness - lightness_threshold)){
						*out_data++ = 0xFFFFFF;
					}else{
						*out_data++ = 0;
					}
				}else{
					*out_data++ = 0;
				}
			}

			else{
				*out_data++ = 0;
			}
		}
	}
}
