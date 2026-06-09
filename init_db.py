from data.db_manager import DBManager

db = DBManager()

words = [

    ("apple", "苹果", 1),
    ("banana", "香蕉", 1),
    ("orange", "橙子", 1),
    ("teacher", "老师", 1),
    ("student", "学生", 1),
    ("school", "学校", 1),

    ("computer", "计算机", 2),
    ("keyboard", "键盘", 2),
    ("window", "窗口", 2),
    ("mouse", "鼠标", 2),
    ("internet", "互联网", 2),
    ("program", "程序", 2),

    ("algorithm", "算法", 3),
    ("database", "数据库", 3),
    ("framework", "框架", 3),
    ("function", "函数", 3),
    ("variable", "变量", 3),
]

for word in words:

    db.insert_word(
        word[0],
        word[1],
        word[2]
    )

print("词库创建完成")

db.close()