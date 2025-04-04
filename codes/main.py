import pandas as pd
import streamlit as st

credit_df = pd.read_excel("data/credit_card_data.xlsx")
check_df = pd.read_excel("data/check_card_data.xlsx")
# st.subheader("데이터 미리보기")
# st.dataframe(credit_df)

if __name__=='__main__':
    # print(type(credit_df.loc[0,'순위']))
    print("- 사용자의 주사용 카드 입력 -")
    credit_or_check = input("1.신용카드    2.체크카드 : ")
    
    if credit_or_check == '1':
        
        # # 카드 순위 정보 출력 기능
        # print("<< 신용카드 top 99위 >>")
        # for rank, name in zip(credit_df['순위'], credit_df['카드 이름']):
        #     print(f"{rank:>5}위 : {name}")
        # #

        # # 주사용 카드 입력받는 기능
        # card_rank = int(input("주로 사용하는 카드 입력: "))

        # print("사용자님의 카드 : ", end='')
        # print(credit_df.loc[credit_df['순위'] == card_rank, '카드 이름'].values[0])
        # #


        # 사용자 소비패턴 입력받는 기능
        print("- 사용자의 소비패턴 입력 -")

        part_dict = {
            '1':'최대 가맹점 혜택', '2':'최대 교통 혜택', '3':'최대 쇼핑 혜택',
            '4':'최대 카페 혜택', '5':'최대 편의점 혜택', '6':'최대 이동통신 혜택',
            '7':'최대 의료 혜택', '8':'최대 디지털구독 혜택', '9':'최대 배달앱/간편결제 혜택',
            '10':'최대 외식 혜택', '11':'최대 차량 혜택', '12':'항공 혜택 개수',
            '13':'최대 문화생활 혜택' 
        }

        print("""
        1. 가맹점
        2. 교통
        3. 쇼핑
        4. 카페
        5. 편의점
        6. 이동통신
        7. 의료 (병원/약국)
        8. 디지털구독 (OTT/스트리밍)
        9. 배달앱/간편결제
        10. 외식
        11. 차량
        12. 항공 서비스
        13. 문화생활 (영화/테마파크)
        """)
        parts = input("가장 많이 소비하는 영역을 소비가 많은 순서대로 3가지 골라주세요(space 구분): ").split(sep=" ")
        print(parts)
        #
        
        # 가중치 사용한 점수 기반 추천시스템 계산하는 기능
        weights = [0.5, 0.3, 0.2]   # 임시 가중치
        
        
        score_tuple_list = []

        for i in range(len(credit_df)):
            temp_score = 0
            for part, weight in zip(parts, weights):
                part_col = part_dict[part]
                print(credit_df.loc[i, part_col])
                temp_score += credit_df.loc[i, part_col] * weight
            score_tuple_list.append((credit_df.loc[i, '카드 이름'], temp_score))

        print(score_tuple_list)
        
        # 이게 제대로 안나옴 수정 필요!!!!!!
        # print(score_tuple_list.sort(key=lambda x: x[1], reverse=True))
        

        
