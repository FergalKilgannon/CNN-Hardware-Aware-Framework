`timescale 1ns / 1ps

module stateTB;
  
  // Inputs
  reg clk, reset, enable, weightsPulled, dataSent, blockDone, imageDone;

  // Outputs
  wire weights, data, result;
  
  cpState uut (
    .clock(clk),
    .reset(reset),
    .enable(enable),
    .weightsPulled(weightsPulled),
    .dataSent(dataSent),
    .blockDone(blockDone),
    .imageDone(imageDone),
    
    .weights(weights),
    .data(data),
    .result(result)
  );
  
  initial begin
    
    // Initialize inputs
    clk = 1'b0;
    reset = 1'b0;
    enable = 1'b0;
    weightsPulled = 1'b0;
    dataSent = 1'b0;
    blockDone = 1'b0;
    imageDone = 1'b0;
    
    #20;
   	reset = 1'b1;
    #100;
    reset = 1'b0;
    #40;

    enable = 1'b1;			// Move to WEIGHTS
    #40;
	dataSent = 1'b1;
    #40;
    dataSent = 1'b0;
    #40;
    
    weightsPulled = 1'b1;	// Move to DATA
    #40;
    weightsPulled = 1'b0;
    #40;
    
    enable = 1'b0;			// Move to IDLE
    #40;
    
    enable = 1'b1;			// Move to WEIGHTS
    #40;
    
    weightsPulled = 1'b1;	// Move to DATA
    #40;
    
    dataSent = 1'b1;		// Move to RESULT
    #20;
    
    dataSent = 1'b0;		// Move to DATA
    #40;
    
    dataSent = 1'b1;		// Move to RESULT
    #20;
    
    blockDone = 1'b1;		// Move to WEIGHT
    weightsPulled = 1'b0;
    dataSent = 1'b0;
    #20;
    
    blockDone = 1'b0;
    #40;
    
    weightsPulled = 1'b1;	// Move to DATA
    #40;
    
    dataSent = 1'b1;		// Move to RESULT
    #20;
    
    imageDone = 1'b1;		// Move to IDLE
    #20;
    
    enable = 1'b0;
    #20;
    
    $stop;

  end
  
  always #10 clk = ~clk;

  initial begin
   $dumpfile("dump.vcd");
   $dumpvars(2);
  end
  
endmodule