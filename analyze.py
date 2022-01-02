import matplotlib.pyplot as plt
import re
import os

folder_path = os.path.dirname(__file__)


def histogram_analysis():
    print(os.path.join(folder_path, "analysis.txt"))
    with open(os.path.join(folder_path, "analysis.txt"), "r") as analysis_file:
        lines = analysis_file.readlines()

    data = []
    for line in lines:
        number_of_wins = re.search(r"([0-9]*) w", line)
        data.append(int(number_of_wins.group(1)))
    print("data", data)

    count_data = []
    for i in range(len(data)):
        count_data.extend([i]*int(data[i]))
    print(count_data)

    plt.style.use('ggplot')
    plt.hist(count_data, bins=100)
    plt.show()


def run_multiple_times():
    let_analysis_file_path = os.path.join(folder_path, "let_analysis.txt")
    with open(let_analysis_file_path, "w") as analysis_file:
        analysis_file.write("")
    for i in range(1000):
        print(i)
        os.system(f"python {os.path.join(folder_path, 'picomino.py')}")

    with open(let_analysis_file_path, "r") as analysis_file:
        lines = analysis_file.readlines()
    data = []
    for line in lines:
        data.append(line.strip())
    print("data", data)
    count_dict = {}
    for d in data:
        if d in count_dict:
            count_dict[d] += 1
        else:
            count_dict[d] = 1
    print(count_dict)
    plt.style.use('ggplot')
    plt.hist(data)
    plt.show()


histogram_analysis()
