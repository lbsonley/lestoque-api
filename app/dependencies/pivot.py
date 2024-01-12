# https://stackoverflow.com/questions/64019553/how-pivothigh-and-pivotlow-function-work-on-tradingview-pinescript#answer-72490168


def checkhl(data_back, data_forward, hl):
    if hl == "high" or hl == "High":
        ref = data_back[len(data_back) - 1]
        for i in range(len(data_back) - 1):
            if ref < data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref <= data_forward[i]:
                return 0
        return 1
    if hl == "low" or hl == "Low":
        ref = data_back[len(data_back) - 1]
        for i in range(len(data_back) - 1):
            if ref > data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref >= data_forward[i]:
                return 0
        return 1


def pivot(osc, LBL, LBR, highlow):
    pivots = []
    left = []
    right = []
    for i in range(len(osc)):
        if i < LBL + 1:
            left.append(osc[i]["value"])
        if i > LBL:
            right.append(osc[i]["value"])
        if i > LBL + LBR:
            left.append(right[0])
            left.pop(0)
            right.pop(0)
            if checkhl(left, right, highlow):
                pivots.append({**osc[i - LBR], "type": highlow})
    return pivots
