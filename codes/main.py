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
        
        # ####################################
        # # 카드 순위 정보 출력 기능
        # print("<< 신용카드 top 99위 >>")
        # for rank, name in zip(credit_df['순위'], credit_df['카드 이름']):
        #     print(f"{rank:>5}위 : {name}")
        # ####################################

        # ####################################
        # 주사용 카드 입력받는 기능
        user_card_rank = int(input("주로 사용하는 카드 입력: "))
        user_card_info = credit_df.loc[credit_df['순위'] == user_card_rank, :]
        user_card_name = user_card_info['카드 이름'].values[0]
        print(f"사용자님의 카드 : {user_card_name}")
        print()
        # ####################################

        ####################################
        # 사용자 소비패턴 입력받는 기능
        print("- 사용자의 소비패턴 입력 -")

        part_dict = {
            '1':['가맹점', '최대 가맹점 혜택'], '2':['교통', '최대 교통 혜택'], '3':['쇼핑', '최대 쇼핑 혜택'],
            '4':['카페', '최대 카페 혜택'], '5':['편의점', '최대 편의점 혜택'], '6':['이동통신', '최대 이동통신 혜택'],
            '7':['의료 (병원/약국)', '최대 의료 혜택'], '8':['디지털구독 (OTT/스트리밍)', '최대 디지털구독 혜택'], 
            '9':['배달앱/간편결제', '최대 배달앱/간편결제 혜택'], '10':['외식', '최대 외식 혜택'], 
            '11':['차량 서비스', '최대 차량 혜택'], '12':['항공', '항공 혜택 개수'], 
            '13':['문화생활 (영화/테마파크)','최대 문화생활 혜택']
        }

        for i in range(1, len(part_dict)+1):
            print(f"{i+1}. {part_dict[str(i)][0]}")

        parts = input("가장 많이 소비하는 영역을 소비가 많은 순서대로 3가지 골라주세요(space 구분): ").split(sep=" ")
        # print(parts)
        ####################################

        ####################################
        # 가중치 사용한 점수 기반 추천시스템 계산하는 기능
        weights = [0.5, 0.3, 0.2]   # 임시 가중치       
        
        score_dict = {}

        for i in range(len(credit_df)):
            temp_score = 0
            for part, weight in zip(parts, weights):
                part_col = part_dict[part][1]
                # print(credit_df.loc[i, part_col])
                temp_score += credit_df.loc[i, part_col] * weight
            score_dict[credit_df.loc[i, '카드 이름']] = float(temp_score)

        # print(score_dict)

        sorted_dict = sorted(score_dict.items(), key= lambda item:item[1], reverse=True)
        # print(sorted_dict)
        #################################
        
        ##################################
        # 주사용 카드 분석 + 상위 3개 카드 추천
        check = False
        recommend_cards = []
        card_rank = 0
        while len(recommend_cards) < 3:
            if sorted_dict[card_rank][0] == user_card_info['카드 이름'].values[0]:
                check = True
                continue

            recommend_cards.append(sorted_dict[card_rank][0])
            card_rank += 1
            # print(f"사용자에게 맞는 {i+1}위 카드 : {sorted_dict[i][0]}")
        
        if not check:
            print("현재 사용하는 카드는 사용자의 소비패턴에 맞지 않아요!")
            print()
            print(f"- 사용자의 카드 <<{user_card_name}>> 가 제공하는 혜택 top 3 -")
            
            user_card_benefits = {}
            for k, v in part_dict.items():
                user_card_benefits[v[0]] = float(user_card_info[v[1]].values[0])
            sorted_benefits = sorted(user_card_benefits.items(), key= lambda item:item[1], reverse=True)

            for i in range(3):
                print(f"{i+1}. {sorted_benefits[i][0]}", end='  ')

            print()
            print(f"- 사용자의 주 소비 영역 top 3 -")
            part_rank = 1
            for part in parts:
                print(f"{part_rank}. {part_dict[part][0]}", end='   ')
                part_rank += 1

        print()
        print("\n- 사용자 추천 카드 top3 -")
        idx = 1
        for c in recommend_cards:
            print(f"{idx}. {c}")
            idx += 1
            # 추천 카드 혜택 나열 기능 추가해야 함
        ##################################
        
        

        
