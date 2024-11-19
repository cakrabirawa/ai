from vanna.chromadb import ChromaDB_VectorStore
from vanna.google import GoogleGeminiChat
from vanna.flask import VannaFlaskApp

class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        GoogleGeminiChat.__init__(self, config={'api_key': 'AIzaSyAqDgK8o1x1Qmm9jli5Lh1b7OZf0jgtR9M', 'model': 'Gemini 1.5 Flash'})

vn = MyVanna()

vn.connect_to_mysql(host='localhost', dbname='openposcinunukdb2', user='root', password='P@ssw0rd@!', port=3306)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

plan = vn.get_training_plan_generic(df_information_schema)
vn.train(plan=plan)

vn.train(
    question="Whats product best seller ini previous month ?", 
    sql="SELECT a.sIdProduk_fk, sum(a.nSubTotal) as nSubTotal FROM tx_open_pos_d a inner join tx_open_pos_h b on b.sIdTXOpenPOS = a.sIdTXOpenPOS_fk where month(b.dTXOpenPOSDate) = month(current_date) - 1 and year(b.dTXOpenPOSDate) = year(current_date) and a.sStatusDelete is null and b.sStatusDelete is null group by a.sIdProduk_fk"
)

vn.train(
    question="show all header data",
    sql="SELECT * from tx_open_pos_h where sStatusDelete is null"
)

vn.train(
    question="show all detail data",
    sql="SELECT * from tx_open_pos_d where sStatusDelete is null"
)

app = VannaFlaskApp(vn)
app.run()