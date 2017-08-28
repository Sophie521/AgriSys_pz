# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from bson.objectid import ObjectId
import os
import json
from Main.paserManager.newsContentPaser import *
from Main.dbManager.mongoClass import MongoOperator
from Main.recSys.knn import get_K_nearst_love
from Main.recSys.arima import get_min_max_degree
ROOT_URL = os.getcwd()

# Create your views here.
#主界面
def index(request,data={}):
	#data = {"user_name":"jeje","user_pwd":"jeje"}
	# return HttpResponse("Hello world！ This is my first trial. [Poll的笔记]")
	# return Http404
	user_name = request.session.get('user_name')
	data["user_name"] = user_name
	return render(request, ROOT_URL +"/recommend_templates/static/homepage.html", data) # 注意路径一定要写对

def login(request):
	return render(request, ROOT_URL +"/recommend_templates/static/login.html") # 注意路径一定要写对

def register(request):
	return render(request, ROOT_URL +"/recommend_templates/static/register.html") # 注意路径一定要写对

# 用户提交注册
def subRegister(request):
	response_data = {}
	if request.POST:
		try:
			rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
			select1 = request.POST.get('select1')
			select2 = request.POST.get('select2')
			select3 = request.POST.get('select3')
			select4 = request.POST.get('select4')
			user_name = request.POST.get('user_name')
			user_pwd = request.POST.get('user_pwd')
			print select1,select2,select3,select4,user_name,user_pwd
			if checkRegister( user_name, user_pwd )==False: return index(request)
			db_ans = rec_db.find( {"user_name":user_name} ) 
			if db_ans.count() != 0: # 如果用户名和密码已经存在，就返回主页
				return index(request) 
			else:
				db_user = {
					"user_name":user_name,
					"user_pwd":user_pwd,
					"user_love": [select1,select2,select3,select4],
				}
				rec_db.insert(db_user)
				request.session['is_login'] = True
				request.session['user_name'] = user_name
				response_data["user_name"] = user_name
				return index(request, response_data )	
		except: return index(request)
	else: 
		try:
			rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
			select1 = request.GET.get('select1')
			select2 = request.GET.get('select2')
			select3 = request.GET.get('select3')
			select4 = request.GET.get('select4')
			user_name = request.GET.get('user_name')
			user_pwd = request.GET.get('user_pwd')
			db_ans = rec_db.find({"user_name":user_name}) 
			if db_ans.count() != 0: # 如果用户名和密码已经存在，就返回主页
				return index(request) 
			else:
				db_user = {
					"user_name":user_name,
					"user_pwd":user_pwd,
					"user_love": [1,2,3,4],
				}
				rec_db.insert(db_user)
				response_data = {"user_name":user_name}
				return index(request,response_data )	
		except: return index(request)
	return index(request)

# 用户提交登录
def subLogin( request ):
	print "subLogin ......"
	response_data = {}
	if request.POST:
		user_name = request.POST.get('user_name')
		user_pwd = request.POST.get('user_pwd')
	else:
		user_name = request.GET.get('user_name')
		user_pwd = request.GET.get('user_pwd')
	try:
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
		db_ans = rec_db.find( {"user_name":user_name,"user_pwd":user_pwd} ) 
		if db_ans.count() == 0: # 如果用户名和密码不能对上号，就返回主页
			return index(request) 
		else:
			request.session['is_login'] = True
			request.session['user_name'] = user_name
			response_data["user_name"] =  user_name
			return index(request,response_data)	
	except: return index(request)

# 用户提交登出
def subLogout( request ):
	print "subLogout ......"
	request.session['is_login'] = False
	request.session['user_name'] = None
	return index(request)

# 核查注册用户名是否合法
def checkRegister(user_name, user_pwd):
	if user_name==None: return False
	if len(user_name)<=0 or len(user_name)>30: return False
	return True


