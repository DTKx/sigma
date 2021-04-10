import pandas as pd
import os
import pdfplumber

pathDadosOriginais=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","originais")))
pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))
# pathDadosProcessados=(os.path.abspath(os.path.join("..","dados","processados")))
# C:\Users\Debs\Documents\39_INPI_hack\sigma\sigma\dados\originais\classificacao_nice\PortalINPIListaAuxiliarDeServicosNCL112021_20210106.pdf


def addTablesFromMainPdfToDict(path,ixFirstLineFirstPage=1,ixFirstLineOtherPages=1):
    """Extrai tabelas dos PDFs de classificação de nice de tadaabelas principais de produtos e serviço.

    Args:
        path (string): Caminho do arquivo em PDF, com tabela com colunas nas seguintes ordens: Classificação de Nice,Especifição,Nº de base 

    Returns:
        dict: Dicionário no formato {Código do produto/serviço:{Descrição do produto/serviço:Código de NICE}}
        ixFirstLineFirstPage (int): Número da linha em que valores da tabela inicia na primeira página(Deve pular os cabeçalhos).
        ixFirstLineOtherPages (int): Número da linha em que valores da tabela inicia nas páginas seguintes à primeira(Deve pular os cabeçalhos).
    """
    myDict={}
    with pdfplumber.open(path) as pdf:
        i=0
        for page in pdf.pages:
            if i==0:#Primeira página devo pular ixFirstLineFirstPage linhas
                ixFirstLine=ixFirstLineFirstPage
            else:
                ixFirstLine=ixFirstLineOtherPages                
            for line in page.extract_table()[ixFirstLine:]:#Skips the columns names
                if (not line[2]) & (not line[1]) & (not line[0]):#Check empty lines
                    continue
                line[1] = line[1].replace("\n", "")#Remove end of line
                myDict[line[2]]={"Especificação":line[1],"Classe":line[0]}#Código,Descrição,nice
            i+=1
    return myDict

def createCsvMainFrom3ColDict(inputPath,dictAuxiliar,outputPath):   
    df=pd.DataFrame.from_dict({(dictAuxiliar[i][j],j):i
                            for i in dictAuxiliar.keys()
                            for j in dictAuxiliar[i].keys()},
                        orient='index')
    df.to_csv(outputPath)

def exportAsCsvFromDict(myDict,inputPath,outputPath):   
    df=pd.DataFrame.from_dict(myDict,orient='index')
    df.to_csv(outputPath)

def extractTablesFromAuxiliaryPdfToDict(path,idname,ixFirstLineFirstPage=2,ixFirstLineOtherPages=0):
    """Extrai tabelas de PDFs de listas auxiliares de classificação de NICE e adiciona em dicionário.

    Args:
        path (string): Caminho do arquivo em PDF, com tabela com colunas nas seguintes ordens: Descrição,Classe. 
        idname (string): Nome para código de identificação
        ixFirstLineFirstPage (int): Número da linha em que valores da tabela inicia na primeira página(Deve pular os cabeçalhos).
        ixFirstLineOtherPages (int): Número da linha em que valores da tabela inicia nas páginas seguintes à primeira(Deve pular os cabeçalhos).

    Returns:
        dict: Dicionário com os dados adicionais das tabelas auxiliares,no formato {Código do produto/serviço:{Descrição do produto/serviço:Código de NICE}}
    """
    myDict={}
    with pdfplumber.open(path) as pdf:
        i=0
        for page in pdf.pages:
            if i==0:#Primeira página devo pular ixFirstLineFirstPage linhas
                ixFirstLine=ixFirstLineFirstPage
            else:
                ixFirstLine=ixFirstLineOtherPages                
            for line in page.extract_table()[ixFirstLine:]:#Skips the columns names
                if (not line[1]) & (not line[0]):#Check empty lines
                    continue
                line[1] = line[1].replace("\n", "")#Remove end of line
                myDict[idname+str(i)]={"Especificação":line[1],"Classe":line[0]}#Código,Especificação,nice
                i+=1
    return myDict

