# quick start

## 第一个程序

元件浮空几乎成为了修改存档的代名词，因此，就让我们从创建一个悬空的逻辑输入开始吧：

```Python
from physicslab import (
    crt_circuit_experiment,
    LogicOutput,
    Position,
    generate_a_new_sav_path,
)

with crt_circuit_experiment("example") as expe:
    expe.crt_a_element(LogicOutput(Position(0, 0, 0.1)))

    destination = generate_a_new_sav_path()
    if not destination.parent.exists():
        destination.parent.mkdir(parents=True)
    expe.save_to(destination)
```

执行程序，打开物实，打开名为example的实验，即可看到效果

## 连接导线

```Python
from physicslab import (
    crt_circuit_experiment,
    LogicInput,
    LogicOutput,
    Position,
    generate_a_new_sav_path,
)

with crt_circuit_experiment("example") as expe:
    e1 = LogicInput(Position(-0.1, 0, 0))
    e2 = LogicOutput(Position(0.1, 0, 0))
    expe.crt_elements(e1, e2)
    expe.crt_a_wire(e1.o, e2.i)

    destination = generate_a_new_sav_path()
    if not destination.parent.exists():
        destination.parent.mkdir(parents=True)
    expe.save_to(destination)
```

## 通过网络api与物实交互

仿照客户端的行为，向物实服务器发送请求，获取物实服务器的响应

```Python
from physicslab import web

# 登录物实账号
user = web.email_login(YOUR_EMAIL, YOUR_PASSWORD)

# 用户昵称
print(user.nickname)
```

更多用法请查看[web.md](./web.md)
