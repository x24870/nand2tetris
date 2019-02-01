// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//initialize R2, n, sum = 0
@R2
M=0
@n
M=0
@sum
M=0

(LOOP)
//temp = 0
@temp
M=0

//if n = R1 goto STOP
@n
D=M
@temp
M=D
@R1
D=M
@temp//if temp==0
M=M-D
D=M
@STOP
D;JEQ

//do loop
@R0
D=M
@sum
M=M+D
//n++
@n
M=M+1
@LOOP
0;JMP

(STOP)
@sum
D=M
@R2
M=D

(END)
@END
0;JMP