module image_SRAM(  input [7:0] dataIn,
                    output reg [7:0] dataOut,
                    input [3:0] addr,
                    input CS, WE, RD, pixels, Clk
              );

  localparam PIXELS = 28;
  
  //internal variables
  reg [7:0] SRAM [PIXELS-1:0];

  always @ (posedge Clk)
      begin
        if (CS == 1'b1) begin
          if (pixels == 1'b1) begin
              dataOut = 8'd28;
          end
          if (WE == 1'b1 && RD == 1'b0) begin
            SRAM [addr] = dataIn;
              end
          else if (RD == 1'b1 && WE == 1'b0) begin
            dataOut = SRAM [addr]; 
          end
          else begin
            dataOut = 8'b0;
          end
        end
        else;
      end

endmodule