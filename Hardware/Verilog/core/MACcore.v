`include "linearMAC.sv"

module MACcore( input [7:0] data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16,
               
               input [7:0] weight1, weight2, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10, weight11, weight12, weight13, weight14, weight15, weight16,
               
               input [4:0] addrWeight1, addrWeight2, addrWeight3, addrWeight4, addrWeight5, addrWeight6, addrWeight7, addrWeight8, addrWeight9, addrWeight10, addrWeight11, addrWeight12, addrWeight13, addrWeight14, addrWeight15, addrWeight16,
               
               output reg [16:0] dataOut1, dataOut2, dataOut3, dataOut4, dataOut5, dataOut6, dataOut7, dataOut8, dataOut9, dataOut10, dataOut11, dataOut12, dataOut13, dataOut14, dataOut15, dataOut16,
               
                input [15:0] addrEn,
               input [3:0] rowResult,
                input [15:0] reset,
                input WE, NEWDATA, COMP, Clk
);
  
  reg [7:0] dataIn [15:0];
  reg [7:0] weightIn [15:0];
  reg [4:0] addrWeight [15:0];
  reg [16:0] dataOut [15:0];
  
  	always @(posedge Clk)
    	begin
          dataIn[0] = data1;
          dataIn[1] = data2;
          dataIn[2] = data3;
          dataIn[3] = data4;
          dataIn[4] = data5;
          dataIn[5] = data6;
          dataIn[6] = data7;
          dataIn[7] = data8;
          dataIn[8] = data9;
          dataIn[9] = data10;
          dataIn[10] = data11;
          dataIn[11] = data12;
          dataIn[12] = data13;
          dataIn[13] = data14;
          dataIn[14] = data15;
          dataIn[15] = data16;
          
          weightIn[0] = weight1;
          weightIn[1] = weight2;
          weightIn[2] = weight3;
          weightIn[3] = weight4;
          weightIn[4] = weight5;
          weightIn[5] = weight6;
          weightIn[6] = weight7;
          weightIn[7] = weight8;
          weightIn[8] = weight9;
          weightIn[9] = weight10;
          weightIn[10] = weight11;
          weightIn[11] = weight12;
          weightIn[12] = weight13;
          weightIn[13] = weight14;
          weightIn[14] = weight15;
          weightIn[15] = weight16;
          
          addrWeight[0] = addrWeight1;
          addrWeight[1] = addrWeight2;
          addrWeight[2] = addrWeight3;
          addrWeight[3] = addrWeight4;
          addrWeight[4] = addrWeight5;
          addrWeight[5] = addrWeight6;
          addrWeight[6] = addrWeight7;
          addrWeight[7] = addrWeight8;
          addrWeight[8] = addrWeight9;
          addrWeight[9] = addrWeight10;
          addrWeight[10] = addrWeight11;
          addrWeight[11] = addrWeight12;
          addrWeight[12] = addrWeight13;
          addrWeight[13] = addrWeight14;
          addrWeight[14] = addrWeight15;
          addrWeight[15] = addrWeight16;
          
          dataOut1 = dataOut[0];
          dataOut2 = dataOut[1];
          dataOut3 = dataOut[2];
          dataOut4 = dataOut[3];
          dataOut5 = dataOut[4];
          dataOut6 = dataOut[5];
          dataOut7 = dataOut[6];
          dataOut8 = dataOut[7];
          dataOut9 = dataOut[8];
          dataOut10 = dataOut[9];
          dataOut11 = dataOut[10];
          dataOut12 = dataOut[11];
          dataOut13 = dataOut[12];
          dataOut14 = dataOut[13];
          dataOut15 = dataOut[14];
          dataOut16 = dataOut[15];
    	end

    reg [7:0] inMACregs [15:0] [31:0];
    reg signed [7:0] dataToMAC [15:0];
    reg signed [7:0] weightToMAC [15:0];
  wire signed [16:0] outputOfMAC [15:0] [15:0];

    genvar i;
  	genvar m;
    generate
      for (i=0; i<=15; i=i+1) begin: mac_array
        for (m=0; m<=15; m=m+1)
        	begin
              digital_MAC digital_MAC(.clock(Clk), .data_in(dataToMAC[i]), .weight_in(weightToMAC[m]), .reset(reset[i]), .enable(addrEn[i]), .data_out(outputOfMAC[i][m]));
      		end
      end
    endgenerate
  
    integer k;
    // Registers to hold weights
    always @ (posedge Clk)
        begin
          	for (k=0; k<=15; k=k+1)
            begin
              if (reset[k] == 1'b1) begin
                integer m;
                for (m=0; m<=31; m=m+1) begin
                  inMACregs [k] [m] = 8'd0;
                end
              end
                
              else if (WE == 1'b1) begin
                inMACregs [k] [addrWeight[k]] = weightIn[k];
              end
               
              else if (NEWDATA == 1'b1) begin
                weightToMAC [k] = inMACregs [k] [addrWeight[k]];
              end
              else begin
                inMACregs [k] [addrWeight[k]] = inMACregs [k] [addrWeight[k]];
                weightToMAC [k] = 8'd0;
              end
            end
       	end

    integer j;
    // Register for data in
    always @ (posedge Clk)
        begin
          if (NEWDATA == 1'b1) begin
              for (j=0; j<=15; j=j+1)
                begin
                  	dataToMAC [j] = dataIn [j];
                end
            end
            else begin
              for (j=0; j<=15; j=j+1)
                begin
                  	dataToMAC [j] = 16'd0;
                end
            end
        end

    integer n;
    // Output register
    always @ (posedge Clk)
        begin
          for (n=0; n<=15; n=n+1)
            begin
              	if (reset[n] == 1'b1) begin
                  dataOut [n] = 17'd0;
                end
            	else if (COMP == 1'b1) begin
                  dataOut [n] = outputOfMAC [rowResult] [n];
                end
            	else begin
                  dataOut [n] = dataOut[n];	
                end
            end
        end


endmodule