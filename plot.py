import matplotlib.pyplot as plt
import schemdraw as schem
import schemdraw.elements as elm
import numpy as np

def split_text(text):
    text = text.replace('R', '')
    list_text = []
    count_x = 0
    count_y = 0
    temp = ''
    for i in range(len(text)):
        if text[i] == '[':
            count_x += 1
        if text[i] == ']':
            count_y += 1
        temp += text[i]
        if count_x == count_y:
            temp = temp.replace('[', '')
            temp = temp.replace(']', '')
            list_text.append(temp)
            temp = ''
    return list_text

def split_val(value):
    value = value.split(';')
    for i in range(len(value)):
        value[i] = value[i].strip('R').split('=')
    take_val = dict()
    for res, val in value:
        take_val[res] = float(val)
    return take_val

def draw(dacta):
    list_text = split_text(dacta)
    res = dict()
    count_ss = 0
    count_nt = 0
    end = ''
    start = ''
    d = schem.Drawing()
    d.add(elm.Dot)
    d0 = d.add(elm.LINE, d='down', l=2)
    d1 = d.add(elm.LINE, d='down', l=2)
    d.add(elm.Dot)
    d.add(elm.Line, d = 'right', l=2)
    for idx in list_text:
        if '*' not in idx and idx != '+':
            temp = idx.split('+')
            if count_nt == 0:
                for i in temp:
                    res[i] = d.add(elm.ResistorIEC, d='right', label='R{}'.format(i))
                    end = i
                count_nt += 1
            else:
                for i in range(len(temp)):
                    if i == 0:
                        res[temp[i]] = d.add(elm.ResistorIEC, d='right', xy = res[end].end, label='R{}'.format(temp[i]))
                        end = temp[i]
                    else:
                        res[temp[i]] = d.add(elm.ResistorIEC, d='right', label='R{}'.format(temp[i]))
                        end = temp[i]
            d.add(elm.Dot)
        if '*' in idx and idx != '+':
            temp = idx.split('*')
            length_idx_temp = []
            list_temp = []
            for i in temp:
                temp_ = i.split('+')
                list_temp.append(temp_)
                length_idx_temp.append(len(temp_))
            length_idx_temp = sorted(length_idx_temp, reverse=True)
            if count_ss != 0:
                d.add(elm.Line, d='right', xy = res[end].end, l=2)
                d.add(elm.Dot)
            for i in range(len(length_idx_temp)):
                    if i == 0:
                        d2 = d.add(elm.LINE, d='up', l=2)
                        for j in range(len(list_temp)):
                            if len(list_temp[j]) == length_idx_temp[i]:
                                for z in list_temp[j]:
                                    res[z] = d.add(elm.ResistorIEC, d='right',label='R{}'.format(z))
                                    end = z
                                list_temp = np.delete(list_temp, j)
                                break
                    elif i == 1:
                        for j in range(len(list_temp)):
                            if len(list_temp[j]) == length_idx_temp[i]:
                                for z in range(len(list_temp[j])):
                                    if z == 0:
                                        if length_idx_temp[i] == 1:
                                            res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', xy=d2.start, tox = res[end].end, label='R{}'.format(list_temp[j][z]))
                                            end = list_temp[j][z]
                                        else:
                                            res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', xy=d2.start, label='R{}'.format(list_temp[j][z]))
                                        start = list_temp[j][z]
                                    elif z == len(list_temp[j]) - 1:
                                        res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', tox = res[end].end, label='R{}'.format(list_temp[j][z]))
                                        end = list_temp[j][z]
                                    else:
                                        res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', label='R{}'.format(list_temp[j][z]))
                                list_temp = np.delete(list_temp, j)
                                break
                    else:
                        d.add(elm.LINE, d='down', xy = res[start].start, l=2)
                        for j in range(len(list_temp)):
                            if len(list_temp[j]) == length_idx_temp[i]:
                                for z in range(len(list_temp[j])):
                                    if z == 0:
                                        if length_idx_temp[i] == 1:
                                            res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', tox = res[end].end, label='R{}'.format(list_temp[j][z]))
                                        else:
                                            res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', label='R{}'.format(list_temp[j][z]))
                                        start = list_temp[j][z]
                                    elif z == len(list_temp[j]) - 1:
                                        res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', tox = res[end].end, label='R{}'.format(list_temp[j][z]))
                                    else:
                                        res[list_temp[j][z]] = d.add(elm.ResistorIEC, d='right', label='R{}'.format(list_temp[j][z]))
                                list_temp = np.delete(list_temp, j)
                                break
            for i in range(len(length_idx_temp) - 1):
                    d.add(elm.Line, d = 'up', l = 2)
            count_ss += 1
            d.add(elm.Dot, xy=res[end].end)

    d.add(elm.Line, d = 'right', xy = res[end].end, l = 2)
    d.add(elm.Dot)
    d.add(elm.LINE, d='up', l=2)
    d3 = d.add(elm.LINE, d='up', l=2)
    d.add(elm.Dot)
    vt = d.add(elm.BatteryCell, d='right', xy=d0.start, tox=d3.end, lblofst=0.3, label='E,r')
    d.save('picture.png')
    #d.draw()

def compute_res(dacta, value):
    lst_txt = split_text(dacta)
    lst_val = split_val(value)
    temp_val = []
    for idx in lst_txt:
        if '*' not in idx and idx != '+':
            temp = idx.split('+')
            val = 0
            for i in temp:
                val += lst_val[i]
            temp_val.append(val)
        if '*' in idx and idx != '+':
            temp_val_ss = []
            temp = idx.split('*')
            for i in temp:
                if '+' not in i:
                    temp_val_ss.append(1 / lst_val[i])
                else:
                    temp_i = i.split('+')
                    val = 0
                    for i in temp_i:
                        val += lst_val[i]
                    temp_val_ss.append(1 / val)
                b = sum(temp_val_ss)
            temp_val.append(1 / sum(temp_val_ss))
    return sum(temp_val)

def main(dacta, value):
    draw(dacta)
    return compute_res(dacta, value)