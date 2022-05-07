# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
import base64
import re 
import asyncio
import aiohttp

async def get_room(taskHash):
    url = f"https://api-edu.skysmart.ru/api/v1/task/preview"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTE2ODQ2MzQsImV4cCI6MTY1NDI3NjYzNCwicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJhdXRoVXNlcklkIjoxNTMyOTA5MiwidXNlcklkIjo1ODM2MzMxMCwiZW1haWwiOm51bGwsIm5hbWUiOiLQkNGA0YLRkdC8INChIiwic3VybmFtZSI6bnVsbCwiaWRlbnRpdHkiOiJiYWJlbWVkb3pvIn0.eyosslDChDC59he0Gef_bJaYbtkftwAYQB3U39daN89tOMLCQMMzepQjXaKOKEtIV6U2Q6fMt5Z1BqMPWJglNtTF7yLcOTD4GdNQlreXNXd1agFgwfLaTa7K9JK22CdueLyHffus2kah93b0G8JC54yr2M6JtbjVaInID4Zzholz-3IRYNkDrrvdmUmp7wW8T9AqQ4FoS2LHRubj3Wkz-CHi6px4QXGrQmdQX0-_i-so1cX8VVc9pYjw0oALxHdlEsrz89Jg944BPfeIoiNeeCeda6n1Nt78g_0cz3AX0MphcrT7pJoky6zSbPafdxP1xxlJfhbVQH95H4QhqwAGoZZpdcqgXvA5zfX-zbWLA5G4S6SqTdFZAClgWDi5oGzys1VkKQ0HjlZx9lfAGE3KDRzyKesch7bgvU5aCrdfkVdhByYJtXKXy1QhkKkwBT0Qd4QqGbTAlWUbNQzFCyuyK8pKPMMxxK_7mtxb_57IPtaS_-H80pH-qmNO_PG2ChjpzaIaEFGo_Um2CbvYgdFMyjLYLs1DGrRpKJSZ4CBUInGzI2pmIM_ZT7ifrj8yPOMzDKiuOpKxDT6TsVLGqgGpnJfcBz_sCQ0hyKj5OtqVf4vDbaPuDVRR7u4FWq2V84_mAxfUc_GD8DCMLXY3rHUCq5nFtVvkeSDp05SVRGe2jfo',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Accept:': 'application/json, text/plain, */*'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            steps_raw = await resp.json() 
            print(steps_raw)
            await session.close()
            return steps_raw['meta']['stepUuids'] # все uuid заданий
            
async def get_json_html(uuid):
    url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTE2ODQ2MzQsImV4cCI6MTY1NDI3NjYzNCwicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJhdXRoVXNlcklkIjoxNTMyOTA5MiwidXNlcklkIjo1ODM2MzMxMCwiZW1haWwiOm51bGwsIm5hbWUiOiLQkNGA0YLRkdC8INChIiwic3VybmFtZSI6bnVsbCwiaWRlbnRpdHkiOiJiYWJlbWVkb3pvIn0.eyosslDChDC59he0Gef_bJaYbtkftwAYQB3U39daN89tOMLCQMMzepQjXaKOKEtIV6U2Q6fMt5Z1BqMPWJglNtTF7yLcOTD4GdNQlreXNXd1agFgwfLaTa7K9JK22CdueLyHffus2kah93b0G8JC54yr2M6JtbjVaInID4Zzholz-3IRYNkDrrvdmUmp7wW8T9AqQ4FoS2LHRubj3Wkz-CHi6px4QXGrQmdQX0-_i-so1cX8VVc9pYjw0oALxHdlEsrz89Jg944BPfeIoiNeeCeda6n1Nt78g_0cz3AX0MphcrT7pJoky6zSbPafdxP1xxlJfhbVQH95H4QhqwAGoZZpdcqgXvA5zfX-zbWLA5G4S6SqTdFZAClgWDi5oGzys1VkKQ0HjlZx9lfAGE3KDRzyKesch7bgvU5aCrdfkVdhByYJtXKXy1QhkKkwBT0Qd4QqGbTAlWUbNQzFCyuyK8pKPMMxxK_7mtxb_57IPtaS_-H80pH-qmNO_PG2ChjpzaIaEFGo_Um2CbvYgdFMyjLYLs1DGrRpKJSZ4CBUInGzI2pmIM_ZT7ifrj8yPOMzDKiuOpKxDT6TsVLGqgGpnJfcBz_sCQ0hyKj5OtqVf4vDbaPuDVRR7u4FWq2V84_mAxfUc_GD8DCMLXY3rHUCq5nFtVvkeSDp05SVRGe2jfo',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Accept:': 'application/json, text/plain, */*'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            answer_row = await resp.json()
            await session.close()
    return BeautifulSoup(answer_row['content'], 'html.parser')


