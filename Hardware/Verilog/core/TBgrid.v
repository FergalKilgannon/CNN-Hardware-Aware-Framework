`timescale 1ns / 1ps

module syncRAM_tb;


 // Inputs

  reg [7:0] dataIn [15:0];
  reg [7:0] weightIn [15:0];
  reg [4:0] addrWeight [15:0];
  reg [15:0] addrEn;
  reg [3:0] addrResult;
  reg [15:0] reset;
  reg WE;
  reg NEWDATA;
  reg COMP;
  reg Clk;
  
  reg [3:0] x;
  reg [3:0] y;


 // Outputs

  wire [16:0] dataOut [15:0];
  
  
  // Integer variable to count errors
	integer error_count;
  


 // Instantiate the Unit Under Test (UUT)

 MACcore uut (
   .data1(dataIn[0]),
   .data2(dataIn[1]),
   .data3(dataIn[2]),
   .data4(dataIn[3]),
   .data5(dataIn[4]),
   .data6(dataIn[5]),
   .data7(dataIn[6]),
   .data8(dataIn[7]),
   .data9(dataIn[8]),
   .data10(dataIn[9]),
   .data11(dataIn[10]),
   .data12(dataIn[11]),
   .data13(dataIn[12]),
   .data14(dataIn[13]),
   .data15(dataIn[14]),
   .data16(dataIn[15]),
   
   .weight1(weightIn[0]),
   .weight2(weightIn[1]),
   .weight3(weightIn[2]),
   .weight4(weightIn[3]),
   .weight5(weightIn[4]),
   .weight6(weightIn[5]),
   .weight7(weightIn[6]),
   .weight8(weightIn[7]),
   .weight9(weightIn[8]),
   .weight10(weightIn[9]),
   .weight11(weightIn[10]),
   .weight12(weightIn[11]),
   .weight13(weightIn[12]),
   .weight14(weightIn[13]),
   .weight15(weightIn[14]),
   .weight16(weightIn[15]),
   
   .addrWeight1(addrWeight[0]),
   .addrWeight2(addrWeight[1]),
   .addrWeight3(addrWeight[2]),
   .addrWeight4(addrWeight[3]),
   .addrWeight5(addrWeight[4]),
   .addrWeight6(addrWeight[5]),
   .addrWeight7(addrWeight[6]),
   .addrWeight8(addrWeight[7]),
   .addrWeight9(addrWeight[8]),
   .addrWeight10(addrWeight[9]),
   .addrWeight11(addrWeight[10]),
   .addrWeight12(addrWeight[11]),
   .addrWeight13(addrWeight[12]),
   .addrWeight14(addrWeight[13]),
   .addrWeight15(addrWeight[14]),
   .addrWeight16(addrWeight[15]),
   
   .dataOut1(dataOut[0]),
   .dataOut2(dataOut[1]),
   .dataOut3(dataOut[2]),
   .dataOut4(dataOut[3]),
   .dataOut5(dataOut[4]),
   .dataOut6(dataOut[5]),
   .dataOut7(dataOut[6]),
   .dataOut8(dataOut[7]),
   .dataOut9(dataOut[8]),
   .dataOut10(dataOut[9]),
   .dataOut11(dataOut[10]),
   .dataOut12(dataOut[11]),
   .dataOut13(dataOut[12]),
   .dataOut14(dataOut[13]),
   .dataOut15(dataOut[14]),
   .dataOut16(dataOut[15]),
   
   .addrEn(addrEn),
   .addrResult(addrResult),
   .reset(reset),
   .WE(WE),
   .NEWDATA(NEWDATA),
   .COMP(COMP), 
   .Clk(Clk)
  );


 initial begin

  // Initialize Inputs

   integer k;
   integer n;
   integer j;
   
   for (k=0; k<=15; k=k+1)
     begin
       dataIn [k] = 8'd0;
     end
   
   for (n=0; n<=15; n=n+1)
     begin
       weightIn [n] = 8'd0;
     end
   
   for (j=0; j<=15; j=j+1)
     begin
       addrWeight [j] = 5'd0;
     end
   
   addrEn = 16'd0;
   reset = 16'd0;
   WE  = 1'b0;
   COMP  = 1'b0;
   NEWDATA = 1'b0;
   Clk  = 1'b0;
  
   error_count = 0;
   
   #20;
   reset = 16'd65535;

  // Wait 100 ns for global reset to finish

   #100;
   reset = 16'd0;
   #20;
   
   

  // Add stimulus here
   
	x = 4'd0;
    y = 4'd0;
   
   // Load in Weights (0)
   WEIGHT_IN(x, 8'd1, 5'd0);
   WEIGHT_IN(x, 8'd2, 5'd1);
   WEIGHT_IN(x, 8'd3, 5'd2);
   WEIGHT_IN(x, 8'd0, 5'd3);
   
   // MAC (0,0)
   DATA_IN (y, 8'd1);
   COMPUTE (y, x, 16'b1, 5'd0);
   #40;
   CHECK (x, 17'd1);
   #20;
   
   DATA_IN (y, 8'd0);
   COMPUTE (y, x, 16'b1, 5'd1);
   #40;
   CHECK (x, 17'd1);
   #20;
   
   DATA_IN (y, 8'd2);
   COMPUTE (y, x, 16'b1, 5'd2);
   #40;
   CHECK (x, 17'd7);
   #20;
   
   DATA_IN (y, 8'd4);
   COMPUTE (y, x, 16'b1, 5'd3);
   #40;
   CHECK (x, 17'd7);
   #100;
   
   // MAC (0,1)
   x = 4'd0;
   y = 4'd1;
   
   DATA_IN (y, 8'd0);
   COMPUTE (y, x, 16'b11, 5'd0);
   DATA_IN (y, 8'd2);
   COMPUTE (y, x, 16'b11, 5'd1);
   #40;
   CHECK (x, 17'd4);
   #20;
   
   DATA_IN (y, 8'd4);
   COMPUTE (y, x, 16'b11, 5'd2);
   #40;
   CHECK (x, 17'd16);
   #20;
   
   // MAC (0,15)
   x = 4'd0;
   y = 4'd15;
   
   DATA_IN (y, 8'd0);
   COMPUTE (y, x, 16'b1000000000000011, 5'd0);
   DATA_IN (y, 8'd2);
   COMPUTE (y, x, 16'b1000000000000011, 5'd1);
   #40;
   CHECK (x, 17'd4);
   #20;
   
   DATA_IN (y, 8'd4);
   COMPUTE (y, x, 16'b1000000000000011, 5'd2);
   #40;
   CHECK (x, 17'd16);
   #20;
   
   x = 4'd1;
   y = 4'd1;
   
   // Load in Weights (1)
   WEIGHT_IN(x, 8'd2, 5'd0);
   WEIGHT_IN(x, 8'd4, 5'd1);
   WEIGHT_IN(x, 8'd100, 5'd2);
   WEIGHT_IN(x, 8'd0, 5'd3);
   
   // MAC (1,1)
   DATA_IN (y, 8'd0);
   COMPUTE (y, x, 16'b11, 5'd1);
   DATA_IN (y, 8'd2);
   COMPUTE (y, x, 16'b11, 5'd3);
   #40;
   CHECK (x, 17'd0);
   #20;
   
   DATA_IN (y, 8'd4);
   COMPUTE (y, x, 16'b11, 5'd2);
   #40;
   CHECK (x, 17'd400);
   #20;
   
   x = 4'd15;
   y = 4'd15;
   
   // Load in Weights (15)
   WEIGHT_IN(x, 8'd2, 5'd0);
   WEIGHT_IN(x, 8'd4, 5'd1);
   WEIGHT_IN(x, -8'd100, 5'd2);
   WEIGHT_IN(x, 8'd127, 5'd3);
   
   // MAC (15,15)
   DATA_IN (y, 8'd0);
   COMPUTE (y, x, 16'b1000000000000000, 5'd1);
   DATA_IN (y, 8'd2);
   COMPUTE (y, x, 16'b1000000000000000, 5'd3);
   #40;
   CHECK (x, 17'd254);
   #20;
   
   DATA_IN (y, 8'd4);
   COMPUTE (y, x, 16'b1000000000000000, 5'd2);
   #40;
   CHECK (x, -17'd146);
   #20;
   
   // Check when disabled
   DATA_IN (y, 8'd8);
   COMPUTE (y, x, 16'b0, 5'd1);
   #40;
   CHECK (x, -17'd146);
   #20;
   
   $display("Simulation finished with %d errors", error_count);
   $stop;

 end
  
  // Task to fill weight registers
  task WEIGHT_IN ( input [3:0] reg_choice, input [7:0] weight_in, input [4:0] weight_addr);
    begin
      @ (negedge Clk) WE = 1'b1;
      weightIn [reg_choice] = weight_in;
      addrWeight [reg_choice] = weight_addr;
      @ (negedge Clk) WE = 1'b0;
    end 
  endtask
  
  // Task to simulate data in
  task DATA_IN ( input [3:0] row_choice, input [7:0] data_in );
    begin
      dataIn [row_choice] = data_in;
    end
  endtask
  
  // Task to compute MAC
  task COMPUTE ( input [3:0] row_result, input [3:0] col_result, input [15:0] enableMAC, input [4:0] weightAddr);
    begin
      @ (negedge Clk) NEWDATA = 1'b1;
      addrEn = enableMAC;
      addrResult = row_result;
      addrWeight [col_result] = weightAddr;
      @ (negedge Clk) NEWDATA = 1'b0;
    end
  endtask
  
  // Task to check MAC result
  task CHECK ( input [3:0] col_result, input [16:0] expected );
    begin
      @ (negedge Clk) COMP = 1'b1;
      @ (negedge Clk) COMP = 1'b0;
      @ (negedge Clk)
      if (dataOut[col_result] !== expected)
        	begin
          		error_count = error_count + 1;
        	end
    end
  endtask

   

 always #10 Clk = ~Clk;

 initial begin
    $dumpfile("dump.vcd");
    $dumpvars(2);
  end

endmodule

