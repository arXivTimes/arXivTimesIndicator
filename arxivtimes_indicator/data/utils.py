import numpy as np
import requests


def download(url, file_name):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024):
                file.write(chunk)


def break_line(names):
    table = {
        'AudioRecognition': 'Audio\nRecognition',
        'AudioSynthesis': 'Audio\nSynthesis',
        'ComputerVision': 'Computer\nVision',
        'DataRepresentation': 'Data\nRepresentation',
        'ReinforcementLearning': 'Reinforcement\nLearning'
    }
    names = [table[name] if name in table else name for name in names]
    return names


def std_score(a):
    return np.round_(50 + 10 * (a - np.average(a)) / np.std(a))
