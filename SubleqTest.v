`include "Subleq.v"
module SubleqTest;

reg [31:0] mem [1023:0];

wire [9:0] addr;
wire writeEnable;
wire [31:0] writeData;
wire [31:0] readData;

reg clk = 0;
reg reset = 1;

always #2 clk = ~clk;
always #2 reset = 0;

Subleq subleq(addr, writeEnable, writeData, readData, clk, reset);

assign readData = mem[addr];

always @ (posedge clk) begin
  if  (writeEnable == 1) begin
    mem[addr] <= writeData;
    // Probably not the best way but eh
    $writememh("test/output.hex", mem);
  end
end

initial begin
  $dumpfile("test/dump.vcd");
  $dumpvars;
  $readmemh("test/input.hex", mem);
end

endmodule
