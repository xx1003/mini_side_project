import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import json

class Recommend:
    def __init__(self):
        self.credit_df = pd.read_excel("data/credit_data_final.xlsx")
        self.check_df = pd.read_excel("data/check_data_final.xlsx")

        self.bene_list = ['카페 브랜드', '편의점 브랜드', '쇼핑 브랜드', '배달앱 브랜드', '문화생활 브랜드', '디지털구독 브랜드']
        
        for col in self.bene_list:
            self.credit_df[col] = self.credit_df[col].apply(json.loads)
            self.check_df[col] = self.check_df[col].apply(json.loads)

        self.temp_credit_df = self.credit_df.copy()
        self.temp_check_df = self.check_df.copy()

        # 신용카드, 체크카드 카드사
        self.credit_card_company = self.temp_credit_df['카드사'].drop_duplicates().values
        self.check_card_company = self.temp_check_df['카드사'].drop_duplicates().values

        # 사용자 주사용 카드 정보
        self.user_card_info = None


    def custom_cards(self):
        pass
    
    def get_card(self, credit_or_check, df, card_company):
        print("\n카드사 선택")
        for idx, company in enumerate(card_company):
            print(f"{idx+1}. {company}")

        card_company_name = card_company[int(input(": "))- 1]
        
        if credit_or_check == 1:
            print(f"\n{card_company_name}의 신용카드")
        elif credit_or_check == 2:
            print(f"\n{card_company_name}의 체크카드")

        card_names = df.loc[df['카드사'] == card_company_name, '카드 이름'].values
        for idx, card_name in enumerate(card_names):
            print(f"{idx+1}. {card_name}")
        
        user_card_idx = int(input("\n카드 선택: ")) - 1
        self.user_card_info = df.loc[df['카드 이름'] == card_names[user_card_idx], :]
        
        print(f"선택한 카드 : {self.user_card_info['카드 이름'].values[0]}")

    def get_user_card(self):
        print("분석하고 싶은 카드 정보를 입력해주세요.\n")

        print("카드 종류 선택")
        print("1. 신용카드     2. 체크카드")
        card_sort = input(": ")

        if card_sort == '1':
            self.get_card(card_sort, self.temp_credit_df, self.credit_card_company)            
        elif card_sort == '2':
            self.get_card(card_sort, self.temp_check_df, self.check_card_company) 
         

    def recommend_cards(self):

        pass

    def show_cards(self):
        print("조회할 카드 종류")
        print("1. 신용카드     2. 체크카드")
        card_sort = input(": ")
        
        # 신용카드 순위 출력
        if card_sort == '1':
            print("<< 신용카드 top 99위 >>")
            for rank, name in zip(self.temp_credit_df['순위'], self.temp_credit_df['카드 이름']):
                print(f"{rank:>5}위 : {name}")

        # 체크카드 순위 출력 
        elif card_sort == '2':
            print("<< 체크카드 top 99위 >>")
            for rank, name in zip(self.temp_check_df['순위'], self.temp_check_df['카드 이름']):
                print(f"{rank:>5}위 : {name}")

        print()

    def start():
        pass

    

if __name__ == "__main__":
    r = Recommend()

    r.get_user_card()