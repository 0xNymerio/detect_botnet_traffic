
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pickle import load

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics

# Setar que as saidas só possuam duas casas decimais
float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})
np.set_printoptions(precision=2)

def pred(inx):
    dt_y = clf_dt.predict(inx)
    nb_y = clf_nb.predict(inx)
    rf_y = clf_rf.predict(inx)
    rlog_y = clf_rlog.predict(inx)

    print('\nDT: ', dt_y)
    print(np.unique(dt_y))

    print('\nNB: ', nb_y)
    print(np.unique(nb_y))

    print('\nRF: ', rf_y)
    print(np.unique(rf_y))

    print('\nRLOG: ', rlog_y)
    print(np.unique(rlog_y))

nc = pd.read_csv("./data/dataset_port_scanning/nc_p22.csv",low_memory=False).values
nmap_sV = pd.read_csv("./data/dataset_port_scanning/nmap_sV.csv",low_memory=False).values
nmap_T5 = pd.read_csv("./data/dataset_port_scanning/nmap_T5.csv",low_memory=False).values


clf_dt =  load(open('./modelos_treinados/ataque/dt.pkl', 'rb')) # 3 labels
clf_nb =  load(open('./modelos_treinados/ataque/nb.pkl', 'rb')) # 3 labels
clf_rf =  load(open('./modelos_treinados/ataque/rf.pkl', 'rb')) # 3 labels
clf_rlog =  load(open('./modelos_treinados/ataque/rlog.pkl', 'rb')) # 3 labels

print("\nnc",pred(nc))
print("\nnmap sV",pred(nmap_sV))
print("\nnmap T5",pred(nmap_T5))
