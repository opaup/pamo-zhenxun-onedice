# 真寻骰 ~pamo-zhenxun-onedice~
一个给真寻bot或nonebot使用的dice骰娘功能，主要服务于真寻bot

除继承基础的常用骰功能外，希望在指令使用感上进一步优化，同时添加一些方便有趣的附属功能，如[团贴功能](#fun_notice)


**一个简单功能介绍**
<details>
   <summary>基础roll点</summary>
   <p>
- **基础roll点** ~rd~

  即最基础也是最简单的dice指令，默认为1d100，如果群内设置了默认骰，如20，则默认为1d20。同时支持附加表达式的简单计算，如：.rd20+1d3 | .r3d6*5 | .r2d6+6

  > "d"是什么意思？ d即是 dice的意思，如1d100就是roll 1次100面骰

   </p>
</details>
  

<details>
   <summary>人物卡相关操作</summary>
   <p>
- **人物卡做成** ~make~

  目前仅实现了coc7th的人物卡做成，指令格式如 .coc | .coc5 ，后面跟数字即是做成n次

  未来预期实现支持dnd、coc5th、coc幼年调查员做成或其他规则

  

- **人物卡操作** ~st~

  同样为人物卡相关的操作指令，包括录入、切换、更新、属性调整 、卡锁定、卡删除、查看当前角色卡的详细信息、查看当前角色卡的特定属性、查看已创建的角色卡列表

  - 角色卡录入

  支持目前coc7th主流xls半自动卡导出的如这样的格式进行角色卡的录入，注意必须为[角色名-属性]的形式哦。

  ```
  .st鹿诗瑶-力量45str45敏捷50dex50意志50pow50体质50con50外貌75app75教育75edu75体型35siz35智力70灵感70int70san50san值50理智50理智值50幸运80运气80mp10魔法10hp8体力8会计5人类学1估价5考古学1魅惑15攀爬20计算机70计算机使用70电脑70信用30信誉30信用评级30克苏鲁0克苏鲁神话0cm0乔装5闪避25汽车20驾驶20汽车驾驶20电气维修10电子学1话术5斗殴60手枪20急救40历史5恐吓15跳跃20母语75法律45图书馆60图书馆使用60聆听50开锁1撬锁1锁匠1机械维修10医学1博物学35自然学35领航10导航10神秘学5重型操作1重型机械1操作重型机械1重型1说服65精神分析1心理学50骑术5妙手10侦查50潜行20生存10游泳20投掷20追踪55驯兽5潜水1爆破1读唇1催眠1炮术1
  ```

  - **属性调整**

  `指令格式：.st 力量+20 .st智力-100`

  使用该指令需先录入角色卡

  - **角色卡切换** 

  `指令格式： .st 角色名` 

  进行角色卡切换，如在群聊中锁定了人物卡，则需要先解锁才可以切换，注意这里的切换为全局切换（如果想要不同的群使用不同的卡则需要用到角色卡锁定功能）。

  - **查看已创建的角色卡列表**

  `指令格式： .st list`

  - **查看当前角色卡的详细信息**

  `指令格式：.st show `

  该指令会返回包括角色名、id、全部属性在内的详细json信息

  - **查看当前角色卡的特定属性**

  `指令格式： .st show 属性名`

  

  TODO： 角色卡锁定与删除

  
   </p>
</details>
<details>
   <summary>进阶检定</summary>
   <p>
- **进阶检定** ~rh/ra/sc/rb/rp~

  分别为：暗骰、属性/技能检定、san check、惩罚骰、奖励骰

  - **暗骰**

  即经典的暗骰检定，支持如rd一样的表达式，该指令必须于群聊中使用。效果：在使用后会通知群聊进行了暗骰检定，同时发送检定结果到检定人的私聊窗口。

  - **属性/技能检定**

  `指令格式：.ra灵感 | .ra 摸鱼50 | .ra技能名+2d3`

  使用该指令需先录入角色卡，否则默认属性值为0，支持临时输入属性值，支持附加表达式的简单计算。

  同时会根据当前的房规进行检定结果判断

  默认房规：当值小于50时，1大成功，98-100大失败；大于50时，1-3大成功，100大失败

  该检定会计入检定统计次数，之后就可以看到自己roll出过多少大失败啦！

  <u>当然也可以根据计算的数字由kp自行判断结果</u>

  

  TODO：其他的预置房规支持

  - **san值检定**

  `指令格式：.sc 0/1 | .sc1/1d2 | .sc1d3/2d4`

  使用该指令需先录入角色卡。该指令必须包括成功减少值与失败减少值。

  说明：san值检定，对灵感进行检定，如成功则减少 “/” 前面的值，失败减少后面的值，在进行检定后会自动对san属性进行相关的减值，记得在使用前一定一定要检查当前使用的卡是否正确哦！

  - **惩罚骰、奖励骰**

  `指令格式：.rb | .rp2`

  默认检定为coc规则的检定，可切换为dnd模式或其他规则

  指令后只能跟随1位数字，表示拥有n个惩罚骰/奖励骰，并进行相关计算

  

  TODO：支持dnd模式或其他规则

  

- **疯狂状态** ~ti/li~

  **未完成**

  即抽取随机的疯狂症状，虽然目前还没有这个指令，但kp可以自行去规则书抽。

  </p>
</details>
<details>
   <summary>队伍相关的指令</summary>
   <p>

- team

  **未完成**

  队伍相关的指令，包括：

  - team

  查看团队列表

  - team clear/clr/cls 

  清空队伍

  - team call 

  一键呼叫队伍全体成员

  - team add/rm 

  添加到队伍/从队伍删除

  - team 属性调整

  调整成员角色卡卡属性

  - team lock 

  队伍内一键全体角色卡上锁

  
   </p>
</details>

<details>
   <summary>其他指令</summary>
   <p>
- **今日人品** ~jrrp~

  **未完成**

  查看今天的随机人品值，不知道大家为什么都喜欢这个。

  

- **群组独立配置** ~dice set~

  

- **跑团记录** ~log~

  **未完成**

  

- <span id="fun_notice">**团贴功能**</span> ~notice~

  **未完成**

  介绍：为避免广告、诈骗、危险或垃圾消息群发，发布团贴需要审核kp身份，可以使用积分/真寻的金币/jrrp等来发布团贴，帖子会扩散到全部开启了团贴功能的群聊

  

- **先攻** ~rw~

  **未完成**

  

- **秘密团** ~secret~

  **未完成**

  秘密团相关指令，包括：设置自己为kp、加入ob队列......

   </p>
</details>

















开发进度：

- [x] rd基础投掷
- [x] coc任务卡做成
- [x] st录入/切卡/属性调整
- [x] ra技能检定
- [x] sanCheck
- [x] rh暗骰
- [x] rp、rb 惩罚奖励骰
- [ ] 团队功能
- [ ] ti li 疯狂状态
- [ ] st lock、st rm
- [ ] jrrp
- [x] 群组独立配置
- [ ] 跑团记录功能
- [ ] 团贴功能 ❤
- [ ] 数据同步与备份
- [ ] 先攻
- [ ] 秘密团功能
- [ ] 规则书查询
- [ ] 模组查询
- [ ] 其他规则支持

