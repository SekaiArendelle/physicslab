# 通过`physicslab`使用物实网络API

## class User

`User`类是对一个真实的物实用户的封装

* 匿名用户登录:

```python
from physicslab import web
user = web.anonymous_login()
```

* 通过邮箱密码登录:

```python
from physicslab import web
user = web.email_login(YOUR_EMAIL, YOUR_PASSWORD)
```

* 通过`Token`, `AuthCode`登录:

```python
from physicslab import *
user = web.token_login(
    token=YOUR_TOKEN,
    auth_code=YOUR_AUTH_CODE,
)
```

* 通过《量子物理》本地的登录缓存登录(无需邮箱密码):

```python
from physicslab import web
from physicslab import quantum_physics
user = web.preference_login(quantum_physics.get_preference_path())
```

> 注: 该方式要求本机(Windows)装有《量子物理》并登录过CIVITAS账号; 若缓存的凭证已失效, 服务器会返回认证错误, 请改用邮箱密码登录。

一个`User`的对象有以下属性:

* is_binded: 该账号是否绑定了邮箱或第三方关联账号
* user_id: 用户id
* gold: 金币
* level: 等级
* device_id: 硬件指纹
* avatar_region
* decoration
* nickname: 用户昵称
* signature: 用户签名
* avatar: 当前头像的索引
* avatar_region
* decoration
* verification
~~为什么有些属性没写是什么意思呢? 因为我也不知道()~~

`User`类也提供了一些方法, 这些方法是对物实网络api的封装:
> 注: 以`async_`开头的方法为协程风格的api

详见 [API Reference - Web User](api/web_user.md)
