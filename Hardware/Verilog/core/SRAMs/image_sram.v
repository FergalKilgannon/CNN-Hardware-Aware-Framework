module image_SRAM(  input [7:0] dataIn,
                    output reg [7:0] dataOut,
                    input [3:0] addrX,
                    input [3:0] addrY,
                    input [3:0] addrC,
                    input CS, WE, RD, Xpixels, Ypixels, channels, Clk
              );

  localparam XPIX = 28;
  localparam YPIX = 28;
  localparam CHANNELS = 1;
  
  //internal variables
  reg [7:0] SRAM [CHANNELS-1:0] [XPIX-1:0] [YPIX-1:0];

  always @ (posedge Clk)
      begin
        if (CS == 1'b1) begin
          if (Xpixels == 1'b1) begin
              dataOut = 8'd28;
          end
          if (Ypixels == 1'b1) begin
              dataOut = 8'd28;
          end
          if (channels == 1'b1) begin
              dataOut = 8'd1;
          end
          if (WE == 1'b1 && RD == 1'b0) begin
            SRAM [addrC] [addrX] [addrY]= dataIn;
              end
          else if (RD == 1'b1 && WE == 1'b0) begin
            dataOut = SRAM [addrC] [addrX] [addrY]; 
          end
          else begin
            dataOut = 8'b0;
          end
        end
        else;
      end

endmodule