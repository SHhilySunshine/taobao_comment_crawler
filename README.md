# taobao_comment_crawler
淘宝商品评论爬虫 - 基于Selenium的评论采集工具
# 淘宝评论爬虫

基于Selenium实现的淘宝/天猫商品评论爬虫，支持多页自动翻页采集。

## 功能特点
- 自动登录淘宝账号
- 多页评论抓取
- 数据保存为文本文件
- 支持自定义抓取页数

## 运行环境
- Python 3.6+
- Chrome浏览器
- chromedriver

## 使用说明
1. 安装依赖：`pip install selenium`
2. 下载对应版本的[chromedriver](https://chromedriver.chromium.org/)
3. 修改代码中的chromedriver路径
4. 运行脚本：`python taobao_comment_crawler.py`

## 注意
- 需要手动扫码登录淘宝账号
- 请遵守网站爬虫协议
