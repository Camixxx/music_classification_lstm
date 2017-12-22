import pretty_midi
import filestream
import numpy as np
import music21
"""
打开xml文件后，处理音符数据，转化为数组和字典
part：声部
measure：小节，每个小节有若干个音符note
note：音符
 -pitch 音高{step，octave}可以是一个1~84的数据，0代表休止符
    octave：八度音阶
    step:
key：规定升降号，大调小调 key{fifths:升降号数目,mode:major }
clef：clef{sign:(G),line(2)}规定了一条谱子高音谱号或是低音谱号在第几条线上,如果有两个clef则说明有两条谱子
division，duration： duration/division = type的值,duration是1，也就是全音符的秒数
type：whole是全音符1，half是二分音符1/2
time：time{beats，beat-type} 以1/beat-type为一拍，一个小节有beats个拍子
"""

def read_xml(name):
    # music21读取xml方法
    # stream = filestream.getStream(name)

    # 自行读取XML
    music = filestream.getXmlMusic(name)
    print(music)
    return music

def read_midi(name,tempo = 120):
    midi = pretty_midi.PrettyMIDI('data/'+ name)
    # 默认只有一个乐器进行演出
    notes = midi.instruments[0].notes
    timeSignature = midi.time_signature_changes[0]
    # 每一拍的时间 * 一个小节中的拍子数
    measureTime = (60/tempo) * timeSignature.numerator

    # 把时间转换为小节数
    for each in notes:
        if each.start >= measureTime:
            each.start = each.start % measureTime
            each.start = each.start / (60 / tempo) # 有多少拍
        else:
            each.start = each.start / (60 / tempo)  # 有多少拍

        if each.end > measureTime:
            each.end = each.end % measureTime
            each.end = each.end + 0.002
            each.end = round(each.end / (60 / tempo),2)
        else:
            each.end = each.end + 0.002
            each.end = round(each.end / (60 / tempo),2)

    return notes

def note2np(notes,pathname):
    resultP = []
    resultS = []
    resultE = []
    pitch = [notes[0].pitch]
    start = [notes[0].start]
    end = [notes[0].end]
    for n in range(1,len(notes)):
        note = notes[n]
        if note.start == 0:
            resultP.append(pitch)
            resultS.append(start)
            resultE.append(end)
            pitch=[notes[0].pitch]
            start=[notes[0].start]
            end=[notes[0].end]
        else:
            pitch.extend([note.pitch])
            start.extend([note.start])
            end.extend([note.end])

    pitchMeasure = np.array(resultP)
    startMeasure = np.array(resultS)
    endMeasure = np.array(resultE)

    return pitchMeasure,startMeasure,endMeasure
    # np.save("npdata/pitch.npy", pitchMeasure)
    # np.save("npdata/start.npy", startMeasure)
    # np.save("npdata/end.npy",endMeasure)

def note2sentences(notes):
    word = str(notes[0].pitch) + 's' + str(notes[0].start) + 'e' + str(notes[0].end)
    sentence = [word]
    result=[]
    for n in range(1,len(notes)):
        note = notes[n]
        w = str(note.pitch) + 's' + str(note.start) + 'e' + str(note.end)
        if note.start == 0:
            result.append(sentence)
            sentence=[w]
        else:
            sentence.append(w)
    return result

def test():
    #notes = read_midi('601598.mid')
    #sentence = note2sentences(notes)
    music_xml = music21.converter.parse('data/Nostalgia.xml');
    #music_xml.chordify()
    #music_xml.measures(0,10).write("romantext","test.txt");
    #music_xml.measures(0,10).show()
    flat = music_xml.measure(1)[0]._offsetDict
    for ele in flat:
        #if type(flat[ele][1])=='music21.note.Note':
            print(type(flat[ele][1]))
            print(flat[ele][1])


    return

test()