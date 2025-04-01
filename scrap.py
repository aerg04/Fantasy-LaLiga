import logging
import requests
from bs4 import BeautifulSoup
import json

# Replace 'URL' with the actual URL of the webpage you want to scrape
class Scrap:
    @staticmethod
    def getPlayersUrl():
        list_txt = []
        with open("files/teams.txt","r") as f:
            for url in f:
                # Send HTTP request to the webpage
                response = requests.get(url.rstrip())

                # Parse HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all <a> tags with the class 'juggador pos-0 flex-column'
                a_tags = soup.find_all('a', class_='juggador pos-0 flex-column')

                # Extract and print the href attribute of each <a> tag
                hrefs = list({a['href'] for a in a_tags if 'href' in a.attrs})
                list_txt.append(hrefs)
                

        #print(list_txt)
        with open("files/players.txt", "w",encoding="utf-8") as f:
            for i in list_txt:
                print(i)
                f.write(json.dumps(i,ensure_ascii=False)+'\n')
        print("ready")
    
    @staticmethod
    def getPlayersInfo(url:str):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if(soup == None):
                return None
            #quiero el nombre
            #print(soup.find_all("h1"))
            name = soup.find('h1', class_="display-initial").text
            
            if(name.find(".")!=-1):
                
                #hay jugadores que no tienen su nombre de pila"
                name = name.split(".")[1].lstrip()
            #quiero el equipo
            team = Scrap.getTeam(soup)
            position = Scrap.getPosition(soup)
            if(team == None):
                print(url)            
            #quiero los puntos
            span_elements = soup.find_all('span', class_=lambda x: x and 'laliga-fantasy' in x)
            points = []
            for span in span_elements:
                try:
                    points.append(int(str(span.text).replace('\n', '').strip()))
                except:
                    points.append(0)
            #encontrar tendencia
            if(sum(points[3:]) > 12):
                trend = "upward"
            else:
                trend = "downward"
            return [team,name,position,trend,points]
        except Exception as e:
            logging.exception(url)
        
    @staticmethod
    def getTeam(soup:BeautifulSoup):
        
        try: 
            team = soup.find("div", "img-underphoto text-center col-12 info border-0 font-weight-bold mt-0 mb-0 pb-0 mt-md-0 txtc")
            if(team):
                team = team.find("img").get("alt")
            else:
                team = soup.find("div","img-underphoto text-center col-12 info border-0 font-weight-bold txtc")
                team = team.find("img").get("alt")
        except Exception:
            logging.exception("error equipo")
            #print(soup.find("div", "img-underphoto text-center col-12 info border-0 font-weight-bold mt-0 mb-0 pb-0 mt-md-0 txtc"))
        return team
    
    @staticmethod
    def getPosition(soup:BeautifulSoup):
        try:
            div_tag = soup.find('div', class_='mb-0 mt-0 info txtl posicion Defensa')
            position = div_tag.find('span').text
        except:
            div_tag = soup.find("div", class_="mb-0 mt-0 info txtl d-flex")
            position = div_tag.find('span').text
        return position

    @staticmethod
    def getLastFiveGames():
        request = requests.get("https://www.lavanguardia.com/deportes/resultados/laliga-primera-division/calendario")
        soup = BeautifulSoup(request.content, 'html.parser')
        #listas de jornadas
        games = soup.find_all("div",class_="col-md-6 col-xs-12")
        valid_games = Scrap.filterGames(games)
        
        gamesdict = []
        for i in valid_games[-6:]:
            Scrap.getResults(i,gamesdict)
        return Scrap.calPoints(gamesdict)
    
    @staticmethod
    def getResults(soup: BeautifulSoup, gamelist: list):
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, 'html.parser')

        bloques_partido = soup.find_all('div', class_='tpl-match-block-teams')

        for bloque in bloques_partido:
            equipo_local = bloque.find('h2', class_='tpl-match-team first').text.strip()
            equipo_visitante = bloque.find('h2', class_='tpl-match-team second').text.strip()

            # Extraer el marcador
            resultado = bloque.find('span', class_='tpl-match-results-detail first').text.strip()
            # Verificar que el marcador contiene dos números separados por " - "
            if " - " in resultado:
                partes = resultado.split(' - ')
                if len(partes) == 2 and partes[0].replace(" ","").isdigit() and partes[1].replace(" ","").isdigit():
                    # Dividir y convertir los goles en enteros
                    goles_local, goles_visitante = map(int, partes)

                    # Agregar el partido a la lista
                    gamelist.append({
                        "equipo_local": equipo_local,
                        "equipo_visitante": equipo_visitante,
                        "goles_local": goles_local,
                        "goles_visitante": goles_visitante
                    })

    @staticmethod
    def filterGames(games: list, filter = " - "):
        valid_games = []
        for game in games:
            # si encuentra un partido de la jornada que se jugo incluye todos los partidos de esa jornada 
            # Extract the result tpl-match-results-detail first
            result_block = game.find('span', class_='tpl-match-results-detail first')
            if result_block is not None:
                result_text = result_block.text.strip()

                # Validate the result (ensure it contains " - " and two valid scores)
                if filter in result_text:
                    if filter == " - ":
                        parts = result_text.split(' - ')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            valid_games.append(game)
                    else:
                        valid_games.append(game)

        return valid_games

    @staticmethod
    def calPoints(games:list):
        gamesperteam = {}
        #print(len(games))
        #devuelve un diccionario con los equipos como keys y una lista de sus partidos como value
        #print(games)
        for i in games:
            if(i["equipo_local"] in gamesperteam):
                gamesperteam[i["equipo_local"]].append(i)
            else:
                gamesperteam[i["equipo_local"]] = [i]
            if(i["equipo_visitante"] in gamesperteam):
                gamesperteam[i["equipo_visitante"]].append(i)
            else:
                gamesperteam[i["equipo_visitante"]] = [i]
            
        return gamesperteam

    @staticmethod
    def getTeamPointsSummary(gamesperteam: dict):
        team_points_summary = {}
        for team, games in gamesperteam.items():
            total_points = 0
            max_points = len(games[-5:])*3  # Assuming 3 points per game
            for game in games[-5:]:
                #print(games[-5:])
                if game["equipo_local"] == team:
                    if game["goles_local"] > game["goles_visitante"]:
                        total_points += 3
                    elif game["goles_local"] == game["goles_visitante"]:
                        total_points += 1
                elif game["equipo_visitante"] == team:
                    if game["goles_visitante"] > game["goles_local"]:
                        total_points += 3
                    elif game["goles_visitante"] == game["goles_local"]:
                        total_points += 1
            team_points_summary[team] =total_points/max_points
        return team_points_summary
    
    @staticmethod
    def getNextGames():
        request = requests.get("https://www.lavanguardia.com/deportes/resultados/laliga-primera-division/calendario")
        soup = BeautifulSoup(request.content, 'html.parser')
        #listas de jornadas
        games = soup.find_all("div",class_="col-md-6 col-xs-12")
        valid_games = Scrap.filterGames(games,"h")
        gamesdict = []
        for i in valid_games:
            Scrap.getNext(i,gamesdict)
        games = []
        for i in gamesdict:
            if(i not in games):
                games.append(i)
        return Scrap.calPoints(games)
    
    @staticmethod
    def getNext(soup: BeautifulSoup, gamelist: list):
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, 'html.parser')

        bloques_partido = soup.find_all('div', class_='tpl-match-block-teams')
        #tpl-match-results-detail first
        for bloque in bloques_partido:
            equipo_local = bloque.find('h2', class_='tpl-match-team first').text.strip()
            equipo_visitante = bloque.find('h2', class_='tpl-match-team second').text.strip()

            # Extraer el marcador
            resultado = bloque.find('span', class_='tpl-match-results-detail first').text.strip()
            # Verificar que el marcador contiene dos números separados por " - "
            if "h" in resultado:
                # Si el resultado contiene "h", significa que el partido no se ha jugado
                gamelist.append({
                    "equipo_local": equipo_local,
                    "equipo_visitante": equipo_visitante,
                })
    
    @staticmethod
    def getPredictions():
        output = Scrap.getLastFiveGames()
        team_summary = Scrap.getTeamPointsSummary(output)
        
        team_nextgames = Scrap.getNextGames()
        #print(team_nextgames)
        output = []
        for team, games in team_nextgames.items():
            predicts =[team]
            for game in games:
                if game["equipo_local"] == team:
                    predicts.append({str(game):team_summary[game["equipo_local"]]-team_summary[game["equipo_visitante"]]})
                else:
                    predicts.append({str(game):team_summary[game["equipo_visitante"]]-team_summary[game["equipo_local"]]})
            output.append(predicts)

        with open("files/predict.txt", "w",encoding="utf-8") as f:
            f.write(json.dumps(output,indent=2,ensure_ascii=False))

if __name__ == "__main__":
    print(Scrap.getPlayersInfo("https://www.futbolfantasy.com/jugadores/diego-lopez-1"))
