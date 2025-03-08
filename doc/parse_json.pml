import json
import re

data = """
For Reference:
A01 Unleash Xi
Genre : Dubstep
D1 : Ah Super Saw Seq
D2 : Scream at me Seq
DR : TR-909 Kit 4
AN : We'reGoingDn
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 1
A02 Dist Seq
Genre : Techno
D1 : Dist Flt TB2 Lead
D2 : LFO ResoPad2 Strings/Pad
DR : Techno Kit 3
AN : SawSweep Bs1
Measure Length : 1
Scale : 1/16
Tempo : 135
MSB : 85
LSB : 64
PC : 2
A03 SPACED
Genre : Trap
D1 : SqrTrapPlk 2 Seq
D2 : Unison SynLd Bass
DR : TR-808 Kit 5
AN : Twister 2
Measure Length : 1
Scale : 1/16
Tempo : 71
MSB : 85
LSB : 64
PC : 3
A04 GETTIN'CLOSE
Genre : Deep House
D1 : Pluck+SynStr Strings/Pad
D2 : FilterPanPad Bass
DR : 808&7*7 Kit2
AN : Backwards 2
Measure Length : 1
Scale : 1/16
Tempo : 124
MSB : 85
LSB : 64
PC : 4
A05 Trance 1
Genre : Trance
D1 : Pluck Synth2 Seq
D2 : Super Saw 3 Lead
DR : TR-909 Kit 5
AN : Saw Bass 2
Measure Length : 2
Scale : 1/16
Tempo : 135
MSB : 85
LSB : 64
PC : 5

A06 EDM KIDS
Genre : EDM
D1 : HPF Poly 2 Strings/Pad
D2 : Tuned Winds2 FX/Other
DR : TR-808 Kit 6
AN : Buzz Bass
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 6
A07 COME ON BABY
Genre : Trap
D1 : Buzz Lead 3 Lead
D2 : Monster Bs 5 Bass
DR : R&B Kit 2
AN : Juxtrans
Measure Length : 1
Scale : 1/32
Tempo : 74
MSB : 85
LSB : 64
PC : 7
A08 Hardstyle 1
Genre : Hardstyle
D1 : OldSchool Ld Bass
D2 : Noise Groove FX/Other
DR : TR-909 Kit 6
AN : ClassicHrdBs
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 8
A09 DUBBER
Genre : Dubstep
D1 : Wobble Bs 5 Bass
D2 : Noise Snare FX/Other
DR : TR-808 Kit 7
AN : Bacon Bass
Measure Length : 1
Scale : 1/16
Tempo : 84
MSB : 85
LSB : 64
PC : 9
A10 Hip-Hop 1
Genre : Hip-Hop
D1 : DnB Bass 2 Bass
D2 : Harp 2 Keyboard
DR : Hiphop Kit 3
AN : Sqr Lead
Measure Length : 2
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 64
PC : 10

A11 CARONDO
Genre : Trap
D1 : Tekno Lead 5 Lead
D2 : WaveShapeLd2 Lead
DR : TR-808 Kit 8
AN : Springer
Measure Length : 1
Scale : 1/32
Tempo : 70
MSB : 85
LSB : 64
PC : 11
A12 Electro 1
Genre : Electro
D1 : Seq Bass 3 Bass
D2 : Glideator 2 Lead
DR : TR-808 Kit 9
AN : Squeak Bass
Measure Length : 1
Scale : 1/16
Tempo : 124
MSB : 85
LSB : 64
PC : 12
A13 NEUWERK
Genre : Techno
D1 : Sweet 5th 2 Lead
D2 : SqrTrapPlk 3 Seq
DR : Hiphop Kit 4
AN : Sqr Bass 2
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 13
A14 CLIX
Genre : Trap
D1 : Tekno Lead 6 Lead
D2 : Monster Bs 6 Bass
DR : TR-909 Kit 7
AN : Fluttertwerk
Measure Length : 1
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 64
PC : 14
A15 PUFFS
Genre : Trap
D1 : SqrTrapPlk 4 Seq
D2 : OSC-SyncLd 2 Lead
DR : CR-78 Kit 2
AN : Spitshine
Measure Length : 1
Scale : 1/32
Tempo : 105
MSB : 85
LSB : 64
PC : 15

A16 IN DA HOUSE
Genre : House
D1 : SqrFilterBs2 Bass
D2 : Buzz Lead 4 Lead
DR : TR-606 Kit 2
AN : Torque Bass
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 16
A17 Moombahton 1
Genre : Moombahton
D1 : JD RingMod 2 Lead
D2 : Wobble Bs 6 Bass
DR : TR-909 Kit 8
AN : Laser Lead 2
Measure Length : 1
Scale : 1/16
Tempo : 110
MSB : 85
LSB : 64
PC : 17
A18 Seq Phrase 1
Genre : Techno
D1 : FltSweep Pd2 Strings/Pad
D2 : Syn Brass 3 Brass
DR : 707&727 Kit3
AN : Pulse SEQ 1
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 18
A19 House 1
Genre : House
D1 : Sync Pad Strings/Pad
D2 : Sqr Bass 1 Bass
DR : EDM Kit 3
AN : Pulse Lead 1
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 64
PC : 19

A20 DRAGON FIRE
Genre : House
D1 : Sonar Pluck2 Seq
D2 : SEQ Saw 2 FX/Other
DR : 909&7*7 Kit2
AN : Snake Glide2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 20

A21 E-D-M
Genre : EDM
D1 : Seq Bass 4 Bass
D2 : JUNO Sqr Bs2 Bass
DR : TR-808 Kit10
AN : Stream Synth
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 21
A22 EDM 1
Genre : EDM
D1 : SideChainBs3 Bass
D2 : Growl Bass 2 Bass
DR : EDM Kit 4
AN : Sqr SEQ 2
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 22
A23 EDM 2
Genre : EDM
D1 : 5th Stac Bs2 Bass
D2 : EDM Synth 2 Seq
DR : EDM Kit 5
AN : Buzz Saw Ld2
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 23
A24 EDM 3
Genre : EDM
D1 : HPF SweepPd2 Strings/Pad
D2 : Pluck Synth3 Seq
DR : Techno Kit 4
AN : Saw Bass 3
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 24

A25 UPMAN
Genre : EDM
D1 : Trance Key 3 Seq
D2 : SEQ Tri 2 FX/Other
DR : EDM Kit 6
AN : Saw+Sub Bs 2
Measure Length : 2
Scale : 1/16
Tempo : 132
MSB : 85
LSB : 64
PC : 25


A26 EDM 4
Genre : EDM
D1 : SuperSaw/SC Seq
D2 : BuzzLd/Legat Lead
DR : EDM Kit 7
AN : SideChainBs1
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 26
A27 EDM 5
Genre : EDM
D1 : Shape Bs/SC Lead
D2 : Buzz Ld/SC Seq
DR : EDM Kit 8
AN : Siren FX 1
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 27
A28 EDM 6
Genre : EDM
D1 : Super Saw 4 Seq
D2 : Fall/Sta&Hol FX/Other
DR : EDM Kit 9
AN : Siren FX 2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 28
A29 EDM 7
Genre : EDM
D1 : Mod Sqr FX/Other
D2 : Super Saw 5 Seq
DR : EDM Kit 10
AN : Buzz/Stacc
Measure Length : 2
Scale : 1/8 Triple
Tempo : 130
MSB : 85
LSB : 64
PC : 29
A30 EDM 8
Genre : EDM
D1 : Sonar Pluck3 Seq
D2 : EDM Synth 3 Seq
DR : TR-909 Kit 9
AN : Saw Buzz 2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 30

A31 EDM 9
Genre : EDM
D1 : Super Saw 6 Seq
D2 : Trance Key 4 Seq
DR : TR-909 Kit10
AN : Sqr+Sub Bazz
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 31
A32 Big Room 1
Genre : Big Room
D1 : Hatter drop$ Lead
D2 : RiSER 2 Bass
DR : TR-909 Kit11
AN : Kick Sub
Measure Length : 1
Scale : 1/8 Triple
Tempo : 128
MSB : 85
LSB : 64
PC : 32
A33 Big Room 2
Genre : Big Room
D1 : RelaxngBeeps Seq
D2 : Snare Noise Seq
DR : TR-909 Kit12
AN : BigRoom Bass
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 33
A34 DUBSTOP
Genre : Dubstep
D1 : DistBacking1 Seq
D2 : FlngFallRiff Seq
DR : EDM Kit 11
AN : DarkSaw SEQ
Measure Length : 2
Scale : 1/32
Tempo : 130
MSB : 85
LSB : 64
PC : 34
A35 THE ANKH
Genre : Dubstep
D1 : Square Ld 3 Lead
D2 : Wobble Bs 7 Bass
DR : EDM Kit 12
AN : Sick Bass
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 35

A36 Dubstep 1
Genre : Dubstep
D1 : CuttingLead2 Lead
D2 : Wobble Bs 8 Bass
DR : Techno Kit 5
AN : Dubber Bass
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 36
A37 Dubstep 2
Genre : Dubstep
D1 : Grim Grime Bass
D2 : Dirt Lead Lead
DR : EDM Kit 13
AN : Bugs
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 37
A38 SCORPION BIT
Genre : Dubstep
D1 : Sonar Pluck4 Seq
D2 : Sine Lead 2 Lead
DR : EDM Kit 14
AN : Insect 1000
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 38
A39 PRAWN STAR
Genre : Dubstep
D1 : 106 Bass 4 Bass
D2 : Sine Lead 3 Lead
DR : EDM Kit 15
AN : Phat n Wide
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 39
A40 BENGAL BUS
Genre : Dubstep
D1 : Wobble Bs 9 Bass
D2 : SideChainBs4 Bass
DR : TR-808 Kit11
AN : Bass Mover
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 40

A41 Dubstep 3
Genre : Dubstep
D1 : Wah-Wah Strings/Pad
D2 : Harder Pluck Lead
DR : TR-909 Kit13
AN : Fast Wobbles
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 41
A42 Dubstep 4
Genre : Dubstep
D1 : Whoop Echo Seq
D2 : Whoa Lead Lead
DR : TR-909 Kit14
AN : 808 Bass 2
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 42
A43 Dubstep 5
Genre : Dubstep
D1 : Bass Saw Seq
D2 : Arp Lead Lead
DR : TR-909 Kit15
AN : HitThe Floor
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 43
A44 Dubstep 6
Genre : Dubstep
D1 : Tringle Arp Seq
D2 : Sine Bells Seq
DR : TR-909 Kit16
AN : Higher Wob
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 44
A45 Dubstep 7
Genre : Dubstep
D1 : Hip-Hop Lead Lead
D2 : Delay Away Seq
DR : TR-909 Kit17
AN : Crasy Sub
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 45

A46 Dubstep 8
Genre : Dubstep
D1 : Yay Lead Lead
D2 : Wobble Bs 10 Bass
DR : TR-909 Kit18
AN : Saw & Per 2
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 46
A47 Dubstep 9
Genre : Dubstep
D1 : Drty/Vel&Lg1 Bass
D2 : Super Saw 7 Seq
DR : TR-909 Kit19
AN : Saw Buzz 3
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 47
A48 Dubstep 10
Genre : Dubstep
D1 : Dirty /Mod Bass
D2 : Sqr Buzz Ld2 Lead
DR : TR-909 Kit20
AN : Saw&SubBazz
Measure Length : 2
Scale : 1/16
Tempo : 165
MSB : 85
LSB : 64
PC : 48
A49 DRUMSTEP1
Genre : Drumstep
D1 : DirtyFat/Mod Bass
D2 : SawTrap Ld 2 Lead
DR : TR-909 Kit21
AN : Tri Bass 2
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 49
A50 DRUMSTEP2
Genre : Drumstep
D1 : Drty/Vel&Lg2 Bass
D2 : Super Saw 8 Seq
DR : TR-909 Kit22
AN : Tri Bass 3
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 50

A51 Moombahton 2
Genre : Moombahton
D1 : yo son Bass
D2 : Knight Noise Keyboard
DR : TR-808 Kit12
AN : Pulse Lead 2
Measure Length : 1
Scale : 1/16
Tempo : 112
MSB : 85
LSB : 64
PC : 51
A52 ElectroH 1
Genre : Electro House
D1 : Monster Bs 7 Bass
D2 : Reso Bass 6 Bass
DR : EDM Kit 16
AN : Noisy Bass
Measure Length : 2
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 64
PC : 52
A53 ElectroH 2
Genre : Electro House
D1 : ShapeLd /Leg Lead
D2 : Super Saw 9 Seq
DR : EDM Kit 17
AN : Eletro Bass
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 53
A54 ElectroH 3
Genre : Electro House
D1 : Soft Brass 2 Brass
D2 : Ramdom Vox FX/Other
DR : EDM Kit 18
AN : House Bass 2
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 54
A55 Progressive1
Genre : Progressive
House
D1 : SideChainPd3 Strings/Pad
D2 : Prog Clouds Lead
DR : EDM Kit 19
AN : Fat Sub 1
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 55

A56 Progressive2
Genre : Progressive
House
D1 : PianoTone Strings/Pad
D2 : Revalation 2 Strings/Pad
DR : TR-909 Kit23
AN : House Saw Bs
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 56
A57 Progressive3
Genre : Progressive
House
D1 : PlckSyn/Vel1 Seq
D2 : SideChainPd5 Strings/Pad
DR : TR-909 Kit24
AN : Sqr Bass 3
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 57
A58 ACHORDANCE
Genre : Deep House
D1 : ConChord Seq
D2 : Syn Bass 2 Bass
DR : TR-909 Kit25
AN : Soft Bass 2
Measure Length : 1
Scale : 1/16
Tempo : 124
MSB : 85
LSB : 64
PC : 58
A59 STRAIGHT
Genre : Deep House
D1 : StraightChrd Seq
D2 : House Org 3 Keyboard
DR : 808&7*7 Kit3
AN : ClickerBass2
Measure Length : 1
Scale : 1/16
Tempo : 123
MSB : 85
LSB : 64
PC : 59
A60 Deep House 1
Genre : Deep House
D1 : Analog Str 2 Strings/Pad
D2 : Analog Poly5 Seq
DR : 808&909 Kit3
AN : Warm Bass
Measure Length : 2
Scale : 1/16
Tempo : 123
MSB : 85
LSB : 64
PC : 60

A61 Deep House 2
Genre : Deep House
D1 : UpBeat Pluck Seq
D2 : Wood Plucks Seq
DR : TR-909 Kit26
AN : Move That Bs
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 61
A62 Deep House 3
Genre : Deep House
D1 : TriangleFeel Seq
D2 : LFO SuperSaw Seq
DR : TR-909 Kit27
AN : The Bass
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 62
A63 Deep House 4
Genre : Deep House
D1 : One Deeper Bass
D2 : 80 Wow Lead
DR : TR-909 Kit28
AN : Fat Sub 2
Measure Length : 1
Scale : 1/16
Tempo : 122
MSB : 85
LSB : 64
PC : 63
A64 Deep House 5
Genre : Deep House
D1 : SideChainPd2 Strings/Pad
D2 : Porta S-Saw Lead
DR : TR-909 Kit29
AN : Dark Tri Bs
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 64

B01 House 2
Genre : house
D1 : MeanSuperSaw Seq
D2 : RisngScremer Seq
DR : TR-909 Kit30
AN : Pulled Bass
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 65
B02 CHICAGO
Genre : House
D1 : MinStack Ld2 Lead
D2 : Organ Bass 2 Bass
DR : TR-808 Kit13
AN : Cold Bass
Measure Length : 1
Scale : 1/16
Tempo : 124
MSB : 85
LSB : 64
PC : 66
B03 CLUBBIN'
Genre : House
D1 : S-SawStacLd2 Lead
D2 : Dist TB Sqr2 Lead
DR : TR-808 Kit14
AN : Floor Bass
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 67
B04 TRAUMA
Genre : House
D1 : Chow Bass 3 Bass
D2 : Paperclip 2 Seq
DR : TR-909 Kit31
AN : Pumper Bass2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 68
B05 THE DONK
Genre : House
D1 : JP8 Strings5 Strings/Pad
D2 : Hover Lead 2 Lead
DR : TR-909 Kit32
AN : Slo worn 2
Measure Length : 2
Scale : 1/32
Tempo : 130
MSB : 85
LSB : 64
PC : 69
B06 TUBULA SWELL
Genre : House
D1 : Dist TB Sqr3 Lead
D2 : LFO Pad 2 Strings/Pad
DR : TR-808 Kit15
AN : Berry Frog
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 70
B07 SUNSET STRIP
Genre : House
D1 : Awakening 2 Strings/Pad
D2 : Organ Bass 3 Bass
DR : Hiphop Kit 5
AN : Underneath
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 71
B08 ORGAN DONOR
Genre : House
D1 : LFO CarvePd2 Strings/Pad
D2 : Organ Bass 4 Bass
DR : Hiphop Kit 6
AN : No. 94 House
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 72
B09 CHEWY BACCA
Genre : House
D1 : Maker's 303 Lead
D2 : Saw Lead 2 Lead
DR : 808&7*7 Kit4
AN : Blip
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 73
B10 House 3
Genre : House
D1 : Noise Hit 1 FX/Other
D2 : Bouncy Pluck Lead
DR : TR-909 Kit33
AN : Up Bass
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 74
B11 House 4
Genre : House
D1 : Whoop Scream Seq
D2 : Detund S-Saw Lead
DR : TR-909 Kit34
AN : Hit hem Hard
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 75
B12 House 5
Genre : House
D1 : SquaredJumpy Seq
D2 : More Pads Strings/Pad
DR : TR-909 Kit35
AN : Fat Bass
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 76
B13 House 6
Genre : Indie House
D1 : Dark Horn Lead
D2 : Pluck It Bass
DR : 808&909 Kit4
AN : Feedback
Measure Length : 1
Scale : 1/16
Tempo : 112
MSB : 85
LSB : 64
PC : 77
B14 PACIFIC+8090
Genre : House
D1 : Lead Sax Brass
D2 : SweepStrings Lead
DR : Hiphop Kit 7
AN : ResoPulseBs2
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 78
B15 House 7
Genre : House
D1 : House Org 4 Keyboard
D2 : Flute 1 Brass
DR : House Kit 2
AN : Sqr+Sub Bs 1
Measure Length : 1
Scale : 1/16
Tempo : 118
MSB : 85
LSB : 64
PC : 79

B16 Latin
Genre : Latin
D1 : JD Piano 2 Keyboard
D2 : House Bass 2 Bass
DR : House Kit 3
AN : Porta Tri Ld
Measure Length : 1
Scale : 1/16
Tempo : 118
MSB : 85
LSB : 64
PC : 80
B17 BRISTOL BABY
Genre : Drum & Bass
D1 : Sine Lead 4 Lead
D2 : Noise SEQ 2 FX/Other
DR : Drum&Bs Kit2
AN : Zippers 4
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 81
B18 Drum&Bass 1
Genre : Drum & Bass
D1 : SmallSync Ld Seq
D2 : PchSweep Sin Lead
DR : TR-909 Kit36
AN : OffBeat Wob2
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 82
B19 NOSTALGIA
Genre : Drum & Bass
D1 : Hollow Pad 2 Strings/Pad
D2 : Sqr Bass 2 Bass
DR : EDM Kit 20
AN : Tear Drop 2
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 83
B20 RUBBER BAND
Genre : Drum & Bass
D1 : Hollow Pad 3 Strings/Pad
D2 : MKS-50 Bass2 Bass
DR : EDM Kit 21
AN : Squelchy 2
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 84
B21 CYCLIC BITE
Genre : Drum & Bass
D1 : Hollow Pad 4 Strings/Pad
D2 : 106 Bass 5 Bass
DR : EDM Kit 22
AN : Squelchy 3
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 85
B22 THE SPEAKER
Genre : Drum & Bass
D1 : Sine Lead 5 Lead
D2 : Bright Pad 2 Strings/Pad
DR : Drum&Bs Kit3
AN : Unsteady Bs
Measure Length : 4
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 86
B23 TURN IT UP
Genre : Drum & Bass
D1 : Detune Bs 2 Bass
D2 : Growl Bass 3 Bass
DR : Hiphop Kit 8
AN : Bo Wop
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 87
B24 ROLLIN!
Genre : Drum & Bass
D1 : Growl Bass 4 Bass
D2 : Growl Bass 5 Keyboard
DR : Hiphop Kit 9
AN : DnB Wobbler2
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 88
B25 Drum&Bass 2
Genre : Drum & Bass
D1 : Alarma Lead
D2 : Ready4u Bass
DR : TR-909 Kit37
AN : Water
Measure Length : 1
Scale : 1/16
Tempo : 180
MSB : 85
LSB : 64
PC : 89
B26 Drum&Bass 3
Genre : Drum & Bass
D1 : Vib Wurly 2 Keyboard
D2 : HPF Poly 3 Strings/Pad
DR : Drum&Bs Kit4
AN : Tri Bass 4
Measure Length : 2
Scale : 1/16
Tempo : 170
MSB : 85
LSB : 64
PC : 90
B27 DRUMATIC
Genre : Drum & Bass
D1 : Sweep JD 2 Strings/Pad
D2 : Digital Tp Seq
DR : Drum&Bs Kit5
AN : Deep Bass
Measure Length : 1
Scale : 1/16
Tempo : 160
MSB : 85
LSB : 64
PC : 91
B28 WAR MASTER
Genre : Drum & Bass
D1 : Square Bs 3 Bass
D2 : Vibraphone 2 Keyboard
DR : Drum&Bs Kit6
AN : Tri Bass 5
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 64
PC : 92
B29 SHACKLES
Genre : Drum & Bass
D1 : Sweet5th SEQ Lead
D2 : HouseResoHit FX/Other
DR : Drum&Bs Kit7
AN : Tri Fall Bs2
Measure Length : 2
Scale : 1/16
Tempo : 180
MSB : 85
LSB : 64
PC : 93
B30 Drumso
Genre : Drum & Bass
D1 : Saw Sweep Pd Strings/Pad
D2 : Dist Sine Bs Bass
DR : Drum&Bs Kit8
AN : Tri Lead 2
Measure Length : 4
Scale : 1/32
Tempo : 192
MSB : 85
LSB : 64
PC : 94
B31 WA*SA*BI
Genre : Drum & Bass
D1 : S-Saw Vib Pd Seq
D2 : S-Saw Pad 2 Seq
DR : EDM Kit 23
AN : Saw+Sub Bs 3
Measure Length : 2
Scale : 1/16
Tempo : 185
MSB : 85
LSB : 64
PC : 95
B32 Circadian
Genre : Drum & Bass
D1 : Fall Down Pd FX/Other
D2 : Low Bass 3 Bass
DR : Hiphop Kit10
AN : Saw+Sub SEQ
Measure Length : 2
Scale : 1/32
Tempo : 180
MSB : 85
LSB : 64
PC : 96
B33 Drum&Bass 4
Genre : Drum & Bass
D1 : DnB Bass 3 Bass
D2 : Trance Key 5 Seq
DR : Drum&Bs Kit9
AN : ResoSaw SEQ1
Measure Length : 2
Scale : 1/16
Tempo : 160
MSB : 85
LSB : 64
PC : 97
B34 DARK TB
Genre : Techno
D1 : Buzz Lead 5 Lead
D2 : Dist TB Sqr4 Lead
DR : TR-808 Kit16
AN : Pure Comp
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 98
B35 TECHNO LOVE
Genre : Techno
D1 : 106 Bass 6 Bass
D2 : House Bass 3 Bass
DR : TR-808 Kit17
AN : Hamster
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 64
PC : 99

B36 HARTFLUR
Genre : Techno
D1 : Dist TB Sqr5 Lead
D2 : Analog Str 3 Strings/Pad
DR : TR-808 Kit18
AN : Fundamental
Measure Length : 1
Scale : 1/16
Tempo : 127
MSB : 85
LSB : 64
PC : 100
B37 CLUBTOOL
Genre : Techno
D1 : Chubby Lead2 Lead
D2 : Tri Stac Ld2 Lead
DR : 808&909 Kit5
AN : Chirp Bass
Measure Length : 1
Scale : 1/16
Tempo : 123
MSB : 85
LSB : 64
PC : 101
B38 CULTURE
Genre : Techno
D1 : MinStack Ld3 Lead
D2 : JD RingMod 3 Lead
DR : 808&7*7 Kit5
AN : Average Bass
Measure Length : 2
Scale : 1/16
Tempo : 125
MSB : 85
LSB : 64
PC : 102
B39 IMITATION($)
Genre : Techno
D1 : Saw Backing Strings/Pad
D2 : Tri + Nz SEQ Seq
DR : Techno Kit 6
AN : PortaSawRiff
Measure Length : 1
Scale : 1/16
Tempo : 108
MSB : 85
LSB : 64
PC : 103
B40 MOBILE SUIT
Genre : Techno
D1 : Saw+Sqr Wah Seq
D2 : PortaSqrRiff Seq
DR : 808&909 Kit6
AN : ResoPulseBs3
Measure Length : 1
Scale : 1/16
Tempo : 102
MSB : 85
LSB : 64
PC : 104
B41 HUUP AMP
Genre : Techno
D1 : LFO Saw SEQ Seq
D2 : Saw+Nz SEQ Seq
DR : 808&909 Kit7
AN : Saw+Sub Bs 4
Measure Length : 1
Scale : 1/16
Tempo : 132
MSB : 85
LSB : 64
PC : 105
B42 Techno 1
Genre : Techno
D1 : SinStackRiff Lead
D2 : Saw+Sqr SEQ2 Seq
DR : Techno Kit 7
AN : AcidSaw SEQ2
Measure Length : 1
Scale : 1/16
Tempo : 152
MSB : 85
LSB : 64
PC : 106
B43 STARS
Genre : Techno
D1 : EP SEQ Keyboard
D2 : Trip 2 Mars2 Strings/Pad
DR : 808&7*7 Kit6
AN : Tri Bass 6
Measure Length : 2
Scale : 1/32
Tempo : 128
MSB : 85
LSB : 64
PC : 107
B44 Parabola
Genre : Techno
D1 : Sine SEQ Seq
D2 : Soft Nz Pad Strings/Pad
DR : TR-808 Kit19
AN : Tri Bass 7
Measure Length : 1
Scale : 1/16
Tempo : 125
MSB : 85
LSB : 64
PC : 108
B45 HOTDOGER
Genre : Techno
D1 : Syn Sniper 2 Strings/Pad
D2 : Bend Lead 2 FX/Other
DR : TR-909 Kit38
AN : ResoSaw SEQ2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 109
B46 Techno 2
Genre : Techno
D1 : TB Sqr Seq 2 Seq
D2 : S-Saw Pad 3 Seq
DR : Techno Kit 8
AN : Saw Bass 4
Measure Length : 1
Scale : 1/16
Tempo : 132
MSB : 85
LSB : 64
PC : 110
B47 Seq Phrase 2
Genre : Techno
D1 : TB Saw Seq 2 Seq
D2 : Reso S&H Pd2 Strings/Pad
DR : TR-808 Kit20
AN : Pulse+SubBs
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 111
B48 Seq Phrase 3
Genre : Techno
D1 : Seq Bass 5 Bass
D2 : S-SawStacLd3 Lead
DR : Techno Kit 9
AN : Saw SEQ
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 112
B49 Seq Phrase 4
Genre : Techno
D1 : LFO Pad 3 Strings/Pad
D2 : Sweet 5th 3 Lead
DR : 808&909 Kit8
AN : Sqr SEQ 3
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 64
PC : 113
B50 HardHouse
Genre : Techno
D1 : ResoSweepPd1 Strings/Pad
D2 : ResoSaw SEQ1 Seq
DR : TR-909 Kit39
AN : Saw Bass 5
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 114
B51 AcidHrdstyle
Genre : Acid Hardstyle
D1 : RingMod Lead Lead
D2 : Sweeporama FX/Other
DR : TR-909 Kit40
AN : Tri+SubOSCBs
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 115
B52 TechHouse1
Genre : Tech House
D1 : House Org 5 Keyboard
D2 : Sweet 5th 4 Lead
DR : EDM Kit 24
AN : Tri Bass 8
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 64
PC : 116
B53 TechHouse2
Genre : Tech House
D1 : MinStack Ld4 Lead
D2 : Mute Guitar Keyboard
DR : EDM Kit 25
AN : Tri Bass 9
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 64
PC : 117
B54 TechHouse3
Genre : Tech House
D1 : RETROX 139 2 Strings/Pad
D2 : E.Grand 2 Keyboard
DR : EDM Kit 26
AN : Tri Bass 10
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 64
PC : 118
B55 Hardstyle 2
Genre : Hardstyle
D1 : Sliding Lead Lead
D2 : Noise Hit 2 FX/Other
DR : TR-909 Kit41
AN : SideChainBs2
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 119

B56 Hardstyle 3
Genre : Hardstyle
D1 : Synth Crazy Seq
D2 : FallingS-Saw Seq
DR : TR-909 Kit42
AN : HarderKickBs
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 120
B57 Hardstyle 4
Genre : Hardstyle
D1 : SideChainPd4 Strings/Pad
D2 : Lets go fast Lead
DR : TR-909 Kit43
AN : Open Bass
Measure Length : 1
Scale : 1/16
Tempo : 160
MSB : 85
LSB : 64
PC : 121
B58 Hardstyle 5
Genre : Hardstyle
D1 : Ahhh Bass
D2 : Detuner Man Lead
DR : TR-909 Kit44
AN : Big Kick
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 122
B59 Hardstyle 6
Genre : HardStyle
D1 : UnisonBuzzLd Lead
D2 : SawBuzz Ld 2 Lead
DR : TR-909 Kit45
AN : SawSweep Bs2
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 64
PC : 123
B60 Hardcore 1
Genre : Hardcore
Techno
D1 : Sonar Noise FX/Other
D2 : Hover Lead 3 Lead
DR : TR-909 Kit46
AN : Pulse SEQ 2
Measure Length : 2
Scale : 1/16
Tempo : 170
MSB : 85
LSB : 64
PC : 124
B61 Hardcore 2
Genre : Hardcore
Techno
D1 : Dist Saw SEQ Seq
D2 : SqrUnisonRif Seq
DR : Hardcore Kit
AN : Dist LFO Bs2
Measure Length : 2
Scale : 1/16
Tempo : 190
MSB : 85
LSB : 64
PC : 125
B62 Gabbas
Genre : Gabba
D1 : Sqr+Sine Ld Lead
D2 : Pan S-Saw Ld Lead
DR : Gabba Kit
AN : Dist TB Bs 2
Measure Length : 2
Scale : 1/16
Tempo : 202
MSB : 85
LSB : 64
PC : 126
B63 90'S TRANCE
Genre : Trance
D1 : Seq Bass 6 Bass
D2 : House Bass 4 Bass
DR : Techno Kit10
AN : Tranalog
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 127
B64 DEEP INSIDE
Genre : Trance
D1 : Buzz Lead 6 Lead
D2 : Soft ResoPd2 Strings/Pad
DR : 808&909 Kit9
AN : Oompf Bass
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 64
PC : 128
C01 SHIFTER
Genre : Trance
D1 : 106 Bass 7 Bass
D2 : LFO Pad 4 Strings/Pad
DR : Hiphop Kit11
AN : Trance Bass1
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 1
C02 TEMPER
Genre : Trance
D1 : Filter Bass2 Bass
D2 : SEQ Saw 3 FX/Other
DR : 808&909Kit10
AN : Arpy Synth
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 2
C03 EXILE
Genre : Trance
D1 : 5th Stac Bs3 Bass
D2 : JUNO Sqr Bs3 Bass
DR : 808&909Kit11
AN : Exile Synth
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 3
C04 TOXIC
Genre : Trance
D1 : Buzz Lead 7 Lead
D2 : Seq Bass 7 Bass
DR : 808&909Kit12
AN : Toxic Bass 2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 4
C05 Trance 2
Genre : Trance
D1 : Beauty Bass
D2 : Trance Pad Lead
DR : Techno Kit11
AN : Sync Bass
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 5
C06 Trance 3
Genre : Trance
D1 : Dots Seq
D2 : More Bass Bass
DR : TR-909 Kit47
AN : LFO Line
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 65
PC : 6
C07 Trance 4
Genre : Trance
D1 : SuperSaw Hit Seq
D2 : SlidngPtchLd Lead
DR : TR-909 Kit48
AN : More Bass
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 7
C08 NEURAL
Genre : Trance
D1 : Acid SEQ Bass
D2 : SawDetuneSEQ Brass
DR : TR-909 Kit49
AN : DarkSawBass1
Measure Length : 1
Scale : 1/16
Tempo : 136
MSB : 85
LSB : 65
PC : 8
C09 Trance 5
Genre : Trance
D1 : Pluck /Vel Seq
D2 : SideChainPd6 Seq
DR : TR-909 Kit50
AN : Sqr Bass 4
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 9
C10 Trance 6
Genre : Trance
D1 : S-Saw Pad 4 Seq
D2 : SideChainPd7 Strings/Pad
DR : TR-909 Kit51
AN : Trance Bass2
Measure Length : 2
Scale : 1/16
Tempo : 134
MSB : 85
LSB : 65
PC : 10

C11 Trance 7
Genre : Trance
D1 : Clv&Sync/Vel Keyboard
D2 : Sqr Buzz Ld3 Lead
DR : TR-909 Kit52
AN : Psy Bass 4
Measure Length : 2
Scale : 1/16
Tempo : 137
MSB : 85
LSB : 65
PC : 11
C12 Trance 8
Genre : Trance
D1 : BPF Syn Bs 3 Bass
D2 : Super Saw 10 Seq
DR : TR-909 Kit53
AN : Sqr SEQ 4
Measure Length : 1
Scale : 1/16
Tempo : 135
MSB : 85
LSB : 65
PC : 12
C13 DIGI
Genre : Psytrance
D1 : Square Ld 4 Lead
D2 : Reso Bass 7 Bass
DR : Techno Kit12
AN : Psy Bass 5
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 13
C14 Psytrance
Genre : Psytrance
D1 : Wobble Bs 11 Bass
D2 : Seq Bass 8 Bass
DR : 808&7*7 Kit7
AN : Psy Bass 6
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 14
C15 VIBRATION
Genre : R&B
D1 : PaperclipHit Seq
D2 : FM E.Piano 3 Keyboard
DR : 707&727 Kit4
AN : ResoSaw Bs 3
Measure Length : 1
Scale : 1/16
Tempo : 82
MSB : 85
LSB : 65
PC : 15
C16 R&B
Genre : R&B
D1 : Trem EP 2 Keyboard
D2 : MG Bass 5 Bass
DR : R&B Kit 3
AN : Sine Lead 2
Measure Length : 1
Scale : 1/32
Tempo : 70
MSB : 85
LSB : 65
PC : 16
C17 Hip-Hop 2
Genre : Hip-hop
D1 : D. Mute Gtr2 Keyboard
D2 : Flutter Saw Lead
DR : Hiphop Kit12
AN : Stinger Bass
Measure Length : 1
Scale : 1/16
Tempo : 95
MSB : 85
LSB : 65
PC : 17
C18 Hip-Hop 3
Genre : Hip-hop
D1 : BPF Syn Bs 4 Bass
D2 : Tekno Lead 7 Lead
DR : Hiphop Kit13
AN : Beep Synth
Measure Length : 1
Scale : 1/16
Tempo : 90
MSB : 85
LSB : 65
PC : 18
C19 SWAG BABY
Genre : Hip-hop
D1 : Vintager 2 Lead
D2 : SEQ Saw 4 FX/Other
DR : R&B Kit 4
AN : Xi Power Bs
Measure Length : 1
Scale : 1/16
Tempo : 96
MSB : 85
LSB : 65
PC : 19
C20 FLY EAST
Genre : Hip-Hop
D1 : Synth Flute Lead
D2 : Super Saw 11 Seq
DR : TR-808 Kit21
AN : Saw Bass 6
Measure Length : 2
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 65
PC : 20
C21 Hip-Hop 4
Genre : Hip-Hop
D1 : 5th SawLead2 Lead
D2 : Monster Bs 8 Bass
DR : Hiphop Kit14
AN : Sub Bass 2
Measure Length : 2
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 21
C22 SLACK NOIZ
Genre : Hip-Hop
D1 : LFO CarvePd3 Strings/Pad
D2 : JD Piano 3 Keyboard
DR : Hiphop Kit15
AN : Orient Flute
Measure Length : 2
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 22
C23 Hip-Hop 5
Genre : Hip-Hop
D1 : Oldskool Strings/Pad
D2 : Gator Strings/Pad
DR : 808&7*7 Kit8
AN : Robo sweep
Measure Length : 1
Scale : 1/32
Tempo : 75
MSB : 85
LSB : 65
PC : 23
C24 Trap 1
Genre : Trap
D1 : RiSER 3 FX/Other
D2 : Super Saw 12 Lead
DR : TR-909 Kit54
AN : LFBlow
Measure Length : 1
Scale : 1/16
Tempo : 78
MSB : 85
LSB : 65
PC : 24
C25 Trap 2
Genre : Trap
D1 : Monster Bs 9 Bass
D2 : EDM Synth 4 Seq
DR : TR-909 Kit55
AN : Celoclip 2
Measure Length : 1
Scale : 1/16
Tempo : 92
MSB : 85
LSB : 65
PC : 25
C26 BELFREEZ
Genre : Trap
D1 : Fantasy 2 Strings/Pad
D2 : Wide Bass 2 Bass
DR : TR-909 Kit56
AN : Resocut 2
Measure Length : 1
Scale : 1/16
Tempo : 98
MSB : 85
LSB : 65
PC : 26
C27 BAD GIRLZ
Genre : Trap
D1 : JD RingMod 4 Lead
D2 : 106 Bass 8 Bass
DR : TR-909 Kit57
AN : Creeper
Measure Length : 1
Scale : 1/16
Tempo : 136
MSB : 85
LSB : 65
PC : 27
C28 DRAGONFLY
Genre : Trap
D1 : Awakening 3 Strings/Pad
D2 : 106 Bass 9 Bass
DR : TR-909 Kit58
AN : Sub Pulse
Measure Length : 1
Scale : 1/16
Tempo : 68
MSB : 85
LSB : 65
PC : 28
C29 BURNED
Genre : Trap
D1 : HPF Poly 4 Strings/Pad
D2 : Buzz Lead 8 Lead
DR : TR-909 Kit59
AN : Chewy
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 65
PC : 29
C30 Trap 3
Genre : Trap
D1 : EDM Synth 5 Seq
D2 : Tri Stac Ld3 Lead
DR : TR-909 Kit60
AN : TriPE
Measure Length : 1
Scale : 1/32
Tempo : 75
MSB : 85
LSB : 65
PC : 30

C31 CLAX
Genre : Trap
D1 : D-50 Pizz 2 Strings/Pad
D2 : Cincosoft 2 Strings/Pad
DR : TR-909 Kit61
AN : Orange Alert
Measure Length : 1
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 65
PC : 31
C32 CRUTCHES
Genre : Trap
D1 : JP8 Strings6 Strings/Pad
D2 : Monster Bs10 Bass
DR : TR-909 Kit62
AN : ZipPhase 2
Measure Length : 1
Scale : 1/32
Tempo : 80
MSB : 85
LSB : 65
PC : 32
C33 Trap 4
Genre : Trap
D1 : Buzz Lead 9 Lead
D2 : Psychoscilo2 Strings/Pad
DR : 90's Kit 2
AN : SawLFO Bass1
Measure Length : 1
Scale : 1/32
Tempo : 74
MSB : 85
LSB : 65
PC : 33
C34 BACKFLIP
Genre : Trap
D1 : Syn Sniper 3 Strings/Pad
D2 : Monster Bs11 Bass
DR : R&B Kit 5
AN : Hollwcrisp
Measure Length : 1
Scale : 1/32
Tempo : 70
MSB : 85
LSB : 65
PC : 34
C35 DENIED
Genre : Trap
D1 : SawBuzz Ld 3 Lead
D2 : SqrTrapPlk 5 Seq
DR : TR-808 Kit22
AN : Stinger 2
Measure Length : 1
Scale : 1/32
Tempo : 76
MSB : 85
LSB : 65
PC : 35
C36 NEEDED
Genre : Trap
D1 : Syn Sniper 4 Strings/Pad
D2 : PXZoon 2 Strings/Pad
DR : TR-808 Kit23
AN : Foundry
Measure Length : 1
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 65
PC : 36
C37 THE UNGOOD
Genre : Trap
D1 : Trance Key 6 Seq
D2 : Detune Bs 3 Bass
DR : R&B Kit 6
AN : Chatter
Measure Length : 1
Scale : 1/32
Tempo : 96
MSB : 85
LSB : 65
PC : 37
C38 Trap 5
Genre : Trap
D1 : Syn Sniper 5 Strings/Pad
D2 : Monster Bs12 Bass
DR : R&B Kit 7
AN : Buzzreed
Measure Length : 1
Scale : 1/32
Tempo : 74
MSB : 85
LSB : 65
PC : 38
C39 GET THE $
Genre : Trap
D1 : OSC-SyncLd 3 Lead
D2 : Ac. Brs Sect Brass
DR : R&B Kit 8
AN : Sus Zap 2
Measure Length : 1
Scale : 1/32
Tempo : 88
MSB : 85
LSB : 65
PC : 39
C40 Trap 6
Genre : Trap
D1 : Tekno Lead 8 Lead
D2 : Buzz Lead 10 Lead
DR : R&B Kit 9
AN : Bowouch 2
Measure Length : 1
Scale : 1/32
Tempo : 88
MSB : 85
LSB : 65
PC : 40
C41 Trap 7
Genre : Trap
D1 : D-50 Stack 2 Strings/Pad
D2 : LFO CarvePd4 Strings/Pad
DR : TR-808 Kit24
AN : Roomboom
Measure Length : 1
Scale : 1/32
Tempo : 62
MSB : 85
LSB : 65
PC : 41
C42 CLONED
Genre : Trap
D1 : Rising SEQ 2 FX/Other
D2 : UnisonSynBs2 Bass
DR : TR-808 Kit25
AN : Icepick
Measure Length : 1
Scale : 1/16
Tempo : 70
MSB : 85
LSB : 65
PC : 42
C43 ANTIHERO
Genre : Trap
D1 : SEQ Tri 3 FX/Other
D2 : Syn Vox 2 FX/Other
DR : TR-808 Kit26
AN : SawLFO Bass2
Measure Length : 1
Scale : 1/32
Tempo : 96
MSB : 85
LSB : 65
PC : 43
C44 CHOKED
Genre : Trap
D1 : RETROX 139 3 Strings/Pad
D2 : WaveShapeLd3 Lead
DR : TR-808 Kit27
AN : Tanker
Measure Length : 1
Scale : 1/32
Tempo : 96
MSB : 85
LSB : 65
PC : 44
C45 C-SHOP
Genre : Trap
D1 : Kick Bass 2 Bass
D2 : SideChainPd8 Strings/Pad
DR : TR-909 Kit63
AN : Lobotone
Measure Length : 1
Scale : 1/16
Tempo : 76
MSB : 85
LSB : 65
PC : 45
C46 NEON
Genre : Trap
D1 : Kick Bass 3 Bass
D2 : Super Saw 13 Lead
DR : TR-909 Kit64
AN : DarkSawBass2
Measure Length : 1
Scale : 1/32
Tempo : 78
MSB : 85
LSB : 65
PC : 46
C47 BRONZE
Genre : Trap
D1 : SideChainBs5 Bass
D2 : Super Saw 14 Lead
DR : TR-909 Kit65
AN : Copper Tone
Measure Length : 1
Scale : 1/16
Tempo : 74
MSB : 85
LSB : 65
PC : 47
C48 FROST
Genre : Trap
D1 : FX 4 FX/Other
D2 : Dreaming 2 Strings/Pad
DR : TR-909 Kit66
AN : Popsickle
Measure Length : 1
Scale : 1/32
Tempo : 67
MSB : 85
LSB : 65
PC : 48
C49 DRILLED
Genre : Trap
D1 : Rising SEQ 3 FX/Other
D2 : Super Saw 15 Lead
DR : TR-909 Kit67
AN : Looowww
Measure Length : 1
Scale : 1/32
Tempo : 72
MSB : 85
LSB : 65
PC : 49
C50 BUZZ KILL
Genre : Trap
D1 : Rising SEQ 4 FX/Other
D2 : Bend Lead 3 FX/Other
DR : TR-909 Kit68
AN : ToadThroat
Measure Length : 1
Scale : 1/32
Tempo : 76
MSB : 85
LSB : 65
PC : 50

C51 TRAPPED
Genre : Trap
D1 : Square Ld 5 Lead
D2 : SawTrap Ld 3 Lead
DR : TR-808 Kit28
AN : Spooky Bass1
Measure Length : 2
Scale : 1/16
Tempo : 74
MSB : 85
LSB : 65
PC : 51
C52 PUMP THAT
Genre : Trap
D1 : Hover Lead 4 Lead
D2 : Bend Lead 4 FX/Other
DR : 808&909Kit13
AN : HooverSuprt2
Measure Length : 2
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 65
PC : 52
C53 Trap 8
Genre : Trap
D1 : Sqr Trap Ld2 Lead
D2 : O'Skool Hit2 FX/Other
DR : Hiphop Kit16
AN : Long & Deep
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 65
PC : 53
C54 Trap 9
Genre : Trap
D1 : SquaredLFOLd Lead
D2 : Swelling Wow Seq
DR : TR-909 Kit69
AN : Harp Sub
Measure Length : 1
Scale : 1/32
Tempo : 130
MSB : 85
LSB : 65
PC : 54
C55 Trap 10
Genre : Trap
D1 : 808 Kick Bs Bass
D2 : Epic Saws Lead
DR : TR-909 Kit70
AN : Siren Hell 2
Measure Length : 1
Scale : 1/32
Tempo : 70
MSB : 85
LSB : 65
PC : 55
C56 Trap 11
Genre : Trap
D1 : Susans Horn Lead
D2 : Pluck You Bass
DR : TR-808 Kit29
AN : Little Bot
Measure Length : 1
Scale : 1/16
Tempo : 145
MSB : 85
LSB : 65
PC : 56
C57 LAZER CHEST
Genre : Trap
D1 : Super Saw 16 Lead
D2 : Super Saw 17 Lead
DR : TR-808 Kit30
AN : Zippers 5
Measure Length : 2
Scale : 1/32
Tempo : 130
MSB : 85
LSB : 65
PC : 57
C58 Trap 12
Genre : Trap
D1 : CuttingLead3 Lead
D2 : Growl Bass 6 Bass
DR : TR-808 Kit31
AN : Reel 2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 58
C59 TRAPPED DOOR
Genre : Trap
D1 : SawTrap Ld 4 Lead
D2 : Growl Bass 7 Bass
DR : TR-808 Kit32
AN : Reel 3
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 59
C60 Trap 13
Genre : Trap
D1 : D-50 Stack 3 Strings/Pad
D2 : LFO CarvePd5 Strings/Pad
DR : EDM Kit 27
AN : Fall Synth 2
Measure Length : 1
Scale : 1/32
Tempo : 140
MSB : 85
LSB : 65
PC : 60
C61 Trap 14
Genre : Trap
D1 : Sqr Trap Ld3 Lead
D2 : Tekno Lead 9 Lead
DR : EDM Kit 28
AN : Porta Lead 2
Measure Length : 1
Scale : 1/32
Tempo : 107
MSB : 85
LSB : 65
PC : 61
C62 Trap 15
Genre : Trap
D1 : SawBuzz Ld 4 Lead
D2 : Super Saw 18 Seq
DR : EDM Kit 29
AN : SirenFX/Mod2
Measure Length : 1
Scale : 1/32
Tempo : 140
MSB : 85
LSB : 65
PC : 62
C63 Trap 16
Genre : Trap
D1 : Kick Bass 4 Bass
D2 : Talking Bs 2 Bass
DR : Hiphop Kit17
AN : SqrTrapPluck
Measure Length : 1
Scale : 1/32
Tempo : 70
MSB : 85
LSB : 65
PC : 63
C64 Ambient
Genre : Ambient
D1 : Analog Str 4 Strings/Pad
D2 : Seq Bass 9 Bass
DR : Noise Kit 2
AN : Mustard
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 64
D01 INNER PEACE
Genre : Ambient
D1 : JP8 Strings7 Strings/Pad
D2 : Harp 3 Keyboard
DR : CR-78 Kit 3
AN : Sub Bass 3
Measure Length : 2
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 65
PC : 65
D02 CYGNUS X
Genre : Ambient
D1 : Syn Sniper 6 Strings/Pad
D2 : UnisonSynBs3 Bass
DR : TR-808 Kit33
AN : Cygnus Bass
Measure Length : 1
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 65
PC : 66
D03 DESCENT
Genre : Ambient
D1 : JP8 Strings8 Strings/Pad
D2 : Vibraphone 3 Keyboard
DR : TR-808 Kit34
AN : RelaxationBs
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 67
D04 CHILL WAVE
Genre : Chill Wave
D1 : Vox Pad/SC FX/Other
D2 : PlckSyn/Vel2 Bass
DR : EDM Kit 30
AN : SawLd&PanDly
Measure Length : 2
Scale : 1/16
Tempo : 90
MSB : 85
LSB : 65
PC : 68
D05 80s Re-Vamp
Genre : 80s Re-Vamp
D1 : UnderTheSea Strings/Pad
D2 : Pluck Me Bass
DR : 808&909Kit14
AN : Saw LFO Lead
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 69

D06 Experimental
Genre : Experimental
D1 : Deep Vibes Lead
D2 : Lil guy Bass
DR : TR-909 Kit71
AN : Wobbler sub
Measure Length : 1
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 65
PC : 70
D07 Future Bass
Genre : Future Bass
D1 : Weewoo Seq
D2 : Breathe Lead
DR : TR-909 Kit72
AN : Saw Bass 7
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 71
D08 PULL UP
Genre : Ghetto Funk
D1 : Soft Pad 3 Strings/Pad
D2 : PLS Pad 3 Strings/Pad
DR : 808&7*7 Kit9
AN : Zippers 6
Measure Length : 4
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 72
D09 GRIME TIME
Genre : Grime
D1 : Sqr Lead 2 Lead
D2 : D-50 Pizz 3 Strings/Pad
DR : TR-808 Kit35
AN : LFO Skips
Measure Length : 2
Scale : 1/32
Tempo : 135
MSB : 85
LSB : 65
PC : 73
D10 Electronica1
Genre : Electronica
D1 : Vib Wurly 3 Keyboard
D2 : LowBitSample Strings/Pad
DR : EDM Kit 31
AN : Tri Bass 11
Measure Length : 2
Scale : 1/16
Tempo : 132
MSB : 85
LSB : 65
PC : 74
D11 Electronica2
Genre : Electronica
D1 : Vib Wurly 4 Keyboard
D2 : Psychoscilo3 Strings/Pad
DR : EDM Kit 32
AN : Polta Lead
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 65
PC : 75
D12 Electronic
Genre : Electronic
D1 : Pop Lead Lead
D2 : Saw Pad Strings/Pad
DR : TR-909 Kit73
AN : SideChainHrd
Measure Length : 1
Scale : 1/16
Tempo : 116
MSB : 85
LSB : 65
PC : 76
D13 LATE NIGHT
Genre : Electronic
D1 : Sine Lead 6 Lead
D2 : Brite Str 2 Strings/Pad
DR : CR-78 Kit 4
AN : Spooky Bass2
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 77
D14 NEW WAVE
Genre : Electronic
D1 : S-SawStacLd4 Lead
D2 : Seq Bass 10 Bass
DR : TR-626 Kit 2
AN : Slime Bass
Measure Length : 1
Scale : 1/16
Tempo : 115
MSB : 85
LSB : 65
PC : 78
D15 70'S SEQ
Genre : Electronic
D1 : FilterEnvBs2 Bass
D2 : JUNO Octavr2 Seq
DR : Noise Kit 3
AN : Soak Bottle
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 79
D16 TRONIX
Genre : Electronic
D1 : JP8 Strings9 Strings/Pad
D2 : Seq Bass 11 Bass
DR : TR-606 Kit 3
AN : Lava Bass
Measure Length : 1
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 65
PC : 80
D17 CRUISING
Genre : Electronic
D1 : MG Bass 6 Bass
D2 : Analog Str 5 Strings/Pad
DR : Drum&BsKit10
AN : Attack Bass
Measure Length : 1
Scale : 1/16
Tempo : 90
MSB : 85
LSB : 65
PC : 81
D18 Ring Mod
Genre : Electronic
D1 : SinDetuneBs2 Bass
D2 : PluckBacking Seq
DR : TR-808 Kit36
AN : Saw+Sub Lead
Measure Length : 1
Scale : 1/16
Tempo : 90
MSB : 85
LSB : 65
PC : 82
D19 LoFi
Genre : Electronic
D1 : Flute 2 Brass
D2 : Trem EP 3 Keyboard
DR : 90's Kit 3
AN : Sqr+Sub Bs 2
Measure Length : 1
Scale : 1/16
Tempo : 90
MSB : 85
LSB : 65
PC : 83
D20 DUCKS ATTACK
Genre : Electro
D1 : Dist Flt TB3 Lead
D2 : Seq Bass 12 Bass
DR : TR-808 Kit37
AN : Gargle
Measure Length : 1
Scale : 1/16
Tempo : 124
MSB : 85
LSB : 65
PC : 84
D21 ILLEKTRO
Genre : Electro
D1 : Organ Bass 5 Bass
D2 : JUNO Str 2 Strings/Pad
DR : 808&909Kit15
AN : Roller Bass
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 85
D22 ELECTROFYING
Genre : Electro
D1 : Square Ld 6 Lead
D2 : JP8 Str 10 Strings/Pad
DR : TR-808 Kit38
AN : Drama Lead
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 86
D23 Electro 2
Genre : Electro
D1 : 5th SawLead3 Lead
D2 : Tri Stac Ld4 Lead
DR : 808&909Kit16
AN : PulseOfLife2
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 87
D24 Electro 3
Genre : Electro
D1 : Groovy Pluck Seq
D2 : High Clicks Seq
DR : TR-909 Kit74
AN : Sawed Out
Measure Length : 1
Scale : 1/16
Tempo : 114
MSB : 85
LSB : 65
PC : 88
D25 Electro 4
Genre : Electro
D1 : Stab it Lead
D2 : Old whip Bass
DR : TR-909 Kit75
AN : Afro Crack
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 65
PC : 89

D26 Electro 5
Genre : Electro
D1 : Crusty Ba$$ Lead
D2 : Laserhead FX/Other
DR : TR-909 Kit76
AN : Init Grime
Measure Length : 1
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 65
PC : 90
D27 Electro 6
Genre : Electro
D1 : Big Plucker Bass
D2 : Creeper Lead
DR : TR-909 Kit77
AN : Guitar Sweep
Measure Length : 1
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 91
D28 Electro 7
Genre : Electro
D1 : Metallic Aci Lead
D2 : Throw Up Lead
DR : TR-808 Kit39
AN : Crying Alien
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 65
PC : 92
D29 Gio-Gio-MRD
Genre : Electro
D1 : Pulse Synth Seq
D2 : S-Saw Pad 5 Strings/Pad
DR : Techno Kit13
AN : Pulse Bass 2
Measure Length : 1
Scale : 1/16
Tempo : 136
MSB : 85
LSB : 65
PC : 93
D30 MAINLINE
Genre : Breakbeat
D1 : PLS Pad 4 Strings/Pad
D2 : House Org 6 Keyboard
DR : Hiphop Kit18
AN : Drift & Grit
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 94
D31 FIRE FIGHT
Genre : Breakbeat
D1 : SEQ 5 Seq
D2 : Low Bass 4 Bass
DR : Hiphop Kit19
AN : Fat as That2
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 95
D32 END OF NIGHT
Genre : Breakbeat
D1 : JD Piano 4 Keyboard
D2 : Detune Bs 4 Bass
DR : Hiphop Kit20
AN : PWM Basic
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 96
D33 LOCK UP!
Genre : Garage
D1 : Sine Lead 7 Lead
D2 : D-50 Pizz 4 Strings/Pad
DR : TR-909 Kit78
AN : Knat Squat
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 97
D34 MINISTRY
Genre : Garage
D1 : Hollow Pad 5 Strings/Pad
D2 : JD Piano 5 Keyboard
DR : TR-909 Kit79
AN : ReeceClassic
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 98
D35 LORNA's VIBE
Genre : Garage
D1 : Revalation 3 Strings/Pad
D2 : JD Piano 6 Keyboard
DR : TR-909 Kit80
AN : Bouncy Bass2
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 99
D36 GOPHER GOLD
Genre : Garage
D1 : Sine Lead 8 Lead
D2 : Sine Lead 9 Lead
DR : TR-909 Kit81
AN : Slurry Bass
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 100
D37 Chiptune 1
Genre : Chiptune
D1 : 8bitSqr /Mod Bass
D2 : EDM Synth 6 Seq
DR : EDM Kit 33
AN : 8bitBass/Leg
Measure Length : 2
Scale : 1/16
Tempo : 170
MSB : 85
LSB : 65
PC : 101
D38 Chiptune 2
Genre : Chiptune
D1 : 8bit Per Seq
D2 : DirtyBass/SC Seq
DR : EDM Kit 34
AN : Bleep Bass
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 65
PC : 102
D39 9BIT
Genre : Chiptune
D1 : Sqr Backing Seq
D2 : Sqr SEQ Seq
DR : ElectricKit1
AN : Tri Bass 12
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 103
D40 STRIKE
Genre : Chiptune
D1 : Tri Bass 2 Bass
D2 : Sqr+Pls Pad Strings/Pad
DR : 707&727 Kit5
AN : Sqr SEQ 5
Measure Length : 2
Scale : 1/16
Tempo : 175
MSB : 85
LSB : 65
PC : 104
D41 90sVideoGame
Genre : Chiptune
D1 : Dist Guitar2 Keyboard
D2 : 4Op FM Bass2 Bass
DR : TR-626 Kit 3
AN : Pulse Lead 3
Measure Length : 2
Scale : 1/16
Tempo : 150
MSB : 85
LSB : 65
PC : 105
D42 Synth Pop
Genre : Synth Pop
D1 : Saw+S-SawSEQ Strings/Pad
D2 : ResoSweepPd2 Seq
DR : Techno Kit14
AN : Saw Bass 8
Measure Length : 2
Scale : 1/16
Tempo : 125
MSB : 85
LSB : 65
PC : 106
D43 TECHOtooOLD
Genre : Synth Pop
D1 : Saw+S-Saw Pd Bass
D2 : Synth Snare FX/Other
DR : TR-808 Kit40
AN : Analog Kick2
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 107
D44 Idol Error
Genre : Synth Pop
D1 : DistBacking2 Seq
D2 : Saw+Sqr Riff Seq
DR : Techno Kit15
AN : ResoSaw Bs 4
Measure Length : 1
Scale : 1/16
Tempo : 136
MSB : 85
LSB : 65
PC : 108
D45 Fancy'70s
Genre : Synth Pop
D1 : LFO S-SawSyn Strings/Pad
D2 : Saw+Sqr SEQ1 Seq
DR : CR-78 Kit 5
AN : Tri+Sub SEQ
Measure Length : 1
Scale : 1/16
Tempo : 118
MSB : 85
LSB : 65
PC : 109

D46E E 1024K
Genre : Synth Pop
D1 : ResoSaw SEQ2 Seq
D2 : S&H Reso Pad Strings/Pad
DR : ElectricKit2
AN : Pulse Bass 3
Measure Length : 2
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 110
D47 SYMPATHY
Genre : Eurobeat
D1 : MMM Box Bs Bass
D2 : S-Saw Pad 6 Seq
DR : Techno Kit16
AN : Sqr SEQ 6
Measure Length : 1
Scale : 1/16
Tempo : 126
MSB : 85
LSB : 65
PC : 111
D48 Eurobeat
Genre : Eurobeat
D1 : 4Op FM Bass3 Bass
D2 : Bend SynBrs1 Brass
DR : 80's Kit 2
AN : PulseSweepLd
Measure Length : 2
Scale : 1/16
Tempo : 125
MSB : 85
LSB : 65
PC : 112
D49 Pop 1
Genre : Pop
D1 : Monster Bs13 Bass
D2 : Bend SynBrs2 Brass
DR : R&B Kit 10
AN : Sub Buzz Bs
Measure Length : 1
Scale : 1/16
Tempo : 80
MSB : 85
LSB : 65
PC : 113
D50 POP STAR
Genre : Pop
D1 : Monster Bs14 Bass
D2 : SawBuzz Ld 5 Lead
DR : R&B Kit 11
AN : Rub Bass
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 114
D51 Pop 2
Genre : Pop
D1 : PortaSaw Ld2 Lead
D2 : Tekno Lead10 Lead
DR : EDM Kit 35
AN : Xi Saw
Measure Length : 1
Scale : 1/16
Tempo : 95
MSB : 85
LSB : 65
PC : 115
D52 TWERK IT
Genre : Pop
D1 : Vintager 3 Lead
D2 : Monster Bs15 Bass
DR : TR-808 Kit41
AN : Boing Synth
Measure Length : 1
Scale : 1/16
Tempo : 100
MSB : 85
LSB : 65
PC : 116
D53 DREAM
Genre : Pop
D1 : SynStrBackng Seq
D2 : Pluck Synth4 Seq
DR : Pop Kit 3
AN : ResoSaw Bs 5
Measure Length : 1
Scale : 1/16
Tempo : 110
MSB : 85
LSB : 65
PC : 117
D54 YOKAI
Genre : Pop
D1 : Stiff Bass Bass
D2 : S-Saw Pad 7 Seq
DR : ElectricKit3
AN : Sqr SEQ 7
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 118
D55 Fake Side
Genre : Pop
D1 : Oct Saw Bass Bass
D2 : SideChainPd9 Strings/Pad
DR : TR-909 Kit82
AN : PortaSaw Ld2
Measure Length : 2
Scale : 1/16
Tempo : 135
MSB : 85
LSB : 65
PC : 119
D56 CHANCE!
Genre : Pop
D1 : OSC-SyncLd 4 Lead
D2 : Bright Pad 3 Strings/Pad
DR : 80's Kit 3
AN : Saw Bs&SEQ
Measure Length : 2
Scale : 1/16
Tempo : 130
MSB : 85
LSB : 65
PC : 120
D57 Pop 3
Genre : Pop
D1 : Awakening 4 Strings/Pad
D2 : Chubby SEQ Lead
DR : Pop Kit 4
AN : Saw+Sub Bs 5
Measure Length : 2
Scale : 1/16
Tempo : 128
MSB : 85
LSB : 65
PC : 121
D58 Pop 4
Genre : Pop
D1 : Funk Guitar2 Keyboard
D2 : Slap Bass 2 Bass
DR : Pop Kit 5
AN : ResoPulseSEQ
Measure Length : 1
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 65
PC : 122
D59 Pop 5
Genre : Pop
D1 : Fantasy 3 Strings/Pad
D2 : FM E.Piano 4 Keyboard
DR : TR-808 Kit42
AN : Saw Bass 9
Measure Length : 1
Scale : 1/16
Tempo : 70
MSB : 85
LSB : 65
PC : 123
D60 GENIE SMOKE
Genre : Other
D1 : Fantasy 4 Strings/Pad
D2 : Sine Lead 10 Lead
DR : CR-78 Kit 6
AN : PWM Base 2
Measure Length : 2
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 124
D61 Orch
Genre : Symphony
D1 : Strings 2 Strings/Pad
D2 : Harp 4 Keyboard
DR : Pop Kit 6
AN : Analog Tp 2
Measure Length : 1
Scale : 1/8 Triple
Tempo : 120
MSB : 85
LSB : 65
PC : 125
D62 Vocoder Tmpl
Genre : Template
D1 : Voc:Ensemble FX/Other
D2 : UnisonSynBs4 Bass
DR : Pop Kit 7
AN : Init Tone
Measure Length : 1
Scale : 1/16
Tempo : 140
MSB : 85
LSB : 65
PC : 126
D63 AutoPch Tmpl
Genre : Template
D1 : AP:Elct Pch1 ---
D2 : Fingerd Bs 2 Bass
DR : Pop Kit 8
AN : Init Tone
Measure Length : 1
Scale : 1/16
Tempo : 120
MSB : 85
LSB : 65
PC : 127
D64 Voice In
Genre : Template
D1 : Voice In ---
D2 : Seq Bass 13 Bass
DR : TR-909 Kit83
AN : Init Tone
Measure Length : 1
Scale : 1/16
Tempo : 135
MSB : 85
LSB : 65
PC : 128

"""


# Regular expression to match each program entry
program_regex = re.compile(
    r"(?P<id>[A-D]\d{2}) (?P<name>.+?)\n"
    r"Genre : (?P<genre>.+?)\n"
    r"D1 : (?P<d1>.+?)\n"
    r"D2 : (?P<d2>.+?)\n"
    r"DR : (?P<dr>.+?)\n"
    r"AN : (?P<an>.+?)\n"
    r"Measure Length : (?P<measure_length>\d+)\n"
    r"Scale : (?P<scale>.+?)\n"
    r"Tempo : (?P<tempo>\d+)\n"
    r"MSB : (?P<msb>\d+)\n"
    r"LSB : (?P<lsb>\d+)\n"
    r"PC : (?P<pc>\d+)"
)

# Parse the data
programs = []
for match in program_regex.finditer(data):
    program = match.groupdict()
    programs.append(program)

# Convert to JSON
json_data = json.dumps(programs, indent=4)

# Print or save the JSON data
print(json_data)

from pathlib import Path
# Save to file
with open(Path.home() / 'programs.json', 'w') as f:
    f.write(json_data)
