module image_SRAM(  input [7:0] dataIn,
                    output reg [7:0] dataOut,
                    input [3:0] addr,
                    input CS, WE, RD, Clk
              );

    
    //internal variables
    reg [7:0] SRAM [27:0];

    always @ (posedge Clk)
        begin
            if (CS == 1'b1) begin
                if (WE == 1'b1 && RD == 1'b0) begin
                  SRAM [addr] = dataIn;
                    end
                else if (RD == 1'b1 && WE == 1'b0) begin
                  dataOut = SRAM [addr]; 
                end
                else;
            end
            else;
        end

endmodule