;************************************************
; snesmod soundbank data                        *
; total size:       3422 bytes                  *
;************************************************

.include "hdr.asm"

.BANK 5
.SECTION "SOUNDBANK" ; need dedicated bank(s)

SOUNDBANK__:
.incbin "soundbank.bnk"
.ENDS
