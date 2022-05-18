import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_text(file):
    f = open(file, "r")
    
    headers = f.readline()
    data = f.read()
    
    f.close()
    
    headers = headers.split()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split()
    
    df = pd.DataFrame(data, columns=headers)
    
    return df