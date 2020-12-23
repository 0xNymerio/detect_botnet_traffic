# FATEC Americana - Monografia 2020 - Aprendizado de Máquina na Detecção de Tráfego de Botnet


Neste repositório consta a aplicação final elaborada na Monografia "Aprendizado de Máquina na Detecção de Tráfego de Botnet" pela FATEC Americana. O documento da monografia está neste repositório, que pode ser acessado pelo [link](https://github.com/0xNymerio/detect_botnet_traffic/blob/main/tulio_tcc_SI2020.pdf).


Utilizando o dataset ["An empirical comparison of botnet detection methods"](opa), a proposta foi elaborar uma aplicação que realizasse a classificação de tráfego de rede utilizando machine learning, classificando então como: Tráfego Normal ou Tráfego de Botnet. Ampliando as possibilidades de estudo, foi explorado o classificador utilizando para três classes alvo: Tráfego Normal, Tráfego de Botnet e Tráfego de Ataque do tipo de Port scanning. Para validar este modelo, também foi elaborado um dataset utilizando as ferramentas mais utilizadas no mercado para a validar os tipos de ataque (**netcat e nmap**). 

O arquivo [preparar_data.py](https://github.com/0xNymerio/detect_botnet_traffic/blob/main/preparar_data.py) realiza o pré-processamento dos datasets. O [gerar_modelos.py](https://github.com/0xNymerio/detect_botnet_traffic/blob/main/gerar_modelos.py) realiza o treinamento dos modelos e salva cada um em formato **Pickle**. O [detect_botnet_flow.py](https://github.com/0xNymerio/detect_botnet_traffic/blob/main/detect_botnet_flow.py) realiza a predição pra cada tipo de ataque e seus parâmetros. Sobre fundamentação teórica e as métricas utilizadas, o cenário experimental elaborado e ferramentas utilizadas, tratamento e pré-processamento de dados, datasets utilizados e resultados obtidos, sugiro a leitura da [monografia]https://github.com/0xNymerio/detect_botnet_traffic/blob/main/tulio_tcc_SI2020.pdf) que contém todas as informações citadas bem como as refências utilizadas.

Caso tenha dúvidas ou queira entrar em contato para discutir sobre a monografia e a aplicação, me chame no [telegram](https://t.me/tcgomes).
