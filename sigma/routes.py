import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flask_login.utils import logout_user
from sigma import app
from sigma.scripts import correlateKeywordsToNice as ckn
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
    cnaes = request.args.get('cnaes', '').strip().split(',')
    products = request.args.get('products', '').strip().split(',')
    services = request.args.get('services', '').strip().split(',')

    # Carrega dicts
    pathDadosProcessados=(os.path.abspath(os.path.join(os.getcwd(),"sigma","dados","processados")))
    dictProdServNiceKeywords = ckn.loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProdServNiceKeywords.json"))
    dictProductsServicesNice = ckn.loadJson(os.path.join(pathDadosProcessados,"classificacao_nice","dictProductsServicesNice.json"))
    dictCnaeKeywords = ckn.loadJson(os.path.join(pathDadosProcessados,"cnae","ibge","dictCnaeKeywords.json"))
    # # Casos de uso
    # threshhold=80

    # # Lista de produtos
    # keywordsProductsSet={'venda de automóveis','comércio de peças automotivas'}
    # myNice=getNiceFromKeywordsSetLevenshtein(keywordsProductsSet,dictProdServNiceKeywords,dictProductsServicesNice,threshhold,'p')
    # print('Fuzz',myNice)
    # for key in myNice:
    #     print(dictProductsServicesNice[key])

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


    niceFromCnae=cnaes
    niceFromProducts=products
    niceFromServices=services

    # if cnaes == '':
    #     msg = 'Você não informou os seus CNAEs.'
    #     niceFromCnae='Você não informou os seus CNAEs.'
    #     niceFromProducts
    #     niceFromServices
    # else:
    #     msg = cnaes+products+services
    return render_template('show_results.html',niceFromCnae=niceFromCnae,niceFromProducts=niceFromProducts,niceFromServices=niceFromServices)



    # form=NiceClassificationForm()
#     if form.validate_on_submit():
#         post=Post(title=form.title.data,content=form.content.data,author=current_user)
#         flash('Your post has been created','success')
#         return redirect(url_for('home'))
    return render_template('create_nice_class.html',title='Classificação de Nice',form=form,legend='Classificação de Nice')

