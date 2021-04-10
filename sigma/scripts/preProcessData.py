import json
import os
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from string import punctuation
import codecs

pathDadosOriginais=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","originais")))
pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))
stopwords=set(stopwords.words('portuguese'))#Palavras stopwords


def keysStrtoInt(x):
    return {int(k): v for k, v in x.items()}

def loadJson(path):
    with open(path,encoding='utf-8') as f:
        jsonData=json.load(f)
    return jsonData


def createDictIncludedExcludedKeywords(myDictString,dictSubkeyStr):
    """Creates a new dict using the key of a dictionary, splits a value by string 'exceto', therefore separating a string of keywords included in classification and a string of keywords excluded.
Steps:1) Splits strings before and after word 'exceto'. 2) Removes stopwords in portuguese.3)Adds to dict.


    Args:
        myDictString (dict): Dictionary to be parsed, in the format {idkey:{'dictSubkeyStr':String to be preprocessed,...}}
        dictSubkeyStr (str): Name of dictionary subkey to be used to get the string to be processed.

    Returns:
        [dict]: Dictionary with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
    """
    dictKeywords={}
    for key,value in myDictString.items():
        descricaoSplitExceto=value[dictSubkeyStr].lower().translate(str.maketrans('', '', punctuation)).split('exceto')#Transforma lower case e remove pontuação
        #Remove stopwords e pontuação
        includedStr=" ".join(word for word in descricaoSplitExceto[0].split() if word not in stopwords)
        if len(descricaoSplitExceto)>1:
            excludedStr=" ".join(word for word in descricaoSplitExceto[1].split() if word not in stopwords)
            dictKeywords[key]={"Incluso":includedStr,"Excluso":excludedStr}#Palavras chave inclusas, palavras chave exceção
        else:
            dictKeywords[key]={"Incluso":includedStr,"Excluso":""}#Palavras chave inclusas
    return dictKeywords

def exportToJson(data,path):
    with open(path, 'wb') as f:
        json.dump(data,codecs.getwriter('utf-8')(f), ensure_ascii=False)

def main():    
    # Classificação de nice
    # Load dict
    dictProductsServicesNice = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json"))
    # Cria dicionário keywords inclusas e exclusas
    dictProdServNiceKeywords=createDictIncludedExcludedKeywords(dictProductsServicesNice,"Especificação")
    # Exporta dicionário em formato json
    outputPathJson=os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json")
    exportToJson(dictProdServNiceKeywords,outputPathJson)
    print('Length dictProdServNiceKeywords',len(dictProdServNiceKeywords))

    # Base de dados de CNAE
    # Load dict
    dictCnae = loadJson(os.path.join(pathDadosProcessados,"cnae","ibge","dictCnae.json"))
    # Cria dicionário keywords inclusas e exclusas
    dictProdServCnaeKeywords=createDictIncludedExcludedKeywords(dictCnae,"Denominaçao")
    # Exporta dicionário em formato json
    outputPathJson=os.path.join(pathDadosProcessados,"cnae","ibge","dictCnaeKeywords.json")
    exportToJson(dictProdServCnaeKeywords,outputPathJson)
    print('Length dictProdServCnaeKeywords',len(dictProdServCnaeKeywords))

if __name__=="__main__":
    main()