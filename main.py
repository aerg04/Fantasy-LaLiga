from stats import Stats
from scrap import Scrap
import threading
import json

class Main:
    @staticmethod
    def main():
        #Scrap.getPlayersUrl()
        Main.savePlayersData()
        Main.insight()
        pass
    
    @staticmethod
    def savePlayersData():
        playersdata = []
        lock = threading.Lock()

        def iterateLinks(urls:list):
            data_list = []
            for url in urls:
                player_info = Scrap.getPlayersInfo(url)
                if(player_info != None):
                    data_list.append(player_info)
            with lock:
                playersdata.extend(data_list)


        threads = []
        with open("files/players.txt", "r") as f:
            for line in f:
                data = json.loads(line)
                t = threading.Thread(target=iterateLinks, args=(data,))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()
            print(t.name)

        with open("files/playersdata.txt", "w",encoding="utf-8") as f:
            f.write(json.dumps(playersdata,indent=4,ensure_ascii=False))
    
    @staticmethod
    def insight():
        data = 0
        with open("files/playersdata.txt","r",encoding="utf-8") as f:
            data = json.load(f)
        
        predf = []
        dictplayers = {}
        for player in data:
            dictplayers["team"] = player[0]
            dictplayers["name"] = player[1]
            dictplayers["position"] = player[2]
            dictplayers["price_trend"] = player[3]
            dictplayers.update(Stats.analyse(player[4]))
            predf.append(dictplayers)
            dictplayers = {}

        Stats.saveBestPlayersCsv(predf)
        Stats.querys(predf)
        #Stats.saveAllPlayer(predf)
        
if __name__ == "__main__":
    Main.main()