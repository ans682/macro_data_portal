import sqlite3
import json
import insert_in_closure_table

indicator_name = "ОТЧЕТ О ПОСТУПЛЕНИЯХ И ИСПОЛЬЗОВАНИИ НАЦИОНАЛЬНОГО ФОНДА РЕСПУБЛИКИ КАЗАХСТАН"
file_names_list = ["ОТЧЕТ О ПОСТУПЛЕНИЯХ И ИСПОЛЬЗОВАНИИ НАЦИОНАЛЬНОГО ФОНДА РЕСПУБЛИКИ КАЗАХСТАН НА 1 МАЯ 2019 ГОДА",
                    "ОТЧЕТ О ПОСТУПЛЕНИЯХ И ИСПОЛЬЗОВАНИИ НАЦИОНАЛЬНОГО ФОНДА РЕСПУБЛИКИ КАЗАХСТАН НА 1 ФЕВРАЛЯ 2022 ГОДА ",
                    "ОТЧЕТ О ПОСТУПЛЕНИЯХ И ИСПОЛЬЗОВАНИИ НАЦИОНАЛЬНОГО ФОНДА РЕСПУБЛИКИ КАЗАХСТАН НА 1 АВГУСТА 2021 ГОДА "]
month_names_list = ["1 МАЯ 2019 ГОДА", "1 ФЕВРАЛЯ 2022 ГОДА", "1 АВГУСТА 2021 ГОДА"]
source_name = "MinFin"

db_file = 'taldau_indicator1.db'

# Create SQL connection to the database
con = sqlite3.connect(db_file)

# Create a cursor
cur = con.cursor()


# -----------------------------------------------
# Read loaded json file
json_file = open(file_names_list[0] + '.json')

# Return json object as a dictionary
json_object = json.load(json_file)

print("Size of json: ", len(json_object))
v_tom_chisle = "в том числе"


