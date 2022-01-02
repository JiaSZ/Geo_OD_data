    m = 0
    for feature in data:
        m += 1
        print (feature.GetField("START_H"))
        if m == 10:
            break