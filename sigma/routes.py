import os
import secrets
import pandas as pd
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flask_login.utils import logout_user
from sigma import app
from sigma.scripts import correlateKeywordsToNice as ckn
from sigma.scripts import preProcessData as ppd
from flask_login import login_user,current_user,login_required

@app.route("/")#ROOT
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/nice",methods=['GET','POST'])
def get_nice_class():
    return render_template('get_nice_class.html')

@app.route("/show_nice_results",methods=['GET','POST'])
def show_nice_results():
    cnaes = request.args.get('cnaes', '')
    products = request.args.get('products', '')
    services = request.args.get('services', '')
    # Preprocessa input
    keywordsProductsSet=set(ppd.removeStopwordsPunctuation(products))
    keywordsServicesSet=set(ppd.removeStopwordsPunctuation(services))
    print('keywordsProductsSet',keywordsProductsSet)
    print('keywordsServicesSet',keywordsServicesSet)

    # Carrega dicts
    pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))
    dictProdServNiceKeywords = ckn.loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json"))
    dictProductsServicesNice = ckn.loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json"))
    dictCnaeKeywords = ckn.loadJson(os.path.join(pathDadosProcessados,"cnae","ibge","dictCnaeKeywords.json"))

    # Casos de uso
    threshhold=95

    #Cnae        
    keywordsCnaeSet=ckn.getCnaeKeywords(set(cnaes.split(',')),dictCnaeKeywords)

    niceFromCnae=ckn.getNiceFromKeywordsSetLevenshtein(keywordsCnaeSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'t')
    dfniceFromCnae=pd.DataFrame.from_dict({key:{'Especificação':dictProductsServicesNice[key]['Especificação'],'Classe Nice':dictProductsServicesNice[key]['Classe']} for key in niceFromCnae},orient='index')

    # Lista de produtos
    niceFromProducts=ckn.getNiceFromKeywordsSetLevenshtein(keywordsProductsSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'p')
    print(niceFromProducts)
    dfniceFromProducts=pd.DataFrame.from_dict({key:{'Especificação':dictProductsServicesNice[key]['Especificação'],'Classe Nice':dictProductsServicesNice[key]['Classe']} for key in niceFromProducts},orient='index')

    # Lista de serviços
    niceFromServices=ckn.getNiceFromKeywordsSetLevenshtein(keywordsServicesSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'s')
    dfniceFromServices=pd.DataFrame.from_dict({key:{'Especificação':dictProductsServicesNice[key]['Especificação'],'Classe Nice':dictProductsServicesNice[key]['Classe']} for key in niceFromServices},orient='index')
    return render_template('show_results_tables.html',tables= [dfniceFromCnae.to_html(classes='data'),dfniceFromProducts.to_html(classes='data'),dfniceFromServices.to_html(classes='data')],titles=['na','CNAEs','Lista de Produtos','Lista de Serviços'])    
