from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import test
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import requests
from bs4 import BeautifulSoup
import re


numbers = []
class NumberApp(App):

    def build(self):
        # 主要布局容器
        self.layout = BoxLayout(orientation="vertical")
        
        # 用于存储输入框的列表
        self.text_inputs = []
        
        # 添加初始输入框
        self.add_field(None)

        # 添加和提交按钮
        btn_layout = BoxLayout()
        add_button = Button(text="Add Field")
        add_button.bind(on_press=self.add_field)
        btn_layout.add_widget(add_button)

        submit_button = Button(text="Submit")
        submit_button.bind(on_press=self.display_numbers)
        btn_layout.add_widget(submit_button)

        self.layout.add_widget(btn_layout)

        # 用于显示结果的标签
        self.result_label = Label()
        self.layout.add_widget(self.result_label)
        
        return self.layout

    def add_field(self, instance):
        new_text_input = TextInput(hint_text="Enter a number", multiline=False, input_filter='float')
        self.text_inputs.append(new_text_input)  # 将新输入框添加到列表的末尾
        self.layout.add_widget(new_text_input, index=2)  # 在按钮之前插入新输入框


    def display_numbers(self, instance):
        for text_input in self.text_inputs:
            if text_input.text:  # 检查输入是否为空
                numbers.append(text_input.text)
        self.result_label.text = ", ".join(numbers)
        print("fdghjdkshkljlsjsfdfdfd")
        test.run_func(numbers) #******important part********
        print("fdghjdkdsf328323233223shkljlsjsfdfdfd")
        # 将数据写入txt文件
        with open('numbers.txt', 'w') as file:
            for number in numbers:
                file.write(number + '\n')  # 每个数字占一行

        # 创建并显示完成的弹出窗口
        popup = Popup(title='Completed', content=Label(text='Data generation completed!'),
                    size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    NumberApp().run()
