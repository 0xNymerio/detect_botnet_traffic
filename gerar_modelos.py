import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

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

n_state = 74
# Load Data
df_c6 = pd.read_csv("./data/dataset_full/trafego/cenario_6__trafego.csv",low_memory=False)
df_c8 = pd.read_csv("./data/dataset_full/trafego/cenario_8__trafego.csv",low_memory=False)

df_c6 = df_c6.fillna(0)
df_c8 = df_c8.fillna(0)

# Separar uma proporção de labels 0 (background), labels 1 (background-botnet) e labels 2 (botnet)
df6_l0 = df_c6.loc[df_c6['Label'] == 0] # 513527 instancias
df6_l1 = df_c6.loc[df_c6['Label'] == 1] # 7433 instancias
df6_l2 = df_c6.loc[df_c6['Label'] == 2] # 230 instancias
df8_l2 = df_c8.loc[df_c8['Label'] == 2] # 397 instancias

# Pegar as 1k primeiras instancias do label 0, 1k do label 1 e todos do label 2 em ambos os cenários
df6_l0 = df6_l0[:25000]
# Concatenar os dataframes
frames = [df6_l0, df6_l1, df6_l2, df8_l2]
df_final = pd.concat(frames)

# separar X- features e y-labels
x_c6 = df_final.drop(['Label'],axis=1).values
y_c6 = df_final['Label'].values

# Separando data de treino e de validação
train_x_c6, test_x_c6, train_y_c6, test_y_c6 = train_test_split(x_c6, y_c6, test_size = 0.25, random_state = n_state)


scaling = MinMaxScaler(feature_range=(-1,1)).fit(train_x_c6)
train_x_c6 = scaling.transform(train_x_c6)
test_x_c6 = scaling.transform(test_x_c6)


def save_pickle(nome,clf):
    #pickle.dump(clf, open("./modelos_treinados/trafego_f_extra/"+ nome +"_f.pkl", 'wb'))
    pass

def plot_conf_matrix(nome_modelo,clf_plot):

    titles_options = [("Matrix de Confusão, sem Normalização - "+nome_modelo, None), ("Matrix de Confusão Normalizada - "+nome_modelo, 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(clf_plot, test_x_c6, test_y_c6,cmap=plt.cm.Blues, normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()

def plt_roc_biclass(dt,nb,rf,rlog,y_test):
    plt.figure(figsize=(12,7))


    preds_dt = dt[:,1]
    preds_nb = nb[:,1]
    preds_rf = rf[:,1]
    preds_rlog = rlog[:,1]

    fpr_dt, tpr_dt, threshold_dt = metrics.roc_curve(y_test, preds_dt)
    roc_auc_dt = metrics.auc(fpr_dt, tpr_dt)
    plt.plot(fpr_dt, tpr_dt,label="AUC - Decision Tree: = %0.2f" % roc_auc_dt, color='blue', linewidth=2)

    fpr_nb, tpr_nb, threshold_nb = metrics.roc_curve(y_test, preds_nb)
    roc_auc_nb = metrics.auc(fpr_nb, tpr_nb)
    plt.plot(fpr_nb, tpr_nb,label="AUC - Naive Bayes: = %0.2f" % roc_auc_nb, color='orange', linewidth=2)

    fpr_rf, tpr_rf, threshold_rf = metrics.roc_curve(y_test, preds_rf)
    roc_auc_rf = metrics.auc(fpr_rf, tpr_rf)
    plt.plot(fpr_rf, tpr_rf,label="AUC - Random Forest: = %0.2f" % roc_auc_rf, color='green', linewidth=2)

    fpr_rlog, tpr_rlog, threshold_rlog = metrics.roc_curve(y_test, preds_rlog)
    roc_auc_rlog = metrics.auc(fpr_rlog, tpr_rlog)
    plt.plot(fpr_rlog, tpr_rlog,label="AUC - Logistic Regression: = %0.2f" % roc_auc_rlog, color='purple', linewidth=2)


    plt.plot([0, 1], [0, 1], 'r--', lw=1)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.title('Receiver Operating Characteristic - Dataset 1')
    plt.xlabel('Taxa de Falso Positivo')
    plt.ylabel('Taxa de Verdadeiro Positivo')
    plt.grid(True)
    plt.legend(loc="lower right")
    plt.show()

# ###########################################
# Algoritmos ML
# ###########################################

def dt():
    clf_dt = DecisionTreeClassifier().fit(train_x_c6, train_y_c6)
    y_model_dt = clf_dt.predict(test_x_c6)
    save_pickle("dt",clf_dt)
    print("Decision Tree accuracy: ", accuracy_score(test_y_c6, y_model_dt))
    #print(cross_val_score(clf_dt, train_x_c6, train_y_c6))

    #plot_conf_matrix("Decision Tree",clf_dt)
    probs = clf_dt.predict_proba(test_x_c6)
    return probs

def nb():
    clf_nb = GaussianNB().fit(train_x_c6, train_y_c6)
    y_model_nb = clf_nb.predict(train_x_c6)

    save_pickle("nb",clf_nb)

    print("Naive Bayes accuracy : ",accuracy_score(train_y_c6, y_model_nb))
    #print(cross_val_score(clf_nb, train_x_c6, train_y_c6))

    #plot_conf_matrix("Naive Bayes",clf_nb)

    probs = clf_nb.predict_proba(test_x_c6)
    return probs

def random_forest():
    clf_rf = RandomForestClassifier(n_estimators=1000, random_state=1, criterion='entropy', bootstrap=True, oob_score=True, verbose=0, n_jobs=-1).fit(train_x_c6,train_y_c6)
    y_pred_R =clf_rf.predict(test_x_c6)

    save_pickle("rf",clf_rf)

    print("Random Forest Accuracy:", accuracy_score(test_y_c6, y_pred_R))
    #print(cross_val_score(clf_rf,train_x_c6, train_y_c6))

    #plot_conf_matrix("Random Forest",clf_rf)

    probs = clf_rf.predict_proba(test_x_c6)
    return probs

def rlog():
    clf_rlog = LogisticRegression(random_state=0, max_iter=2500).fit(train_x_c6, train_y_c6)
    y_pred_rlog = clf_rlog.predict(test_x_c6)

    save_pickle("rlog",clf_rlog)

    print("R Log Accuracy:", accuracy_score(test_y_c6, y_pred_rlog))
    #print(cross_val_score(clf_rlog,train_x_c6, train_y_c6))

    #plot_conf_matrix("Logistic Regression",clf_rlog)

    probs = clf_rlog.predict_proba(test_x_c6)
    return probs


# Main
prob_dt = dt()
prob_nb = nb()
prob_rf = random_forest()
prob_rlog = rlog()
plt_roc_biclass(prob_dt,prob_nb,prob_rf,prob_rlog,test_y_c6)
