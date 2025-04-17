import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import json

credit_df = pd.read_excel("data/credit_data_final.xlsx")
check_df = pd.read_excel("data/check_data_final.xlsx")

bene_list = ['카페 브랜드', '편의점 브랜드', '쇼핑 브랜드', '배달앱 브랜드', '문화생활 브랜드', '디지털구독 브랜드']

for col in bene_list:
    credit_df[col] = credit_df[col].apply(json.loads)
    check_df[col] = check_df[col].apply(json.loads)

def set_kor_font():
    plt.rcParams['font.family'] = 'Malgun Gothic' 
    plt.rcParams['axes.unicode_minus'] = False 
    sns.set(font='Malgun Gothic', 
            rc={'axes.unicode_minus' : False}, 
            style='darkgrid')


if __name__=='__main__':
    # print(type(credit_df.loc[0,'순위']))
    print("- 사용자의 주사용 카드 입력 -")
    credit_or_check = input("1.신용카드    2.체크카드 : ")
    
    if credit_or_check == '1':
        temp_credit_df = credit_df.copy()

        ####################################
        # 카드 순위 정보 출력 기능
        print("<< 신용카드 top 99위 >>")
        for rank, name in zip(temp_credit_df['순위'], temp_credit_df['카드 이름']):
            print(f"{rank:>5}위 : {name}")
        ####################################

        # ####################################
        # 주사용 카드 입력받는 기능
        user_card_rank = int(input("주로 사용하는 카드 입력: "))
        user_card_info = temp_credit_df.loc[temp_credit_df['순위'] == user_card_rank, :]
        user_card_name = user_card_info['카드 이름'].values[0]
        user_card_company = user_card_info['카드사'].values[0]
        user_card_margin = user_card_info['실적'].values[0]
        user_card_fee = user_card_info['연회비'].values[0]

        print(f"사용자님의 카드 : {user_card_name}")
        print()
        # ####################################

        ####################################
        # 사용자 소비패턴 입력받는 기능
        print("- 사용자님의 주사용 카드 소비패턴 입력 -")

        total_amount = int(input("해당 카드의 월 평균 소비금액을 알려주세요: "))
        
        
        # 자주 사용하는 소비 항목 입력받는 기능
        part_dict = {
            '1':['가맹점', '최대 가맹점 혜택'], '2':['교통', '최대 교통 혜택'], '3':['쇼핑', '최대 쇼핑 혜택', '쇼핑 브랜드'],
            '4':['카페', '최대 카페 혜택', '카페 브랜드'], '5':['편의점', '최대 편의점 혜택', '편의점 브랜드'], '6':['이동통신', '최대 이동통신 혜택'],
            '7':['의료 (병원/약국)', '최대 의료 혜택'], '8':['디지털구독 (OTT/스트리밍)', '최대 디지털구독 혜택', '디지털구독 브랜드'], 
            '9':['배달앱/간편결제', '최대 배달앱/간편결제 혜택', '배달앱 브랜드'], '10':['외식', '최대 외식 혜택'], 
            '11':['차량 서비스', '최대 차량 혜택'], '12':['항공', '항공 혜택 개수'], 
            '13':['문화생활 (영화/테마파크)','최대 문화생활 혜택', '문화생활 브랜드']
        }

        for i in range(1, len(part_dict)+1):
            print(f"{i}. {part_dict[str(i)][0]}")

        temp_parts = input("자주 사용하는 소비 항목 세가지를 골라주세요.(space 구분): ").split(sep=" ")
        
        parts = []

        # 띄어쓰기 때문에 공백 들어가는 거 방지
        for part in temp_parts:            
            if part:
                parts.append(part)

        # 소비 항목별 이용금액 입력받는 기능
        print("\n자주 사용하는 소비 항목의 대략적인 금액을 작성해주세요.")
        print(f"사용자의 월 평균 소비 금액 : {total_amount}원")
        consume_amount = {}
        for idx, part in enumerate(parts):
            consume_amount[part] = int(input(f"{idx+1}. {part_dict[part][0]}: "))
        
        sorted_consume_amount = sorted(consume_amount.items(), key= lambda item:item[1], reverse=True)
        
        # parts 많이 쓰는 순서대로 정렬
        parts = [x[0] for x in sorted_consume_amount]

        # 선택한 소비영역에서 자주 사용하는 브랜드 입력받는 기능
        brand_dict = {
            '3':["현대백화점", "롯데백화점", "신세계백화점",\
                 "롯데마트", "이마트",\
                 "쿠팡", "11번가", "G마켓", "옥션", "무신사"],
            '4':["스타벅스", "투썸", "이디야", "메가커피", "컴포즈"],
            '5':["CU", "GS25", "세븐일레븐"], 
            '8':["넷플릭스", "티빙", "쿠팡플레이", "쿠팡 플레이", "웨이브", "유튜브"], 
            '9':["배달의민족", "배달의 민족", "배민", "요기요", "쿠팡이츠", "쿠팡 이츠"], 
            '13':["CGV", "메가박스", "롯데시네마", "에버랜드", "롯데월드"]
        }

        print("\n영역별 자주 사용하는 브랜드를 골라주세요.")

        # 소비영역별 자주 쓰는 브랜드 담을 딕셔너리
        user_brands = {}
        
        # 브랜드 없는 것들 제외
        for part in parts:
            brands = brand_dict[part]
            print(f"< {part_dict[part][0]} 영역 브랜드 >")
            for i, brand in enumerate(brands):
                print(f"{i+1}. {brand}", end=" ")
            print()
            temp_part_brands = input(": ").split(" ")

            # 띄어쓰기 때문에 공백 들어가는 거 방지
            part_brands = []
            for p in temp_part_brands:            
                if p:
                    part_brands.append(p)
            # print(part_brands)

            # 브랜드 이름 담을 리스트
            temp_brand_names = []
            
            if len(part_brands)== 0 or not part_brands[0]:   # 브랜드를 선택하지 않은 경우
                continue

            for part_brand in part_brands:  # index 자료형 str -> int 변경 필요
                if not part_brand:
                    continue
                temp_brand_names.append(brand_dict[part][int(part_brand) - 1])  # -1 하는 이유 : 인덱스에 적용하기 위해서
            
            user_brands[part] = temp_brand_names

        print()

        for k, v in user_brands.items():
            print(f"{part_dict[k][0]} 영역 브랜드 : ", end='')
            for brand in v:
                print(brand, end=" ")
            print()

        ######################################################



        ######################################################
        # 현재카드 분석하는 기능
        print("- 사용자님의 카드 사용 분석 -")
        
        # 실적 / 월 평균 소비금액
        print(f"카드사 : {user_card_company}")
        print(f"카드 : {user_card_name}")
        print("----------------------------------------")

        set_kor_font()
        st.subheader('카드 요약')

        ################################
        # 소비내역 원그래프로 나타내기 
        ratio = [x/total_amount*100 for x in consume_amount.values()]
        # 기타 비율 추가
        etc = (total_amount-sum(consume_amount.values()))/total_amount
        if etc != 0:
            ratio.append(etc*100)
        labels = [part_dict[x][0] for x in consume_amount.keys()]
        labels.append('기타')
        wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
        colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']

        fig, ax= plt.subplots(figsize=(3,3))
        ax.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, wedgeprops=wedgeprops, colors=colors, textprops={'fontsize':8})
        # plt.title()
        st.pyplot(fig)
        ####################################

        print()
        print(f"실적 {total_amount}원 / {user_card_margin}원")
        print(f"연회비 {user_card_fee}원")
        
        user_card_benefits = {}
        for k, v in part_dict.items():
            user_card_benefits[v[0]] = float(user_card_info[v[1]].values[0])
        sorted_benefits = sorted(user_card_benefits.items(), key= lambda item:item[1], reverse=True)

        for i in range(3):
            print(f"{i+1}. {sorted_benefits[i][0]}", end='  ')







        ######################################################



        #######################################################
        # 추천카드 선정하는 기능 
        temp_credit_df['브랜드 카드 점수'] = 0
        temp_credit_df['혜택률 카드 점수'] = 0

        # step 1. 카드 혜택에 사용자가 선택한 브랜드가 포함되어 있는지 필터링
        brand_include_cards = {}   # 사용자가 선택한 브랜드 혜택을 포함하는 카드 이름 저장

        for user_brand in user_brands.keys():                           # 소비영역별로 for 루프 돌기
            consume_part_num = user_brand                               # 소비영역 번호 (자료형:str)
            consume_part_str = part_dict[consume_part_num][0]           # 소비영역명 (자료형:str)
            bene_percent = part_dict[consume_part_num][1]               # 소비영역 최대 혜택률 (자료형:float)
            consume_part_brand_col = part_dict[consume_part_num][2]     # 소비영역 브랜드 컬럼명 (ex: '카페 브랜드')
            user_choose_brands = user_brands[consume_part_num]          # 사용자가 선택한 브랜드들 (자료형:list)

            # print(f"\n- 사용자가 {consume_part_str} 영역에서 선택한 브랜드 혜택을 포함하는 카드 -")

            # 1차 필터링 : 소비영역 포함 카드
            part_include_cards = temp_credit_df.loc[temp_credit_df[bene_percent]!=0, :]   
            part_include_cards.reset_index(drop=True, inplace=True)

            temp_card_names = []
           
            # 2차 필터링 : 사용자가 고른 브랜드를 포함하는 카드, 브랜드를 많이 포함할수록 점수 ++
            for ucb in user_choose_brands:                                      
                for idx in range(len(part_include_cards)):
                    if ucb in part_include_cards.loc[idx, consume_part_brand_col]:
                        temp_card_names.append(part_include_cards.loc[idx, '카드 이름'])
                        temp_credit_df.loc[idx, '브랜드 카드 점수'] += 1
            temp_card_names = list(set(temp_card_names))

            print()

            brand_include_cards[consume_part_num] = temp_card_names
            print(f"\n- 사용자가 {consume_part_str} 영역에서 선택한 브랜드 혜택을 포함하는 카드 -")
            print(temp_card_names, "\n")
        

        ####################################
        # 가중치 사용한 점수 기반 추천시스템 계산하는 기능
        weights = [50, 30, 20]   # 임시 가중치       
        
        score_dict = {}

        for i in range(len(credit_df)):
            temp_score = 0
            for part, weight in zip(parts, weights):
                part_col = part_dict[part][1]
                # print(credit_df.loc[i, part_col])
                temp_score += temp_credit_df.loc[i, part_col] * weight
            temp_credit_df.loc[i, '혜택률 카드 점수'] = float(temp_score)

        temp_credit_df['총합 카드 점수'] = temp_credit_df['브랜드 카드 점수'] + temp_credit_df['혜택률 카드 점수']
        
        
        temp_credit_df.sort_values('총합 카드 점수', ascending=False, inplace=True)
        temp_credit_df = temp_credit_df.reset_index(drop=True)
        print(temp_credit_df.loc[:,['카드 이름', '브랜드 카드 점수', '혜택률 카드 점수', '총합 카드 점수']])
        #################################
        
        ##################################
        # 주사용 카드 분석 + 상위 3개 카드 추천
        check = False
        recommend_cards = []
        card_rank = 0       

        while len(recommend_cards) < 3:
            if str(temp_credit_df.iloc[card_rank]['카드 이름']) == user_card_name:
                check = True
            else:
                recommend_cards.append(temp_credit_df.loc[card_rank, '카드 이름'])
            card_rank += 1
        
        if not check:
            print()
            print("현재 사용하는 카드는 사용자의 소비패턴에 맞지 않아요!")
            print()
            print(f"- 사용자의 카드 <<{user_card_name}>> 가 제공하는 혜택 top 3 -")

            for i in range(3):
                print(f"{i+1}. {sorted_benefits[i][0]}", end='  ')

            print()
            print(f"- 사용자의 주 소비 영역 top 3 -")
            part_rank = 1
            for part in parts:
                print(f"{part_rank}. {part_dict[part][0]}", end='   ')
                part_rank += 1
            print()
        else:
            print("좋은 카드 선택!\n")
            print("비슷한 카드를 추천드릴게요")

        print("\n- 사용자 추천 카드 top3 -")
        idx = 1
        for c in recommend_cards:
            print(f"{idx}. {c}")
            idx += 1
