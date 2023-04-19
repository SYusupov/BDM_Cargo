import pandas as pd
import requests
import io



def dhl_raw_data_loader(url):

    username = '997-icu'
    token = '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'

    session = requests.Session()
    session.auth = (username, token)
    

    cursor = session.get(url)
    if cursor.ok == False:
        print("Something went wrong when fetching the file from {}".format(url))
        return 0
    else:
        file = cursor.content
        return file
        




if __name__ == "__main__":
    Domestic_Price_url = "https://raw.githubusercontent.com/SYusupov/BDM_Cargo/main/dhl_service_fee/raw_data/Domestic_Price.txt" 
    Domestic_Zona_url = "https://raw.githubusercontent.com/SYusupov/BDM_Cargo/main/dhl_service_fee/raw_data/Domestic_Zona.csv"
    Zona_Matrix_url = "https://github.com/SYusupov/BDM_Cargo/blob/b069c2da856b9999b3c668e1503eb7f9c8880a6e/dhl_service_fee/raw_data/Zona_Matrix.xlsx"

    DP = dhl_raw_data_loader(Domestic_Price_url)
    DZ = dhl_raw_data_loader(Domestic_Zona_url)
    ZM = dhl_raw_data_loader(Zona_Matrix_url)
    
    DP_df = pd.read_csv(io.StringIO(DP.decode('utf-8')),sep=" ",names = ["Peso(en kg)", "A", "B","C","D"],skiprows=[0])
    DZ_df = pd.read_csv(io.StringIO(DZ.decode('utf-8')),sep=",")
    ZM_df = pd.read_csv(io.StringIO(ZM.decode('utf-8')))
    


    print(DP_df)
    print(DZ_df)
    print(ZM_df)