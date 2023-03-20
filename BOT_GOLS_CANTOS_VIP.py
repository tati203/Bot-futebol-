import datetime
import os
import time
import requests
import telebot
from unidecode import unidecode
import schedule
import traceback

collection_over05ht = {}
collection_overgolosft ={}
collection_cantosht ={}
collection_cantosft ={}
collection_resultados_diarios_gols = {}
collection_resultados_diarios_cantos = {}

# Configuração e criação do bot do telegram VIP
token = '5502600126:AAHp4CD-q-cAvqnF3Hb4mUDSTPKEa8NxHRA'
chat_id_gols = '-1001756870357'
chat_id_cantos = '-1001612491361'

bot = telebot.TeleBot(token)

#bot.send_message(chat_id=chat_id_gols, text="<b>BOT-GOLS ANALISANDO</b>", parse_mode="HTML", disable_web_page_preview= True)

#bot.send_message(chat_id=chat_id_cantos, text="<b>BOT-CANTOS ANALISANDO</b>", parse_mode="HTML", disable_web_page_preview= True)

def data_atual():
    date_now = datetime.datetime.now()
    data_atual = f'{date_now.day}/{date_now.month}/{date_now.year}'
    return data_atual

def iniciar_bd_diario_resultados_gols():
    dado = {
        'data':  data_atual,
        'green':0,
        'red': 0,
        }
    collection_resultados_diarios_gols[data_atual] = dado
    
def iniciar_bd_diario_resultados_cantos():
    dado = {
        'data':  data_atual,
        'green':0,
        'red': 0,
        }
    collection_resultados_diarios_cantos[data_atual] = dado 
  

# trata o placar do jogo quando esta no formato "3-1" separando os numeros e retorna a soma dos placares
def tratarPlacar(placar):
    numbers = placar.split("-")
    number1 = int(numbers[0])
    number2 = int(numbers[1])
    result = number1 + number2
    return result

def relatorio_diario_gols():

    date_now = datetime.datetime.now()
    data_atual = f'{date_now.day}/{date_now.month}/{date_now.year}'
    resultado_bd = collection_resultados_diarios_gols[data_atual]
    try:
        calculo_dia = float((100/(resultado_bd['green']+resultado_bd['red']))*resultado_bd['green'])
    except:
        calculo_dia = float(0)
    resultado_dia_gols = f'''
RESULTADO DO DIA-GOLS <b>{data_atual}</b>


🔰 <b>{resultado_bd['green']+resultado_bd['red']}</b> ALERTAS ENVIADOS
✅ <b>{resultado_bd['green']}</b> GREENS 
✖️ <b>{resultado_bd['red']}</b> RED

<b>💲 COM UMA ASSERTIVIDADE DE {calculo_dia:.2f}%</b>
                '''
    msg = bot.send_message(chat_id=chat_id_gols, text=resultado_dia, parse_mode="HTML", disable_web_page_preview="True")
    msg_id = msg.message_id
    bot.pin_chat_message(chat_id=chat_id_gols, message_id=msg_id)    

schedule.every().day.at("03:30:00").do(relatorio_diario_gols)

def relatorio_diario_cantos():
    
    date_now = datetime.datetime.now()
    data_atual = f'{date_now.day}/{date_now.month}/{date_now.year}'
    resultado_bd = collection_resultados_diarios_cantos[data_atual]
    try:
        calculo_dia = float((100/(resultado_bd['green']+resultado_bd['red']))*resultado_bd['green'])
    except:
        calculo_dia = float(0)
    resultado_dia_cantos = f'''
RESULTADO DO DIA-CANTOS <b>{data_atual}</b>


🔰 <b>{resultado_bd['green']+resultado_bd['red']}</b> ALERTAS ENVIADOS
✅ <b>{resultado_bd['green']}</b> GREENS 
✖️ <b>{resultado_bd['red']}</b> RED

<b>💲 COM UMA ASSERTIVIDADE DE {calculo_dia:.2f}%</b>
                '''
    msg = bot.send_message(chat_id=chat_id_cantos, text=resultado_dia, parse_mode="HTML", disable_web_page_preview="True")
    msg_id = msg.message_id
    bot.pin_chat_message(chat_id=chat_id_cantos, message_id=msg_id)    

schedule.every().day.at("03:30:00").do(relatorio_diario_cantos)

