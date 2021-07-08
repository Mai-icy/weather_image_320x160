#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import re
import datetime
from PIL import Image, ImageDraw, ImageFont


class WeatherApi(object):
    def __init__(self):
        self.url = 'http://wthrcdn.etouch.cn/weather_mini?city='
        self.ttf_path = '..\\Requirement\\font\\simhei.ttf'

    def get_weather(self, location):
        request_url = self.url + str(location)
        back_data = requests.get(request_url)
        json_weather = json.loads(back_data.text)
        return json_weather['data']

    def process_data(self):
        json_weather = self.get_weather('上海')['data']
        tips = json_weather['ganmao']
        temperature_now = json_weather['wendu']
        weather_forecast = json_weather['forecast']
        # m = re.findall("\d+", weather_forecast[1]['high'])[0]
        return tips, temperature_now, weather_forecast

    def img_crate(self, json_weather, location):
        column = 1
        back_ground = Image.open('..\\Requirement\\background\\weather\\dark.png')
        data_today = json_weather["forecast"][0]
        day_type = data_today['type']
        if day_type == '晴' or day_type == '多云':
            back_ground = Image.open('..\\Requirement\\background\\weather\\bright.png')
        month = datetime.datetime.now().month
        img_draw = ImageDraw.Draw(back_ground)
        for i in range(1, 5):
            data = json_weather["forecast"][i]
            week = '周' + data['date'][-1]
            date = re.findall(r'\d+日', data['date'])[0]
            if int(re.findall(r'\d+', data['date'])[0]) == 1:
                month = month + 1
            date = str(month) + '月' + date
            day_type = data['type']
            high = re.findall(r'\d+℃', data['high'])[0]
            low = int(re.findall(r'\d+', data['low'])[0])
            if low < 10:
                low = ' '+str(low)
            temperature = str(low) + '-' + high
            day_text = data['type']
            if day_type == '阴' or day_type == '晴':
                day_type = ' ' + day_type
            try:
                day_img = Image.open('..\\Requirement\\img\\small_weather_img\\' + day_text + '.png')
            except FileNotFoundError:
                day_img = Image.open('..\\Requirement\\img\\small_weather_img\\NA.png')
            back_ground.paste(day_img, (47 + 52 * column, 57), day_img)
            ttf = ImageFont.truetype(self.ttf_path, 10)
            img_draw.text((49 + 52 * column, 94), temperature, font=ttf, fill=(255, 255, 255))
            img_draw.text((49 + 52 * column, 45), date, font=ttf, fill=(183, 183, 183))
            ttf = ImageFont.truetype(self.ttf_path, 15)
            img_draw.text((50 + 52 * column, 106), day_type, font=ttf, fill=(255, 255, 255))
            ttf = ImageFont.truetype(self.ttf_path, 16)
            img_draw.text((51 + 52 * column, 29), week, font=ttf, fill=(255, 255, 255))
            column = column + 1
        day_type = data_today['type']
        high = re.findall(r'\d+℃', data_today['high'])[0]
        low = int(re.findall(r'\d+', data_today['low'])[0])
        if low < 10:
            low = ' ' + str(low)
        temperature = str(low) + '-' + high
        day_text = data_today['type']
        try:
            day_img = Image.open('..\\Requirement\\img\\big_weather_img\\' + day_text + '.png')
        except FileNotFoundError:
            day_img = Image.open('..\\Requirement\\img\\big_weather_img\\NA.png')
        tem_now = json_weather['wendu']
        if int(tem_now) < 10:
            tem_now = ' ' + tem_now
        tips = json_weather['ganmao']  # 插入换行符
        tips = tips[0:21] + '\n' + tips[21:-1]
        ttf = ImageFont.truetype(self.ttf_path, 14)
        img_draw.text((58, 77), '℃', font=ttf, fill=(255, 255, 255))
        img_draw.text((59, 94), day_type, font=ttf, fill=(255, 255, 255))
        ttf = ImageFont.truetype(self.ttf_path, 39)
        img_draw.text((18, 75), tem_now, font=ttf, fill=(255, 255, 255))
        ttf = ImageFont.truetype(self.ttf_path, 12)
        img_draw.text((22, 128), 'tip:' + tips + '(天气仅供参考,请以实际为准哦qwq)', font=ttf, fill=(240, 240, 240))
        img_draw.text((35, 109), temperature, font=ttf, fill=(255, 255, 255))
        ttf = ImageFont.truetype(self.ttf_path, 21)
        img_draw.text((8, 3), location, font=ttf, fill=(255, 255, 255))
        back_ground.paste(day_img, (18, 30), day_img)
        back_ground.show()
        # back_ground.save('your path')


if __name__ == "__main__":
    a = WeatherApi()
    location = '北京'
    a.img_crate(a.get_weather(location), location)