async def answerparse(taskHash):
    x = 0
    results = []
    # ---- получение uuid заданий в тесте ----#
    
    # ---- тут получаем html в json ----#
    allsteps = await get_room(taskHash)
    random = False # проверка на рандомные задания
    for uuid in allsteps:
        print(uuid)
        x = x + 1
        soup = await get_json_html(uuid)
        try:
            anstitlerow = f'`№{x}📝Вопрос: ' + (soup.find('vim-instruction').text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        except:
            try:
                anstitlerow = f'`№{x}📝Вопрос: ' + (soup.find('vim-content-section-title').text.replace('\n', ' ')).replace('\r',' ')
                results.append(anstitlerow)
            except:
                try:
                    anstitlerow = f'`№{x}📝Вопрос: ' + (soup.find('vim-text').text.replace('\n', ' ')).replace('\r',' ')
                    results.append(anstitlerow)
                except:
                    anstitlerow = f'`№{x}📝Вопрос'
                    results.append(anstitlerow)
        # а тут много циклов,каждый цикл это разные типы заданий,знаю стремно,но мне лень переделывать
        if random:
            results.append('Это задание рандомное! Ответы могут не совпадать!')
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-order-sentence-verify-item'):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-input-answers'):            
            j = i.find('vim-input-item')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            results.append(f'{i.text} - Верный')
        for i in soup.find_all('math-input'):
            j = i.find('math-input-answer')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-dnd-text-drop'):
            for f in soup.find_all('vim-dnd-text-drag'):
                if i['drag-ids'] == f['answer-id']:
                    results.append(f'{await ochistka(f.text)}')
        for i in soup.find_all('vim-dnd-group-drag'):
            for f in soup.find_all('vim-dnd-group-item'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{await ochistka(f.text)} - {await ochistka(i.text)}')
        for i in soup.find_all('vim-groups-row'):
            for l in i.find_all('vim-groups-item'):
                try:
                    a = base64.b64decode(l['text']) 
                    results.append(f"{await ochistka(a.decode('utf-8'))}")   
                except:
                    pass
        for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-dnd-image-set-drag'):
            for f in soup.find_all('vim-dnd-image-set-drop'):
                if i['answer-id'] in f['drag-ids']:
                    image = await ochistka(f['image'])
                    text = await ochistka(i.text)
                    results.append(f'{image} - {text}')
        for i in soup.find_all('vim-dnd-image-drag'):
            for f in soup.find_all('vim-dnd-image-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
    
    return results

async def ochistka(string):
    string = string.replace('\n', '')
    string = '→ ' + string
    fraction = re.compile("dfrac{(.*?)}{(.*?)}")
    square_root = re.compile("sqrt{(.*?)}")
    power = re.compile("(.*?)\^(.*)")
    bol = re.compile("gt")
    men = re.compile("lt")
    pm = re.compile('pm')
    perp = re.compile('perp')
    menrav = re.compile('le')
    bolrav = re.compile('ge')
    syst = re.compile('begin{cases}')
    systend = re.compile('end{cases}')
    him = re.compile('mathrm{(.*?)}')
    dot = re.compile('cdot')
    strel = re.compile('rarr')
    pi = re.compile('pi')
    besk = re.compile('infty')
    for i in him.findall(string):
        string = string.replace("\mathrm{" + str(i) + "}", str(i))
    for i in fraction.findall(string):
        string = string.replace("\dfrac{" + str(i[0]) + "}{" + str(i[1]) + "}", str(i[0]) + "/" + str(i[1]))

    for i in square_root.findall(string):
        string = string.replace("\sqrt{" + str(i) + "}", "корень из " + str(i))

    for i in power.findall(string):
        string = string.replace(str(i[0]) + "^" + str(i[1]), str(i[0]) + " ^ " + str(i[1]))

    for i in bol.findall(string):
        string = string.replace("\gt", ">")
    for i in men.findall(string):
        string = string.replace("\lt", "<")
    for i in pm.findall(string):
        string = string.replace("\pm", "±")
    for i in perp.findall(string):
        string = string.replace("\perp", "⊥")
    for i in menrav.findall(string):
        string = string.replace("\le", "≤")
    for i in bolrav.findall(string):
        string = string.replace("\ge", "≥")
    for i in syst.findall(string):
        string = string.replace(r"\begin{cases}", "{")
    for i in systend.findall(string):
        string = string.replace("\end{cases}", "}")
    for i in dot.findall(string):
        string = string.replace(r"\cdot", " ⋅")
    for i in strel.findall(string):
        string = string.replace(r"\rarr", " →")
    for i in pi.findall(string):
        string = string.replace(r"\pi", "π")
    for i in besk.findall(string):
        string = string.replace(r"\infty", "∞")
    return string