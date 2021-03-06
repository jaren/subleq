# subleq
Implementation of a OISC Subleq CPU in SpinalHDL
https://en.wikipedia.org/wiki/One_instruction_set_computer

## ISA Spec
- Base instruction format: `subleq a b c`
- `Mem[b] = Mem[b] - Mem[a]; if (Mem[b] <= 0) goto c;`
- a, b, c are each 10 bits, representing the address of a 32-bit number
- Instructions take 4 cycles to execute: read instruction, read a, read b, and write b + update PC
- Each instruction is encoded as a 32-bit word

| 31 30 | 29     20 | 19     10 | 9     0 |
| :---: | :-------: | :-------: | :-----: |
|  N/A  |     c     |     b     |     a   |

## Assembler Spec
- Assemble with `assemble.py`
- Pseudoinstructions:
    * `subleq A B` ==> `Mem[B] = Mem[B] - Mem[A]`
- Assembly format:
    * Lines may contain either a label, subleq instruction, comment, 32-bit literal, or pseudoinstruction
    * Comments begin with //
    * Labels are in the format "LABELNAME:"
    * Literals are a signed decimal number
    * Subleq and pseudoinstructions must include 10-bit literals or label names as their parameters
- See test files for examples
