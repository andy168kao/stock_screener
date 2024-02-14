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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput



class NumberApp(App):

    def build(self):
        # 主要布局容器
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # 用于存储输入框的列表
        self.text_inputs = []
        self.spinners = []
        
        # 添加初始输入框
        self.add_field(None)

        # 添加和提交按钮
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
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
        # Create a horizontal BoxLayout
        hbox = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        # Create a new text input
        new_text_input = TextInput(hint_text="Enter a number", multiline=False, input_filter='float', size_hint_x=0.5)
        self.text_inputs.append(new_text_input)
        # Create a dropdown menu (Spinner)
        spinner = Spinner(
            # Provide a list of values for the dropdown
            values=('Listed Stock', 'OTC Stock'),
            size_hint_x=0.5,
            text='Select an option'
        )
        self.spinners.append(spinner)
        # Bind the on_text event of the spinner to a callback function

        # Add the text input and spinner to the horizontal BoxLayout
        hbox.add_widget(new_text_input)
        hbox.add_widget(spinner)
        
        # Add the horizontal BoxLayout to the main layout
        self.layout.add_widget(hbox, index=2)  # Adjust index as needed

    def display_numbers(self, instance):
        numbers = []
        print("Starting to collect numbers...")  # Debugging message
        for text_input, spinner in zip(self.text_inputs, self.spinners):
            
            print(f"TextInput: '{text_input}', Spinner: '{spinner}'")  # Debugging message
            if text_input.text:  # 检查输入是否为空
                numbers.append((text_input.text, spinner.text))
                
            else:
                print("Found an empty TextInput.")  # Debugging message
        # self.result_label.text = ", ".join(numbers)
        if not numbers:
                print("No data collected. Ensure TextInputs are filled.")  # Debugging message
        else:
            # Assuming you want to see the tuples printed out
            for num in numbers:
                print(num)  # This will print each tuple in the list

        # This line will print the entire list (which might be empty if no inputs were filled)
        print("Collected numbers:", numbers)  # Debugging message
        test.run_func(numbers) #******important part********
        print("fdghjdkdsf328323233223shkljlsjsfdfdfd")
        # 将数据写入txt文件
        # with open('numbers.txt', 'w') as file:
        #     for number in numbers:
        #         file.write(number + '\n')  # 每个数字占一行

        # # 创建并显示完成的弹出窗口
        # popup = Popup(title='Completed', content=Label(text='Data generation completed!'),
        #             size_hint=(None, None), size=(400, 200))
        # popup.open()

if __name__ == '__main__':
    NumberApp().run()
    #12312332