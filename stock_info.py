
import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib
import matplotlib.pyplot as plt 
import yfinance as yf

from io import BytesIO
import plotly.graph_objects as go
import pandas as pd
import requests

# caching
# 인자가 바뀌지 않는 함수 실행 결과를 저장 후 크롬의 임시 저장 폴더에 저장 후 재사용
@st.cache_data
# def get_stock_info():
#     base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
#     method = "download"
#     url = "{0}?method={1}".format(base_url, method)   
#     df = pd.read_html(url, header=0)[0]
#     df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
#     df = df[['회사명','종목코드']]
#     return df

# def get_ticker_symbol(company_name):     
#     df = get_stock_info()
#     code = df[df['회사명']==company_name]['종목코드'].values    
#     ticker_symbol = code[0]
#     return ticker_symbol
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    # url = "{0}?method={1}".format(base_url, method)
    url = f"{base_url}?method={method}"
    response = requests.get(url)
    response.encoding = 'euc-kr'  # 또는 'cp949'
    df = pd.read_html(response.text, header=0)[0]
    # df = pd.read_html(url, header=0)[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")
    df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    ticker_symbol = code[0]
    return ticker_symbol

with st.sidebar:
    st.title('회사 이름과 기간을 입력하세요')
    stock_name = st.text_input('회사이름', '삼성전자')

    date_range = st.date_input(
        "시작일 - 종료일", (datetime.date(2019,1,1), (datetime.date(2022,12,31)))
    )
    search_btn = st.button('주가 데이터 확인')
    
st.title('무슨 주식을 사야 부자가 되려나..')


    
# def main():
#     st.title("무슨 주식을 사야 부자가 되려나...")
#     st.sidebar.title("회사 이름과 기간을 입력하세요")
#     ticker = st.sidebar.text_input("회사 이름", value = "삼성전자")
#     date_range = st.sidebar.date_input("시작일 - 종료일", datetime.date(2019,1,1), (datetime.date(2022,12,31)))

# 	# #ticker 종목의 시작~종료 날짜 사이의 가격변화를 데이터로 보여줌
#     # data = yf.download(ticker, start= start_date, end= end_date)
#     #st.dataframe(date_range)
    
    


# #코드조각
# ticker_symbol = get_ticker_symbol(stock_name)     
# start_p = date_range[0]               
# end_p = date_range[1] + datetime.timedelta(days=1) 
# df = fdr.DataReader(f'KRX:{ticker_symbol}', start_p, end_p)
# df.index = df.index.date
# st.subheader(f"[{stock_name}] 주가 데이터")
# st.dataframe(df.tail(7))

# excel_data = BytesIO()      
# df.to_excel(excel_data)

# st.download_button("엑셀 파일 다운로드", 
#         excel_data, file_name='stock_data.xlsx')

if search_btn:
    # 코드 조각 추가
    ticker_symbol = get_ticker_symbol(stock_name)

    start_p = date_range[0]
    end_p = date_range[1] + datetime.timedelta(days=1)

    stock_df = yf.download(ticker_symbol + '.KS',
                        start=start_p,
                        end=end_p,
                        progress=False).reset_index()
    # 그래프
    fig = go.Figure(data=[go.Candlestick(x=stock_df['Date'],
                                        open = stock_df['Open'],
                                        high = stock_df['High'],
                                        low = stock_df['Low'],
                                        close = stock_df['Close'])])


    st.subheader(f"[{stock_name}] 주가 데이터")
    st.dataframe(stock_df.tail(7))
    st.write(fig)
    excel_data = BytesIO()
    stock_df.to_excel(excel_data)
    st.download_button("엑셀 파일 다운로드",
                            excel_data, file_name='stock_data.xlsx') 
