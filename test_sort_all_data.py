import os 

direct = os.listdir('./')

# print(direct)
for i in direct:
    # print(i)
    if i.startswith('A') & i.endswith('v'):
        print(i)
    if i.startswith('B') & i.endswith('v'):
        print(i)
    if i.startswith('C') & i.endswith('v'):
        print(i)