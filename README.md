# Solução desenvolvida pela Equipe Sigma durante o Hack INPI.
Este repositório contém a solução desenvolvida pela Equipe Sigma, durante o Hack INPI 2021.
O objetivo é auxiliar o preenchimento do pedido de Marcas através da recomendação de números de Classificação de Nice.

## Conteúdo
- [Motivação](#motivação)
- [Objetivo](#objetivo)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Licença](#licença)

## Motivação
Muitos empreendedores desconhecem os procedimentos corretos/benefícios de proteções efetivas de marcas. Podendo gerar atrasos, eventual proteção jurídica inferior ao esperado e refletir em um sentimento de insatisfação. Um dos pontos críticos durante o pedido de marcas é a seleção da Classificação de NICE, dado a sua criticidade desenvolveu se uma ferramenta de suporte à tomada de decisão do empreendedor, que realiza uma busca automática e indica categorias recomendadas.

## Objetivo

### Entradas
- CNAEs da empresa
- Lista de produtos da empresa
- Lista de serviços 
### Saídas
- Classificações NICE que podem ser relevante à proteção da marca da empresa com base em:
	- CNAEs da empresa
	- Lista de produtos da empresa
	- Lista de serviços 

## Instalação
### Python
Realize a instalação do [Python](https://www.python.org/downloads/).

### Criando o Ambiente Virtual
Pode se realizar a instalação dos pacotes necessários de forma simplificada utilizando pip ou conda.

Utilizando pip no cmd:
```
pip install -r environment.yml
```
#### Anaconda (Opcional)
Realize a instalação do gestor de pacotes do python [Anaconda](https://www.anaconda.com/products/individual).

Utilizando terminal Conda:
```
conda env create -f environment.yml
```

## Utilização
Após ativar o Ambiente Virtual criado, execute run.py o arquivo no cmd.
```
python run.py
```
Clique então no link que surgirá e você será redirecionado à interface de uma página web da ferramenta.

Na página web, preencha os dados da empresa. Clique em classificar e a sugestão de números de Classificação de Nice surgirá.

## Licença
GNU GPL
v2.0
