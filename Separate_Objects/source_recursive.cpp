#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>
#include <vector>


void mark_pixel(int x, int y, int color, bool (&detection)[360][640], volatile uint32_t* &in_hand) {
	if (x < 0 || x == 640) return;
	if (y < 0 || y == 360) return;
	if (!detection[y][x]) return;

	// mark the current pixel
	detection[y][x] = 0;
	in_hand[y*1280+x+460800] = color;

	// recursively mark the neighbors
	mark_pixel(x+1, y, color, detection, in_hand);
	mark_pixel(x, y+1, color, detection, in_hand);
	mark_pixel(x-1, y, color, detection, in_hand);
	mark_pixel(x, y-1, color, detection, in_hand);
	
}

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
	unsigned int colors[] = {
			0x0000FF, 0x00FF00, 0xFF0000,
			0x00FFFF, 0xFF00FF, 0xFFFF00,
			0xFFFFFF};
	uint8_t color_i = 0;
	i_loop: for (uint16_t i = 0; i < 360; ++i){
			j_loop: for (uint16_t j = 0; j < 640; ++j){
				if (detection[i][j]){
					mark_pixel(i, j, color, detection, hand);
					color_i = color_i+1;
					color_i = color_i%7;
				}

}
