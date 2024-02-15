module weight_SRAM( input [7:0] dataIn,
                    output reg [7:0] dataOut,
                    input [3:0] kernAddr,
                    input [5:0] pixAddr, 
                    input CS, WE, RD, ifmaps, pixels, Clk
              );

    localparam IFMAPS = 16;
    localparam PIXELS = 25;
    
    //internal variables
    reg [7:0] SRAM [IFMAPS-1:0] [PIXELS-1:0];

    always @ (posedge Clk)
        begin
          if (CS == 1'b1) begin
            if (ifmaps == 1'b1) begin
              dataOut = 8'd16;
            end
            else if (pixels == 1'b1) begin
              dataOut = 8'd16;
            end
            else if (WE == 1'b1 && RD == 1'b0) begin
              SRAM [kernAddr][pixAddr] = dataIn;
                end
            else if (RD == 1'b1 && WE == 1'b0) begin
              dataOut = SRAM [kernAddr][pixAddr]; 
            end
            else begin
              dataOut = 8'b0;
            end
            else;
          end
        end

endmodule