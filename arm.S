.global compute
.text

compute:
    mov w2, #0
    mov w3, w3
    
loop:
    ldrb w4, [x0, w3, uxtw]
    cmp w4, #0
    beq done
    cmp w4, w1
    bne not_found
    add w2, w2 #1

not_found:
    add w3, w3, #1

done:
    mov w0, w2 
    ret