`include "coProcModules.sv"

module coProcessor(input clock, enable,
                   input [7:0] weightIn, dataIn,
                   output enableWSRAM, writeWSRAM, readWSRAM, readWifmaps, readWpixels,
                   output [3:0] WkernAddr,
                   output [5:0] WpixAddr);
  
  wire weightsPulled, singleKernel, allKernel, dataSent, blockDone, imageDone, cumulationDone, 
  		enWeightState, enDataState, enResultState, enSendOutput;
  
  reg resetMapCounter, resetPixCounter, countMap, countWPix;
  
  reg [7:0] numMapW, numPixW;
  
  cpState cpState(.clock(clock), .reset(reset), .enable(enable), .weightsPulled(weightsPulled), .dataSent(dataSent),
                  .blockDone(blockDone), .imageDone(imageDone), .cumulationDone(cumulationDone), .weights(enWeightState),
                  .data(enDataState), .result(enResultState), .sendOutput(enSendOutput));
      
  ofmapCounter counter(.maxCount(numMapW), .countUp(countMap), .reset(resetMapCounter), .clock(clock), .done(allKernel));
  
  pixelCounter counter(.maxCount(numPixW), .countUp(countWPix), .reset(resetPixCounter), .clock(clock), .done(singleKernel));
  
endmodule