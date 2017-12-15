# 火车票脚本

## 依赖模块安装
```bash
sudo python setup.py install
```
## 查询


```bash
python src/query_trains.py [出发站点] [目的站点] [日期]
```

![test](./img/test.png)

## 登录

```bash
python src/request_login.py 
```

## 自动下单
### Usage:

```bash
python    src/auto_get_order.py [-f] FROM_STATION [-t] TO_STATION [-d] DATE [-c] TRAIN_CODE [-s] SEAT_TYPE
```

### Arguments:
```
    FROM_STATION 出发站点(eg. 北京)
    TO_STATION   目的站点(eg. 上海)
    DATE         出发日期(eg. 2017-12-25)
    TRAIN_CODE   列车类型(eg. D,G,T,Z,K,L)
    SEAT_TYPE    座位型号(eg. 0)---[0 商务, 1 一等, 2 二等, 3 高级软卧, 4 软卧, 5 动卧, 6 硬卧, 7 软座, 8 硬座, 9 无座]
```

### Options:
```
    -h --help       show this
    -f --from       start station
    -t --to         to station
    -d --date       start off date
    -c --code       train code
    -s --seat       seat type
```

### Example:
```bash
    python src/auto_get_order.py -f 上海 -t 成都 -d 2017-12-25 -c DGTZK -s 012345678
```    