while True:
    # try:
        schedule.run_pending()

        date_now = datetime.datetime.now()
        data_atual = f'{date_now.day}/{date_now.month}/{date_now.year}'
        resultado_bd_gols = collection_resultados_diarios_gols.get(data_atual)
        resultado_bd_cantos = collection_resultados_diarios_cantos.get(data_atual)


        if resultado_bd_gols:
            pass
        else:
            iniciar_bd_diario_resultados_gols()
        if resultado_bd_cantos:
            pass
        else:
            iniciar_bd_diario_resultados_cantos()

        over05HT_enviado = []
        overgolosFT_enviado = []
        cantosHT_enviado = []
        cantosFT_enviado = []

        url = "https://api.sportsanalytics.com.br/api/v1/fixtures-svc/fixtures/livescores"
        querystring = {"include":"weatherReport,additionalInfo,league,stats,pressureStats,probabilities"}
        payload = ""
        headers = {
            "cookie": "route=f69973370a0dd0883a57c7b955dfc742; SRVGROUP=common",
            "authority": "api.sportsanalytics.com.br",
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://playscores.com",
            "referer": "https://playscores.com/",
            "sec-ch-ua": "^\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            dic_response = response.json()

            iniciando_analise = " ANALISANDO AS PARTIDAS EM LIVE (AO VIVO) "
            print(iniciando_analise.center(50, "#"))
            print('')

            for game in dic_response['data']:
                
                # date
                date = game['date']

                # fixtureId (Identificação unica da partida)
                fixtureId = game['fixtureId']

                # status da partida (LIVE, HT. FT OU ET)
                status_partida = game['status']

                # Team (Dados de equipes e torneio)
                awayTeam = game['awayTeam']['name']
                homeTeam = game['homeTeam']['name']
                league = game['league']['name']

                # currentTime (Tempo atual da partida)
                minute = 0 if game['currentTime']['minute'] is None else game['currentTime']['minute']
                second = game['currentTime']['second']


                # scores (Placar atual da partida)
                homeTeamScore = game['scores']['homeTeamScore']
                awayTeamScore = game['scores']['awayTeamScore']
                total = (homeTeamScore+awayTeamScore) +0.5
                htScore = game['scores']['htScore']
                ftScore = game['scores']['ftScore']

                if 'stats' in game:
                    if game['stats'] != None:
                        #corners(Escanteios)
                        corners_home = game['stats']['corners']['home'] or 0
                        corners_away = game['stats']['corners']['away'] or 0         
                       
                        c_t = (corners_home+corners_away) + 0.5
                        c_t2 = (corners_home+corners_away) + 1       
                       
                                    
                        

                        # dangerousAttacks (Ataques perigosos)
                        dangerousAttacks_home = game['stats']['dangerousAttacks']['home']
                        dangerousAttacks_away = game['stats']['dangerousAttacks']['away']

                        # shotsOffgoal (Chutes para fora)
                        shotsOffgoal_home = game['stats']['shotsOffgoal']['home'] or 0
                        shotsOffgoal_away = game['stats']['shotsOffgoal']['away'] or 0

                        # shotsOngoal (Chutes no gol)
                        shotsOngoal_home = game['stats']['shotsOngoal']['home'] or 0
                        shotsOngoal_away = game['stats']['shotsOngoal']['away'] or 0

                        # yellowredcards (Cartões amarelo)
                        yellowredcards_home = game['stats']['yellowredcards']['home']
                        yellowredcards_away = game['stats']['yellowredcards']['away']
                        
                        # possessiontime (Posse de bola)
                        possessiontime_home = 0 if game['stats']["possessiontime"]['home'] is None else game['stats']["possessiontime"]['home']
                        possessiontime_away = 0 if game['stats']["possessiontime"]['away'] is None else game['stats']["possessiontime"]['away']

                if 'pressureStats' in game:
                    
                    if game['pressureStats'] != None:
                        # appm1 (Indica a média de ataques perigosos por minutos. Ataques perigosos dividido por tempo do jogo)
                        appm1_home = 0 if game['pressureStats']['appm1']['home'] is None else game['pressureStats']['appm1']['home']
                        appm1_away = 0 if game['pressureStats']['appm1']['away'] is None else game['pressureStats']['appm1']['away']

                        # appm2 (Mesma coisa do APM¹ porém checando somente os últimos 10 minutos)
                        appm2_home = 0 if game['pressureStats']['appm2']['home'] is None else game['pressureStats']['appm2']['home']
                        appm2_away = 0 if game['pressureStats']['appm2']['away'] is None else game['pressureStats']['appm2']['away']

                        # exg (Indica a expectativa de gol. Considera apenas os últimos 10 minutos da partida. Chute no Gol + Chute fora + Cantos, entre outros inputs (métricas). Pontuação máxima de 2. Pontuação entre 1.50 a 2 mostra um cenário de muita pressão de uma determinada equipe)
                        exg_home = 0 if game['pressureStats']['exg']['home'] is None else game['pressureStats']['exg']['home']
                        exg_away = 0 if game['pressureStats']['exg']['away'] is None else game['pressureStats']['exg']['away']

                        # mh1 (Chance de gol e ele gera pontuação a partir dos dados de chute ao gol + posse de bola, + outros inputs. Valor ideal para uma única equipe a partir de 50, e a soma das duas equipes a partir de 60)
                        mh1_home = 0 if game['pressureStats']['mh1']['home'] is None else game['pressureStats']['mh1']['home']
                        mh1_away = 0 if game['pressureStats']['mh1']['away'] is None else game['pressureStats']['mh1']['away']

                        # mh2 (Posicionamento ofensivo da equipe, quando uma equipe está rodeando a área adversária sem muitas interrupções (por exemplo: faltas e escanteios). Valor ideal para uma única equipe a partir de 10, e a soma das duas equipes a partir de 15)
                        mh2_home = 0 if game['pressureStats']['mh2']['home'] is None else game['pressureStats']['mh2']['home']
                        mh2_away = 0 if game['pressureStats']['mh2']['away'] is None else game['pressureStats']['mh2']['away']

                        # mh3 (A soma da competição entre os índices. Qualquer valor de uma única equipe acima de 6 é um bom indicativo)
                        mh3_home = 0 if game['pressureStats']['mh3']['home'] is None else game['pressureStats']['mh3']['home']
                        mh3_away = 0 if game['pressureStats']['mh3']['away'] is None else game['pressureStats']['mh3']['away']

                        # attack_momentum (Poder de ataque da equipe)
                        attack_momentum_home = 0 if game['pressureStats']['attack_momentum']['home'] is None else game['pressureStats']['attack_momentum']['home']
                        attack_momentum_away = 0 if game['pressureStats']['attack_momentum']['away'] is None else game['pressureStats']['attack_momentum']['away']

                else:
                    print('NO pressureStats')
                    appm1_home = 0
                    appm1_away = 0
                    appm2_home = 0
                    appm2_away = 0 
                    exg_home = 0
                    exg_away = 0 
                    mh1_home = 0 
                    mh1_away = 0
                    mh2_home = 0
                    mh2_away = 0
                    mh3_home = 0 
                    mh3_away = 0
                    attack_momentum_home = 0 
                    attack_momentum_away = 0

                if 'probabilities' in game:
                    if game['probabilities'] != None :
                        AT_over_0_5 = 0 if game['probabilities']['AT_over_0_5'] is None else game['probabilities']['AT_over_0_5']
                        AT_over_1_5 = 0 if game['probabilities']['AT_over_1_5'] is None else game['probabilities']['AT_over_1_5']
                        AT_under_0_5 = 0 if game['probabilities']['AT_under_0_5'] is None else game['probabilities']['AT_under_0_5']
                        AT_under_1_5 = 0 if game['probabilities']['AT_under_1_5'] is None else game['probabilities']['AT_under_1_5']
                        HT_over_0_5 = 0 if game['probabilities']['HT_over_0_5'] is None else game['probabilities']['HT_over_0_5']
                        HT_over_1_5 = 0 if game['probabilities']['HT_over_1_5'] is None else game['probabilities']['HT_over_1_5']
                        HT_under_0_5 = 0 if game['probabilities']['HT_under_0_5'] is None else game['probabilities']['HT_under_0_5']
                        HT_under_1_5 = 0 if game['probabilities']['HT_under_1_5'] is None else game['probabilities']['HT_under_1_5']
                        home = 0 if game['probabilities']['home'] is None else game['probabilities']['home']
                        away = 0 if game['probabilities']['away'] is None else game['probabilities']['away']
                        btts = 0 if game['probabilities']['btts'] is None else game['probabilities']['btts']
                        draw = 0 if game['probabilities']['draw'] is None else game['probabilities']['draw']
                        over_0_5 = 0 if game['probabilities']['over_0_5'] is None else game['probabilities']['over_0_5']
                        over_1_5 = 0 if game['probabilities']['over_1_5'] is None else game['probabilities']['over_1_5'] 
                        over_2_5 = 0 if game['probabilities']['over_2_5'] is None else game['probabilities']['over_2_5']
                        over_3_5 = 0 if game['probabilities']['over_3_5'] is None else game['probabilities']['over_3_5']
                        under_0_5 = 0 if game['probabilities']['under_0_5'] is None else game['probabilities']['under_0_5']
                        under_1_5 = 0 if game['probabilities']['under_1_5'] is None else game['probabilities']['under_1_5']
                        under_2_5 = 0 if game['probabilities']['under_2_5'] is None else game['probabilities']['under_2_5']
                        under_3_5 = 0 if game['probabilities']['under_3_5'] is None else game['probabilities']['under_3_5']

                if 'probabilities' not in game:
                    AT_over_0_5 = 0 
                    AT_over_1_5 = 0
                    AT_under_0_5 = 0
                    AT_under_1_5 = 0
                    HT_over_0_5 = 0 
                    HT_over_1_5 = 0 
                    HT_under_0_5 = 0 
                    HT_under_1_5 = 0 
                    home = 0 
                    away = 0 
                    btts = 0 
                    draw = 0
                    over_0_5 = 0 
                    over_1_5 = 0 
                    over_2_5 = 0 
                    over_3_5 = 0 
                    under_0_5 = 0 
                    under_1_5 = 0 
                    under_2_5 = 0 
                    under_3_5 = 0 

                if game['stats'] != None and  game['pressureStats'] != None:
                    # shotsTotal (Soma de chutes no gol e fora do gol)
                    shotsTotal_home = shotsOngoal_home+shotsOffgoal_home
                    shotsTotal_away = shotsOngoal_away+shotsOffgoal_away

                    # CG (chutes gols + chutes para fora + escanteios)
                    CG_home = shotsOffgoal_home+shotsOngoal_home+corners_home
                    CG_away = shotsOffgoal_away+shotsOngoal_away+corners_away

                    # Rendimento (appm x posse de bola)
                    rendimento_home = appm1_home * possessiontime_home
                    rendimento_away = appm1_away * possessiontime_away

                # Verifica o time que tem menos caracteres, remove os acentos e cria link para partida na BET365
                if len(homeTeam) < len(awayTeam):
                    timeMenosCaracteres = unidecode(homeTeam)
                else:
                    timeMenosCaracteres = unidecode(awayTeam)
                time_para_link = timeMenosCaracteres.replace(" ","%20") #SUBSTITUI ESPAÇOS DO NOME DO TIME POR %20
                time_para_link_formatado = time_para_link.replace("'", '')
                link_jogo_bet365 = f"https://bet365.com/#/AX/K%5E{time_para_link_formatado}/" #ACRESCENTA O NOME DO TIME AO LINK

                partida_info = f"fixtureId: {fixtureId} | {minute}' {status_partida} - {homeTeam} {homeTeamScore} X {awayTeamScore} {awayTeam}"

                print(partida_info.center(50, " "))

                # Estratégia para Over 0.5 gols HT
                document = collection_over05ht.get(fixtureId)
                exists = bool(document)
                
                try:
                    p1_over05ht = (homeTeamScore+awayTeamScore == 0) and (appm1_away+appm1_home >= 2.2) and (minute >= 8 and minute <= 20) and ((minute/(shotsTotal_home+shotsTotal_away)) >= 4 )
                except Exception as e:
                    print(e)
                    p1_over05ht = False
                try:
                    p2_over05ht = ((homeTeamScore+awayTeamScore == 0) and (minute >= 8 and minute <= 20) and (appm1_home >= 1.90) and (CG_home >= 23) and (rendimento_home >= 90)) or ((homeTeamScore+awayTeamScore == 0) and (minute >= 8 and minute <= 20) and (appm1_away >= 1.90) and (CG_away >= 23) and (rendimento_away >= 90))
                except Exception as e:
                    print(e)
                    p2_over05ht = False
                
                if exists != True:
                     if game['pressureStats'] != None and game['stats'] != None:
                          if p1_over05ht or p2_over05ht:
                                alerta05HT = f'''<b> BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {homeTeam} {homeTeamScore} x {awayTeamScore} {awayTeam}
🏆 <b>Competição:</b> {league}
🕛 <b>Tempo:</b> {minute}' minutos

<b>Estratégia:</b>
<b>+0.5 Gol HT</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {appm1_home:.2f} - {appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {appm2_home} - {appm2_away}
🥅 Remates baliza: {shotsOngoal_home} - {shotsOngoal_away}
🥅 Remates lado: {shotsOffgoal_home} - {shotsOffgoal_away}
⛳️ Cantos: {corners_home} - {corners_away}

📲  <b> <a href='{link_jogo_bet365}'>Bet365</a> </b>'''
                            
                                mensagem = bot.send_message(chat_id=chat_id_gols, text=alerta05HT, parse_mode="HTML", disable_web_page_preview= True)
                                msg_id = mensagem.message_id
                                dado1 = {
                                    'fixtureId': fixtureId,
                                    'msg_id': msg_id,
                                    'homeTeam': homeTeam,
                                    'awayTeam': awayTeam,
                                    'league': league,
                                    'minute': minute,
                                    'homeTeamScore': homeTeamScore,
                                    'awayTeamScore': awayTeamScore,
                                    'corners_home': corners_home,
                                    'corners_away': corners_away,
                                    'dangerousAttacks_home': dangerousAttacks_home,
                                    'dangerousAttacks_away': dangerousAttacks_away,
                                    'appm1_home': appm1_home,
                                    'appm1_away': appm1_away,
                                    'appm2_home': appm2_home,
                                    'appm2_away': appm2_away,
                                    'shots_home': shotsOffgoal_home+shotsOngoal_home,
                                    'shots_away': shotsOngoal_away+shotsOffgoal_away,
                                    'shotsOngoal_home': shotsOngoal_home,
                                    'shotsOngoal_away': shotsOngoal_away,
                                    'shotsOffgoal_home': shotsOffgoal_home,
                                    'shotsOffgoal_away': shotsOffgoal_away
                                    }
                                collection_over05ht[fixtureId] = dado1
                                time.sleep(2)
                                    
                document = collection_overgolosft.get(fixtureId)
                exists = bool(document)
                
                try:
                    p1_overft = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and (appm1_away+appm1_home >= 2.2) and (minute >= 59 and minute <= 68) and ((minute/(shotsTotal_home+shotsTotal_away)) >= 4 )
                except Exception as e:
                    print(e)
                    p1_overft = False
                try:
                    p2_overft = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm1_home >= 1.9) or (appm1_away >= 1.9)) and ((appm2_home >= 1.9) or (appm2_away >= 1.9)) and (CG_home+CG_away >= 30) and (minute >= 59 and minute <= 68)
                except Exception as e:
                    print(e)
                    p2_overft = False
                try:
                    p3_overft = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm2_home >= 1.9) or (appm2_away >= 1.9)) and ((CG_home >= 30) or (CG_away >= 30)) and ((shotsTotal_home >= 13) or (shotsTotal_away >= 13)) and (minute >= 59 and minute <= 68)
                except Exception as e:
                    print(e)
                    p3_overft = False
                
                if exists != True:
                        if game['pressureStats'] != None and game['stats'] != None:
                            if p1_overft or p2_overft or p3_overft:
                                alertaovergolosFT = f'''<b>BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {homeTeam} {homeTeamScore} x {awayTeamScore} {awayTeam}
🏆<b>Competição:</b> {league}
🕛 <b>Tempo:</b> {minute}' minutos

<b>Estratégia:</b>
<b>+ {total} Gols</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {appm1_home:.2f} - {appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {appm2_home} - {appm2_away}
🥅 Remates baliza: {shotsOngoal_home} - {shotsOngoal_away}
🥅 Remates lado: {shotsOffgoal_home} - {shotsOffgoal_away}
⛳️ Cantos: {corners_home} - {corners_away}

📲  <b> <a href='{link_jogo_bet365}'>Bet365</a> </b>'''
                            
                                mensagem = bot.send_message(chat_id=chat_id_gols, text=alertaovergolosFT, parse_mode="HTML", disable_web_page_preview= True)
                                msg_id = mensagem.message_id
                                # msg_id=123123123
                                dado2 = {
                                    'fixtureId': fixtureId,
                                    'msg_id': msg_id,
                                    'homeTeam': homeTeam,
                                    'awayTeam': awayTeam,
                                    'league': league,
                                    'minute': minute,
                                    'homeTeamScore': homeTeamScore,
                                    'awayTeamScore': awayTeamScore,
                                    'total': total,
                                    'corners_home': corners_home,
                                    'corners_away': corners_away,
                                    'dangerousAttacks_home': dangerousAttacks_home,
                                    'dangerousAttacks_away': dangerousAttacks_away,
                                    'appm1_home': appm1_home,
                                    'appm1_away': appm1_away,
                                    'appm2_home': appm2_home,
                                    'appm2_away': appm2_away,
                                    'shots_home': shotsOffgoal_home+shotsOngoal_home,
                                    'shots_away': shotsOngoal_away+shotsOffgoal_away,
                                    'shotsOngoal_home': shotsOngoal_home,
                                    'shotsOngoal_away': shotsOngoal_away,
                                    'shotsOffgoal_home': shotsOffgoal_home,
                                    'shotsOffgoal_away': shotsOffgoal_away
                                    }
                                collection_overgolosft[fixtureId] = dado2
                                time.sleep(2) 
                                    
                document = collection_cantosht.get(fixtureId)
                exists = bool(document)
                
                try:
                    p1_cantoht = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm2_home >= 1.3) or (appm2_away >= 1.3)) and ((appm1_home >= 1.2) or (appm1_away >= 1.2)) and ((CG_home >= 8) or (CG_away >= 8)) and ((corners_away >= 3) or (corners_home >= 3)) and ((shotsOngoal_away >= 2) or (shotsOngoal_home >= 2)) and (minute >= 32 and minute <= 35)
                except Exception as e:
                    print(e)
                    p1_cantoht = False
                try:
                    p2_cantoht = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm2_home >= 1.3) or (appm2_away >= 1.3)) and (minute >= 32 and minute <= 35) and ((shotsTotal_home >= 5) or (shotsTotal_away >= 5)) and (corners_home+corners_away >= 5)
                except Exception as e:
                    print(e)
                    p2_cantoht = False

                if exists != True:
                        if game['pressureStats'] != None and game['stats'] != None:
                            if p1_cantoht or p2_cantoht:
                                alertacantoHT = f'''<b>BOT-CANTOS</b>
                                
🏟 <b>Jogo:</b> {homeTeam} {homeTeamScore} x {awayTeamScore} {awayTeam}
🏆 <b>Competição:</b> {league}
🕛 <b>Tempo:</b> {minute} minutos

<b>Estratégia:</b>                           
⛳️ Cantos LIMITE 1°Tempo
    +{c_t}  | +{c_t2} Escanteio Asiáticos

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {appm1_home:.2f} - {appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {appm2_home} - {appm2_away}
🥅 Remates baliza: {shotsOngoal_home} - {shotsOngoal_away}
🥅 Remates lado: {shotsOffgoal_home} - {shotsOffgoal_away}
⛳️ Cantos: {corners_home} - {corners_away}

📲   <b><a href='{link_jogo_bet365}'>Bet365</a> </b>'''
                            
                                mensagem = bot.send_message(chat_id=chat_id_cantos, text=alertacantoHT, parse_mode="HTML", disable_web_page_preview= True)
                                msg_id = mensagem.message_id
                                dado3 = {
                                    'fixtureId': fixtureId,
                                    'msg_id': msg_id,
                                    'homeTeam': homeTeam,
                                    'awayTeam': awayTeam,
                                    'league': league,
                                    'minute': minute,
                                    'homeTeamScore': homeTeamScore,
                                    'awayTeamScore': awayTeamScore,
                                    'corners_home': corners_home,
                                    'corners_away': corners_away,
                                    'dangerousAttacks_home': dangerousAttacks_home,
                                    'dangerousAttacks_away': dangerousAttacks_away,
                                    'appm1_home': appm1_home,
                                    'appm1_away': appm1_away,
                                    'appm2_home': appm2_home,
                                    'appm2_away': appm2_away,
                                    'shots_home': shotsOffgoal_home+shotsOngoal_home,
                                    'shots_away': shotsOngoal_away+shotsOffgoal_away,
                                    'shotsOngoal_home': shotsOngoal_home,
                                    'shotsOngoal_away': shotsOngoal_away,
                                    'shotsOffgoal_home': shotsOffgoal_home,
                                    'shotsOffgoal_away': shotsOffgoal_away
                                    }
                                collection_cantosht[fixtureId] = dado3
                                time.sleep(2)
                                    
                document = collection_cantosft.get(fixtureId)
                exists = bool(document)
                
                try:
                    p1_cantoft = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm2_home >= 1.3) or (appm2_away >= 1.3)) and ((CG_home >= 15) or (CG_away >= 15)) and (minute >= 80 and minute <= 82)
                except Exception as e:
                    print(e)
                    p1_cantoft = False
                try:
                    p2_cantoft = ((homeTeamScore-awayTeamScore == 0) or (homeTeamScore-awayTeamScore == 1)) and ((appm2_home >= 1.3) or (appm2_away >= 1.3)) and (minute >= 80 and minute <= 82) and ((shotsTotal_home >= 10) or (shotsTotal_away >= 10)) and (corners_home+corners_away >= 10) 
                except Exception as e:
                    print(e)
                    p2_cantoft = False
                
                if exists != True:
                        if game['pressureStats'] != None and game['stats'] != None:
                            if p1_cantoft or p2_cantoft:
                                alertacantoFT = f'''<b>BOT-CANTOS</b>
                                
🏟 <b>Jogo:</b> {homeTeam} {homeTeamScore} x {awayTeamScore} {awayTeam}
🏆 <b>Competição:</b> {league}
🕛 <b>Tempo:</b> {minute} minutos

<b>Estratégia:</b>                           
⛳️ Cantos LIMITE 2°Tempo
    +{c_t}  | +{c_t2} Escanteio Asiáticos

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {appm1_home:.2f} - {appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {appm2_home} - {appm2_away}
🥅 Remates baliza: {shotsOngoal_home} - {shotsOngoal_away}
🥅 Remates lado: {shotsOffgoal_home} - {shotsOffgoal_away}
⛳️ Cantos: {corners_home} - {corners_away}

📲   <b><a href='{link_jogo_bet365}'>Bet365</a> </b>'''
                            
                                mensagem = bot.send_message(chat_id=chat_id_cantos, text=alertacantoFT, parse_mode="HTML", disable_web_page_preview= True)
                                msg_id = mensagem.message_id
                                # msg_id = 123123123
                                dado4 = {
                                    'fixtureId': fixtureId,
                                    'msg_id': msg_id,
                                    'homeTeam': homeTeam,
                                    'awayTeam': awayTeam,
                                    'league': league,
                                    'minute': minute,
                                    'homeTeamScore': homeTeamScore,
                                    'awayTeamScore': awayTeamScore,
                                    'corners_home': corners_home,
                                    'corners_away': corners_away,
                                    'dangerousAttacks_home': dangerousAttacks_home,
                                    'dangerousAttacks_away': dangerousAttacks_away,
                                    'appm1_home': appm1_home,
                                    'appm1_away': appm1_away,
                                    'appm2_home': appm2_home,
                                    'appm2_away': appm2_away,
                                    'shots_home': shotsOffgoal_home+shotsOngoal_home,
                                    'shots_away': shotsOngoal_away+shotsOffgoal_away,
                                    'shotsOngoal_home': shotsOngoal_home,
                                    'shotsOngoal_away': shotsOngoal_away,
                                    'shotsOffgoal_home': shotsOffgoal_home,
                                    'shotsOffgoal_away': shotsOffgoal_away
                                    }
                                collection_cantosft[fixtureId] = dado4
                                time.sleep(2)                                    

        else:
            print("RETORNO DA API FALHOU AGUARDANDO 60 SEGUNDOS PARA TENTAR NOVAMENTE 1")
            time.sleep(60)

        print("")
        lista_correcao = " LISTAS DE ALERTAS ENVIADOS "
        print(lista_correcao.center(50, "#"))
        print("")

        # Cria lista de partidas enviadas over 0.5 gols HT
        resultado = collection_over05ht
        for dado in resultado:
            partida = resultado[dado]
            if partida not in over05HT_enviado:
                over05HT_enviado.append(partida.get('fixtureId'))
        lista_over05ht = f'Over 0.5 HT - {over05HT_enviado}'
        print(lista_over05ht.center(50, " "))
        
        resultado = collection_overgolosft
        for dado in resultado:
            partida = resultado[dado]
            if partida not in overgolosFT_enviado:
                overgolosFT_enviado.append(partida.get('fixtureId'))
        lista_overgolosFT = f'Over golos FT - {overgolosFT_enviado}'
        print(lista_overgolosFT.center(50, " "))
        
        resultado = collection_cantosht
        for dado in resultado:
            partida = resultado[dado]
            if partida not in cantosHT_enviado:
                cantosHT_enviado.append(partida.get('fixtureId'))
        lista_cantosHT = f'cantos HT - {cantosHT_enviado}'
        print(lista_cantosHT.center(50, " "))
        
        resultado = collection_cantosft
        for dado in resultado:
            partida = resultado[dado]
            if partida not in cantosFT_enviado:
                cantosFT_enviado.append(partida.get('fixtureId'))
        lista_cantosFT = f'cantos FT - {cantosFT_enviado}'
        print(lista_cantosFT.center(50, " "))        

        print("")
        lista_correcao = " CORREÇÃO DE ALERTAS ENVIADOS "
        print(lista_correcao.center(50, "#"))
        print("")

        for item in over05HT_enviado:
            url = f"https://api.sportsanalytics.com.br/api/v1/fixtures-svc/fixtures/{item}"
            querystring = {"include":"weatherReport,additionalInfo,league,stats,pressureStats,probabilities"}
            payload = ""
            headers = {
                "cookie": "route=f69973370a0dd0883a57c7b955dfc742; SRVGROUP=common",
                "authority": "api.sportsanalytics.com.br",
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://playscores.com",
                "referer": "https://playscores.com/",
                "sec-ch-ua": "^\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code == 200:
                dic_response = response.json()

                htScore = dic_response['data'][0]['scores']['htScore']
                status_partida = dic_response['data'][0]['status']
                minute_atual = dic_response['data'][0]['currentTime']['minute']

                resultado_bd = collection_over05ht.get(item)
                
                bd_fixtureId = resultado_bd['fixtureId']
                bd_msg_id = resultado_bd['msg_id']
                bd_homeTeam = resultado_bd['homeTeam']
                bd_awayTeam = resultado_bd['awayTeam']
                bd_league = resultado_bd['league']
                bd_minute = resultado_bd['minute']
                bd_homeTeamScore = resultado_bd['homeTeamScore']
                bd_awayTeamScore = resultado_bd['awayTeamScore']
                bd_corners_home = resultado_bd['corners_home']
                bd_corners_away = resultado_bd['corners_away']
                bd_dangerousAttacks_home = resultado_bd['dangerousAttacks_home']
                bd_dangerousAttacks_away = resultado_bd['dangerousAttacks_away']
                bd_appm1_home = resultado_bd['appm1_home']
                bd_appm1_away = resultado_bd['appm1_away']
                bd_appm2_home = resultado_bd['appm2_home']
                bd_appm2_away = resultado_bd['appm2_away']
                bd_shots_home = resultado_bd['shots_home']
                bd_shots_away = resultado_bd['shots_away']
                bd_shotsOngoal_home = resultado_bd ['shotsOngoal_home']
                bd_shotsOngoal_away = resultado_bd['shotsOngoal_away']
                bd_shotsOffgoal_home = resultado_bd['shotsOffgoal_home']
                bd_shotsOffgoal_away = resultado_bd['shotsOffgoal_away']
                
                filter = bd_fixtureId
                
                if htScore is None or status_partida != "HT":
                    partida_andamento_05ht = f'+0.5 GOLS HT - {item} - Partida em andamento'
                    print(partida_andamento_05ht.center(50, " "))
                if minute_atual == 45 and status_partida == "HT":
                    if tratarPlacar(htScore)>=1:
                        correcao_alerta05HT = f'''<b>BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos

<b>Estratégia:</b>
<b>+0.5 Gol HT</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉 <b>Resultado:</b> ✅✅✅✅'''
                        
                        bot.edit_message_text(text=correcao_alerta05HT , chat_id = chat_id_gols , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_over05ht.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_gols.get(data_atual)
                        collection_resultados_diarios_gols.get(data_atual)['green'] = resultados_bd['green']+1
                        time.sleep(2)
                        partida_corrigida_05ht = f'+0.5 GOLS HT - {item} | {htScore} | Green'
                        print(partida_corrigida_05ht.center(50, " "))
                        
                    if tratarPlacar(htScore)<1:
                        correcao_alerta05HT = f'''<b>BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos

<b>Estratégia:</b>
<b>+0.5 Gol HT</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉<b>Resultado:</b> ❌❌❌❌'''
                        
                        bot.edit_message_text(text=correcao_alerta05HT , chat_id = chat_id_gols , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_over05ht.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_gols.get(data_atual)
                        collection_resultados_diarios_gols.get(data_atual)['red'] = resultados_bd['red']+1
                        time.sleep(2)
                        partida_corrigida_05ht = f'+0.5 GOLS HT - {item} | {htScore} | Red'
                        print(partida_corrigida_05ht.center(50, " "))
                        
        for item in overgolosFT_enviado:
            url = f"https://api.sportsanalytics.com.br/api/v1/fixtures-svc/fixtures/{item}"
            querystring = {"include":"weatherReport,additionalInfo,league,stats,pressureStats,probabilities"}
            payload = ""
            headers = {
                "cookie": "route=f69973370a0dd0883a57c7b955dfc742; SRVGROUP=common",
                "authority": "api.sportsanalytics.com.br",
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://playscores.com",
                "referer": "https://playscores.com/",
                "sec-ch-ua": "^\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code == 200:
                dic_response = response.json()
                
                ftScore = dic_response['data'][0]['scores']['ftScore']
                status_partida = dic_response['data'][0]['status']
                minute_atual = dic_response['data'][0]['currentTime']['minute']

                resultado_bd = collection_overgolosft.get(item)
                
                bd_fixtureId = resultado_bd['fixtureId']
                bd_msg_id = resultado_bd['msg_id']
                bd_homeTeam = resultado_bd['homeTeam']
                bd_awayTeam = resultado_bd['awayTeam']
                bd_total = resultado_bd['total']
                bd_league = resultado_bd['league']
                bd_minute = resultado_bd['minute']
                bd_homeTeamScore = resultado_bd['homeTeamScore']
                bd_awayTeamScore = resultado_bd['awayTeamScore']
                bd_corners_home = resultado_bd['corners_home']
                bd_corners_away = resultado_bd['corners_away']
                bd_dangerousAttacks_home = resultado_bd['dangerousAttacks_home']
                bd_dangerousAttacks_away = resultado_bd['dangerousAttacks_away']
                bd_appm1_home = resultado_bd['appm1_home']
                bd_appm1_away = resultado_bd['appm1_away']
                bd_appm2_home = resultado_bd['appm2_home']
                bd_appm2_away = resultado_bd['appm2_away']
                bd_shots_home = resultado_bd['shots_home']
                bd_shots_away = resultado_bd['shots_away']
                bd_shotsOngoal_home = resultado_bd ['shotsOngoal_home']
                bd_shotsOngoal_away = resultado_bd['shotsOngoal_away']
                bd_shotsOffgoal_home = resultado_bd['shotsOffgoal_home']
                bd_shotsOffgoal_away = resultado_bd['shotsOffgoal_away']
                
                filter = bd_fixtureId
                
                if ftScore is None or status_partida != "FT":
                    partida_andamento_golosft = f'GOLS FT - {item} - Partida em andamento'
                    print(partida_andamento_golosft.center(50, " "))
                if status_partida =="FT":
                    if tratarPlacar(ftScore)>bd_homeTeamScore+bd_awayTeamScore:
                        correcao_alertagolosFT = f'''<b>BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos

<b>Estratégia:</b>
<b>+ {bd_total} Gols</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉 <b>Resultado:</b> ✅✅✅✅'''
                        
                        bot.edit_message_text(text=correcao_alertagolosFT , chat_id = chat_id_gols , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_overgolosft.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_gols.get(data_atual)
                        collection_resultados_diarios_gols.get(data_atual)['green'] = resultados_bd['green']+1
                        time.sleep(2)
                        partida_corrigida_golosft = f'GOLS FT - {item} | {ftScore} | Green'
                        print(partida_corrigida_golosft.center(50, " "))
                        
                    if tratarPlacar(ftScore)==bd_homeTeamScore+bd_awayTeamScore:
                        correcao_alertagolosFT = f'''<b>BOT-GOLS</b>
                                
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos

<b>Estratégia:</b>
<b>+ {bd_total} Gols</b>

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉 <b>Resultado:</b>❌❌❌❌'''
                        
                        bot.edit_message_text(text=correcao_alertagolosFT , chat_id = chat_id_gols , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_overgolosft.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_gols.get(data_atual)
                        collection_resultados_diarios_gols.get(data_atual)['red'] = resultados_bd['red']+1
                        time.sleep(2)
                        partida_corrigida_golosft = f'GOLS FT - {item} | {ftScore} |  Red'
                        print(partida_corrigida_golosft.center(50, " "))
                        
        for item in cantosHT_enviado:
            url = f"https://api.sportsanalytics.com.br/api/v1/fixtures-svc/fixtures/{item}"
            querystring = {"include":"weatherReport,additionalInfo,league,stats,pressureStats,probabilities"}
            payload = ""
            headers = {
                "cookie": "route=f69973370a0dd0883a57c7b955dfc742; SRVGROUP=common",
                "authority": "api.sportsanalytics.com.br",
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://playscores.com",
                "referer": "https://playscores.com/",
                "sec-ch-ua": "^\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code == 200:
                dic_response = response.json()
                
                htScore = dic_response['data'][0]['scores']['htScore']
                status_partida = dic_response['data'][0]['status']
                minute_atual = dic_response['data'][0]['currentTime']['minute']
                corners_home = dic_response['data'][0]['stats']['corners']['home']
                corners_away = dic_response['data'][0]['stats']['corners']['away']

                resultado_bd = collection_cantosht.get(item)
                
                bd_fixtureId = resultado_bd['fixtureId']
                bd_msg_id = resultado_bd['msg_id']
                bd_homeTeam = resultado_bd['homeTeam']
                bd_awayTeam = resultado_bd['awayTeam']
                bd_league = resultado_bd['league']
                bd_minute = resultado_bd['minute']
                bd_homeTeamScore = resultado_bd['homeTeamScore']
                bd_awayTeamScore = resultado_bd['awayTeamScore']
                bd_corners_home = resultado_bd['corners_home']
                bd_corners_away = resultado_bd['corners_away']
                bd_dangerousAttacks_home = resultado_bd['dangerousAttacks_home']
                bd_dangerousAttacks_away = resultado_bd['dangerousAttacks_away']
                bd_appm1_home = resultado_bd['appm1_home']
                bd_appm1_away = resultado_bd['appm1_away']
                bd_appm2_home = resultado_bd['appm2_home']
                bd_appm2_away = resultado_bd['appm2_away']
                bd_shots_home = resultado_bd['shots_home']
                bd_shots_away = resultado_bd['shots_away']
                bd_shotsOngoal_home = resultado_bd ['shotsOngoal_home']
                bd_shotsOngoal_away = resultado_bd['shotsOngoal_away']
                bd_shotsOffgoal_home = resultado_bd['shotsOffgoal_home']
                bd_shotsOffgoal_away = resultado_bd['shotsOffgoal_away']
                
                filter = bd_fixtureId
                
                if status_partida != "HT":
                    partida_andamento_cantosht = f'cantos HT - {item} - Partida em andamento'
                    print(partida_andamento_cantosht.center(50, " "))
                if status_partida == "HT":
                    if corners_home+corners_away>bd_corners_home+bd_corners_away:
                        correcao_alertacantosHT = f'''<b>BOT-CANTOS</b>
                        
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos                        

<b>Estratégia:</b>
⛳️ Cantos LIMITE 1°Tempo

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉 <b>Resultado:</b> ✅✅✅✅'''
                        bot.edit_message_text(text=correcao_alertacantosHT , chat_id = chat_id_cantos , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_cantosht.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_cantos.get(data_atual)
                        collection_resultados_diarios_cantos.get(data_atual)['green'] = resultados_bd['green']+1
                        time.sleep(2)
                        partida_corrigida_cantosht = f'cantos HT - {item} | {corners_home} - {corners_away} | Green'
                        print(partida_corrigida_cantosht.center(50, " "))
                        
                    if corners_home+corners_away==bd_corners_home+bd_corners_away:
                        correcao_alertacantosHT = f'''<b>BOT-CANTOS</b>
                        
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos                        

<b>Estratégia:</b>
⛳️ Cantos LIMITE 1°Tempo

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

👉 <b>Resultado:</b> ❌❌❌❌ '''
                        bot.edit_message_text(text=correcao_alertacantosHT , chat_id = chat_id_cantos , message_id = bd_msg_id, parse_mode = "HTML")
                        collection_cantosht.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_cantos.get(data_atual)
                        collection_resultados_diarios_cantos.get(data_atual)['red'] = resultados_bd['red']+1
                        time.sleep(2)
                        partida_corrigida_cantosht = f'cantos HT - {item} | {corners_home} - {corners_away} | Red'
                        print(partida_corrigida_cantosht.center(50, " "))
                        
        for item in cantosFT_enviado:
            url = f"https://api.sportsanalytics.com.br/api/v1/fixtures-svc/fixtures/{item}"
            querystring = {"include":"weatherReport,additionalInfo,league,stats,pressureStats,probabilities"}
            payload = ""
            headers = {
                "cookie": "route=f69973370a0dd0883a57c7b955dfc742; SRVGROUP=common",
                "authority": "api.sportsanalytics.com.br",
                "accept": "application/json, text/plain, */*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "origin": "https://playscores.com",
                "referer": "https://playscores.com/",
                "sec-ch-ua": "^\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            if response.status_code == 200:
                dic_response = response.json()
                
                ftScore = dic_response['data'][0]['scores']['ftScore']
                status_partida = dic_response['data'][0]['status']
                minute_atual = dic_response['data'][0]['currentTime']['minute']
                corners_home = dic_response['data'][0]['stats']['corners']['home']
                corners_away = dic_response['data'][0]['stats']['corners']['away']

                resultado_bd = collection_cantosft.get(item)
                
                bd_fixtureId = resultado_bd['fixtureId']
                bd_msg_id = resultado_bd['msg_id']
                bd_homeTeam = resultado_bd['homeTeam']
                bd_awayTeam = resultado_bd['awayTeam']
                bd_league = resultado_bd['league']
                bd_minute = resultado_bd['minute']
                bd_homeTeamScore = resultado_bd['homeTeamScore']
                bd_awayTeamScore = resultado_bd['awayTeamScore']
                bd_corners_home = resultado_bd['corners_home']
                bd_corners_away = resultado_bd['corners_away']
                bd_dangerousAttacks_home = resultado_bd['dangerousAttacks_home']
                bd_dangerousAttacks_away = resultado_bd['dangerousAttacks_away']
                bd_appm1_home = resultado_bd['appm1_home']
                bd_appm1_away = resultado_bd['appm1_away']
                bd_appm2_home = resultado_bd['appm2_home']
                bd_appm2_away = resultado_bd['appm2_away']
                bd_shots_home = resultado_bd['shots_home']
                bd_shots_away = resultado_bd['shots_away']
                bd_shotsOngoal_home = resultado_bd ['shotsOngoal_home']
                bd_shotsOngoal_away = resultado_bd['shotsOngoal_away']
                bd_shotsOffgoal_home = resultado_bd['shotsOffgoal_home']
                bd_shotsOffgoal_away = resultado_bd['shotsOffgoal_away']
                
                filter = bd_fixtureId
                
                if status_partida != "FT":
                    partida_andamento_cantosft = f'cantos FT - {item} - Partida em andamento'
                    print(partida_andamento_cantosft.center(50, " "))
                if status_partida == "FT":
                    if corners_home+corners_away>bd_corners_home+bd_corners_away:
                        correcao_alertacantosFT = f'''<b>BOT-CANTOS</b>
                        
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos                        

<b>Estratégia:</b>
⛳️ Cantos LIMITE 2°Tempo

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

 
👉 <b>Resultado:</b> ✅✅✅✅'''
                        
                        bot.edit_message_text(text=correcao_alertacantosFT , chat_id = chat_id_cantos , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_cantosft.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_cantos.get(data_atual)
                        collection_resultados_diarios_cantos.get(data_atual)['green'] = resultados_bd['green']+1
                        time.sleep(2)
                        partida_corrigida_cantosft = f'cantos FT - {item} | {corners_home} - {corners_away} | Green'
                        print(partida_corrigida_cantosft.center(50, " "))
                        
                    if corners_home+corners_away==bd_corners_home+bd_corners_away:
                        correcao_alertacantosFT = f'''<b>BOT-CANTOS</b>
                        
🏟 <b>Jogo:</b> {bd_homeTeam} {bd_homeTeamScore} x {bd_awayTeamScore} {bd_awayTeam}
🏆 <b>Competição:</b> {bd_league}
🕛 <b>Tempo:</b> {bd_minute} minutos                        

<b>Estratégia:</b>
⛳️ Cantos LIMITE 2°Tempo

Estatísticas da partida:
⚔️ Ataques Perigosos p/min: {bd_appm1_home:.2f} - {bd_appm1_away:.2f}
⚔️ Ataques Perigosos 10 min: {bd_appm2_home} - {bd_appm2_away}
🥅 Remates baliza: {bd_shotsOngoal_home} - {bd_shotsOngoal_away}
❌ Remates lado: {bd_shotsOffgoal_home} - {bd_shotsOffgoal_away}
⛳️ Cantos: {bd_corners_home} - {bd_corners_away}

 
👉 <b>Resultado:</b> ❌❌❌❌''' 
                        
                        bot.edit_message_text(text=correcao_alertacantosFT , chat_id = chat_id_cantos , message_id = bd_msg_id, parse_mode = "HTML")

                        collection_cantosft.pop(filter, None)
                        resultados_bd = collection_resultados_diarios_cantos.get(data_atual)
                        collection_resultados_diarios_cantos.get(data_atual)['red'] = resultados_bd['red']+1
                        time.sleep(2)
                        partida_corrigida_cantosft = f'cantos FT - {item} | {corners_home} - {corners_away} | Red'
                        print(partida_corrigida_cantosft.center(50, " "))                        
                        
            else:
                print("RETORNO DA API FALHOU AGUARDANDO 60 SEGUNDOS PARA TENTAR NOVAMENTE 2")
                time.sleep(60)

        print("")
        lista_correcao = " PROCESSOS DE ANALISE E CORREÇÕES ENCERRADAS, PRÓXIMA ANALISE EM 60 SEGUNDOS "
        print(lista_correcao.center(50, "#"))
        print("")

        time.sleep(60)
        #os.system("cls")
        #except Exception as e:
        #traceback.print_exc()
        #pass