import json,codecs
def exportToJson(data,path):
    with open(path, 'wb') as f:
        json.dump(data,codecs.getwriter('utf-8')(f), ensure_ascii=False)


def main():
    dictProductsServicesNice={}#Dicionario principal
    # Lista de produtos principal

    # Caminhos
    inputPath=os.path.join(pathDadosOriginais,"classificacao_nice","PORTALINPIListaDeProdutosEmOrdemDeClasseNCL112021_20210106.pdf")
    outputPathCsv=os.path.join(pathDadosProcessados,"classificacao_nice","dfProducts.csv")
    # Adiciona ao dicionário a lista de produtos principal.
    dictProductsServicesNice=addTablesFromMainPdfToDict(inputPath)
    # Exporta CSV da lista para visualização e verificação
    exportAsCsvFromDict(dictProductsServicesNice,inputPath,outputPathCsv)

    # Lista de produtos auxiliar
    # Caminhos
    inputPath=os.path.join(pathDadosOriginais,"classificacao_nice","PortalINPIListaAuxiliarDeProdutosNCL112021_20210106.pdf")
    outputPathCsv=os.path.join(pathDadosProcessados,"classificacao_nice","dfProductsAux.csv")
    idname="auxprod6_1_21_"

    # Adiciona ao dicionário a lista de produtos auxiliar.
    dictProductsAuxNice=extractTablesFromAuxiliaryPdfToDict(inputPath,idname)
    # Exporta CSV da lista para visualização e verificação
    exportAsCsvFromDict(dictProductsAuxNice,inputPath,outputPathCsv)
    # Atualiza o dicionário principal
    print("len before add dictProductsAuxNice",len(dictProductsServicesNice))
    dictProductsServicesNice.update(dictProductsAuxNice)
    print("len after add dictProductsAuxNice",len(dictProductsServicesNice))
    
    # Lista de serviços principal

    inputPath=os.path.join(pathDadosOriginais,"classificacao_nice","PortalINPIListaDeServicosEmOrdemDeClasseNCL112021_20210106.pdf")
    outputPathCsv=os.path.join(pathDadosProcessados,"classificacao_nice","dfServices.csv")

    # Cria dicionarios
    dictServicesNice=addTablesFromMainPdfToDict(inputPath)
    # Exporta CSV da lista para visualização e verificação
    exportAsCsvFromDict(dictServicesNice,inputPath,outputPathCsv)
    # Atualiza o dicionário principal
    print("len before add dictServicesNice",len(dictServicesNice))
    dictProductsServicesNice.update(dictServicesNice)
    print("len after add dictProductsServicesNice",len(dictProductsServicesNice))

    # Lista de serviços auxiliar
    # Caminhos
    inputPath=os.path.join(pathDadosOriginais,"classificacao_nice","PortalINPIListaAuxiliarDeServicosNCL112021_20210106.pdf")
    outputPathCsv=os.path.join(pathDadosProcessados,"classificacao_nice","dfServicesAux.csv")
    idname="auxserv_6_1_21_"

    # Cria dicionarios
    dictServicesAuxNice=extractTablesFromAuxiliaryPdfToDict(inputPath,idname)
    # Exporta CSV da lista para visualização e verificação
    exportAsCsvFromDict(dictServicesAuxNice,inputPath,outputPathCsv)
    # Atualiza o dicionário principal
    print("len before add dictServicesAuxNice",len(dictServicesAuxNice))
    dictProductsServicesNice.update(dictServicesAuxNice)
    print("len after add dictProductsServicesNice",len(dictProductsServicesNice))

    # Exporta dicionário em formato json
    outputPathJson=os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json")
    exportToJson(dictProductsServicesNice,outputPathJson)


if __name__=="__main__":
    main()