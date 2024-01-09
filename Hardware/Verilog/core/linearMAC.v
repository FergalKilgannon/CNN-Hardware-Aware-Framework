`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company:       	UCD School of Electrical and Electronic Engineering
// Student:      	Fergal Kilgannon
// Student num:	  	19315126
// Project:       	CNN Hardware-Software Codesign
// Description:   	Digital Multiply-and-Accumulate module
// Last edited:   	26th December 2023
//////////////////////////////////////////////////////////////////////////////////

module digital_MAC(
	input clock,
  	input signed [7:0] data_in,
  	input signed [7:0] weight_in,
	input reset,
  	input enable,
  	output reg signed [16:0] data_out
	);
	
	
  	always @ (posedge clock)
    	if (reset)
			data_out <= 1'b0;
		else
      		data_out <= enable ? data_out + (data_in * weight_in): data_out;
    
endmodule