import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

def get_youtube_search(query,order,regionCode,channel_id = ''):
    import os

    import google_auth_oauthlib.flow
    import googleapiclient.discovery
    import googleapiclient.errors

    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
    
    if channel_id == '':
        request = youtube.search().list(
                part="snippet",
                maxResults=50,
                order=order,
                q=query,
                regionCode=regionCode
            )
    else:
        request = youtube.search().list(
                part="snippet",
                maxResults=50,
                channelId=channel_id,
                order=order,
                q=query,
                regionCode=regionCode
            )
    
    response = request.execute()
    
    return response
  
#-----------Россия 24-------------
  
search_result_1 = get_youtube_search(query = "Россия 24", order = "viewCount", regionCode = "RU")
search_result_1_df = pd.DataFrame(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU",channel_id = 'UC_IEcnNeHc_bwd92Ber-lew')
search_result_2_df = pd.DataFrame(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU",channel_id = 'UC_IEcnNeHc_bwd92Ber-lew')
search_result_3_df = pd.DataFrame(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU",channel_id = 'UC_IEcnNeHc_bwd92Ber-lew')
search_result_4_df = pd.DataFrame(search_result_4['items'])


data_for_wordcloud = []

for i in range(2,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split(' - Россия 24')[0]
    data_for_wordcloud.append(title)

for i in range(2,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split(' - Россия 24')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split(' Специальный репортаж')[0]
    data_for_wordcloud.append(title)
    
    
for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split(' - Россия 24')[0]
    data_for_wordcloud.append(title)
    
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace(' - россия 24','')
    title = title.replace('россия 24','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('александра сладкова','')
    title = title.replace('москва 24','')
    title = title.replace('москва. кремль. кутин','')
    title = title.replace('// . от 07.03.2021','')
    title = title.replace('авторская программа Аркадия Мамонтова','')
    title = title.replace('марата кримчеева','')
    title = title.replace('фильм анны афанасьевой','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('репортаж','')
    title = title.replace('интервью','')
    title = title.replace('программа','')
    title = title.replace('эксклюзивный','')
    title = title.replace('дежурная часть','')
    title = title.replace('вести недели с дмитрием киселевым','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('путина','путин')
    title = title.replace('россии','россия')
    title = title.replace('китая','китай')
    title = title.replace('донбассе','донбасс')
    title = title.replace('карабахе','карабах')
    data_for_wordcloud_preprocessed.append(title)
    
data_for_wordcloud_preprocessed_string_r24 = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_r24 = data_for_wordcloud_preprocessed_string_r24 + title + ' '    
  
  
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="red").generate(data_for_wordcloud_preprocessed_string_r24)

wordcloud.to_file("Russia24_WordCloud.png")



#-----------RT на русском-------------

search_result_1 = get_youtube_search(query = "RT на русском", order = "viewCount", regionCode = "RU")
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UCFU30dGHNhZ-hkh0R10LhLw')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UCFU30dGHNhZ-hkh0R10LhLw')
search_result_3_df = pd.DataFrame.from_dict(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU", channel_id = 'UCFU30dGHNhZ-hkh0R10LhLw')
search_result_4_df = pd.DataFrame.from_dict(search_result_4['items'])


data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split(' / ')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split(' / ')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split(' / ')[0]
    data_for_wordcloud.append(title)

for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split(' / ')[0]
    data_for_wordcloud.append(title)
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('новости','')
    title = title.replace('репортаж','')
    title = title.replace('репортаж','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('россии','россия')
    title = title.replace('путина','путин')
    title = title.replace('путин:','путин')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('украинские','украина')
    title = title.replace('украинской','украина')
    title = title.replace('украине','украина')
    title = title.replace('украину','украина')
    title = title.replace('украины','украина')
    title = title.replace(': ',' ')
    data_for_wordcloud_preprocessed.append(title)
    
data_for_wordcloud_preprocessed_string_rt = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_rt = data_for_wordcloud_preprocessed_string_rt + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="green").generate(data_for_wordcloud_preprocessed_string_rt)    

wordcloud.to_file("RT_WordCloud.png")


#-----------Телеканал Дождь-------------

search_result_1 = get_youtube_search(query = "Телеканал Дождь", order = "viewCount", regionCode = "RU")
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UCdubelOloxR3wzwJG9x8YqQ')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UCdubelOloxR3wzwJG9x8YqQ')
search_result_3_df = pd.DataFrame.from_dict(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU", channel_id = 'UCdubelOloxR3wzwJG9x8YqQ')
search_result_4_df = pd.DataFrame.from_dict(search_result_4['items'])

data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split(' /')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split(' /')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split(' /')[0]
    data_for_wordcloud.append(title)

for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split(' /')[0]
    data_for_wordcloud.append(title)
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('"','')
    title = title.replace('репортаж','')
    title = title.replace('репортаж','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('россии','россия')
    title = title.replace('путина','путин')
    title = title.replace('навального','навальный')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('беларуси','беларусь')
    title = title.replace(': ',' ')
    data_for_wordcloud_preprocessed.append(title)

data_for_wordcloud_preprocessed_string_rain = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_rain = data_for_wordcloud_preprocessed_string_rain + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="purple").generate(data_for_wordcloud_preprocessed_string_rain)

wordcloud.to_file("TvRain_WordCloud.png")


#-----------DW на русском-------------

search_result_1 = get_youtube_search(query = "DW на русском", order = "viewCount", regionCode = "RU")
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UCXoAjrdHFa2hEL3Ug8REC1w')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UCXoAjrdHFa2hEL3Ug8REC1w')
search_result_3_df = pd.DataFrame.from_dict(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU", channel_id = 'UCXoAjrdHFa2hEL3Ug8REC1w')
search_result_4_df = pd.DataFrame.from_dict(search_result_4['items'])


data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split('DW Новости')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split('DW Новости')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split('DW Новости')[0]
    data_for_wordcloud.append(title)

for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split('DW Новости')[0]
    data_for_wordcloud.append(title)
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('"','')
    title = title.replace('репортаж','')
    title = title.replace('dw','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('россии','россия')
    title = title.replace('путина','путин')
    title = title.replace('путину','путин')
    title = title.replace('москве','москва')
    title = title.replace('москву','москва')
    title = title.replace('навального','навальный')
    title = title.replace('навальным','навальный')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('беларуси','беларусь')
    title = title.replace('германии','германия')
    title = title.replace('германию','германия')
    title = title.replace('кремля','кремль')
    title = title.replace('санкций','санкции')
    title = title.replace(': ',' ')
    data_for_wordcloud_preprocessed.append(title)
    
data_for_wordcloud_preprocessed_string_dw = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_dw = data_for_wordcloud_preprocessed_string_dw + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="blue").generate(data_for_wordcloud_preprocessed_string_dw) 

wordcloud.to_file("DW_WordCloud.png")


#-----------Настоящее Время-------------


search_result_1 = get_youtube_search(query = "Настоящее Время", order = "viewCount", regionCode = "RU", channel_id = 'UCBG57608Hukev3d0d-gvLhQ')
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UCBG57608Hukev3d0d-gvLhQ')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UCBG57608Hukev3d0d-gvLhQ')
search_result_3_df = pd.DataFrame.from_dict(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU", channel_id = 'UCBG57608Hukev3d0d-gvLhQ')
search_result_4_df = pd.DataFrame.from_dict(search_result_4['items'])

data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split('|')[0]
    data_for_wordcloud.append(title)

for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('"','')
    title = title.replace('репортаж','')
    title = title.replace('dw','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('россии','россия')
    title = title.replace('путина','путин')
    title = title.replace('путину','путин')
    title = title.replace('москве','москва')
    title = title.replace('москву','москва')
    title = title.replace('навального','навальный')
    title = title.replace('навальным','навальный')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('беларуси','беларусь')
    title = title.replace('германии','германия')
    title = title.replace('германию','германия')
    title = title.replace('кремля','кремль')
    title = title.replace('санкций','санкции')
    title = title.replace('таджикистана','таджикистан')
    title = title.replace('таджикистане','таджикистан')
    title = title.replace('казахстана','казахстан')
    title = title.replace('казахстане','казахстан')
    title = title.replace('кыргызстана','кыргызстан')
    title = title.replace('кыргызстане','кыргызстан')
    title = title.replace('хабаровского','хабаровск')
    title = title.replace('хабаровске','хабаровск')
    title = title.replace(': ',' ')
    title = title.replace('.',' ')
    data_for_wordcloud_preprocessed.append(title)
    
    
data_for_wordcloud_preprocessed_string_nt = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_nt = data_for_wordcloud_preprocessed_string_nt + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "darkblue",
                      relative_scaling=0.5,
                      background_color="white").generate(data_for_wordcloud_preprocessed_string_nt)

wordcloud.to_file("NT_WordCloud.png")


#-----------Новости на Первом канале-------------


search_result_1 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UCKonxxVHzDl55V7a9n_Nlgg')
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UCKonxxVHzDl55V7a9n_Nlgg')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    if 'Выпуск ' not in title:
        data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    if 'Выпуск ' not in title:
        data_for_wordcloud.append(title)
    
    
data_for_wordcloud_set = set(data_for_wordcloud)


data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('эксклюзивное интервью','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('"','')
    title = title.replace('репортаж','')
    title = title.replace('dw','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace('как',' ')
    title = title.replace('россии','россия')
    title = title.replace('путина','путин')
    title = title.replace('путину','путин')
    title = title.replace('москве','москва')
    title = title.replace('москву','москва')
    title = title.replace('первому','')
    title = title.replace('первого','')
    title = title.replace('канала','')
    title = title.replace('каналу','')
    title = title.replace('навального','навальный')
    title = title.replace('навальным','навальный')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('беларуси','беларусь')
    title = title.replace('германии','германия')
    title = title.replace('германию','германия')
    title = title.replace('кремля','кремль')
    title = title.replace('санкций','санкции')
    title = title.replace('таджикистана','таджикистан')
    title = title.replace('таджикистане','таджикистан')
    title = title.replace('казахстана','казахстан')
    title = title.replace('казахстане','казахстан')
    title = title.replace('кыргызстана','кыргызстан')
    title = title.replace('кыргызстане','кыргызстан')
    title = title.replace('хабаровского','хабаровск')
    title = title.replace('хабаровске','хабаровск')
    title = title.replace(': ',' ')
    title = title.replace('.',' ')
    data_for_wordcloud_preprocessed.append(title)


data_for_wordcloud_preprocessed_string_tv1 = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_tv1 = data_for_wordcloud_preprocessed_string_tv1 + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="darkblue").generate(data_for_wordcloud_preprocessed_string_tv1)

wordcloud.to_file("TV1_WordCloud.png")


#-----------BBC News - Русская служба-------------
    

search_result_1 = get_youtube_search(query = "BBC News - Русская служба", order = "viewCount", regionCode = "RU", channel_id = 'UC8zQiuT0m1TELequJ5sp5zw')
search_result_1_df = pd.DataFrame.from_dict(search_result_1['items'])

search_result_2 = get_youtube_search(query = "", order = "viewCount", regionCode = "RU", channel_id = 'UC8zQiuT0m1TELequJ5sp5zw')
search_result_2_df = pd.DataFrame.from_dict(search_result_2['items'])

search_result_3 = get_youtube_search(query = "репортаж", order = "viewCount", regionCode = "RU", channel_id = 'UC8zQiuT0m1TELequJ5sp5zw')
search_result_3_df = pd.DataFrame.from_dict(search_result_3['items'])

search_result_4 = get_youtube_search(query = "новости", order = "viewCount", regionCode = "RU", channel_id = 'UC8zQiuT0m1TELequJ5sp5zw')
search_result_4_df = pd.DataFrame.from_dict(search_result_4['items'])

data_for_wordcloud = []

for i in range(1,search_result_1_df.shape[0]):
    title = search_result_1_df.snippet[i]['title']
    title = title.split('- BBC Russian')[0]
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_2_df.shape[0]):
    title = search_result_2_df.snippet[i]['title']
    title = title.split('- BBC Russian')[0]
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
for i in range(1,search_result_3_df.shape[0]):
    title = search_result_3_df.snippet[i]['title']
    title = title.split('- BBC Russian')[0]
    title = title.split('|')[0]
    data_for_wordcloud.append(title)

for i in range(1,search_result_4_df.shape[0]):
    title = search_result_4_df.snippet[i]['title']
    title = title.split('- BBC Russian')[0]
    title = title.split('|')[0]
    data_for_wordcloud.append(title)
    
data_for_wordcloud_set = set(data_for_wordcloud)

data_for_wordcloud_preprocessed = []
for title in data_for_wordcloud_set:
    title = title.lower()
    title = title.replace('&quot;','')
    title = title.replace('специальный репортаж','')
    title = title.replace('документальный фильм','')
    title = title.replace('последние','')
    title = title.replace('новости','')
    title = title.replace('"','')
    title = title.replace('репортаж','')
    title = title.replace('dw','')
    title = title.replace(' на ',' ')
    title = title.replace(' не ',' ')
    title = title.replace(' из ',' ')
    title = title.replace(' за ',' ')
    title = title.replace(' для ',' ')
    title = title.replace(' по ',' ')
    title = title.replace(' от ',' ')
    title = title.replace(' под ',' ')
    title = title.replace('россии','россия')
    title = title.replace('российские','россия')
    title = title.replace('путина','путин')
    title = title.replace('путину','путин')
    title = title.replace('москве','москва')
    title = title.replace('москву','москва')
    title = title.replace('навального','навальный')
    title = title.replace('навальным','навальный')
    title = title.replace('владимира','владимир')
    title = title.replace('коронавируса','коронавирус')
    title = title.replace('беларуси','беларусь')
    title = title.replace('германии','германия')
    title = title.replace('германию','германия')
    title = title.replace('кремля','кремль')
    title = title.replace('санкций','санкции')
    title = title.replace('таджикистана','таджикистан')
    title = title.replace('таджикистане','таджикистан')
    title = title.replace('казахстана','казахстан')
    title = title.replace('казахстане','казахстан')
    title = title.replace('кыргызстана','кыргызстан')
    title = title.replace('кыргызстане','кыргызстан')
    title = title.replace('хабаровского','хабаровск')
    title = title.replace('хабаровске','хабаровск')
    title = title.replace('дагестана','дагестан')
    title = title.replace('карабахе','карабах')
    title = title.replace('армении','армения')
    title = title.replace('коронавирусом','коронавирус')
    title = title.replace('как ',' ')
    title = title.replace('что ',' ')
    title = title.replace('почему ',' ')
    title = title.replace(' его ',' ')
    title = title.replace('войны','война')
    title = title.replace(': ',' ')
    title = title.replace('би-би-си',' ')
    title = title.replace('кадырова','кадыров')
    title = title.replace('рамзана','')
    data_for_wordcloud_preprocessed.append(title)

data_for_wordcloud_preprocessed_string_bbc = ''
for title in data_for_wordcloud_preprocessed:
    data_for_wordcloud_preprocessed_string_bbc = data_for_wordcloud_preprocessed_string_bbc + title + ' '
    
wordcloud = WordCloud(width = 1000, 
                      height = 500, 
                      max_font_size=400, 
                      max_words=200,
                      color_func=lambda *args, **kwargs: "white",
                      relative_scaling=0.5,
                      background_color="darkred").generate(data_for_wordcloud_preprocessed_string_bbc)

wordcloud.to_file("BBC_WordCloud.png")


    
