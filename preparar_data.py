import pandas as pd
import numpy as np

# Dataset - https://www.stratosphereips.org/datasets-ctu13

#Carregando os datasets --- usar o delim_whitespace=True para os pcaps convertidos

df_s6 = pd.read_csv("./data/pcaps_ataque/nmap_sV.flow",delim_whitespace=True,low_memory=False)
df_s6 = df_s6.fillna(0)
#df_s6 = pd.read_csv("./data/scenario_6_capture20110817.bitnetflow", header=0)
#df_s8 = pd.read_csv("./data/scenario_8_capture20110816-3.binetflow", header=0)


# Drop features
#df_s6 = df_s6.drop(['StartTime', 'SrcAddr', 'Sport', 'DstAddr', 'Dport'], axis=1)
#df_s8 = df_s8.drop(['StartTime', 'SrcAddr', 'Sport', 'DstAddr', 'Dport'], axis=1)

# Fill all NaN with -1.
df_s6['dTos'] = df_s6['dTos'].fillna(-1)
df_s6['sTos'] = df_s6['sTos'].fillna(-1)
df_s6['State'] = df_s6['State'].fillna(-1)

# df_s8['dTos'] = df_s8['dTos'].fillna(-1)
# df_s8['sTos'] = df_s8['sTos'].fillna(-1)
# df_s8['State'] = df_s8['State'].fillna(-1)

# Criando novas features
df_s6['TotBytes_over_TotPkts'] = df_s6['TotBytes'] / df_s6['TotPkts']
df_s6['SrcBytes_over_TotPkts'] = df_s6['SrcBytes'] / df_s6['TotPkts']
df_s6['TotPkts_over_Dur'] =  df_s6['TotPkts'] / df_s6['Dur']
df_s6['TotBytes_over_Dur'] =  df_s6['TotBytes'] / df_s6['Dur']
df_s6['SrcBytes_over_Dur'] =  df_s6['SrcBytes'] / df_s6['Dur']

# df_s8['TotBytes_over_TotPkts'] = df_s8['TotBytes'] / df_s8['TotPkts']
# df_s8['SrcBytes_over_TotPkts'] = df_s8['SrcBytes'] / df_s8['TotPkts']
# df_s8['TotPkts_over_Dur'] = df_s8['TotPkts'] / df_s8['Dur']
# df_s8['TotBytes_over_Dur'] =  df_s8['TotBytes'] / df_s8['Dur']
# df_s8['SrcBytes_over_Dur'] =  df_s8['SrcBytes'] / df_s8['Dur']

# Existem Quatro grupos de dataset explorados:
        # Grupo 1 - Datasset possui 2 labels (Tráfego Normal e Tráfego Botnet)
        # Grupo 2 - Datasset possui 2 labels (Tráfego Normal e Tráfego Botnet) + features extras
        # Grupo 3 - Datasset possui 3 labels (Tráfego Normal e Tráfego Botnet e Tráfego background Botnet)
        # Grupo 3 - Datasset possui 3 labels (Tráfego Normal e Tráfego Botnet e Tráfego background Botnet) + features extras

# Denominar as tuples para facilitar a hora da criação dos datasets.


# Apenas os labels 'from-bonet' é o nosso label alvo do atacante.
# Então vamos transformar todos os que possuem "from-botnet" em um unico label alvo.

# ###########################################################
# Alterar os valores de Proto, State, Dir e Label para valores inteiros
# ###########################################################

# 2 Labels --- Label 0 (Tráfego Normal) e Label 1 (Tráfego Botnet)
dict_s6_2_labels = {"flow=From-Normal-V47-Jist": 1, "flow=From-Normal-V47-UDP-CVUT-DNS-Server": 1,"flow=From-Normal-V47-Grill": 1, "flow=From-Normal-V47-Stribrek": 1,"flow=From-Normal-V47-MatLab-Server": 1,"flow=From-Normal-V47-CVUT-WebServer": 1,"flow=Normal-V47-HTTP-windowsupdate": 1, "flow=From-Botnet-V47-UDP-DNS": 1,"flow=From-Botnet-V47-TCP-Established-HTTP-Ad-4": 1,"flow=From-Botnet-V47-TCP-CC73-Not-Encrypted": 1,"flow=From-Botnet-V47-TCP-Attempt-SPAM": 1,"flow=From-Botnet-V47-TCP-Established-HTTP-Ad-62": 1,"flow=From-Botnet-V47-TCP-Attempt": 1,"flow=From-Botnet-V47-UDP-Attempt": 1}

