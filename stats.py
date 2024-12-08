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
        
        # df = df.query("position == 'MED'")
        # df = df.query("count > 5 and `50%` >= 5")

        df = df.query("name == ['3. Raúl Albiol', '2. Logan Costa','23. Pablo Maffeo','14. Santi Comesaña','13. Augusto Batalla','10. Sergi Darder','9. Kylian Mbappé','11. Raphinha']")
        
        df = df.sort_values(by=["relative_deviation","count"], ascending=[True,False])

        print(df)

if __name__ == "__main__":
    print(Stats.analyse([2,
            5,
            0,
            10,
            6,
            2,
            1,
            4,
            5,
            -1,
            3,
            0,
            6,
            2
        ]))
