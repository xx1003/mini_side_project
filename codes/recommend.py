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
        
        # 카드 혜택 목록
        self.part_dict = {
            '1':['가맹점', '최대 가맹점 혜택'], '2':['교통', '최대 교통 혜택'], '3':['쇼핑', '최대 쇼핑 혜택', '쇼핑 브랜드'],
            '4':['카페', '최대 카페 혜택', '카페 브랜드'], '5':['편의점', '최대 편의점 혜택', '편의점 브랜드'], '6':['이동통신', '최대 이동통신 혜택'],
            '7':['의료 (병원/약국)', '최대 의료 혜택'], '8':['디지털구독 (OTT/스트리밍)', '최대 디지털구독 혜택', '디지털구독 브랜드'], 
            '9':['배달앱/간편결제', '최대 배달앱/간편결제 혜택', '배달앱 브랜드'], '10':['외식', '최대 외식 혜택'], 
            '11':['차량 서비스', '최대 차량 혜택'], '12':['항공', '항공 혜택 개수'], 
            '13':['문화생활 (영화/테마파크)','최대 문화생활 혜택', '문화생활 브랜드']
        }
        
        # 월 평균 소비
        self.total_amount = 0

        # 3개 주요 소비영역 소비 순서대로 key값 저장
        self.parts = None

        # 3개 주요 소비영역 : 월 평균 구매액 (정렬X)
        self.consume_amount = None
        # 3개 주요 소비영역 소비 순서대로 튜플 리스트
        self.sorted_consume_amount = None

        # 혜택 브랜드 목록
        self.brand_dict = {
            '3':["현대백화점", "롯데백화점", "신세계백화점",\
                 "롯데마트", "이마트",\
                 "쿠팡", "11번가", "G마켓", "옥션", "무신사"],
            '4':["스타벅스", "투썸", "이디야", "메가커피", "컴포즈"],
            '5':["CU", "GS25", "세븐일레븐"], 
            '8':["넷플릭스", "티빙", "쿠팡플레이", "쿠팡 플레이", "웨이브", "유튜브"], 
            '9':["배달의민족", "배달의 민족", "배민", "요기요", "쿠팡이츠", "쿠팡 이츠"], 
            '13':["CGV", "메가박스", "롯데시네마", "에버랜드", "롯데월드"]
        }

        # 주로 사용하는 브랜드 딕셔너리
        self.user_brands = None

        # 주사용 카드 혜택 top3
        self.sorted_benefits = None
    
    # streamlit 한글 폰트 적용
    def set_kor_font():
        plt.rcParams['font.family'] = 'Malgun Gothic' 
        plt.rcParams['axes.unicode_minus'] = False 
        sns.set(font='Malgun Gothic', 
                rc={'axes.unicode_minus' : False}, 
                style='darkgrid')
    
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

    def print_parts(self):
        for i in range(1, len(self.part_dict)+1):
            print(f"{i}. {self.part_dict[str(i)][0]}")

    def get_user_brands(self):
        # 소비영역별 자주 쓰는 브랜드 담을 딕셔너리
        user_brands = {}
        
        # 브랜드 있는 소비영역에서 사용자가 주로 사용하는 브랜드 입력받기
        for k, v in self.brand_dict.items():
            brands = v  # v
            print(f"< {self.part_dict[k][0]} 영역 브랜드 >")
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
                temp_brand_names.append(self.brand_dict[k][int(part_brand) - 1])  # -1 하는 이유 : 인덱스에 적용하기 위해서
            
            user_brands[k] = temp_brand_names
        return user_brands

    def get_user_consume_info(self):
        # 월 평균 소비금액 입력
        self.total_amount = int(input("해당 카드의 월 평균 소비금액을 알려주세요: "))

        # 자주 사용하는 소비 항목 입력받는 기능
        self.print_parts()
        
        temp_parts = input("자주 사용하는 소비 항목 세가지를 골라주세요.(space 구분): ").split(sep=" ")
        
        parts = []  # 사용자 주소비영역 딕셔너리 키 (part_dict의 키)

        # 띄어쓰기 때문에 공백 들어가는 거 방지
        for part in temp_parts:            
            if part:
                parts.append(part)

        # 소비 항목별 이용금액 입력받는 기능
        print("\n자주 사용하는 소비 항목의 대략적인 금액을 작성해주세요.")
        print(f"사용자의 월 평균 소비 금액 : {self.total_amount}원")
        consume_amount = {}
        for idx, part in enumerate(parts):
            consume_amount[part] = int(input(f"{idx+1}. {self.part_dict[part][0]}: "))
        
        self.consume_amount = consume_amount
        
        sorted_consume_amount = sorted(consume_amount.items(), key= lambda item:item[1], reverse=True)
        
        # parts 많이 쓰는 순서대로 정렬
        self.parts = [x[0] for x in sorted_consume_amount]
        self.sorted_consume_amount = sorted_consume_amount
        
        # 디버깅용
        print(self.sorted_consume_amount)
        print()

        # 브랜드 입력받는 기능
        print("\n영역별 자주 사용하는 브랜드를 골라주세요.")
        self.user_brands = self.get_user_brands()
        
        # 디버깅용
        # print(self.user_brands)
        print()

        # 사용자가 선택한 브랜드 출력
        for k, v in self.user_brands.items():
            print(f"{self.part_dict[k][0]} 영역 브랜드 : ", end='')
            for brand in v:
                print(brand, end=" ")
            print()
        
    def analy_card(self):
        plt.rcParams['font.family'] = 'Malgun Gothic' 
        plt.rcParams['axes.unicode_minus'] = False 
        sns.set(font='Malgun Gothic', 
                rc={'axes.unicode_minus' : False}, 
                style='darkgrid')
        # self.set_kor_font()
        st.subheader('카드 요약')

        ################################
        # 소비내역 원그래프로 나타내기 
        ratio = [x[1]/self.total_amount*100 for x in self.sorted_consume_amount]

        # # 디버깅
        # print(self.parts)
        # print(self.sorted_consume_amount)
        
        # 기타 비율 추가
        etc = (self.total_amount-sum(self.consume_amount.values()))/self.total_amount
        if etc != 0:
            ratio.append(etc*100)
        print(ratio)

        labels = [self.part_dict[x[0]][0] for x in self.sorted_consume_amount]
        labels.append('기타')
        wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
        colors = ['#1E88E5', '#90CAF9', '#BBDEFB', '#EEEEEE']

        fig, ax= plt.subplots(figsize=(5,3))

        wedges, _ = ax.pie(ratio,
                           colors=colors,
                           startangle=90,
                           counterclock=False,
                           wedgeprops=dict(width=0.5))
        
        # 중앙 텍스트
        ax.text(-0.05, 0.05, '월 평균', ha='center', va='center', fontsize=12)
        ax.text(-0.05, -0.1, '소비', ha='center', va='center', fontsize=12)
        
        # 오른쪽 범례 스타일 텍스트
        for i, (label, value) in enumerate(zip(labels, ratio)):
            y = 0.25 - i * 0.2
            ax.text(1.1, y, '●', fontsize=12, color=colors[i], va='center')
            ax.text(1.25, y, f'{label}   {value:.1f}%', fontsize=10, va='center')
        
        ax.axis('equal')
        plt.box(False)

        st.pyplot(fig)
        ####################################

        ####################################
        # 카드 기본정보 출력
        print()
        user_card_margin = self.user_card_info['실적'].values[0]
        try:
            user_card_fee = self.user_card_info['연회비'].values[0]
        except:
            user_card_fee = 0

        st.text(f"실적 {self.total_amount}원 / {user_card_margin * 10000}원")
        print(f"실적 {self.total_amount}원 / {user_card_margin * 10000}원")
        st.text(f"연회비 {user_card_fee}원")
        print(f"연회비 {user_card_fee}원")
        
        user_card_benefits = {}
        for k, v in self.part_dict.items():
            user_card_benefits[v[0]] = self.user_card_info[v[1]].values[0]
        sorted_benefits = sorted(user_card_benefits.items(), key= lambda item:item[1], reverse=True)
        self.sorted_benefits = sorted_benefits

        st.text("나의 주요 소비")
        for part in self.parts:
            st.text(self.part_dict[part][0])

        st.text("카드의 주요 혜택")
        # 주사용카드가 제공하는 혜택
        temp_sorted_benefits = [x[0] for x in self.sorted_benefits if x[1] != 0.0]
        print(temp_sorted_benefits)
        if len(temp_sorted_benefits) < 3:
            for bene in temp_sorted_benefits:
                print(bene)
                st.text(bene)
        else:
            for i in range(3):
                print(f"{temp_sorted_benefits[i]}", end='  ')
                st.text(f"{temp_sorted_benefits[i]}")
        #######################################
        
        ######################################
        st.subheader('소비 분석')
    
        # 월평균 소비금액 - 주소비영역 소비금액
        lost_bene_amount = self.total_amount

        temp_dict = {
            '소비 금액':[],
            '받는 혜택':[]
        }
        for part, amount in self.sorted_consume_amount:
            temp_dict['받는 혜택'].append(int(amount * self.user_card_info[self.part_dict[part][1]].values[0]))
            temp_dict['소비 금액'].append(int(amount))
            lost_bene_amount -= amount
            
        print([self.part_dict[x][0] for x in self.parts])
        consume_df = pd.DataFrame(temp_dict, index=[self.part_dict[x][0] for x in self.parts])
        st.table(consume_df)
        #########################################
        
        
        #########################################
        st.subheader('혜택 누락')

        # (월평균 소비금액 - 주소비영역 3개 소비금액) / 주소비영역 제외 나머지 영역 개수(13-3=10) = 나머지 영역의 평균 소비금액
        # 나머지 영역의 평균 소비금액 중 해당영역의 혜택률이 0인 부분 소비금액 합 = 누락 혜택 금액
        # 만약 주소비영역의 혜택률이 0이면 실제 소비금액을 누락 혜택 금액에 더함
        total_lost_amount = 0.0

        mean_rest_amount = lost_bene_amount / 10
            
        for k, v in self.part_dict.items():
            if self.user_card_info[v[1]].values[0] == 0.0:
                if k in self.parts:
                    total_lost_amount += self.consume_amount[k]
                else:
                    total_lost_amount += mean_rest_amount
            
        print(f"누락 혜택 금액 {int(total_lost_amount)} 원")

        fig2, ax2 = plt.subplots()
        ratio2 = [total_lost_amount/self.total_amount * 100, 100 - (total_lost_amount/self.total_amount * 100)]
            
        colors = ['#FFD54F', '#EEEEEE']
        # ax2.pie(ratio2, labels=labels2, autopct='%.1f%%', startangle=260, counterclock=False)
            
        wedges, _ = ax2.pie(ratio2,
                            colors=colors,
                            startangle=90,
                            counterclock=False,
                            wedgeprops=dict(width=0.5))
        ax2.text(0, 0.05, '월 평균', ha='center', va='center', fontsize=12)
        ax2.text(0, -0.1, '소비', ha='center', va='center', fontsize=12)

        ax2.text(1.2, 0.15, '총 소비 중', fontsize=11)
        ax2.text(1.2, -0.05, f'{ratio2[0]:.1f}%', fontsize=14, color='#1E88E5', weight='bold')
        ax2.text(1.2, -0.25, '는 혜택을 못받고 있어요', fontsize=10)
        
        # 원형 유지 및 불필요한 테두리 제거
        ax2.axis('equal')
        plt.box(False)

        st.pyplot(fig2)
        ######################################################

        #####################################################
        # 인사이트 도출
        not_bene = []
        yes_bene = []
        recommend_bene = []

        # 사용자 주사용 영역 top3 혜택을 현재 사용 카드가 제공하고 있는지
        for bene in [self.part_dict[x][0] for x in self.parts]:
            if bene in temp_sorted_benefits:
                yes_bene.append(bene)
            else:
                not_bene.append(bene)
        # print(self.sorted_benefits)

        # 현재 사용 카드의 혜택 중 사용자 주사용 영역에 들어가지 않는 영역 찾기
        for bene in temp_sorted_benefits:
            if bene not in [self.part_dict[x][0] for x in self.parts]:
                recommend_bene.append(bene)

        st.subheader('인사이트')
        st.text("좋은 점")
        for bene in yes_bene:
            st.text(f"{bene} 영역의 혜택을 잘 받고 있어요!")
        st.text("개선할 점")
        for bene in not_bene:
            st.text(f"이 카드는 {bene} 영역에서 혜택을 제공하고 있지 않아요.")
        st.text(f"이 카드가 제공하는 {recommend_bene} 영역 혜택을 잘 사용하고 있지 않아요.")

    def recommend_calculate(self, df, ratio):
        df['브랜드 카드 점수'] = 0.0
        df['혜택률 카드 점수'] = 0.0

        # step 1. 카드 혜택에 사용자가 선택한 브랜드가 포함되어 있는지 필터링
        brand_include_cards = {}   # 사용자가 선택한 브랜드 혜택을 포함하는 카드 이름 저장
        
        for user_brand in self.user_brands.keys():                           # 소비영역별로 for 루프 돌기
            consume_part_num = user_brand                               # 소비영역 번호 (자료형:str)
            consume_part_str = self.part_dict[consume_part_num][0]           # 소비영역명 (자료형:str)
            bene_percent = self.part_dict[consume_part_num][1]               # 소비영역 최대 혜택률 (자료형:float)
            consume_part_brand_col = self.part_dict[consume_part_num][2]     # 소비영역 브랜드 컬럼명 (ex: '카페 브랜드')
            user_choose_brands = self.user_brands[consume_part_num]          # 사용자가 선택한 브랜드들 (자료형:list)

            # print(f"\n- 사용자가 {consume_part_str} 영역에서 선택한 브랜드 혜택을 포함하는 카드 -")

            # 1차 필터링 : 소비영역 포함 카드
            part_include_cards = df.loc[df[bene_percent]!=0.0, :]   
            part_include_cards.reset_index(drop=True, inplace=True)
            
            temp_card_names = []
            # ratio = [x[1]/self.total_amount*100 for x in self.sorted_consume_amount]
            
            # 2차 필터링 : 사용자가 고른 브랜드를 포함하는 카드, 브랜드를 많이 포함할수록 점수 ++
            for ucb in user_choose_brands:                                      
                for idx in range(len(part_include_cards)):
                    if ucb in part_include_cards.loc[idx, consume_part_brand_col]:
                        temp_card_names.append(part_include_cards.loc[idx, '카드 이름'])
                        if user_brand in self.parts:
                            if user_brand == self.parts[0]:
                                df.loc[idx, '브랜드 카드 점수'] += 1*(ratio[0]/10)
                            elif user_brand == self.parts[1]:
                                df.loc[idx, '브랜드 카드 점수'] += 1*(ratio[1]/10)
                            elif user_brand == self.parts[2]:
                                df.loc[idx, '브랜드 카드 점수'] += 1*(ratio[2]/10)
                        else:
                            df.loc[idx, '브랜드 카드 점수'] += 1
            temp_card_names = list(set(temp_card_names))

            print()

            brand_include_cards[consume_part_num] = temp_card_names
            # print(f"\n- 사용자가 {consume_part_str} 영역에서 선택한 브랜드 혜택을 포함하는 카드 -")
            # print(temp_card_names, "\n")

            weights = ratio   # 월평균 소비액 대비 해당영역 소비액의 비율로 가중치 선정

            for i in range(len(df)):
                temp_score = 0.0
                for part, weight in zip(self.parts, weights):
                    part_col = self.part_dict[part][1]
                    # print(credit_df.loc[i, part_col])
                    temp_score += float(df.loc[i, part_col]) * weight
                df.loc[i, '혜택률 카드 점수'] = temp_score

            df['총합 카드 점수'] = df['브랜드 카드 점수'] + df['혜택률 카드 점수']
            
            
            df.sort_values('총합 카드 점수', ascending=False, inplace=True)
            df = df.reset_index(drop=True)
            # print(df.loc[:,['카드 이름', '브랜드 카드 점수', '혜택률 카드 점수', '총합 카드 점수']])
            #################################
    
    def recommend_print(self, df, credit_or_check):
        ##################################
        # 주사용 카드 분석 + 상위 5개 카드 추천
        check = False
        recommend_cards = []
        card_rank = 0       

        # 주사용 카드 이름
        if self.user_card_info is None:
            user_card_name = "이름 없음"
        else:
            user_card_name = self.user_card_info['카드 이름'].values[0]
        
        while len(recommend_cards) < 5:
            if str(df.iloc[card_rank]['카드 이름']) != user_card_name:
                recommend_cards.append(df.loc[card_rank, '카드 이름'])
            card_rank += 1

        if credit_or_check == 1:    # 신용카드 추천
            print("\n- 신용카드 -")
        elif credit_or_check == 2:    # 체크카드 추천
            print("\n- 체크카드 -")

        # 추천카드 혜택 출력 수정 필요    
        idx = 1
        for c in recommend_cards:
            print(f"{idx}. {c}")
            print(f"혜택: {df.loc[df['카드 이름'] == c, :]}")
            idx += 1

        
    def recommend_cards(self):
        ratio = [x[1]/self.total_amount*100 for x in self.sorted_consume_amount]
        self.recommend_calculate(self.temp_credit_df, ratio)
        self.recommend_calculate(self.temp_check_df, ratio)

        self.recommend_print(self.temp_credit_df, 1)
        self.recommend_print(self.temp_check_df, 2)
        
        # 카드 데이터프레임 초기화
        self.temp_credit_df = self.credit_df.copy()
        self.temp_check_df = self.check_df.copy()


    def get_custom_info(self, df, credit_or_check):
        print("\n원하는 혜택을 우선 순위대로 선택해주세요.")
        for i in range(1, len(self.part_dict)+1):
            print(f"{i}. {self.part_dict[str(i)][0]}")

        temp_parts = input(": ").split(sep=" ")
        parts = []  # 사용자 주소비영역 딕셔너리 키 (part_dict의 키)

        # 띄어쓰기 때문에 공백 들어가는 거 방지
        for part in temp_parts:            
            if part:
                parts.append(part)
        self.parts = parts

        print("\n혜택을 받고 싶은 브랜드를 선택해주세요.")
        self.user_brands = self.get_user_brands()
        
        # 임의의 소비비율 설정
        ratio = [50, 30, 20]

        self.recommend_calculate(df, ratio)

        for part in self.parts:
            print(f"<{self.part_dict[part][0]}> ", end='')
        print()
        for brand in self.user_brands.values():
            print(brand, end=' ')
        print("\n에 맞춘 카드들을 모아봤어요.")
        self.recommend_print(df, credit_or_check)

    def custom_cards(self):
        print("- 원하는 카드 찾기 -")
        print()

        print("원하는 카드 종류를 선택해주세요.")
        print("1. 신용카드     2. 체크카드")
        credit_or_check = int(input(": "))

        if credit_or_check == 1:
            self.get_custom_info(self.temp_credit_df, credit_or_check)
            self.temp_credit_df = self.credit_df.copy()
        elif credit_or_check == 2:
            self.get_custom_info(self.temp_check_df, credit_or_check)
            self.temp_check_df = self.check_df.copy()

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
    # r.get_user_card()
    # r.get_user_consume_info()
    # print(r.user_brands)
    # r.analy_card()
    # r.recommend_cards()
    r.custom_cards()