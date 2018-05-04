# RESTful API文档

## 1 用户
### 1.1 注册

路径:/api/users

方法:POST

请求体:
```
{
	"name": "hello",
	"email": "hello@qq.com",
	"bio":"hello world",
	"password":"123456"
}
```

返回:
```
{
    "id": "9532867f-6df3-457d-912f-1067bd1ca577",
    "name": "hello",
    "email": "hello@qq.com",
    "bio": "hello world",
    "updated": "2018-05-04T15:04:44.692231"
}
```

# 2 会话
## 2.1 登入

路径:/api/sessions

方法:POST

请求体:
```
{
	"user_name":"hello",
	"password":"123456"
}
```

返回:
```
{
    "user_id": "9532867f-6df3-457d-912f-1067bd1ca577",
    "session": "9cd2fd60-1d0b-41e3-a16b-53ac202498fa"
}
```