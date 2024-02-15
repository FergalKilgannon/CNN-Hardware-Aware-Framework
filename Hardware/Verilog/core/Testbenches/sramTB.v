`timescale 1ns / 1ps

module syncRAM_tb;


 // Inputs

 reg [7:0] dataIn;
 reg [3:0] kernAddr;
 reg [5:0] pixAddr;
 reg CS;
 reg WE;
 reg RD;
 reg Clk;


 // Outputs

 wire [7:0] dataOut;


 // Instantiate the Unit Under Test (UUT)

 syncRAM uut (
  .dataIn(dataIn), 
  .dataOut(dataOut), 
  .kernAddr(kernAddr),
  .pixAddr(pixAddr),
  .CS(CS), 
  .WE(WE), 
  .RD(RD), 
  .Clk(Clk)
  );


 initial begin

  // Initialize Inputs

  dataIn  = 8'h0;
  kernAddr  = 3'h0;
  pixAddr = 5'h0;
  CS  = 1'b0;
  WE  = 1'b0;
  RD  = 1'b0;
  Clk  = 1'b0;

  // Wait 100 ns for global reset to finish

  #100;

  // Add stimulus here

  dataIn  = 8'h0;
  kernAddr  = 3'h0;
  pixAddr = 5'h0;
  CS  = 1'b1;
  WE  = 1'b1;
  RD  = 1'b0;

  #20;

  dataIn  = 8'h0;
  kernAddr  = 3'h0;
  pixAddr = 5'h0;

  #20;

  dataIn  = 8'h1;
  kernAddr  = 3'h0;
  pixAddr = 5'h1;

  #20;

  dataIn  = 8'h10;
  kernAddr  = 3'h0;
  pixAddr = 5'h2;

  #20;

  dataIn  = 8'h6;
  kernAddr  = 3'h0;
  pixAddr = 5'h3;

  #20;

  dataIn  = 8'h12;
  kernAddr  = 3'h0;
  pixAddr = 5'h4;

  #40;

  kernAddr  = 3'h0;
  pixAddr = 5'h0;

  WE  = 1'b0;

  RD  = 1'b1;

  #20;

  kernAddr  = 3'h0;
  pixAddr = 5'h1;

  #20;

  kernAddr  = 3'h0;
  pixAddr = 5'h2;

  #20;

  kernAddr  = 3'h0;
  pixAddr = 5'h3;

  #20;

  kernAddr  = 3'h0;
  pixAddr = 5'h4;

 end

   

 always #10 Clk = ~Clk;

 initial begin
    $dumpfile("dump.vcd");
    $dumpvars(2);
  end

endmodule

