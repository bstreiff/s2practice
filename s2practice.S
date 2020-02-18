	.macro patch name, addr
	.org \addr
__patch$\name\()$\@\():
	.endm

	.macro endpatch p1=0
__endpatch$\@\():
	.endm

// ------------------------------------------

	.section .text

	// Set initial life counter to 99
	patch LifeCount1P, 0x3C78
	dc.w	0x0063
	endpatch

	// Set initial life counter to 99
	patch LifeCount2P, 0x3C7E
	dc.w	0x0063
	endpatch

	// Skip several checks in the title menu and go straight to the
	// level select menu on game start.
	patch ForceLevelSelectMenu, 0x3CCE
	nop
	nop
	nop
	nop
	nop
	nop
	nop
	endpatch

	// Set initial life counter to 99
	patch LifeCount1PFromLevelSel, 0x9490
	dc.w	0x0063
	endpatch

	// Set initial life counter to 99
	patch LifeCount2PFromLevelSel, 0x9496
	dc.w	0x0063
	endpatch
