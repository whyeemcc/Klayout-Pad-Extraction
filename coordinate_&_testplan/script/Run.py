def display():
    print(
'''
===============================================================================

 -> 请填写正确的 testplan 及 Shrink & Reference 完毕后，选择一项：

    1. 生成 WAT 机台相对坐标
    2. 生成 Bench sub_die <Pin针座>
    3. 生成 Bench sub_die <Card针卡>
    4. 生成 Bench Auto 测试 testplan
    5. 生成 Golden Die 分布图
''')

def select(value):
    if value == '1':
        from Wat_Relative_Coordinate import Main
        Main()
    elif value == '2':
        from Bench_Sub_Die_Pin import Main
        Main()
    elif value == '3':
        from Bench_Sub_Die_Card import Main
        Main()
    elif value == '4':
        from Bench_Auto_Testplan import Main
        Main()
    elif value == '5':
        from Golden_Die_Wafer_Map import Main
        Main()        
    else:
        pass    

def run():
    choice = input('\n Select : ')
    select(choice)
       
display()
while True:
    run()
