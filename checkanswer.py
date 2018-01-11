#!/usr/bin/env python
# encoding: utf-8
# 
# 冲顶大会 + 百度OCR + 百度搜索
# 
import urllib, urllib.request, urllib.parse, sys
import ssl
import os
from PIL import Image
import json
import time
import base64
import webbroswer as webbroswer
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--all", required=True,
	help="please input the area of y , value 0 or 1, 0 represent: only problem, 1 represent: problem and choice")
args = vars(ap.parse_args())

def readConfig():
	with open("config.json", "r") as f:
		return json.load(f)

AK = ''
OCRHTTP = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token='
config = readConfig()
AK = config["access_token"]
left_top_x = (int)(config["smartisan_pro_roi"][0])
left_top_y = (int)(config["smartisan_pro_roi"][1])
right_bottom_x = (int)(config["smartisan_pro_roi"][2])
right_bottom_y = (int)(config["smartisan_pro_roi"][3])


def getAK():
	start = time.time()
	global AK
	global config
	# client_id 为官网获取的AK， client_secret 为官网获取的SK
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+config["APIKey"]+'&client_secret='+config["SecretKey"]
	request = urllib.request.Request(host)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = urllib.request.urlopen(request)
	AK = json.load(response)["access_token"]
	print("getAK use time: ")
	print(time.time() - start)

def baiduAS(queryStr):
	url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd='+queryStr #暂时用这种自动打开浏览器的方式 防爬虫访问速度变慢
	webbroswer.open(url)
	# queryStr = queryStr.encode("utf-8")
	# request = urllib.request.Request("https://www.baidu.com/s?wd="+queryStr)
	# response = urllib.request.urlopen(request)
	# if response:
	# 	print("===========================")
	# 	print()
	# 	print("===========================")

def getAnswer(roi):
	global AK
	st = time.time()
	request = urllib.request.Request(OCRHTTP+AK)
	data = {
			"image":base64.b64encode(roi)
		}
	postdata = urllib.parse.urlencode(data)
	postdata = postdata.encode('utf-8')
	request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	print("time1:")
	print(time.time() - st)
	response = urllib.request.urlopen(url=request, data=postdata)
	print("time2:")
	print(time.time() - st)
	# 返回格式
	# {
	# 	"log_id": 2471272194, 
	# 	"words_result_num": 2,
	# 	"words_result": 
	# 		[
	# 			{"words": " TSINGTAO"}, 
	# 			{"words": "青島睥酒"}
	# 		]
	# }
	response = json.load(response)
	# print(response)
	queryStr = ''
	for i in range(0, response["words_result_num"]):
		queryStr = queryStr + response['words_result'][i]['words']
	# print("********************")
	# print(queryStr)
	print("getAnswer use time: ")
	print(time.time() - st)
	baiduAS(queryStr)

def readImg():
	global left_top_x, left_top_y, right_bottom_x, right_bottom_y
	os.system("adb shell screencap -p /sdcard/screenshot.png")
	os.system("adb pull sdcard/screenshot.png")
	im = Image.open('screenshot.png')
	im_resize = im.resize(((int)(im.size[0]/2), (int)(im.size[1]/2)))
	box = (left_top_x, left_top_y, right_bottom_x, right_bottom_y) # 根据不同手机分辨率截取不同的ROI区域（题目区域）
	roi = im.crop(box)
	roi.save("roi.png")
	with open("roi.png", "rb") as imgFile:
		result = imgFile.read()
	print("ROI GET...")
	return result

def readAKFromConfig():
	global AK
	global config
	path = os.getcwd()+"\config.json"
	print(path)
	with open("config.json","r") as f:
		config = json.load(f)
	AK = config["access_token"]

def writeAKToConfig():
	global AK
	global config
	with open("config.json", "w") as f:
		# config = json.load(f)
		config["access_token"] = AK
		config['old_access_token'] = str(time.time())
		json.dump(config, f)
		print("access token write to file success")

def main():
	global AK
	global config, right_bottom_y
	p = (int)(args["all"])
	if p == 0:
		right_bottom_y = (int)(config["smartisan_pro_roi"][3])
	if p == 1:
		right_bottom_y = (int)(config["smartisan_pro_roi"][4])

	print("process......")
	# print(AK)
	if AK!='':
		if time.time() - float(config['old_access_token']) > 30*24*60*60*1.0:
			print("AK need to update...")
			AK = ''
	if AK=='':
		getAK()
		writeAKToConfig()
		roi = readImg()
		getAnswer(roi)
	else:
		roi = readImg()
		getAnswer(roi)
		

if __name__ == '__main__':
    main()