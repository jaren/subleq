package subleq

import spinal.core._
import spinal.lib._

class Subleq extends Component {
  val io = new Bundle {
    val addr = out Bits(10 bits)
    val writeEnable = out Bool
    val writeData = out Bits(32 bits)
    val readData = in Bits(32 bits)
  }

  /*
   * 0 - Read instruction
   * 1 - Read a
   * 2 - Read b
   * 3 - Write b and update pc
   */
  val state = RegInit(U"00")
  state := state + 1
  when (state === 3) {
    state := 0
  }

  val instruction = RegNextWhen(io.readData, state === 0)
  val a = Bits(10 bits)
  a := instruction(9 downto 0)
  val b = Bits(10 bits)
  b := instruction(19 downto 10)
  val c = Bits(10 bits)
  c := instruction(29 downto 20)

  val aVal = RegNextWhen(io.readData, state === 1)
  val bVal = RegNextWhen(io.readData, state === 2)

  io.writeEnable := state === 3
  io.writeData := (bVal.asSInt - aVal.asSInt).asBits

  val pcVal = UInt(10 bits)
  val programCounter = RegNextWhen(pcVal, state === 3) init(0)
  pcVal := programCounter + 1
  when (bVal.asSInt <= 0) {
    pcVal := c.asUInt
  }

  io.addr := pcVal.asBits
  when (state === 1) {
    io.addr := a
  }
  when (state === 2 | state === 3) {
    io.addr := b
  }

}

object Main {
  def main(args: Array[String]) {
    SpinalVerilog(new Subleq)
  }
}
