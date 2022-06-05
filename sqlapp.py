import streamlit as st 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.orm import Session #データ型取得
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey #SQLテーブルのカラム設定用
from sqlalchemy import desc #降順ソート

import pandas as pd
import os, glob

DB_file = 'testDB.db'
csv_file = 'users.csv'
engine = create_engine('sqlite:///' + DB_file, echo=False) #DB接続の設定

Session = scoped_session(
    sessionmaker(
        autocommit=False, #commit自動化の設定
        autoflush=False, #flush自動化の設定
        bind = engine
    )
)

Base =declarative_base()
Base.query = Session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    def __init__(self, name):
        self.name = name

def init_DB():
    Base.metadata.create_all(bind=engine)

init_DB()  

st.title('SqliteをStreamlitで使ってみる')

def read_users(engine):
    df = pd.read_sql('SELECT * FROM users', engine)
    return df

def update_csv(engine):
    df = read_users(engine)
    df.to_csv(csv_file, index=False)

name = st.text_input('名前を入力してください')
if st.button('名前を登録'):
    if name != '':
        user = User(name)
        Session.add(user)
        Session.commit()
        update_csv(engine)
    else:
        st.write('名前を入力してください。')


st.markdown('***')   
if st.button('名前一覧を表示'):
    df = read_users(engine)
    st.dataframe(df)

st.markdown('***')   
filetype = st.selectbox('ファイルタイプを選択してください', ['csv', 'sqlite'])
if filetype == 'csv':
    df = read_users(engine)
    st.download_button(label=f'{filetype}形式でデータをダウンロード',
                    data = df.to_csv(index=False).encode('utf-8'),
                    file_name = csv_file,
                    mime = 'text/csv')
elif filetype == 'sqlite':
    with open(DB_file, "rb") as fp:
        btn = st.download_button(
            label=f'{filetype}形式でデータをダウンロード',
            data=fp,
            file_name=DB_file,
            mime="application/octet-stream" #https://discuss.streamlit.io/t/download-sqlite-db-file/18747/2
        )
else:
    st.write('CSVかsqliteで選択してください。')


st.markdown('***')   
st.markdown('### 参考用')
st.write('os.getcwd()：',os.getcwd())
st.write("glob.glob('*')：",glob.glob('*'))
st.write('os.name：', os.name) #OS名称：Windows->'nt', Linux->'posix'
# st.write('os.getlogin():', os.getlogin())#エラーが出る
st.write('os.cpu_count() :', os.cpu_count()) #CPU数を取得
st.write('親ディレクトリ：',os.path.dirname(os.getcwd()))
st.write('親ディレクトリ内の全ファイル',glob.glob(os.path.dirname(os.getcwd())+'/*'))