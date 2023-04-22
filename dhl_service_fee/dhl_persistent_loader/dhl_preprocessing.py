import pandas as pd

DZ = pd.read_csv("../get_raw_data/Domestic_Zona.csv")
DP = pd.read_csv("../get_raw_data/Domestic_Price.csv")

ZM = pd.read_csv("../get_raw_data/Zona_Matrix.csv")

DP = DP.rename(columns = {"Peso(en kg)":"Weight"}).iloc[:-2]

DP.Weight = DP.Weight.apply(lambda x: int(x))
DP.A = DP.A.apply(lambda x: float(x.replace(",",".")))
DP.B = DP.B.apply(lambda x: float(x.replace(",",".")))
DP.C = DP.C.apply(lambda x: float(x.replace(",",".")))
DP.D = DP.D.apply(lambda x: float(x.replace(",",".")))

DZ = DZ.rename(columns = {"País":"Region","Zona":"Zone"})
DZ = DZ.merge(DZ,how = "cross").rename(columns = {"Region_x":"Region_start",
                                                  "Zone_x":"Zone_start",
                                                  "Region_y":"Region_end",
                                                  "Zone_y":"Zone_end"})




ZM["Unnamed: 0"] = ZM["Unnamed: 0"].apply(lambda x: int(x))

def map_Zone(z_start,z_end):
    v = ZM[ZM["Unnamed: 0"] == int(z_start)][str(z_end)].values[0]
    return v

DZ["Type"] = DZ.apply(lambda x:map_Zone(x.Zone_start,x.Zone_end),axis = 1)

DZ.to_parquet('DHL_Processed_Domestic_Zone.parquet',index = False)
DP.to_parquet('DHL_Processed_Domestic_Price.parquet',index = False)

