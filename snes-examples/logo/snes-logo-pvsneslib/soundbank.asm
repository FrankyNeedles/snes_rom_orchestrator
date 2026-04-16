;************************************************
; snesmod soundbank data                        *
; total size:       2922 bytes                  *
;************************************************

.include "hdr.asm"

.BANK 5
.SECTION "SOUNDBANK" ; need dedicated bank(s)

SOUNDBANK__:
.incbin "soundbank.bnk"
.ENDS
