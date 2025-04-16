import pandas as pd

if __name__ == "__main__":
    # temp = input(": ").split(" ")

    # print(temp)
    # print(len(temp))


    dict1 = {
        'num' : [1,2,3,4,5,6,7,8],
        'num2': [0,0,0,0,0,0,0,0]
    }


    df = pd.DataFrame(dict1)
    df['num3'] = df['num'] + df['num']
    print(df)



    
    