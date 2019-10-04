# 一些有用的开发技巧

## 1、调用pymongo连接mongo，提示“ServerSelectionTimeoutError: No servers found yet”错误的解决

- 原因分析：MongoClient采用后台启动方式，存在线程不安全的问题，立即使用connect可能尚未成功连接
- 解决方法：等待30秒后连接，或者最简单的方法是MongoClient设置`connect＝False`

  > By default, Flask-PyMongo sets the connect keyword argument to False, to prevent PyMongo from connecting immediately. PyMongo itself is **not fork-safe**, and delaying connection until the app is actually used is necessary to avoid issues. If you wish to change this default behavior, pass connect=True as a keyword argument to PyMongo.
  
- [参考文献](https://www.cnblogs.com/dhcn/p/7121395.html)
  
---

## 2、为Mongo数据库的镜像配置初始化用户和口令的方法

以[mongo:3.6镜像文件](https://github.com/docker-library/mongo/tree/master/3.6)为例，启动命令是`/usr/local/bin/docker-entrypoint.sh`

分析该脚本文件可以发现，设置数据库初始化用户是通过在操作系统中设置环境变量`MONGO_INITDB_ROOT_USERNAME`和`MONGO_INITDB_ROOT_PASSWORD`来实现的。  

mongo shell的格式为: ```mongo -u username -p password --authenticationDatabase admin```

注意：mongo初始化用户的角色级别为root，需要授权创建和修改database。

### 发现的问题: 调用flask-mongoengine连接mongo，采用URI方式配置参数一直报各类鉴权错误

- MongoEngine规定：
  >- If the database requires authentication, username, password and authentication_source arguments should be provided.
  >- Database, username and password from URI string overrides corresponding parameters in connect().

    ``` python
    connect(
        db='test',
        username='user',
        password='12345',
        host='mongodb://admin:qwerty@localhost/production'
    )
    ```

    will establish connection to production database using admin username and qwerty password.

- Flask Mongoengine规定：
  >- Uri style connections are also supported, just supply the uri as the host in the ‘MONGODB_SETTINGS’ dictionary with app.config. Note that database name from uri has priority over name.

- 最终建议：启动Mongo鉴权方式，connect时必须显式包含username、password、authentication_source三个参数；而且建议每个参数单独设置，不要采用URI方式。
  标准格式如下：

  ``` python
  MONGODB_SETTINGS = {
    'db': 'cmccb2b',
    'username': os.getenv('MONGODB_USERNAME'),
    'password': os.getenv('MONGODB_PASSWORD'),
    'host': os.getenv('MONGODB_HOST'),
    'port': int(os.getenv('MONGODB_PORT')),
    'connect': False,  # set for pymongo bug fix
    'authentication_source': 'admin', # set authentication source database， default is MONGODB_NAME
  }
  ```

- [Flask Mongoengine的connect官方文档](https://mongoengine-odm.readthedocs.io/guide/connecting.html)
- [Mongoengine的connect官方文档](http://docs.mongoengine.org/guide/connecting.html)
- [Mongo配置鉴权方式的经验](https://www.techcoil.com/blog/how-to-enable-authenticated-mongodb-access-for-flask-mongoengine-applications/)

---

## 3、如何在docker-compose中设置操作系统的环境变量

在docker-compose的配置文件目录，编辑默认环境文件`.env`，并在该文件中定义需要的变量。
> 注意：这些变量只能在`docker-compose.yml`中被引用

``` txt
__VERSION__=1.0

F6R_MONGO_USERNAME=root
F6R_MONGO_PASSWORD=forester
```

然后在`docker-compose.yml`中就可以导入`.env`文件中定义的环境变量

``` yml
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${F6R_MONGO_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${F6R_MONGO_PASSWORD}
```

---

## 4、几个bug修复

- Scrapy: 修复递归调用request时item数据混乱的bug，解决方法是将spider中item()初始化调整到循环体的内部，因为scrapy.request的meta传递是浅复制
- 增加查询专用index，解决pagination内存溢出问题
- `<a herf="#" onclick="gotoPage('2')">`标签等组件包含了默认动作，例如herf属性就会触发页面跳转，导致不需要的页面刷新，
可以通过控制return false的方式阻止默认动作的发生，具体参见[文档](https://www.cnblogs.com/weiwang/archive/2013/08/19/3268374.html) 
- 基于python3.6成功安装pyecharts，但alpine3.7报错很多
- 建立venv/的virtualenv，启动方式为`$ source venv/bin/activate`，退出方式为`$ deactivate`

## scrapy的spider打开shell用于调试xpath的方法

```python
from scrapy.shell import inspect_response
inspect_response(response, self)
```

---

## xpath函数normalize-space()的功能是去掉前后的空格，有两种用法

第一种方法非常实用,normalize-space用在属性上，如  

```python
response.xpath("//div[normalize-space(@class)='nav']/text()")
```

第二种方法：normalize-space用结果上，如  

```python
response.xpath("normalize-space（//div[normalize-space(@class)='nav']/text()）")
```

---

## 提取html所有文本的最简单方法

```python
response.xpath("string(.)")
```