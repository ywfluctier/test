一个用于学校论坛的爬虫
================

早先用python写爬虫纯粹手工，没有使用任何框架。

采用正则表达式去匹配网页源码里的标签，

可谓是费时又费力。

后来尝试采用了scrapy框架。

初始的代码是打算以cookies的方式直接向网站请求信息，

后来发现登录保存回话的方式更可靠。

在非框架模式中，

requests.Session对象可用于处理会话，

该对象内置有

get(url , headers = header )和

post(url , data = data , headers = header )等函数

我用来测试站点服务器的响应情况。

scrapy中的会话是以yield scrapy.http.Request的方式请求回复的。

参数表类似为(url, meta = data , headers = header )

一开始我以为这个对象能用于POST方法，

于是把data数据传递给meta参数，未果。

后来知道POST请求应该通过scrapy.http.FormRequest发送，

参数表为(url, formdata = data , headers = header )

好用多了

只是要注意form避免写成from【笑……】

爬虫的处理部分写得比较简单。

重写了start_requests方法之后就是各种回调。

爬虫仅仅对论坛首页的链接进行了爬取，

得到帖子的主要内容。

翻页功能没有做进一步开发。

因为最早卡在了网站登录上，

何况翻页也不复杂。

最后体会就是框架其实还是很好用的，

尤其里面的解析框架，

大大方便了对网页源码的处理。
