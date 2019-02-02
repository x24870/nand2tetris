// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@8192
D=A
@max_offset
M=D

(LOOP)
@screen_offset
M=0
//if keyboard == 0 then clear
@KBD
D=M
@CLEAR
D;JEQ
@FILL
0;JMP


(FILL)
//if screen_offset < 8192
@screen_offset
D=M
@temp
M=D
@max_offset
D=M
@temp
D=M-D
@LOOP//finish fill
D;JGE

//fill
@SCREEN
D=A
@addr
M=D
@screen_offset
D=M
@addr
M=M+D
A=M
M=-1

//offset++
@screen_offset
M=M+1
@FILL
0;JMP

(CLEAR)
//if screen_offset < 8192
@screen_offset
D=M
@temp
M=D
@max_offset
D=M
@temp
D=M-D
@LOOP//finish clear
D;JGE

//clear
@SCREEN
D=A
@addr
M=D
@screen_offset
D=M
@addr
M=M+D
A=M
M=0

//offset++
@screen_offset
M=M+1
@CLEAR
0;JMP