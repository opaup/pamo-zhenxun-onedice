import utils.data as dataSource
from flow import doFlow

# 初始化
# load_path()


# 入口
def on_message(msg):
    msgData = {
        "msg": msg.replace(".", "").replace("。", ""),
        "username": "绪山美波里",
        "userId": "000000000",
        "groupId": "114514"
    }
    result = doFlow(msgData)
    # 如果没有任何匹配的指令，则跳过
    if type(result) == bool:
        if not result:
            print("跳过拦截")
    return result


# TODO 定时备份到数据库 || init时同步检测数据更新

msg = (".st 犬神香2-力量40str40敏捷40dex40意志55pow55体质45con45外貌85app85教育15知识15edu15体型40siz40智力60灵感60int60san55san值55理智55理智值55"
       "幸运60运气60mp11魔法11hp8体力8会计5人类学1估价5考古学1乐理5取悦15攀爬20计算机5计算机使用5电脑5信用55信誉55信用评级55克苏鲁0克苏鲁神话0cm0乔装5闪避20汽车20驾驶20汽车驾驶20"
       "电气维修10电子学1话术5斗殴25手枪20急救30历史5恐吓15跳跃20母语15法律5图书馆20图书馆使用20聆听20开锁1撬锁1锁匠1机械维修10医学1博物学10自然学10领航10导航10神秘学5重型操作1重型机械1"
       "操作重型机械1重型1说服10精神分析1心理学10骑术5妙手10侦查25潜行20生存10游泳20投掷20追踪10驯兽5潜水1爆破1读唇1催眠1炮术10")
print(on_message(msg))

