`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company:       	UCD School of Electrical and Electronic Engineering
// Student:   		Fergal Kilgannon
// Student num:	  	19315126
// Project:       	CNN Hardware-Software Codesign
// Description:   	Digital Multiply-and-Accumulate module testbench
// Last edited:   	26th December 2023
//////////////////////////////////////////////////////////////////////////////////

module TBlinearMAC;

	reg clock, reset, enable;
	reg [15:0] data_in, weight_in;
	
	wire [16:0] result;
	
// Instantiate top level module
	digital_MAC uut (
		.clock(clock),
		.data_in(data_in),
		.weight_in(weight_in),
		.reset(reset),
      	.enable(enable),
		.data_out(result)
	);

// Generate clock signal at 5 MHz
	initial 
		begin
			clock = 1'b0;  // clock starts at 0
			forever
				#100 clock = ~clock;	// invert clock every 50 ns
		end
		
	initial 
      begin
		reset = 1'b0;
		data_in = 15'b0;
		weight_in = 15'b0;
        enable = 1'b0;
		
		#100;
		reset = 1'b1;
      	@ (negedge clock);
      	@ (negedge clock) reset = 1'b0;
		
		#400;
		data_in = 15'd1;
		weight_in = 15'd1;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = 15'd2;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = -15'd1;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = 15'd127;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		reset = 1'b1;
      	@ (negedge clock);
      	@ (negedge clock) reset = 1'b0;
        
        #200;
		data_in = 15'd1;
		weight_in = 15'd24;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
      end
      
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(2);
  end
  
endmodule`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company:       	UCD School of Electrical and Electronic Engineering
// Student:   		Fergal Kilgannon
// Student num:	  	19315126
// Project:       	CNN Hardware-Software Codesign
// Description:   	Digital Multiply-and-Accumulate module testbench
// Last edited:   	26th December 2023
//////////////////////////////////////////////////////////////////////////////////

module TBlinearMAC;

	reg clock, reset, enable;
	reg [15:0] data_in, weight_in;
	
	wire [16:0] result;
	
// Instantiate top level module
	digital_MAC uut (
		.clock(clock),
		.data_in(data_in),
		.weight_in(weight_in),
		.reset(reset),
      	.enable(enable),
		.data_out(result)
	);

// Generate clock signal at 5 MHz
	initial 
		begin
			clock = 1'b0;  // clock starts at 0
			forever
				#100 clock = ~clock;	// invert clock every 50 ns
		end
		
	initial 
      begin
		reset = 1'b0;
		data_in = 15'b0;
		weight_in = 15'b0;
        enable = 1'b0;
		
		#100;
		reset = 1'b1;
      	@ (negedge clock);
      	@ (negedge clock) reset = 1'b0;
		
		#400;
		data_in = 15'd1;
		weight_in = 15'd1;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = 15'd2;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = -15'd1;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		data_in = 15'd1;
		weight_in = 15'd127;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
        #400;
		reset = 1'b1;
      	@ (negedge clock);
      	@ (negedge clock) reset = 1'b0;
        
        #200;
		data_in = 15'd1;
		weight_in = 15'd24;
        enable = 1'b1;
      	@ (negedge clock);
        @ (negedge clock) enable = 1'b0;
        
      end
      
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(2);
  end
  
endmodule