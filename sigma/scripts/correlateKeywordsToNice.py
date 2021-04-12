import json
import os
import codecs
from fuzzywuzzy import fuzz

pathDadosOriginais=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","originais")))
pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))



def loadJson(path):
    with open(path,encoding='utf-8') as f:
        jsonData=json.load(f)
    return jsonData

def exportToJson(data,path):
    with open(path, 'wb') as f:
        json.dump(data,codecs.getwriter('utf-8')(f), ensure_ascii=False)

def getNiceFromKeywordsSet(keywordsSet,dictProdServNiceKeywords,threshold):
    """Get Nice classification from Keywords. Evaluates similarity between keywords of Nice description considers a match if any of the 4 similarities metrics based on levenshtein distance are above the threshold.

    Args:
        keywordsSet (set of strings): Set of keywords to search.
        dictProdServNiceKeywords (dict): Dictionary of NICE with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
        threshold (int): Threshold to include similarity if any of the metrics are above.

    Returns:
        set of strings: returns a set with the NICE classification for the given set of keywords.    
    """
    recomendedNiceSet=set()   
    for keyword in keywordsSet:
        for nice,niceVal in dictProdServNiceKeywords.items():
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

def main():
    # Carrega dicts
    dictProdServNiceKeywords = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json"))
    dictProductsServicesNice = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json"))
    keywordsSet={'venda de automóveis','comércio de peças automotivas','limpeza de carros'}
    myNice=getNiceFromKeywordsSet(keywordsSet,dictProdServNiceKeywords,100)
    print(myNice)
    for key in myNice:
        print(dictProductsServicesNice[key])






if __name__=="__main__":
    main()