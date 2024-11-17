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
vn.train(plan=plan)

vn.train(ddl="""
    CREATE TABLE `tx_open_pos_d` (
  `sIdTXOpenPOS_fk` varchar(13) NOT NULL,
  `nIdTXType_fk` int(11) NOT NULL,
  `nIdStore_fk` int(11) NOT NULL,
  `sIdProduk_fk` varchar(20) NOT NULL,
  `nQtyJual` int(11) DEFAULT NULL,
  `nHargaJual` double DEFAULT NULL,
  `nDisc` float DEFAULT NULL,
  `nDiscAmount` double DEFAULT NULL,
  `nSubTotal` double DEFAULT NULL,
  `nGrossAmount` double DEFAULT NULL,
  `nIdSuplier_fk` int(11) NOT NULL,
  `nRecvQtyDoc` int(11) DEFAULT NULL,
  `nRecvQtyFisik` int(11) DEFAULT NULL,
  `nRecvQtySelisih` int(11) DEFAULT NULL,
  `nRecvQtyMod` int(11) DEFAULT NULL,
  `nSeqNo` int(11) DEFAULT NULL,
  `sRecvDocNoReff` varchar(20) DEFAULT NULL,
  `dRecvDocNoReff` date DEFAULT NULL,
  `nQtySewa` int(11) DEFAULT NULL COMMENT 'Sewa',
  `nQtySewaMod` int(11) DEFAULT NULL COMMENT 'Sewa',
  `nQtyKembali` int(11) DEFAULT NULL COMMENT 'Kembali',
  `nHargaPokokSewa` double DEFAULT NULL COMMENT 'Sewa',
  `nHargaSewa` double DEFAULT NULL COMMENT 'Sewa',
  `nHargaJaminanSewa` double DEFAULT NULL COMMENT 'Sewa',
  `nPersenSewa` float DEFAULT NULL COMMENT 'Sewa',
  `nLamaSewa` int(11) DEFAULT NULL COMMENT 'Sewa',
  `nSubTotalSewa` double DEFAULT NULL COMMENT 'Sewa',
  `nLamaTelat` int(11) DEFAULT NULL COMMENT 'Kembali',
  `nNilaiDenda` double DEFAULT NULL COMMENT 'Kembali',
  `nPersenDenda` float DEFAULT NULL COMMENT 'Kembali',
  `sIdTXOpenPOSReffSewa_fk` varchar(13) DEFAULT NULL COMMENT 'Kembali',
  `nFisikKembali` int(11) DEFAULT NULL COMMENT 'Kembali',
  `sCreateBy` varchar(50) DEFAULT NULL,
  `dCreateOn` datetime DEFAULT NULL,
  `sLastEditBy` varchar(50) DEFAULT NULL,
  `dLastEditOn` datetime DEFAULT NULL,
  `sDeleteBy` varchar(50) DEFAULT NULL,
  `dDeleteOn` datetime DEFAULT NULL,
  `sStatusDelete` char(1) DEFAULT NULL,
  `sUUID` varchar(36) NOT NULL,
  `nIdDepartemenProduk_fk` int(11) NOT NULL,
  `sNamaDepartemenProduk` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sIdTXOpenPOS_fk`,`nIdTXType_fk`,`nIdStore_fk`,`sIdProduk_fk`,`nIdSuplier_fk`,`sUUID`,`nIdDepartemenProduk_fk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
""")

vn.train(documentation="Our Store Sales Data")

vn.train(sql="SELECT * FROM tx_open_pos_d")

training_data = vn.get_training_data()


#vn.remove_training_data(id='1-ddl')
#vn.ask(question='berikan pada saya 3 penjualan terbesar')

app = VannaFlaskApp(vn)
app.run()