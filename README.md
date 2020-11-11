# data_exchange

## 项目依赖
需安装docker 和docker-compose

## 项目 部署方式
```
git clone git@github.com:18566208560/data_exchange.git
cd data_exchange
chmod 777 mysql_data
cp .env.example .env
cp app/settings.py.example app/settings.py
docker-compose up -d
```

