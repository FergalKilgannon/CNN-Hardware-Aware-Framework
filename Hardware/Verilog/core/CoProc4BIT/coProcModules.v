module cpState (input clock, reset,
                input enable, weightsPulled, dataSent, blockDone, imageDone, cumulationDone,
                output weights, data, result, sendOutput);
  
  reg [2:0] currState, nextState;
  
  localparam [2:0]  IDLE = 3'b000,
  					WEIGHTS = 3'b001,
  					DATA = 3'b010,
  					RESULT = 3'b011,
  					OUTPUT = 3'b100;

  always @ (posedge clock)
    begin
      if (reset)
        currState <= IDLE; // state set to IDLE
      else
        currState <= nextState; // update state
    end
  
  always @ (currState, enable, weightsPulled, dataSent, blockDone, imageDone, resultsFound, cumulationDone)
    case (currState)
      IDLE: if (enable) nextState = WEIGHTS;
      		else nextState = IDLE;
      
      WEIGHTS: 	if (!enable) nextState = IDLE;
      			else if (weightsPulled) nextState = DATA;
      			else nextState = WEIGHTS;
      
      DATA:		if (!enable) nextState = IDLE;
                else if (dataSent) nextState = RESULT;
                else nextState = DATA;
      
      RESULT:	if (!enable) nextState = IDLE;
      			else if (!resultsFound) nextState = RESULT;
      			else if (imageDone) nextState = OUTPUT;
      			else if (blockDone) nextState = WEIGHTS;
                else nextState = DATA;
      
      OUTPUT:	if (!enable || cumulationDone) nextState = IDLE;
      			else nextState = OUTPUT;
        
      default: nextState = IDLE; // safe design
  	endcase
  
  assign weights = (currState == WEIGHTS);
  assign data = (currState == DATA);
  assign result = (currState == RESULT);
  assign sendOutput = (currState == OUTPUT);
  
endmodule



module counter(input [7:0] maxCount, countUp, reset, clock,
                     output done);
  reg [7:0] ct;
  wire [7:0] nextCt;
  
  always @ (posedge clock)
    if (reset) ct <= 8'd0;
  	else ct <= nextCt;
  
  assign nextCt = countUp ? (ct + 8'd1) : 8'd0;
  
  assign done = (ct == maxCount);
endmodule



module subblockSRAM( input [7:0] dataIn,
                    output reg [7:0] dataOut,
                    input [4:0] block,
                    input [4:0] ofmapAddr,
                    input [5:0] XpixAddr,
                    input [5:0] YpixAddr,
                    input CS, WE, RD, Clk
              );

    localparam IFMAPS = 16;
    localparam XPIX = 32;
  	localparam YPIX = 32;
  	localparam MAXBLOCKS = 16;
    
    //internal variables
  	reg [7:0] SRAM [MAXBLOCKS-1:0] [IFMAPS-1:0] [XPIX-1:0] [YPIX-1:0];

    always @ (posedge Clk)
        begin
          if (CS == 1'b1) begin
            if (WE == 1'b1 && RD == 1'b0) begin
              SRAM [block][ofmapAddr][XpixAddr][YpixAddr] = dataIn;
                end
            else if (RD == 1'b1 && WE == 1'b0) begin
              dataOut = SRAM [block][ofmapAddr][XpixAddr][YpixAddr]; 
            end
            else begin
              dataOut = 8'b0;
            end
            else;
          end
        end

endmodule