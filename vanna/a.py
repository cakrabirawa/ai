from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat
from vanna.flask import VannaFlaskApp

class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config={'api_key': 'AIzaSyAqDgK8o1x1Qmm9jli5Lh1b7OZf0jgtR9M', 'model': 'Gemini 1.5 Flash'})

vn = MyVanna()

vn.connect_to_mysql(host='localhost', dbname='openposcinunukdb2', user='root', password='P@ssw0rd@!', port=3306)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'openposcinunukdb2'")

plan = vn.get_training_plan_generic(df_information_schema)
plan

vn.train(ddl="""
    CREATE TABLE IF NOT EXISTS tx_open_pos_d (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")

#vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

vn.train(sql="SELECT * FROM tx_open_pos_d")

training_data = vn.get_training_data()


#vn.remove_training_data(id='1-ddl')
#vn.ask(question='berikan pada saya 3 penjualan terbesar')

app = VannaFlaskApp(vn)
app.run()