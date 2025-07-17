# if, elif, else, for, break, continue をすべて使う例
for i in range(10):
    if i == 0:
        print("start")
    elif i == 5:
        print("break!")
        break
    elif i % 2 == 0:
        continue
    else:
        print(i)
