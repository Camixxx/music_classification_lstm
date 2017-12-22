# 大小调设置
#def mapKey(key,note):
        # 'C':[],
        # 'G':['G'],
        # 'D':['F'],
        # 'A': [],
        # 'E': [],
        # 'Cb': [],
        # 'Gb': [],
        # 'Db': [],
        # 'Ab': [],
        # 'Eb': [],
        # 'Bb': [],
        # 'F': []


mapPitch={
    'C' :12,
    'C#':13,
    'D' :14,
    'D#':15,
    'E' :16,
    'F' :17,
    'F#':18,
    'G' :19,
    'G#':20,
    'A' :21,
    'A#':22,
    'B' :23,
    'B#':24
}
mapCode= dict(map(lambda t:(t[1],t[0]), mapPitch.items()))

def code2picth(code,octave):
    pitch = mapPitch[code]+octave*12
    return pitch

def picth2code(pitch):
    octave = str(int(pitch/12))
    code = mapCode[pitch%12 +12]
    return code,octave

def testPitch():
    print("code2picth A#0")
    print(code2picth('A#',0))
    print("code2picth A#")
    print(code2picth('A#', -1))
    print("code2picth(21)")
    print(picth2code(21))
    print("code2picth(9)")
    print(picth2code(9))

typeName = {
    "whole": 1.0,
    "half": 0.5,
    "quarter": 0.25,
    "eighth": 0.125,
    "sixteenth": 0.0625,
    "32nd": 1/32,
    "64nd": 1/64
}
noteType = {
    1: 1.0,
    2: 0.5,
    4: 0.25,
    8: 0.125,
    16: 0.0625,
    32: 1 / 32,
    64: 1 / 64
}
