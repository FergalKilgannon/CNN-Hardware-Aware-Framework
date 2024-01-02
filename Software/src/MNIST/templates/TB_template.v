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
	reg [7:0] data_in, weight_in;
	
	wire [16:0] result;
  
  // Integer variable to count errors
	integer error_count;
	
// Instantiate top level module
	digital_MAC uut (
		.clock(clock),
		.data_in(data_in),
		.weight_in(weight_in),
		.reset(reset),
      	.enable(enable),
		.data_out(result)
	);

// Generate clock signal at 250 MHz
	initial 
		begin
			clock = 1'b0;  // clock starts at 0
			forever
				#4 clock = ~clock;	// invert clock every 4 ns
		end
		
	initial 
      begin
				reset = 1'b0;
				data_in = 15'b0;
				weight_in = 15'b0;
        enable = 1'b0;
        error_count = 0;	// initialise error counter
        
        #4;
				reset = 1'b1;
      	@ (negedge clock);
      	@ (negedge clock) reset = 1'b0;
		
		// Start of custom

        
        $display("Simulation finished with %d errors", error_count);
				$stop;
        
      end
  
  // Task to simulate key press
  task MULT ( input [15:0] data_fed, input [15:0] weight_fed );
		begin
			data_in = data_fed;
			weight_in = weight_fed;
        	enable = 1'b1;
        	@ (negedge clock) enable = 1'b0;
		end
	endtask
	
			
// Task to check output
  task CHECK_ACCUM ( input [15:0] expResult );
		begin
          
          if (result !== expResult)
				begin
					error_count = error_count + 1;
				end
          reset = 1'b1;
    	@ (negedge clock);
    	@ (negedge clock) reset = 1'b0;
		end
	endtask
	
      
  initial begin
    $dumpfile("dump.vcd");
    $dumpvars(2);
  end
endmodule