dict_s8_2_labels = {"flow=From-Normal-V49-Stribrek": 1,"flow=From-Normal-V49-Grill": 1,"flow=From-Normal-V49-Jist": 1,"flow=From-Normal-V49-CVUT-WebServer": 1, "flow=From-Botnet-V49-UDP-DNS": 1,"low=From-Botnet-V49-TCP-Established-HTTP-Ad-40": 1,"flow=From-Botnet-V49-TCP-HTTP-Google-Net-Established-6": 1,"flow=From-Botnet-V49-UDP-Attempt": 1,"flow=From-Botnet-V49-TCP-Attempt": 1,"flow=From-Botnet-V49-TCP-WEB-Established": 1,"flow=From-Botnet-V49-UDP-Established": 1,"flow=From-Botnet-V49-TCP-Established": 1,"flow=From-Botnet-V49-TCP-CC76-HTTP-Custom-Port-Not-Encrypted-Binary-Download": 1,"flow=From-Botnet-V49-TCP-CC74-HTTP-Custom-Port-Not-Encrypted": 1,"flow=From-Botnet-V49-TCP-CC75-HTTP-Custom-Port-Not-Encrypted-Non-Periodic": 1,"flow=From-Botnet-V49-TCP-Established-HTTP-Binary-Download-11": 1,"flow=From-Botnet-V49-TCP-Established-HTTP-Ad-62": 1,"flow=From-Botnet-V49-UDP-Established-Custom-Encryption-2": 1,"flow=From-Botnet-V49-UDP-Established-Custom-Encryption-1": 1}

# 3 lalbels --- Label 0 (Tráfego Normal) e Label 1 (Tráfego Background Botnet) e Label 2 (Tráfego Botnet)
dict_s6_3_labels = {"flow=From-Normal-V47-Jist": 1, "flow=From-Normal-V47-UDP-CVUT-DNS-Server": 1,"flow=From-Normal-V47-Grill": 1, "flow=From-Normal-V47-Stribrek": 1,"flow=From-Normal-V47-MatLab-Server": 1,"flow=From-Normal-V47-CVUT-WebServer": 1,"flow=Normal-V47-HTTP-windowsupdate": 1,"flow=From-Botnet-V47-UDP-DNS": 2,"flow=From-Botnet-V47-TCP-Established-HTTP-Ad-4": 2,"flow=From-Botnet-V47-TCP-CC73-Not-Encrypted": 2,"flow=From-Botnet-V47-TCP-Attempt-SPAM": 2,"flow=From-Botnet-V47-TCP-Established-HTTP-Ad-62": 2,"flow=From-Botnet-V47-TCP-Attempt": 2,"flow=From-Botnet-V47-UDP-Attempt": 2}

dict_s8_3_labels ={"flow=From-Normal-V49-Stribrek": 1,"flow=From-Normal-V49-Grill": 1,"flow=From-Normal-V49-Jist": 1,"flow=From-Normal-V49-CVUT-WebServer": 1, "flow=From-Botnet-V49-UDP-DNS": 2,"low=From-Botnet-V49-TCP-Established-HTTP-Ad-40": 2,"flow=From-Botnet-V49-TCP-HTTP-Google-Net-Established-6": 2,"flow=From-Botnet-V49-UDP-Attempt": 2,"flow=From-Botnet-V49-TCP-Attempt": 2,"flow=From-Botnet-V49-TCP-WEB-Established": 2,"flow=From-Botnet-V49-UDP-Established": 2,"flow=From-Botnet-V49-TCP-Established": 2,"flow=From-Botnet-V49-TCP-CC76-HTTP-Custom-Port-Not-Encrypted-Binary-Download": 2,"flow=From-Botnet-V49-TCP-CC74-HTTP-Custom-Port-Not-Encrypted": 2,"flow=From-Botnet-V49-TCP-CC75-HTTP-Custom-Port-Not-Encrypted-Non-Periodic": 2,"flow=From-Botnet-V49-TCP-Established-HTTP-Binary-Download-11": 2,"flow=From-Botnet-V49-TCP-Established-HTTP-Ad-62": 2,"flow=From-Botnet-V49-UDP-Established-Custom-Encryption-2": 2,"flow=From-Botnet-V49-UDP-Established-Custom-Encryption-1": 2}

