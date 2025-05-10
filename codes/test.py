import pandas as pd

if __name__ == "__main__":
    # temp = input(": ").split(" ")
    

    # print(temp)
    # print(len(temp))


    dict1 = {
        'num' : [1,2,3,4,5,6,7,8],
        'num2': [2,2,2,2,0,0,0,0]
    }

    print(list(dict1.keys()))

    df = pd.DataFrame(dict1)
    
    # print(df['num2'].drop_duplicates())
    # df['num3'] = df['num'] + df['num']
    # print(df)

    # print(df.iloc[4]['num'])

    s = "     diidididi       "
    print(s.lstrip())
    

    
    