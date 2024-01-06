module syncRAM( input [7:0] dataIn,
                output reg [7:0] dataOut,
                input [3:0] kernAddr,
                input [5:0] pixAddr, 
                input CS, WE, RD, Clk
              );

    
    //internal variables
    reg [7:0] SRAM [3:0] [5:0];

    always @ (posedge Clk)
        begin
            if (CS == 1'b1) begin
                if (WE == 1'b1 && RD == 1'b0) begin
                  SRAM [kernAddr][pixAddr] = dataIn;
                    end
                else if (RD == 1'b1 && WE == 1'b0) begin
                  dataOut = SRAM [kernAddr][pixAddr]; 
                end
                else;
            end
            else;
        end

endmodule