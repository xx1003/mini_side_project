import recommend

if __name__ == "__main__":
    while True:

        r = recommend.Recommend()
        
        print("메뉴 선택\n")

        print("1. 카드 순위 보기")
        print("2. 원하는 카드 찾기")
        print("3. 소비패턴에 맞는 카드 찾기")
        print("q : 종료")
        menu = input(": ")

        if menu == '1':
            r.show_cards()
        elif menu == '2':
            pass
        elif menu == '3':
            pass
        elif menu == 'q':
            "프로그램을 종료합니다."
            break