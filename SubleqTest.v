module SubleqTest;

reg [31:0] mem [1023:0];

wire [9:0] addr;
wire writeEnable;
wire [31:0] writeData;
wire [31:0] readData;

reg clk = 0;
reg reset = 1;

always #5 clk = ~clk;
always #5 reset = 0;

Subleq subleq(addr, writeEnable, writeData, readData, clk, reset);

assign readData = mem[readData];

always @ (posedge clk) begin
  if  (wen == 1) begin
    mem[addr] = writeData;
  end
end

initial begin
  $dumpfile("tmp/TestDump.vcd");
  $dumpvars;
  $readmemb("tmp/TestMemInput.bin", mem);
  $writememb("tmp/TestMemOutput.bin", mem);
