import matplotlib.pyplot as plt
import re
import os

folder_path = os.path.dirname(__file__)

print("starting")
print(os.path.join(folder_path,"analysis.txt"))
with open(os.path.join(folder_path,"analysis.txt"), "r") as analysis_file:
    lines = analysis_file.readlines()

data = []


for line in lines:
    m0 = re.search(r"([0-9]*) w", line)
    data.append(int(m0.group(1)))
print("data",data)


count_data = []
for i in range(len(data)):
    count_data.extend([i]*int(data[i]))
print(count_data)  


plt.style.use('ggplot')
plt.hist(count_data, bins = 100)
plt.show()