try:
    ####### Pre-work ##########
     # Check whether source_name has been inserted into 'sources' table
    cur.execute("SELECT COUNT(1) FROM sources WHERE name='" + source_name + "'")
    records = cur.fetchall()
    print('SELECT query finished')

    source_id = 0
    if records[0][0] == 0:
        
        cur.execute("INSERT INTO sources (name) values ('" + source_name + "')")
        # Retrieve the source id of a newly created source
        cur.execute("SELECT source_id from sources WHERE name='" + source_name + "'")
        records = cur.fetchone()

        source_id = records[0]
        print("Source id: ", source_id)
    else:
        cur.execute("SELECT source_id from sources WHERE name='" + source_name + "'")
        records = cur.fetchone()
        source_id = records[0]
        print("source id: ", source_id)
    con.commit()

    # Insert period into 'periods' table
    period_id = insert_in_closure_table.add_period_name(month_names_list[0])

    # Check if post already exists in the 'posts' table
    cur.execute("SELECT COUNT(1) FROM posts WHERE content='" + indicator_name + "'")
    records = cur.fetchall()
    post_id = 1

    # print("Finished running 'add_period' function")
    # print("Records of posts: ", records)
    # print("Type of records of posts: ", type(records))
    # If term_item_name is not in the table
    if records[0][0] == 0:
        # Insert month into 'posts' table and retrieve the post_id
        post_id = insert_in_closure_table.create_post(indicator_name.strip(), source_id)
        print("New Post's been inserted ...")
    
    else:
        cur.execute("SELECT post_id FROM posts WHERE content='" + indicator_name.strip() + "'")
        
        # post_id = Post.objects.get(content=indicator_name.strip()).values('id')
        
        records = cur.fetchall()
        post_id = records[0][0]
        print("Post already exists. Post_id: ",post_id)
    
    # # Insert month into 'comments_data' table and 'comments_tree' table. Retrieve comment_id.
    # comment_id = insert_in_closure_table.add_comment(str(post_id), month_names_list[0])
    # ### comment_id = insert_in_closure_table.add_comment(str(1), month_names_list[0])

    # # Retrieve idAncestor, idNearestAncestor, commentLevel of a newly added row from the 'comments_tree' table
    # cur.execute("SELECT idAncestor, idNearestAncestor, commentLevel FROM comments_tree WHERE idDescendant = '" + str(comment_id) + "'")
    # records = cur.fetchall()
    # idAncestor = records[0][0]
    # idNearestAncestor = records[0][1]
    # commentLevel = records[0][1]
    ############################

    v_tom_chisle_gen1 = False
    v_tom_chisle_gen2 = False

    # Create variables to store lastly visited comments for every level in comments_tree
    recent_level0_comment_id = 0
    recent_level1_comment_id = 0
    recent_level2_comment_id = 0
    recent_level3_comment_id = 0

    print("Entering for loop ...")
    # Iterate through the json list:
    for item in json_object:

        # Check if the current item is a main category and not a dict
        if v_tom_chisle not in item and v_tom_chisle_gen1 == False and v_tom_chisle_gen2 == False:
            content = item
            comment_sum = json_object[item]

            # commentLevel = 1
            print("Main category: ", content.strip(), " ; Value: ", comment_sum, " ; Type of value: ", type(comment_sum))
            print("---+++---+++---+++---+++---")

            # Insert subcomment under "1 february" comment. Insert row into 'comments_data' table and relevant rows into 'comments_tree' table.
            ### subcomment_lvl1_id = insert_in_closure_table.reply_to_comment(str(1), content, str(recent_level0_comment_id), str(comment_sum))
            subcomment_lvl1_id = insert_in_closure_table.add_comment(post_id = str(post_id), comment_content = content.strip(), period_id = str(period_id), comment_sum = str(comment_sum))
            print("Subcomment level 1 id: ", subcomment_lvl1_id)
            recent_level1_comment_id = subcomment_lvl1_id

        
        # Check if the current item is a dict of main category
        elif v_tom_chisle in item and v_tom_chisle_gen1 == False and v_tom_chisle_gen2 == False:
            v_tom_chisle_gen1 = True
            print("Inside dashed strings")
            for elem in json_object[item]:
                if v_tom_chisle not in elem:
                    print("Dashed string: ", elem, " ; Value: ", json_object[item][elem], " ; Type of value: ", type(json_object[item][elem]))
                    content = elem
                    comment_sum = json_object[item][elem]

                    # Insert subcomment under main category comment. Insert row into 'comments_data' table and relevant rows into 'comments_tree' table.
                    ### subcomment_lvl2_id = insert_in_closure_table.reply_to_comment(str(1), content, str(recent_level1_comment_id), str(comment_sum))
                    subcomment_lvl2_id = insert_in_closure_table.reply_to_comment(post_id=str(post_id), comment_content=content.strip(), root_comment_id=str(recent_level1_comment_id), period_id=str(period_id), comment_sum=str(comment_sum))
                    
                    recent_level2_comment_id = subcomment_lvl2_id
                    
                
                elif v_tom_chisle in elem:
                    print("Found v_tom_chisle_gen2: ", elem)
                    v_tom_chisle_gen2 = True
                    for sub_elem in json_object[item][elem]:
                        print("subcom 2: ", sub_elem, " ; Value: ", json_object[item][elem][sub_elem])
                        content = sub_elem
                        comment_sum = json_object[item][elem][sub_elem]

                        # Insert subcomment under main category comment. Insert row into 'comments_data' table and relevant rows into 'comments_tree' table.
                        ### subcomment_lvl3_id = insert_in_closure_table.reply_to_comment(str(post_id), content, str(recent_level2_comment_id), str(comment_sum))
                        subcomment_lvl3_id = insert_in_closure_table.reply_to_comment(post_id=str(post_id), comment_content=content.strip(), root_comment_id=str(recent_level2_comment_id), period_id=str(period_id), comment_sum=str(comment_sum))
                        print("Subcomment level 3 id: ", subcomment_lvl3_id)
                        recent_level3_comment_id = subcomment_lvl3_id
            
        
            v_tom_chisle_gen1 = False
            v_tom_chisle_gen2 = False


        
except:
    print("ERROR in minfin_insert file")
    con.rollback()
# -----------------------------------------------



# Save (commit) the changes
con.commit()

# Close the connection
con.close()
