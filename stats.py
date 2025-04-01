import pandas as pd

class Stats:
   
    @staticmethod
    def analyse(data:list):
        if not data:
            return {"mean": 0, "std": 0, "min": 0, "25%": 0, "50%": 0, "75%": 0, "max": 0, "relative_deviation": 0, "mode": 0}
        
        df_points = pd.DataFrame(data)

        description = df_points.describe()

        # Calculate relative deviation (standard deviation / mean)
        #if(description.loc['mean'] != 0):
        relative_deviation = description.loc['std'] / description.loc['mean'] * 100
        #else:
           # relative_deviation = 0
        relative_deviation.name = 'relative_deviation'
        mode = df_points.mode().iloc[0]
        mode.name = "mode"
        # Append relative deviation to the description
        description = description._append(relative_deviation)
        description = description._append(mode)

        # Convert description to dictionary and drop 'points' key
        description_dict = description.transpose().to_dict()
        simplified_dict = {key: description_dict[key][0] for key in description_dict}

        return simplified_dict

    @staticmethod
    def querys(data:list):
        df = pd.DataFrame(data)
        # with open("files/output.txt","w", encoding="utf-8") as file:
        #     #file.write(str(df.query("count > 5 and `50%` >= 4.5 and position == 'DEF'").sort_values(by=["relative_deviation","count"], ascending=[True,False])) + "\n")
        #     file.write(str(df.to_csv("files/players.csv",index=True)) + "\n")
        df.to_csv("files/players.csv",index=True)
        # print(df.query("count > 5 and `50%` >= 5 and position == 'MED'").sort_values(by=["relative_deviation","count"], ascending=[True,False])[["name","relative_deviation"]])
        # print(df.query("count > 5 and `50%` >= 5 and position == 'DEF'").sort_values(by=["relative_deviation","count"], ascending=[True,False])["name"])
        # print(df.query("count > 5 and `50%` >= 5 and position == 'DEL'").sort_values(by=["relative_deviation","count"], ascending=[True,False])["name"])

        # df = df.query("name == ['Logan Costa','Pablo Maffeo','Thibaut Courtois','Brais Méndez','Sergi Darder','Aurélien Tchouaméni','Raphinha','Ayoze Pérez','Gorka Guruzeta','Antonio Rüdiger','Luis Milla']")
        
        # #df = df.sort_values(by=["relative_deviation","count"], ascending=[True,False])

        # print("media",df["mean"].sum())
        # print("mediana",df["50%"].sum())

        # sum_var =0
        # for i in df["std"]:
        #     sum_var += i*i
        # print(sum_var)

    @staticmethod
    def saveBestPlayersCsv(data:list):
        df = pd.DataFrame(data)
        defen = df.query("count > 5 and `50%` >= 4.5 and position == 'DEF'").sort_values(by=["relative_deviation","count"], ascending=[True,False])
        mid = df.query("count > 5 and `50%` >= 4.5 and position == 'MED'").sort_values(by=["relative_deviation","count"], ascending=[True,False])
        forward = df.query("count > 5 and `50%` >= 4.5 and position == 'DEL'").sort_values(by=["relative_deviation","count"], ascending=[True,False])
        goalkeepers = df.query("count > 5 and `50%` >= 4.5 and position == 'POR'").sort_values(by=["relative_deviation","count"], ascending=[True,False])
        defen = defen._append(mid)
        defen = defen._append(forward)
        defen = defen._append(goalkeepers)

        defen.to_csv("files/mejoresjugadores.csv",index=True)
    
    @staticmethod
    def saveAllPlayer(data:list):
        df = pd.DataFrame(data)
        df.to_excel("files/todoslosjugadores.xlsx",sheet_name="Hoja1")

if __name__ == "__main__":
    print(Stats.analyse([
            3,
            8,
            10,
            7,
            9,
            12,
            7,
            2,
            9,
            4,
            1,
            2,
            4,
            2,
            11,
            3,
            12,
            1,
            3
        ]))
