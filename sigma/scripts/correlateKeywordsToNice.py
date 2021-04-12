import json
import os
import codecs
from fuzzywuzzy import fuzz
import re
import pandas as pd
pathDadosOriginais=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","originais")))
pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))



def loadJson(path):
    with open(path,encoding='utf-8') as f:
        jsonData=json.load(f)
    return jsonData

def exportToJson(data,path):
    with open(path, 'wb') as f:
        json.dump(data,codecs.getwriter('utf-8')(f), ensure_ascii=False)

def getNiceFromKeywordsSetLevenshtein(keywordsSet,dictProdServNiceKeywords,dictProductsServicesNice,threshold,typeAttributes):
    """Get Nice classification from Keywords. Evaluates similarity between keywords of Nice description considers a match if any of the 4 similarities metrics based on levenshtein distance are above the threshold.

    Args:
        keywordsSet (set of strings): Set of keywords to search.
        dictProdServNiceKeywords (dict): Dictionary of NICE with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
        dictProductsServicesNice (dict): Dicionário no formato {Código do produto/serviço:{"Especificação":Descrição do produto/serviço,"Classe":Código de NICE,"Tipo":Produto(p) ou Serviço(s)}}
        threshold (int): Threshold to include similarity if any of the metrics are above.
        typeAttributes (char): Tipo da base de dados sendo adicionada. (Produtos (P), Serviços(S) ou Todos (t)).

    Returns:
        set of strings: returns a set with the NICE classification for the given set of keywords.    
    """
    recomendedNiceSet=set()   
    for keyword in keywordsSet:
        for nice,niceVal in dictProdServNiceKeywords.items():
            if (dictProductsServicesNice[nice]['Tipo']!=typeAttributes) & (typeAttributes!='t'):#Verifica apenas caso o tipo seja igual ao da keyword sendo avaliada (Produto ou serviço).
                continue
            if niceVal['Excluso']!='':#Verifica se keyword é exclusa da classe
                # Calculates the ratio
                fuzz_ratio=fuzz.ratio(keyword,niceVal['Excluso'])
                # Calculates partial ratio
                fuzz_partial_ratio=fuzz.partial_ratio(keyword,niceVal['Excluso'])
                # Calculates the token sort ratio
                fuzz_token_sort_ratio=fuzz.token_sort_ratio(keyword,niceVal['Excluso'])
                # Calculates the token set ratio
                fuzz_token_set_ratio=fuzz.token_set_ratio(keyword,niceVal['Excluso'])
                if (fuzz_ratio>=threshold) or (fuzz_partial_ratio>=threshold) or (fuzz_token_sort_ratio>=threshold) or (fuzz_token_set_ratio>=threshold):
                    continue
            #Se não há valores de chave em excluso
            # Verifico se pode ser incluso
            # Calculates the ratio
            fuzz_ratio=fuzz.ratio(keyword,niceVal['Incluso'])
            # Calculates partial ratio
            fuzz_partial_ratio=fuzz.partial_ratio(keyword,niceVal['Incluso'])
            # Calculates the token sort ratio
            fuzz_token_sort_ratio=fuzz.token_sort_ratio(keyword,niceVal['Incluso'])
            # Calculates the token set ratio
            fuzz_token_set_ratio=fuzz.token_set_ratio(keyword,niceVal['Incluso'])
            if (fuzz_ratio>=threshold) or (fuzz_partial_ratio>=threshold) or (fuzz_token_sort_ratio>=threshold) or (fuzz_token_set_ratio>=threshold):
                recomendedNiceSet.add(nice)
    return recomendedNiceSet

def getNiceFromKeywordsSetContainAny(keywordsSet,dictProdServNiceKeywords,dictProductsServicesNice,typeAttributes):
    """Get Nice classification from Keywords. Evaluates if contain any keyword in the description.

    Args:
        keywordsSet (set of strings): Set of keywords to search.
        dictProdServNiceKeywords (dict): Dictionary of NICE with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
        dictProductsServicesNice (dict): Dicionário no formato {Código do produto/serviço:{"Especificação":Descrição do produto/serviço,"Classe":Código de NICE,"Tipo":Produto(p) ou Serviço(s)}}
        typeAttributes (char): Tipo da base de dados sendo adicionada. (Produtos (P), Serviços(S) ou Todos (t)).

    Returns:
        set of strings: returns a set with the NICE classification for the given set of keywords.    
    """
    recomendedNiceSet=set()   
    for keywords in keywordsSet:
        for keyword in keywords.split():
            for nice,niceVal in dictProdServNiceKeywords.items():
                if (dictProductsServicesNice[nice]['Tipo']!=typeAttributes) & (typeAttributes!='t'):#Verifica apenas caso o tipo seja igual ao da keyword sendo avaliada (Produto ou serviço).
                    continue
                if niceVal['Excluso']!='':#Verifica se keyword é exclusa da classe
                    excluso=re.search(keyword,niceVal['Excluso'])#Retorna apenas a primeira substring
                    if excluso:
                        continue
                incluso=re.search(keyword,niceVal['Incluso'])#Retorna apenas a primeira substring
                if incluso:
                    recomendedNiceSet.add(nice)
    return recomendedNiceSet


def getCnaeKeywords(cnaeSet,dictCnaeKeywords):
    return set([dictCnaeKeywords[cnae]['Incluso'] for cnae in cnaeSet])


def main():
    # Carrega dicts
    dictProdServNiceKeywords = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json"))
    dictProductsServicesNice = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json"))
    dictCnaeKeywords = loadJson(os.path.join(pathDadosProcessados,"cnae","ibge","dictCnaeKeywords.json"))
    # Casos de uso
    threshhold=80

    # Lista de produtos
    keywordsProductsSet={'venda de automóveis','comércio de peças automotivas'}
    myNice=getNiceFromKeywordsSetLevenshtein(keywordsProductsSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'p')
    print('Fuzz',myNice)
    for key in myNice:
        print(dictProductsServicesNice[key])
    dfProducts=pd.DataFrame.from_dict({key:{'Especificação':dictProductsServicesNice[key]['Especificação'],'Classe Nice':dictProductsServicesNice[key]['Classe']} for key in myNice},orient='index')
    print(dfProducts.to_html())

    # myNice=getNiceFromKeywordsSetContainAny(keywordsProductsSet,dictProdServNiceKeywords,dictProductsServicesNice,'p')
    # print('Contain',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    # # Lista de serviços
    # keywordsServicesSet={'limpeza de carros'}
    # myNice=getNiceFromKeywordsSetLevenshtein(keywordsServicesSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'s')
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    # myNice=getNiceFromKeywordsSetContainAny(keywordsServicesSet,dictProdServNiceKeywords,dictProductsServicesNice,'s')
    # print('Contain',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    # #Cnae        
    # # keywordsCnaeSet={'venda de automóveis','comércio de peças automotivas','limpeza de carros'}
    # cnaeSet={'01.35-1','01.33-4'}
    # keywordsCnaeSet=getCnaeKeywords(cnaeSet,dictCnaeKeywords)
    # print(keywordsCnaeSet)

    # myNice=getNiceFromKeywordsSetLevenshtein(keywordsCnaeSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'t')
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    # myNice=getNiceFromKeywordsSetContainAny(keywordsCnaeSet,dictProdServNiceKeywords,dictProductsServicesNice,'t')
    # print('Contain',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])




if __name__=="__main__":
    main()