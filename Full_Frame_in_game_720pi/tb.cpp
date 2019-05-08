#include <ap_fixed.h>
#include <ap_int.h>
#include <cassert>
#include <iostream>

#include <hls_opencv.h>

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

void flap_detector(volatile uint32_t* in_hand, volatile uint32_t* in_game, volatile uint32_t* out_data, int* mean_height, bool* flap, bool* rise, int colour_threshold, int height_threshold);

int main() {

	//Game input
	cv::Mat game_src = cv::imread("/home/jr4918/perso/game.jpg", CV_LOAD_IMAGE_UNCHANGED);
	std::cout << "Game Image type: " << game_src.type() << ", no. of channels: " << game_src.channels() << std::endl;
	std::cout<<" Game Image size  "<<game_src.size()<<std::endl;
	uchar *game_data = game_src.data;
	uchar *game_im = (uchar *)malloc(640*720*4);
	for (int i=0; i<640*720; i++){
		game_im[4*i + 0] = game_data[3*i + 2]; //R - R
		game_im[4*i + 1] = game_data[3*i + 1]; // B - B
		game_im[4*i + 2] = game_data[3*i + 0]; // G - G
		game_im[4*i + 3] = 0;
	}

	//Hand input
	cv::Mat hand_src = cv::imread("/home/jr4918/perso/hand.jpg", CV_LOAD_IMAGE_UNCHANGED);
	std::cout << "Hand Image type: " << hand_src.type() << ", no. of channels: " << hand_src.channels() << std::endl;
	std::cout<<" Hand Image size  "<<hand_src.size()<<std::endl;
	uchar *hand_data = hand_src.data;
	uchar *hand_im = (uchar *)malloc(1280*720*4);
	for (int i=0; i<1280*720; i++){
		hand_im[4*i + 0] = hand_data[3*i + 2]; //R - R
		hand_im[4*i + 1] = hand_data[3*i + 1]; // B - B
		hand_im[4*i + 2] = hand_data[3*i + 0]; // G - G
		hand_im[4*i + 3] = 0;
	}



	//Output
	cv::Mat out_src = cv::imread("/home/jr4918/perso/out.jpg", CV_LOAD_IMAGE_UNCHANGED);
	std::cout << "Out Image type: " << out_src.type() << ", no. of channels: " << hand_src.channels() << std::endl;
	std::cout<<" Out Image size  "<<out_src.size()<<std::endl;
	uchar *out_data = out_src.data;
	uchar *out_im = (uchar *)malloc(720*1280*4);

	std::cout<<"Executing..."<<std::endl;

	int mean_height =700;
	bool flap = false;
	bool rise = true;

    flap_detector((volatile uint32_t *)hand_im, (volatile uint32_t *)game_im, (volatile uint32_t *)out_im, &mean_height, &flap, &rise, 29, 50);

    std::cout<<"Writing..."<<std::endl;
	for (int i=0; i<1280*720; i++){
		out_data[3*i + 2] = out_im[4*i + 0];
		out_data[3*i + 1] = out_im[4*i + 1];
		out_data[3*i + 0] = out_im[4*i + 2];
	}
	std::cout<<"Success!"<<std::endl;

	//Specify an Absolute Path for Storing Output Image
	cv::imwrite("/home/jr4918/perso/final.jpg",out_src);

	free(hand_im);
	free(game_im);
	free(out_im);

	return 0;

}


