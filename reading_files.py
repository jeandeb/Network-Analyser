import psycopg2
import snap

#TO FIND THE TABLE ID ACCORDING TO ITS NAME
def find_table_id( table_name, table_list ):

    for i in table_list:
        if (i[0] ==  table_name):
            return i[1]

    return 0

#BUILDING THE TABLE ID 
def build_table_id( table_name, table_list ):

    #INTIALIZING COUNTERS
    list_number = len(table_list)
    power_ten_list = list_number
    count_list = 0

    #GETTING THE NUMBER OF TABLES DIVIDED BY TEN
    while (power_ten_list > 0 ):
        
        power_ten_list = power_ten_list//10
        count_list +=1

    #FIND THE TABLE IN THE LIST
    table_number = find_table_id( table_name, table_list )
    power_ten_table = table_number
    count_table = 0

    #WHILE THE PO
    while (power_ten_table > 0 ):
        power_ten_table = power_ten_table//10
        count_table +=1

    table_str_id = ""

    iterator = 0
    diff = count_list - count_table
    while( iterator < diff ):
        table_str_id += "0"
        iterator +=1
    
    table_str_id += str( table_number )
    
    return table_str_id



def read_from_sql( dbname, user, password ) :

    try: 
        #CONNECT TO POSTGRESQL -> CHANGE NECESSARY PARAMETERS
        connection_str = "dbname='" + dbname + "' user='" + user + "' password='" + password + "' "
        conn = psycopg2.connect( connection_str )
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()

    #CREATING A UNDIRECTED GRAPH -> make it easy
    database_network = snap.TUNGraph.New()

    #GET ALL TABLES FROM THE RELATIONAL DATABASE
    all_items_str = "SELECT information_schema.TABLES.TABLE_NAME FROM information_schema.TABLES where table_schema='public'"
    cur.execute("" + all_items_str + "")
    tables = cur.fetchall()

    #CREATING THE TABLE ID CODE TAB
    id_code = []
    for i, table in enumerate(tables, 1):
        #ASSIGNING TO EACH TABLE A UNIQUE INTEGER ID   
        id_code.append([table[0], i ])
    
    #FOREIGN KEYS TAB INIT
    foreign_keys_ref = []

    for table in tables :

        all_requested_keys = ""
        all_requested_foreign_keys = ""

        #FOREIGN KEYS REFERENCES TAB INIT
        foreign_keys_ref = []

        #NAME OF THE TABLE IS THE FIRST ELEMENT
        table_name = table[0]

        #REQUEST TO GET THE PRIMARY KEY(S) NAME(S) OF THE TABLE
        primary_key_request = "SELECT c.column_name, c.ordinal_position FROM information_schema.key_column_usage AS c LEFT JOIN information_schema.table_constraints AS t ON t.constraint_name = c.constraint_name WHERE t.table_name = '" + table_name + "' AND t.constraint_type = 'PRIMARY KEY'"
        cur.execute( "" + primary_key_request  + "" )
        primary_key_char = cur.fetchall()

        #ADD ALL PRIMARY KEYS TO THE REQUEST STRING
        for primary in primary_key_char:
            all_requested_keys +=  "\"" + primary[0] + "\"," 

        #REQUEST TO GERT THE FOREIGN KEY(S) NAME(S) OF THE TABLE
        foreign_key_request = "SELECT c.column_name, c.ordinal_position FROM information_schema.key_column_usage AS c LEFT JOIN information_schema.table_constraints AS t ON t.constraint_name = c.constraint_name WHERE t.table_name = '" + table_name + "' AND t.constraint_type = 'FOREIGN KEY'"
        cur.execute( "" + foreign_key_request + "" )
        foreign_key_char = cur.fetchall()

        #ADD ALL FOREIGN KEYS TO THE REQUEST
        for foreign in foreign_key_char:

            #MODIFIYING THE NAME TO MATCH THE INFORMATION SCHEMA NAMING
            foreign_key_name = "" + table_name + "_" + foreign[0] + "_fkey"
            all_requested_keys +=  "\"" + foreign[0] + "\"," 
        
            #GET THE REFERENCED PRIMARY KEYS
            foreign_key_references_request = "SELECT r.unique_constraint_name FROM information_schema.referential_constraints AS r WHERE r.constraint_name = '" + foreign_key_name + "'  "
            cur.execute( "" + foreign_key_references_request + "" )
            foreign_keys_ref.append(cur.fetchall()[0][0][:-5]) 

        #DELETE THE LAST COMA FROM THE STRING
        all_requested_keys = all_requested_keys[:-1]

        #GET ALL THE NECESSARY KEYS
        item_request = "SELECT " + all_requested_keys + " FROM \"" + table_name + "\""
        cur.execute(  "" + item_request + "" )
        items = cur.fetchall()

        #ITERATE THROUGH THE ITEMS
        for item in items:
            
            #GET THE NUMBER OF EACH KEY TYPE
            iterator = 0
            number_of_primary_keys = len(primary_key_char)
            number_of_foreign_keys = len(foreign_key_char)

            #BUILD THE ITEM'S ID BY ADDING ALL HIS PRIMARY KEYS
            item_id = ""
            for p_key in item[:number_of_primary_keys]:
                item_id += str(p_key)

            #CALL THE BUILD FUNCTION WHICH WILL ADD THE TABLE ID TO THE ITEM
            item_id += build_table_id( table_name, id_code )
            #print item_id

            #PYTHON CANT HANDLE ID HIGHER THAN THIS NUMBER, WE HAVE NO CHOICE BUT TO SKIP
            if int(item_id) > 999999999:
                continue

            #IF THE NODE DOESNT EXIST, THEN CREATE IT
            if not database_network.IsNode( int(item_id) ):
                    database_network.AddNode( int(item_id) )

            #CREATE AN EDGE FOR EACH FOREIGN KEY IN THE TABLE
            for f_key_num, f_key in enumerate(item[number_of_primary_keys:],1):

                #CALL THE BUILD FUNCTION WHICH WILL ADD THE TABLE ID TO THE FOREIGN KEY ID
                f_key_table = foreign_keys_ref[f_key_num-1]
                item_linked_id = str(f_key) + build_table_id( f_key_table, id_code )

                #IF THE NODE DOESNT EXIST, THEN CREATE IT
                if not database_network.IsNode( int(item_linked_id) ):
                   database_network.AddNode( int(item_linked_id) )

                #ADD THE EDGE
                database_network.AddEdge( int(item_id), int(item_linked_id) )

    return database_network




