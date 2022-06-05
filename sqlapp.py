import streamlit as st 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.orm import Session #データ型取得
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey #SQLテーブルのカラム設定用
from sqlalchemy import desc #降順ソート

import pandas as pd

DB_file = 'testDB.db'
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

name = st.text_input('名前を入力してください')
if st.button('名前を登録'):
    if name != '':
        user = User(name)
        Session.add(user)
        Session.commit()
    else:
        st.write('名前を入力してください。')

st.markdown('***')   
if st.button('名前一覧を表示'):
    df = pd.read_sql('select * from users', engine)
    st.dataframe(df)
    