# Associando numeros integer a cada protocolo
dict_proto = {'tcp': 0, 'udp': 1, 'ipx/spx': 2, 'arp': 3, 'icmp': 4, 'pim': 5, 'rtcp': 6, 'igmp' : 7, 'ipv6-icmp': 8, 'esp': 9, 'ipv6': 10, 'udt': 11,'rtp':12, 'rarp':13, 'rsvp':14, 'unas':15}

# Associando numeros integer a cada direção
dict_dir = {'  <?>':0,'<?>':0, '  <->':1,'<->':1, '   ?>':2,'?>':2, '   ->':3,'->':3, '  who':4,'who':4, '  <-':5, '<-':5,'  <?':6,'<?':6}

# Associando numeros integer a cada state
dict_state = {'': 1, 'FSR_SA': 30, '_FSA': 296, 'FSRPA_FSA': 77, 'SPA_SA': 31, 'FSA_SRA': 1181, 'FPA_R': 46, 'SPAC_SPA': 37, 'FPAC_FPA': 2, '_R': 1, 'FPA_FPA': 784, 'FPA_FA': 66, '_FSRPA': 1, 'URFIL': 431, 'FRPA_PA': 5, '_RA': 2, 'SA_A': 2, 'SA_RA': 125, 'FA_FPA': 17, 'FA_RA': 14, 'PA_FPA': 48, 'URHPRO': 380, 'FSRPA_SRA': 8, 'R_':541, 'DCE': 5, 'SA_R': 1674, 'SA_': 4295, 'RPA_FSPA': 4, 'FA_A': 17, 'FSPA_FSPAC': 7, 'RA_': 2230, 'FSRPA_SA': 255, 'NNS': 47, 'SRPA_FSPAC': 1, 'RPA_FPA': 42, 'FRA_R': 10, 'FSPAC_FSPA': 86, 'RPA_R': 3, '_FPA': 5, 'SREC_SA': 1, 'URN': 339, 'URO': 6, 'URH': 3593, 'MRQ': 4, 'SR_FSA': 1, 'SPA_SRPAC': 1, 'URP': 23598, 'RPA_A': 1, 'FRA_': 351, 'FSPA_SRA': 91, 'FSA_FSA': 26138, 'PA_': 149, 'FSRA_FSPA': 798, 'FSPAC_FSA': 11, 'SRPA_SRPA': 176, 'SA_SA': 33, 'FSPAC_SPA': 1, 'SRA_RA': 78, 'RPAC_PA': 1, 'FRPA_R': 1, 'SPA_SPA': 2989, 'PA_RA': 3, 'SPA_SRPA': 4185, 'RA_FA': 8, 'FSPAC_SRPA': 1, 'SPA_FSA': 1, 'FPA_FSRPA': 3, 'SRPA_FSA': 379, 'FPA_FRA': 7, 'S_SRA': 81, 'FSA_SA': 6, 'State': 1, 'SRA_SRA': 38, 'S_FA': 2, 'FSRPAC_SPA': 7, 'SRPA_FSPA': 35460, 'FPA_A': 1, 'FSA_FPA': 3, 'FRPA_RA': 1, 'FSAU_SA': 1, 'FSPA_FSRPA': 10560, 'SA_FSA': 358, 'FA_FRA': 8, 'FSRPA_SPA': 2807, 'FSRPA_FSRA': 32, 'FRA_FPA': 6, 'FSRA_FSRA': 3, 'SPAC_FSRPA': 1, 'FS_': 40, 'FSPA_FSRA': 798, 'FSAU_FSA': 13, 'A_R': 36, 'FSRPAE_FSPA': 1, 'SA_FSRA': 4, 'PA_PAC': 3, 'FSA_FSRA': 279, 'A_A': 68, 'REQ': 892, 'FA_R': 124, 'FSRPA_SRPA': 97, 'FSPAC_FSRA':20, 'FRPA_RPA': 7, 'FSRA_SPA': 8, 'INT': 85813, 'FRPA_FRPA': 6, 'SRPAC_FSPA': 4, 'SPA_SRA': 808, 'SA_SRPA': 1, 'SPA_FSPA': 2118, 'FSRAU_FSA': 2, 'RPA_PA': 171,'_SPA': 268, 'A_PA': 47, 'SPA_FSRA': 416, 'FSPA_FSRPAC': 2, 'PAC_PA': 5, 'SRPA_SPA': 9646, 'SRPA_FSRA': 13, 'FPA_FRPA': 49, 'SRA_SPA': 10, 'SA_SRA': 838, 'PA_PA': 5979, 'FPA_RPA': 27, 'SR_RA': 10, 'RED': 4579, 'CON': 2190507, 'FSRPA_FSPA':13547, 'FSPA_FPA': 4, 'FAU_R': 2, 'ECO': 2877, 'FRPA_FPA': 72, 'FSAU_SRA': 1, 'FRA_FA': 8, 'FSPA_FSPA': 216341, 'SEC_RA': 19, 'ECR': 3316, 'SPAC_FSPA': 12, 'SR_A': 34, 'SEC_': 5, 'FSAU_FSRA': 3, 'FSRA_FSRPA': 11, 'SRC': 13, 'A_RPA': 1, 'FRA_PA': 3, 'A_RPE': 1, 'RPA_FRPA': 20, '_SRA': 74, 'SRA_FSPA': 293, 'FPA_': 118, 'FSRPAC_FSRPA': 2, '_FA': 1, 'DNP': 1, 'FSRPA_FSRPA': 379, 'FSRA_SRA': 14, '_FRPA': 1, 'SR_': 59, 'FSPA_SPA': 517, 'FRPA_FSPA': 1, 'PA_A': 159, 'PA_SRA': 1, 'FPA_RA': 5, 'S_': 68710, 'SA_FSRPA': 4, 'FSA_FSRPA': 1, 'SA_SPA': 4, 'RA_A': 5, '_SRPA': 9, 'S_FRA': 156, 'FA_FRPA': 1, 'PA_R': 72, 'FSRPAEC_FSPA': 1, '_PA': 7, 'RA_S': 1, 'SA_FR': 2, 'RA_FPA': 6, 'RPA_': 5, '_FSPA': 2395, 'FSA_FSPA': 230, 'UNK': 2, 'A_RA': 9, 'FRPA_': 6, 'URF': 10, 'FS_SA': 97, 'SPAC_SRPA': 8, 'S_RPA': 32, 'SRPA_SRA': 69, 'SA_RPA': 30, 'PA_FRA': 4, 'FSRA_SA': 49, 'FSRA_FSA': 206, 'PAC_RPA': 1, 'SRA_': 18, 'FA_': 451, 'S_SA': 6917, 'FSPA_SRPA': 427, 'TXD': 542,'SRA_SA': 1514, 'FSPA_FA': 1, 'FPA_FSPA': 10, 'RA_PA': 3, 'SRA_FSA': 709, 'SRPA_SPAC': 3, 'FSPAC_FSRPA': 10, 'A_': 191, 'URNPRO': 2, 'PA_RPA': 81, 'FSPAC_SRA':1, 'SRPA_FSRPA': 3054, 'SPA_': 1, 'FA_FA': 259, 'FSPA_SA': 75, 'SR_SRA': 1, 'FSA_': 2, 'SRPA_SA': 406, 'SR_SA': 3119, 'FRPA_FA': 1, 'PA_FRPA': 13, 'S_R': 34, 'FSPAEC_FSPAE': 3, 'S_RA': 61105, 'FSPA_FSA': 5326, '_SA': 20, 'SA_FSPA': 15, 'SRPAC_SPA': 8, 'FPA_PA': 19, 'FSRPAE_FSA': 1, 'S_A': 1, 'RPA_RPA': 3, 'NRS': 6, 'RSP': 115, 'SPA_FSRPA': 1144, 'FSRPAC_FSPA': 139,'FRPA_FRA':99901,'FRPA_A':99902,'FRA_A':99903,'SRA_FPA':99904,'FSRA_FA':99905,'FRA_RA':99906,'FA_FSA':99907,'IRQ':99908,'PA_SA':99909,'SRPA_FPA':99910,'A_FA':99911,'SA_FA':99912,'FSA_FA':99913,'SRA_FSRA':99914,'FSRAEC_SPA':99915,'FSPAEC_FSPA':99916,'FSRAC_SPA':99917,'PA_FSPA':99918,'_RPA':99919,'SRAEC_FSA':99920,'S_SPA':99921,'FRPA_FPAC':99922,'SRPA_PA':99923,'FSRPA_FSPAC':99924,'FA_FSPA':99925,'SRA_FA':99926,'FSRPA_FPA':99927,'FSPA_A':99928,'S_FSPA':99929,'RPA_FSA':99930,'FSPA_FRPA':99931,'RPA_SPA':99932,'SEC_SA':99933,'RPA_FSRPA':99934,'RA_R':99935,'R_FA':99936,'SRC_SA':99937,'SRA_R':99938,'FRPA_SPA':99939,'RA_RPA':99940,'SPA_PA':99941,'FSA_A':99942,'SPA_FA':99943,'SRAE_RA':99944,'FPA_FRPAC':99945,'PA_FA':99946,'A_FRA':99947,'FA_PA':99948,'FRPAC_FPA':99949, 'RPA_RA':99950,'FPAC_FRPA' :99951,'R_PA':99952,'A_FPA' :99953,'R_FPA' :99954,'SRE_SA':99955,'SRPAC_SRPA':99956,'SPAEC_SPA' :99957,'FRPAC_PA':99958,'F_':99959,'A_FSPE':99960,'FSAEC_FSPAE':99961,'SRPAEC_FSPA':99962,'SREC_':99963,'SPA_R':99964,'NaN':99965,'_':99966}

