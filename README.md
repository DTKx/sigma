# Solução desenvolvida pela Equipe Sigma durante o Hack INPI.
Este repositório contém a solução desenvolvida pela Equipe Sigma, durante o Hack INPI 2021.
O objetivo é auxiliar o preenchimento do pedido de Marcas através da recomendação de números de Classificação de Nice.

Perceba que o protótipo, dado o tempo, encontra se em fases iniciais de desenvolvimento. Necessitando portanto de melhorias no sistema de busca de palavras chave (implementada utilizando similaridade por métricas baseadas no algoritmo de Levenshtein), além de inclusão de testes de validação de inputs, melhoria em performance, testes de qualidade.
## Conteúdo
- [Motivação](#motivação)
- [Objetivo](#objetivo)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Licença](#licença)
- [Observações](#observações)

## Motivação
Muitos empreendedores desconhecem os procedimentos corretos/benefícios de proteções efetivas de marcas. Podendo gerar atrasos, eventual proteção jurídica inferior ao esperado e refletir em um sentimento de insatisfação. Um dos pontos críticos durante o pedido de marcas é a seleção da Classificação de NICE, dado a sua criticidade desenvolveu se uma ferramenta de suporte à tomada de decisão do empreendedor, que realiza uma busca automática e indica categorias NICE recomendadas para o pedido de proteção da sua marca.

## Objetivo
Ferramenta de suporte à tomada de decisão do empreendedor durante o processo de pedido de proteção de ativos intelectuais. 
Este MVP, possui o foco inicial no foco de suporte à seleção da classificação de NICE recomendada ao pedido de registro de Marcas da empresa do requerente.

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

1. Na página web, clique na aba Marcas. 
![Página Web inicial.](https://github.com/DTKx/sigma/blob/main/images/web1.PNG)
2. Preencha os dados de busca (Números CNAE e/ou produtos e/ou serviços). 
3. Clique em Obter sugestões de Classificação de NICE. 
![Preenchimento de dados da empresa.](https://github.com/DTKx/sigma/blob/main/images/web2.PNG)
4. As sugestões de números de Classificação de Nice surgirá,separadas por seleção com base nos Números CNAE,produtos,serviços.
![Sugestões de Classificações de NICE para a empresa.](https://github.com/DTKx/sigma/blob/main/images/web3.PNG)

## Licença
GNU GPL
v2.0
## Observações sobre a implementação

O presente protótipo, está em fase de desenvolvimento. Sendo utilizado para demonstrar a ideia, porém necessitando portanto de:
1. Melhorias no pre processamento de bases de dados.
1. Melhorias nos algoritmos de busca. Utiliza se atualmente métricas de similaridade baseadas no algoritmo de Levenshtein considerando um threshhold de similaridade superior a 95%. É necessário avaliar outras técnicas de NLP para uma melhor seleção de categorias.
1. Melhorias de performance, a presente implementação foi implementada em python. Necessitando portanto de melhorias de performance como por exemplo criação de memos de dicionários CNAE para Classificação de NICE.
1. Validação de inputs de usuários. A presente implementação não valida os inputs dos usuários, portanto fazendo se necessário a implementação.
1. Realização de testes de qualidade. Criação de unit tests para reduzir a probabilidade de bugs.