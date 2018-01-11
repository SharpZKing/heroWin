##前言
昨天组会实在无聊，构思了一下这两天火爆的芝士超人怎么使用python来辅助搜索题目答案。最终采用的方案是利用shell获取手机截屏，再配合百度AI开放平台能力中的通用文字识别接口，最后利用python来打开浏览器直接搜素答案。仅限娱乐，想拿奖还是得看你能力啊^-^

##原理说明（仅限Android手机）
1. 每次在题目出现的时候保证手机连接电脑，电脑需要提前配置好ADB调试环境（不知道如何配置adb环境的，借用别人链接<https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4>可参考）
2. 用 ADB 工具获取当前手机截图，并用 ADB 将截图 pull 到电脑上待处理
```
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .
```
3. 读取`config.json`文件中手机型号的需要截取的题目区域，比如这里的`smartisan_pro_roi`代表了在`坚果Pro`上题目出现在屏幕上的位置，可截取两种类型的题目：第一种为直白的问题型，此时截取屏幕左上角点`(x=80,y=370)`和右下角点`(x=980,y=550)`区域的矩形；第二种比如以下哪项为正确型题目那么截取问题和选项区域为左上角点`(x=80,y=370)`和右下角点`(x=980,y=1300)`区域的矩形。***不同的机型可能截取区域不一样，请自行尝试***
```
{
	"APIKey": "",
	"SecretKey": "",
	"access_token": "",
	"old_access_token": "1515656713.5475445",
	"smartisan_pro_roi": ["80", "370", "980", "550", "1300"]
}
```
4. 利用OCR识别图片中文字的能力来获取题目的具体内容。这里采用了百度AI开放平台的OCR识别接口的功能。因此你需要根据自己的情况注册开发者账号创建相应的文字识别的应用，在`config.json`文件中填入`APIKey`和`SecretKey`，而`access_token`第一次运行自动填写无需填写。
5. 解析百度OCR接口返回的内容获取具体问题内容，然后利用webbroswer来打开电脑的默认的浏览器来搜索。


##使用教程
1. 配置好adb环境，手机连接电脑
2. 打开芝士超人app
3. 在每次出现题目的时候，在cmd命令行输入
  ```python checkanswer.py --all 0```或```python checkanswer.py --all 1```
  参数0和1的区别就是截取题目区域的区别，0代表只截取题目区域的内容待搜索，针对第一种情况；1代表截取题目区域和待选项同时搜索，针对第二种情况；
4. **看你眼速，在浏览器看到答案就选了吧**

##截图 
![screenshot](D:\heroWin\screenshot.png)

![问题区域](D:\heroWin\roi.png)



##代码详见
<https://github.com/SharpZKing/heroWin>

##存在问题
如何快速检索正确答案并且识别到选项，目前解决方案不是很友好，故看你眼力和手速吧

##尾
大家玩得愉快，只能当做辅助搜索哦