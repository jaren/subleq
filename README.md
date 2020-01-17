# subleq
Implementation of a OISC Subleq CPU in SpinalHDL
https://en.wikipedia.org/wiki/One_instruction_set_computer

# ISA Spec
- Base instruction format: `subleq a b c`
- `Mem[b] = Mem[b] - Mem[a]; if (Mem[b] <= 0) goto c;`
- a, b, c are each 10 bits, representing the address of a 32-bit number
- Each instruction is encoded as a 32-bit word:
-------------------------------------------
| 31 30 | 29     20 | 19     10 | 9     0 |
|  N/A  |     c     |     b     |     a   |
-------------------------------------------
- Instructions take 4 cycles to execute: Read instruction, Read a, Read b, and Write b + Update PC