#第一类新闻 农业新闻
def class_1(request, data = {}):
	print "class_1 ......"
	try:
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"农业新闻"} )
		data = {}
		ans_list = []
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				"news_id": str(news["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["news_list"] = ans_list
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/class_1.html",data) # 注意路径一定要写对


#第二类新闻 病虫害
def class_2(request, data = {}):
	print "class_2 ......"
	try:
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"病虫害"} )
		data = {}
		ans_list = []
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				"news_id": str(news["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["news_list"] = ans_list
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/class_2.html",data) # 注意路径一定要写对

#第三类新闻
def class_3(request, data = {}):
	print "class_3 ......"
	try:
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"果蔬种植"} )
		data = {}
		ans_list = []
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				"news_id": str(news["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["news_list"] = ans_list
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/class_3.html",data) # 注意路径一定要写对

#第四类新闻
def class_4(request, data = {}):
	print "class_4 ......"
	try:
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"市场价格"} )
		data = {}
		ans_list = []
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				"news_id": str(news["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["news_list"] = ans_list
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/class_4.html",data) # 注意路径一定要写对

#第四类新闻
def class_5(request, data = {}):
	print "class_5 ......"
	try:
		user_name = request.session.get('user_name')
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
		db_ans = rec_db.find({"class_name":"政策法规"} )
		data = {}; ans_list = []
		for i,news in enumerate(list(db_ans),0):
			ans_list.append( {
				"news": news,
				"news_id": str(news["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["news_list"] = ans_list
		data["user_name"] = user_name
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/class_5.html",data) # 注意路径一定要写对

def myRecommend(request,data = {}):
	print "myRecommend ......"
	user_name = request.session.get('user_name')
	try:
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
		db_ans = rec_db.find({"user_name":user_name} )[0]
		new_id_list = db_ans.get("looked_list")
		if new_id_list == None: #面对冷启动问题
			pass #
		else:
			print "========*****#######*********"
			rec_new_id_list = get_K_nearst_love(8,new_id_list) #推荐5个最优新闻名称给用户
		print "========**************",new_id_list
		ans_list = []
		for i,news_id in enumerate(rec_new_id_list,0):
			rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
			db_ans = rec_db.find({"_id":ObjectId(news_id)} )
			if db_ans.count() == 0: continue;
			db_ans = db_ans[0]
			ans_list.append({
				"news": db_ans,
				"news_id": str(db_ans["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			})
		data["user_name"] = user_name
		data["news_list"] = ans_list
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/myRecommend.html",data) # 注意路径一定要写对	

def history(request,data = {}):
	print "history ......"
	user_name = request.session.get('user_name')
	try:
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
		db_ans = rec_db.find({"user_name":user_name} )[0]
		new_id_list = db_ans.get("looked_list")
		ans_list = []
		for i,news_id in enumerate(new_id_list,0):
			rec_db = MongoOperator('localhost',27017,'AgriRecSys','news')
			db_ans = rec_db.find({"_id":ObjectId(news_id)} )
			if db_ans.count() == 0: continue;
			db_ans = db_ans[0]
			ans_list.append( {
				"news": db_ans,
				"news_id": str(db_ans["_id"]),

				"href": "#href_id%d"%(i), 
				"content_id": "href_id%d"%(i), 

				"click_id": "ajax_id_%d"%(i), 
				"ajax_id": "#ajax_id_%d"%(i), 
			} )
		data["user_name"] = user_name
		data["news_list"] = ans_list
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/history.html",data) # 注意路径一定要写对

# 获取用户对某一个新闻的点击 ajax技术
def count_click_times(request):
	print "count_click_times ...... "
	if request.POST:	
		news_id = request.POST.get('news_id')
		user_name = request.POST.get('user_name')
	else:
		news_id = request.GET.get('news_id')
		user_name = request.GET.get('user_name')
	try:
		rec_db = MongoOperator('localhost',27017,'AgriRecSys','user')
		db_ans = rec_db.find( {"user_name":user_name} )[0]
		if db_ans.get("looked_list") is None:
			looked_list = set([news_id])
		else:
			looked_list = set( list(db_ans["looked_list"]) ) 
			looked_list = looked_list | set([news_id])
		print news_id, user_name
		rec_db.update(   
			{'user_name':user_name},
			{'$set':{"looked_list":list(looked_list)}},   
		)
	except: return index(request)

def shift_title_bar(request):
	print "shift_title_bar ...... "
	data = []
	if request.POST:
		bar_name = request.POST.get('bar_name')
		user_name = request.POST.get('user_name')
	else:
		bar_name = request.GET.get('bar_name')
		user_name = request.GET.get('user_name')
	data["bar_name"] = bar_name
	data["user_name"] = user_name
	return JsonResponse(data)

#天气栏
def weather(request):
	print "weather ......"
	try:
		pred_min_list, pred_max_list = get_min_max_degree()
		user_name = request.session.get('user_name')
		data = {}; ans_list = []
		weather_list = paserWeather() #[{},{},{},...]
		for i, weather in enumerate(weather_list,0):
			if i >= 7: break;
			ans_list.append( {
				"key": i,
				"content": weather,
			} )
		data["weather_data"] = ans_list
		data["user_name"] = user_name
		data["pred_max"] = [ "%.2f"%(degree) for degree in pred_max_list[1:]]
		data["pred_min"] = [ "%.2f"%(degree) for degree in pred_min_list[1:]]
	except: return index(request)
	return render(request, ROOT_URL +"/recommend_templates/static/weather.html",data) # 注意路径一定要写对

