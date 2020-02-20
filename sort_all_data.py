import os 
import shutil


direct = os.listdir('./')
# path = '/Users/macuser/Documents/PYTHON:java/testing'
# print(os.listdir(path))
# print(direct)
a_dest = '/Users/macuser/Documents/PYTHON:java/testing/A_data'
b_dest = '/Users/macuser/Documents/PYTHON:java/testing/B_data'
c_dest = '/Users/macuser/Documents/PYTHON:java/testing/C_data'
for i in direct:
    # print(i)
    if i.startswith('A') & i.endswith('v'):
        # print(i)
        shutil.move(i, a_dest)
    if i.startswith('B') & i.endswith('v'):
        # print(i)
        shutil.move(i, b_dest)
    if i.startswith('C') & i.endswith('v'):
        # print(i)
        shutil.move(i, c_dest)