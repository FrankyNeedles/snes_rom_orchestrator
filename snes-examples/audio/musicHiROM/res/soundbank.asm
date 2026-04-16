;************************************************
; snesmod soundbank data                        *
; total size:      59378 bytes                  *
;************************************************

.include "hdr.asm"

.BANK 3
.SECTION "SOUNDBANK" ; need dedicated bank(s)

SOUNDBANK__:
.incbin "res/soundbank.bnk"
.ENDS