# Cenario 6 e 8 - Setando os labels e preenchendo o restante com zero
# df_s6['Label'].replace(dict_s6_3_labels, inplace=True)
# df_s6['Label'] = df_s6['Label'].replace(regex='([a-zA-Z])', value=0)

# df_s8['Label'].replace(dict_s8_3_labels, inplace=True)
# df_s8['Label'] = df_s8['Label'].replace(regex='([a-zA-Z])', value=0)

# Cenario 6
df_s6["Proto"].replace(dict_proto, inplace=True)
df_s6["State"].replace(dict_state, inplace=True)

# Cenario 8
# df_s8["Proto"].replace(dict_proto, inplace=True)
# df_s8["State"].replace(dict_state, inplace=True)

# Cenario 6
df_s6["Dir"].replace(dict_dir, inplace=True)
# Cenario 8
# df_s8["Dir"].replace(dict_dir, inplace=True)

# Drop Inf e NaN ---> df.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
df_s6 = df_s6.replace([np.inf, -np.inf], 0)
# df_s8 = df_s8.replace([np.inf, -np.inf], 0)
df_s6 = df_s6.fillna(0)
# Salvar em CSV
df_s6.to_csv("./data/dataset_port_scanning/nmap_sV_features.csv", index = False)
# df_s8.to_csv("./data/ataques/cenario_8__ataque_features_extra.csv", index = False)

# print(df_s8['Label'].unique())
# print(df_s6['Label'].value_counts())
