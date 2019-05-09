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

void flap_detector(volatile uint32_t* in_hand, uint16_t* mean_height, uint8_t colour_threshold);

int main() {

	//Hand input
	cv::Mat hand_src = cv::imread("/home/jr4918/720piCV2/test_files/in1.jpg", CV_LOAD_IMAGE_UNCHANGED);
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

	std::cout<<"Executing..."<<std::endl;

	uint16_t mean_height =700;
	bool flap = false;
	bool rise = true;

    flap_detector((volatile uint32_t *)hand_im, &mean_height, 29);

    std::cout<<"Writing..."<<std::endl;
	for (int i=0; i<1280*720; i++){
		hand_data[3*i + 2] = hand_im[4*i + 0];
		hand_data[3*i + 1] = hand_im[4*i + 1];
		hand_data[3*i + 0] = hand_im[4*i + 2];
	}
	std::cout<<"Success! Exporting..."<<std::endl;

	//Specify an Absolute Path for Storing Output Image
	cv::imwrite("/home/jr4918/720piCV2/test_files/out1.jpg",hand_src);

	free(hand_im);

	std::cout<<"Done!"<<std::endl;

	return 0;

}
