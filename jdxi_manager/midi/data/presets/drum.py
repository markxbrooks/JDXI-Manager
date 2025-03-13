DRUM_PRESETS_ENUMERATED = [
    '001: TR-909 Kit 1', '002: TR-808 Kit 1', '003: 707&727 Kit1', '004: CR-78 Kit 1', '005: TR-606 Kit 1',
    '006: TR-626 Kit 1', '007: EDM Kit 1',
    '008: Drum&Bs Kit1', '009: Techno Kit 1', '010: House Kit 1', '011: Hiphop Kit 1', '012: R&B Kit 1',
    '013: TR-909 Kit 2', '014: TR-909 Kit 3',
    '015: TR-808 Kit 2', '016: TR-808 Kit 3', '017: TR-808 Kit 4', '018: 808&909 Kit1', '019: 808&909 Kit2',
    '020: 707&727 Kit2', '021: 909&7*7 Kit1',
    '022: 808&7*7 Kit1', '023: EDM Kit 2', '024: Techno Kit 2', '025: Hiphop Kit 2', '026: 80\'s Kit 1',
    '027: 90\'s Kit 1', '028: Noise Kit 1',
    '029: Pop Kit 1', '030: Pop Kit 2', '031: Rock Kit', '032: Jazz Kit', '033: Latin Kit'
]
DRUM_KITS = [
    "TR-808", "TR-909", "CR-78", "TR-606", "TR-707", "ACOUSTIC", "JAZZ", "HOUSE",
    "TECHNO", "HIP-HOP", "DANCE", "ROCK", "ELECTRONIC", "PERCUSSION", "SFX", "USER"
]
DRUM_PARTS = [
    "KICK", "SNARE", "CLOSED HAT", "OPEN HAT", "TOM/PERC 1",
    "TOM/PERC 2", "CRASH/PERC 3", "RIDE/PERC 4"
]
DRUM_CATEGORIES = {
    'Classic Roland': {
        'TR-808': {
            'description': 'The legendary Roland TR-808 sound. Known for deep kick, snappy snare, and iconic cowbell.',
            'style': 'Hip-Hop, Electronic, Pop',
            'era': '1980s'
        },
        'TR-909': {
            'description': 'The Roland TR-909 kit. Punchy kick, crisp hi-hats, and powerful snare. House music staple.',
            'style': 'House, Techno, Dance',
            'era': '1980s'
        },
        'CR-78': {
            'description': 'The CompuRhythm CR-78. Warm, vintage sounds with unique character.',
            'style': 'Pop, Electronic',
            'era': '1970s'
        },
        'TR-606': {
            'description': 'The Drumatix TR-606. Sharp, tight sounds perfect for electronic music.',
            'style': 'Electronic, Experimental',
            'era': '1980s'
        },
        'TR-707': {
            'description': 'Digital drum sounds from the TR-707. Clean and punchy.',
            'style': 'Pop, Dance',
            'era': '1980s'
        }
    },
    'Acoustic': {
        'ACOUSTIC': {
            'description': 'Natural acoustic drum kit with studio-quality samples.',
            'style': 'Rock, Pop, Jazz',
            'era': 'Modern'
        },
        'JAZZ': {
            'description': 'Classic jazz kit with brushes and warm tones.',
            'style': 'Jazz, Blues',
            'era': 'Classic'
        }
    },
    'Electronic': {
        'HOUSE': {
            'description': 'Modern house music kit with tight kicks and crisp hats.',
            'style': 'House, Dance',
            'era': 'Modern'
        },
        'TECHNO': {
            'description': 'Hard-hitting techno kit with industrial elements.',
            'style': 'Techno, Industrial',
            'era': 'Modern'
        },
        'ELECTRONIC': {
            'description': 'Versatile electronic kit with modern production sounds.',
            'style': 'Electronic, Pop',
            'era': 'Modern'
        }
    },
    'Urban': {
        'HIP-HOP': {
            'description': 'Contemporary hip-hop kit with deep kicks and sharp snares.',
            'style': 'Hip-Hop, R&B',
            'era': 'Modern'
        },
        'DANCE': {
            'description': 'High-energy dance kit with punchy sounds.',
            'style': 'Dance, Pop',
            'era': 'Modern'
        }
    },
    'Band': {
        'ROCK': {
            'description': 'Powerful rock kit with big room sound.',
            'style': 'Rock, Alternative',
            'era': 'Modern'
        }
    },
    'Special': {
        'PERCUSSION': {
            'description': 'World percussion collection with various ethnic instruments.',
            'style': 'World, Percussion',
            'era': 'Various'
        },
        'SFX': {
            'description': 'Sound effects and experimental percussion.',
            'style': 'Experimental, Electronic',
            'era': 'Modern'
        },
        'USER': {
            'description': 'User-programmable kit for custom sounds.',
            'style': 'Any',
            'era': 'Custom'
        }
    }
}
DRUM_KIT_MAP = {
    kit_name: {
        'main_category': main_cat,
        'description': info['description'],
        'style': info['style'],
        'era': info['era']
    }
    for main_cat, subcats in DRUM_CATEGORIES.items()
    for kit_name, info in subcats.items()
}
DRUM_WAVES = ['000: Off',
'001: 78 Kick P',    '002: 606 Kick P',   '003: 808 Kick 1aP', '004: 808 Kick 1bP', '005: 808 Kick 1cP', '006: 808 Kick 2aP', '007: 808 Kick 2bP',
'008: 808 Kick 2cP', '009: 808 Kick 3aP', '010: 808 Kick 3bP', '011: 808 Kick 3cP', '012: 808 Kick 4aP', '013: 808 Kick 4bP', '014: 808 Kick 4cP',
'015: 808 Kick 1Lp', '016: 808 Kick 2Lp', '017: 909 Kick 1aP', '018: 909 Kick 1bP', '019: 909 Kick 1cP', '020: 909 Kick 2bP', '021: 909 Kick 2cP',
'022: 909 Kick 3P',  '023: 909 Kick 4',   '024: 909 Kick 5',   '025: 909 Kick 6',   '026: 909 DstKickP', '027: 909 Kick Lp',  '028: 707 Kick 1 P',
'029: 707 Kick 2 P', '030: 626 Kick 1 P', '031: 626 Kick 2 P', '032: Analog Kick1', '033: Analog Kick2', '034: Analog Kick3', '035: Analog Kick4',
'036: Analog Kick5', '037: PlasticKick1', '038: PlasticKick2', '039: Synth Kick 1', '040: Synth Kick 2', '041: Synth Kick 3', '042: Synth Kick 4',
'043: Synth Kick 5', '044: Synth Kick 6', '045: Synth Kick 7', '046: Synth Kick 8', '047: Synth Kick 9', '048: Synth Kick10', '049: Synth Kick11',
'050: Synth Kick12', '051: Synth Kick13', '052: Synth Kick14', '053: Synth Kick15', '054: Vint Kick P',  '055: Jungle KickP', '056: HashKick 1 P',
'057: HashKick 2 P', '058: Lite Kick P',  '059: Dry Kick 1',   '060: Dry Kick 2',   '061: Tight Kick P', '062: Old Kick',     '063: Warm Kick P',
'064: Hush Kick P',  '065: Power Kick',   '066: Break Kick',   '067: Turbo Kick',   '068: TM-2 Kick 1',  '069: TM-2 Kick 2',  '070: PurePhatKckP',
'071: Bright KickP', '072: LoBit Kick1P', '073: LoBit Kick2P', '074: Dance Kick P', '075: Hip Kick P',   '076: HipHop Kick',  '077: Mix Kick 1',
'078: Mix Kick 2',   '079: Wide Kick P',  '080: LD Kick P',    '081: SF Kick 1 P',  '082: SF Kick 2 P',  '083: TY Kick P',    '084: WD Kick P',
'085: Reg.Kick P',   '086: Rock Kick P',  '087: Jz Dry Kick',  '088: Jazz Kick P',  '089: 78 Snr',       '090: 606 Snr 1 P',  '091: 606 Snr 2 P',
'092: 808 Snr 1a P', '093: 808 Snr 1b P', '094: 808 Snr 1c P', '095: 808 Snr 2a P', '096: 808 Snr 2b P', '097: 808 Snr 2c P', '098: 808 Snr 3a P',
'099: 808 Snr 3b P', '100: 808 Snr 3c P', '101: 909 Snr 1a P', '102: 909 Snr 1b P', '103: 909 Snr 1c P', '104: 909 Snr 1d P', '105: 909 Snr 2a P',
'106: 909 Snr 2b P', '107: 909 Snr 2c P', '108: 909 Snr 2d P', '109: 909 Snr 3a P', '110: 909 Snr 3b P', '111: 909 Snr 3c P', '112: 909 Snr 3d P',
'113: 909 DstSnr1P', '114: 909 DstSnr2P', '115: 909 DstSnr3P', '116: 707 Snr 1a P', '117: 707 Snr 2a P', '118: 707 Snr 1b P', '119: 707 Snr 2b P',
'120: 626 Snr 1',    '121: 626 Snr 2',    '122: 626 Snr 3',    '123: 626 Snr 1a P', '124: 626 Snr 3a P', '125: 626 Snr 1b P', '126: 626 Snr 2 P',
'127: 626 Snr 3b P', '128: Analog Snr 1', '129: Analog Snr 2', '130: Analog Snr 3', '131: Synth Snr 1',  '132: Synth Snr 2',  '133: 106 Snr',
'134: Sim Snare',    '135: Jungle Snr 1', '136: Jungle Snr 2', '137: Jungle Snr 3', '138: Lite Snare',   '139: Lo-Bit Snr1P', '140: Lo-Bit Snr2P',
'141: HphpJazzSnrP', '142: PurePhatSnrP', '143: DRDisco SnrP', '144: Ragga Snr',    '145: Lo-Fi Snare',  '146: drums_data Snare',     '147: DanceHallSnr',
'148: Break Snr',    '149: Piccolo SnrP', '150: TM-2 Snr 1',   '151: TM-2 Snr 2',   '152: WoodSnr RS',   '153: LD Snr',       '154: SF Snr P',
'155: TY Snr',       '156: WD Snr P',     '157: Tight Snr',    '158: Reg.Snr1 P',   '159: Reg.Snr2 P',   '160: Ballad Snr P', '161: Rock Snr1 P',
'162: Rock Snr2 P',  '163: LD Rim',       '164: SF Rim',       '165: TY Rim',       '166: WD Rim P',     '167: Jazz Snr P',   '168: Jazz Rim P',
'169: Jz BrshSlapP', '170: Jz BrshSwshP', '171: Swish&Trn P',  '172: 78 Rimshot',   '173: 808 RimshotP', '174: 909 RimshotP', '175: 707 Rimshot',
'176: 626 Rimshot',  '177: Vint Stick P', '178: Lo-Bit Stk P', '179: Hard Stick P', '180: Wild Stick P', '181: LD Cstick',    '182: TY Cstick',
'183: WD Cstick',    '184: 606 H.Tom P',  '185: 808 H.Tom P',  '186: 909 H.Tom P',  '187: 707 H.Tom P',  '188: 626 H.Tom 1',  '189: 626 H.Tom 2',
'190: SimV Tom 1 P', '191: LD H.Tom P',   '192: SF H.Tom P',   '193: TY H.Tom P',   '194: 808 M.Tom P',  '195: 909 M.Tom P',  '196: 707 M.Tom P',
'197: 626 M.Tom 1',  '198: 626 M.Tom 2',  '199: SimV Tom 2 P', '200: LD M.Tom P',   '201: SF M.Tom P',   '202: TY M.Tom P',   '203: 606 L.Tom P',
'204: 808 L.Tom P',  '205: 909 L.Tom P',  '206: 707 L.Tom P',  '207: 626 L.Tom 1',  '208: 626 L.Tom 2',  '209: SimV Tom 3 P', '210: SimV Tom 4 P',
'211: LD L.Tom P',   '212: SF L.Tom P',   '213: TY L.Tom P',   '214: 78 CHH',       '215: 606 CHH',      '216: 808 CHH',      '217: 909 CHH 1',
'218: 909 CHH 2',    '219: 909 CHH 3',    '220: 909 CHH 4',    '221: 707 CHH',      '222: 626 CHH',      '223: HipHop CHH',   '224: Lite CHH',
'225: Reg.CHH',      '226: Rock CHH',     '227: S13 CHH Tip',  '228: S14 CHH Tip',  '229: 606 C&OHH',    '230: 808 C&OHH S',  '231: 808 C&OHH L',
'232: Hip PHH',      '233: Reg.PHH',      '234: Rock PHH',     '235: S13 PHH',      '236: S14 PHH',      '237: 606 OHH',      '238: 808 OHH S',
'239: 808 OHH L',    '240: 909 OHH 1',    '241: 909 OHH 2',    '242: 909 OHH 3',    '243: 707 OHH',      '244: 626 OHH',      '245: HipHop OHH',
'246: Lite OHH',     '247: Reg.OHH',      '248: Rock OHH',     '249: S13 OHH Shft', '250: S14 OHH Shft', '251: 78 Cymbal',    '252: 606 Cymbal',
'253: 808 Cymbal 1', '254: 808 Cymbal 2', '255: 808 Cymbal 3', '256: 909 CrashCym', '257: 909 Rev Cym',  '258: MG Nz Cym',    '259: 707 CrashCym',
'260: 626 CrashCym', '261: Crash Cym 1',  '262: Crash Cym 2',  '263: Rock Crash 1', '264: Rock Crash 2', '265: P17 CrashTip', '266: S18 CrashTip',
'267: Z18kCrashSft', '268: Jazz Crash',   '269: 909 RideCym',  '270: 707 RideCym',  '271: 626 RideCym',  '272: Ride Cymbal',  '273: 626 ChinaCym',
'274: China Cymbal', '275: Splash Cym',   '276: 626 Cup',      '277: Rock Rd Cup',  '278: 808 ClapS1 P', '279: 808 ClapS2 P', '280: 808 ClapL1 P',
'281: 808 ClapL2 P', '282: 909 Clap 1 P', '283: 909 Clap 2 P', '284: 909 Clap 3 P', '285: 909 DstClapP', '286: 707 Clap P',   '287: 626 Clap',
'288: R8 Clap',      '289: Cheap Clap',   '290: Old Clap P',   '291: Hip Clap',     '292: Dist Clap',    '293: Hand Clap',    '294: Club Clap',
'295: Real Clap',    '296: Funk Clap',    '297: Bright Clap',  '298: TM-2 Clap',    '299: Amb Clap',     '300: Disc Clap',    '301: Claptail',
'302: Gospel Clap',  '303: 78 Tamb',      '304: 707 Tamb P',   '305: 626 Tamb',     '306: TM-2 Tamb',    '307: Tamborine 1',  '308: Tamborine 2',
'309: Tamborine 3',  '310: 808 CowbellP', '311: 707 Cowbell',  '312: 626 Cowbell',  '313: Cowbell Mute', '314: 78 H.Bongo P', '315: 727 H.Bongo',
'316: Bongo Hi Mt',  '317: Bongo Hi Slp', '318: Bongo Hi Op',  '319: 78 L.Bongo P', '320: 727 L.Bongo',  '321: Bongo Lo Op',  '322: Bongo Lo Slp',
'323: 808 H.CongaP', '324: 727 H.CngOpP', '325: 727 H.CngMtP', '326: 626 H.CngaOp', '327: 626 H.CngaMt', '328: Conga Hi Mt',  '329: Conga 2H Mt',
'330: Conga Hi Slp', '331: Conga 2H Slp', '332: Conga Hi Op',  '333: Conga 2H Op',  '334: 808 M.CongaP', '335: 78 L.Conga P', '336: 808 L.CongaP',
'337: 727 L.CongaP', '338: 626 L.Conga',  '339: Conga Lo Mt',  '340: Conga Lo Slp', '341: Conga Lo Op',  '342: Conga 2L Mt',  '343: Conga 2L Op',
'344: Conga Slp Op', '345: Conga Efx',    '346: Conga Thumb',  '347: 727 H.Timbal', '348: 626 H.Timbal', '349: 727 L.Timbal', '350: 626 L.Timbal',
'351: Timbale 1',    '352: Timbale 2',    '353: Timbale 3',    '354: Timbale 4',    '355: Timbles LoOp', '356: Timbles LoMt', '357: TimbalesHand',
'358: Timbales Rim', '359: TmbSideStick', '360: 727 H.Agogo',  '361: 626 H.Agogo',  '362: 727 L.Agogo',  '363: 626 L.Agogo',  '364: 727 Cabasa P',
'365: Cabasa Up',    '366: Cabasa Down',  '367: Cabasa Cut',   '368: 78 Maracas P', '369: 808 MaracasP', '370: 727 MaracasP', '371: Maracas',
'372: 727 WhistleS', '373: 727 WhistleL', '374: Whistle',      '375: 78 Guiro S',   '376: 78 Guiro L',   '377: Guiro',        '378: Guiro Long',
'379: 78 Claves P',  '380: 808 Claves P', '381: 626 Claves',   '382: Claves',       '383: Wood Block',   '384: Triangle',     '385: 78 MetalBt P',
'386: 727 StrChime', '387: 626 Shaker',   '388: Shaker',       '389: Finger Snap',  '390: Club FinSnap', '391: Snap',         '392: Group Snap',
'393: Op Pandeiro',  '394: Mt Pandeiro',  '395: PandeiroOp',   '396: PandeiroMt',   '397: PandeiroHit',  '398: PandeiroRim',  '399: PandeiroCrsh',
'400: PandeiroRoll', '401: 727 Quijada',  '402: TablaBayam 1', '403: TablaBayam 2', '404: TablaBayam 3', '405: TablaBayam 4', '406: TablaBayam 5',
'407: TablaBayam 6', '408: TablaBayam 7', '409: Udo',          '410: Udu Pot Hi',   '411: Udu Pot Slp',  '412: Scratch 1',    '413: Scratch 2',
'414: Scratch 3',    '415: Scratch 4',    '416: Scratch 5',    '417: Dance M',      '418: Ahh M',        '419: Let\'s Go M',  '420: Hah F',
'421: Yeah F',       '422: C\'mon Baby F','423: Wooh F',       '424: White Noise',  '425: Pink Noise',   '426: Atmosphere',   '427: PercOrgan 1',
'428: PercOrgan 2',  '429: TB Blip',      '430: D.Mute Gtr',   '431: Flute Fx',     '432: Pop Brs Atk',  '433: Strings Hit',  '434: Smear Hit',
'435: O\'Skool Hit', '436: Orch. Hit',    '437: Punch Hit',    '438: Philly Hit',   '439: ClassicHseHt', '440: Tao Hit',      '441: MG S Zap 1',
'442: MG S Zap 2',   '443: MG S Zap 3',   '444: SH2 S Zap 1',  '445: SH2 S Zap 2',  '446: SH2 S Zap 3',  '447: SH2 S Zap 4',  '448: SH2 S Zap 5',
'449: SH2 U Zap 1',  '450: SH2 U Zap 2',  '451: SH2 U Zap 3',  '452: SH2 U Zap 4',  '453: SH2 U Zap 5']
