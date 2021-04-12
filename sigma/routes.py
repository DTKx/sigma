import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flask_login.utils import logout_user
from sigma import app
from sigma.scripts import correlateKeywordsToNice as ckn
from sigma.scripts import preProcessData as ppd
from flask_login import login_user,current_user,login_required

@app.route("/")#ROOT PAGE OF OUR PAGE
@app.route("/home")#home also would work
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
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])


    # Lista de produtos
    niceFromProducts=ckn.getNiceFromKeywordsSetLevenshtein(keywordsProductsSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'p')
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    # Lista de serviços
    niceFromServices=ckn.getNiceFromKeywordsSetLevenshtein(keywordsServicesSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'s')
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

    return render_template('show_results.html',niceFromCnae=niceFromCnae,niceFromProducts=niceFromProducts,niceFromServices=niceFromServices)
