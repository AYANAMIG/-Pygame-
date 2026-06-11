# import pandas as pd
# import sqlite3
#
# # 读取Excel
# df = pd.read_excel("words.xlsx")
#
# # 连接数据库
# conn = sqlite3.connect("words.db")
#
# cursor = conn.cursor()
#
# for _, row in df.iterrows():
#
#     cursor.execute(
#         """
#         INSERT INTO words
#         (
#             word,
#             hint,
#             difficulty,
#             level
#         )
#         VALUES
#         (
#             ?, ?, ?, ?
#         )
#         """,
#         (
#             row["word"],
#             row["hint"],
#             row["difficulty"],
#             row["level"]
#         )
#     )
#
# conn.commit()
#
# conn.close()
#
# print("导入完成")