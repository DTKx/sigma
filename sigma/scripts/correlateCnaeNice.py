"""
Objetivo:
Correlacionar o número CNAE com códigos de NICE inclusos ou não. Como há termos inclusos e exclusos, haverá códigos de NICE inclusos e exclusos.
Ex:{"01.11-3"(Código CNAE): {"Incluso": "010005,010007,010009"(Códigos de NICE inclusos), "Excluso":"910005,910007,910009"(Códigos de NICE não inclusos)} 

Método:
Será utilizado como métrica a distância de Levenshtein, utiliza como base para verificar similaridade entre strings o número de alterações na string1 para atingir resultado igual a string2.
"""
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


def createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold):
    """Compares dictionaries descriptions to evaluate similarity between keywords. Returns 4 similarities metrics based on levenshtein distance and considers as a match if any of the 4 metrics are above the threshold.

    Args:
        dictCnaeKeywords (dict): Dictionary of Cnaes with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
        dictProdServNiceKeywords (dict): Dictionary of NICE with {Identification key:{'included':keywords included in classification,'excluded':keywords excluded for classification.}}
        threshold (int): Threshold to include similarity if any of the metrics are above.

    Returns:
        dict: returns the dict with the similarity ranks, and also the correlation of CNAE number to NICEs numbers.
    """
    dictSimilarityRank={}
    dictCnaeNice={}
    keys=['Incluso', 'Excluso']
    
    for cnae,cnaeVal in dictCnaeKeywords.items():
        for nice,niceVal in dictProdServNiceKeywords.items():
            include=""
            exclude=""
            ranks=[]
            for i in range(0,2):#Index 0 considera incluso, index 1 verifica excluso
                if (i==1) & (niceVal[keys[i]]=='' or cnaeVal[keys[i]]==''):
                    ranks.append([-1,-1,-1,-1])
                # Calculates the ratio
                fuzz_ratio=fuzz.ratio(cnaeVal[keys[i]],niceVal[keys[i]])
                # Calculates partial ratio
                fuzz_partial_ratio=fuzz.partial_ratio(cnaeVal[keys[i]],niceVal[keys[i]])
                # Calculates the token sort ratio
                fuzz_token_sort_ratio=fuzz.token_sort_ratio(cnaeVal[keys[i]],niceVal[keys[i]])
                # Calculates the token set ratio
                fuzz_token_set_ratio=fuzz.token_set_ratio(cnaeVal[keys[i]],niceVal[keys[i]])
                ranks.append([fuzz_ratio,fuzz_partial_ratio,fuzz_token_sort_ratio,fuzz_token_set_ratio])
                if i==0:
                    i+=1
                    if (fuzz_ratio>=threshold) or (fuzz_partial_ratio>=threshold) or (fuzz_token_sort_ratio>=threshold) or (fuzz_token_set_ratio>=threshold):
                        include+=nice+','
                else:
                    i+=1
                    if (fuzz_ratio>=threshold) or (fuzz_partial_ratio>=threshold) or (fuzz_token_sort_ratio>=threshold) or (fuzz_token_set_ratio>=threshold):
                        exclude+=nice+','
            dictSimilarityRank[f"{cnae},{nice}"]={'include':{'m0':ranks[0][0],'m1':ranks[0][1],'m2':ranks[0][2],'m3':ranks[1][3]},'exclude':{'m0':ranks[1][0],'m1':ranks[1][1],'m2':ranks[1][2],'m3':ranks[1][3]}}
            dictCnaeNice[f"{cnae},{nice}"]={'include':include,'exclude':exclude}
    return dictSimilarityRank,dictCnaeNice

def main():
    print('Start')
    # Load dicts
    dictProdServNiceKeywords = loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json"))
    dictCnaeKeywords = loadJson(os.path.join(pathDadosProcessados,"cnae","ibge","dictCnaeKeywords.json"))
    threshold=100
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    threshold=95
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    threshold=90
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    threshold=80
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    threshold=70
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    threshold=60
    dictSimilarityRank,dictCnaeNice=createSimilarityCorrelationDict(dictCnaeKeywords,dictProdServNiceKeywords,threshold)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictSimilarityRank{threshold}.json")
    exportToJson(dictSimilarityRank,outputPathJson)
    outputPathJson=os.path.join(pathDadosProcessados,f"dictCnaeNice{threshold}.json")
    exportToJson(dictCnaeNice,outputPathJson)
    print(f"Finished{threshold}")
    

if __name__=="__main__":
    main()