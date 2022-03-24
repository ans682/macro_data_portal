import json
import sqlite3

# Save the name of the database
db_file = 'taldau_indicator1.db'

# Create SQL connection to the database
con = sqlite3.connect(db_file)

# Create a cursor
cur = con.cursor()


'''
Goal: Take indicators for 1 february and print them in denormalized (like original) format
1. Read from SQL table
2. If parent print
3. If child gen 1, print with 2 spaces
4. If child gen 2, print with 4 spaces
5. If child gen 3, print with 6 spaces
'''

# Save name of period
month_names_list = ["1 МАЯ 2019 ГОДА", "1 ФЕВРАЛЯ 2022 ГОДА", "1 АВГУСТА 2021 ГОДА"]

cur.execute('''
        SELECT tableData.idEntry, 
        tableData.content, 
        tableTree.idAncestor, 
        tableTree.idDescendant, 
        tableTree.idNearestAncestor, 
        tableTree.commentLevel, 
        tableTree.idSubject,
        tableData.comment_sum
        FROM comments_data AS tableData 
        JOIN comments_tree AS tableTree
        ON tableData.idEntry = tableTree.idDescendant 
        WHERE tableTree.idAncestor = tableTree.idDescendant and tableData.period_id = 3''')
records = cur.fetchall()

# print("Type of records: ", type(records))
# # print("Values: ",records)

for record in records:
    line_indent = 4*record[5]
    print(line_indent*" ", record[1], " - ", record[7])
    # print("comLevel: ", record[5], " ; comSum: ", record[7])
