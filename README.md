比赛服务器辅助网站2.0版本更新

将此文件夹下载至服务器game/csgo中即可（与MatchZy，MatchZy_Stats，MatchZyDataBackup同级即可）

警告：缺少Steamid_Gameid.csv文件，MatchZy_Stats文件夹和Teams.csv文件会导致出错！建议在部署此网站时创建两个名为Steamid_Gameid.csv和Teams.csv的空文件

一个具有战绩计算以及显示功能的网页，需要配合MatchZy插件使用，需要pandas，os，csv，flask库，下载后运行app.py即可，作者所开放的端口为1988，大家使用时注意

程序中有作者自创的rating计算方法，因为作者举办的比赛缩写为SAL故称为rating sal。此rating计算方法鼓励闪光弹的使用，若有更好的计算方法欢迎反馈

目前为version 2.0，有许多不完善的地方，未实现功能有主页美化，比赛报名，战队编辑和登记，ban/pick，demo下载，单场数据查询，比赛资讯，赛程安排等。在2025年7月前会将网页制作完毕

另外，所有代码中的名字均为作者所举办的比赛的名字，请大家使用时注意修改