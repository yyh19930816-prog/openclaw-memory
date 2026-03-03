#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoReplier - AI自动回复微信消息程序
Source: XingYuan55/autoreplier (https://github.com/XingYuan55/autoreplier)
Date: 2023-11-30
Description: 监控微信消息并通过AI自动回复的核心功能实现
"""

import time
import win32clipboard
import pyautogui
import pygetwindow as gw
from PIL import ImageGrab

class ChatWindow:
    """封装微信聊天窗口的基本操作"""
    
    def __init__(self, window_title="微信"):
        """初始化聊天窗口"""
        self.window_title = window_title
        self.window = None
        self._locate_window()
        
    def _locate_window(self):
        """定位微信窗口"""
        try:
            self.window = gw.getWindowsWithTitle(self.window_title)[0]
            self.window.activate()
            time.sleep(0.5)
        except IndexError:
            raise Exception("微信窗口未找到，请确保微信已打开")
            
    def get_last_message(self):
        """获取最后一条消息文本"""
        # 模拟Ctrl+A和Ctrl+C复制消息
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.3)
        
        try:
            win32clipboard.OpenClipboard()
            message = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return message.strip()
        except:
            return ""
            
    def send_message(self, text):
        """发送消息到聊天窗口"""
        # 将文本复制到剪贴板
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
        
        # 粘贴并发送
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(0.5)

class ChatSession:
    """管理完整的聊天会话流程"""
    
    def __init__(self):
        """初始化会话"""
        self.chat_window = ChatWindow()
        self.ai_model = SimpleAIModel()
        
    def process_new_message(self):
        """处理新消息并回复"""
        message = self.chat_window.get_last_message()
        if not message:
            return
            
        print(f"收到消息: {message}")
        reply = self.ai_model.generate_reply(message)
        print(f"发送回复: {reply}")
        self.chat_window.send_message(reply)
        
    def run(self, interval=3):
        """运行自动回复主循环"""
        print("自动回复程序已启动，按Ctrl+C停止...")
        try:
            while True:
                self.process_new_message()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n程序已停止")

class SimpleAIModel:
    """简单的AI回复模型"""
    
    def generate_reply(self, message):
        """生成回复文本（简化版）"""
        # 这里可以替换为真实AI模型接口
        responses = [
            "好的，我明白了",
            "这是个好问题，让我想想",
            "请稍等，我正在处理",
            "您的消息已收到",
            "感谢您的联系"
        ]
        return f"[自动回复] {responses[len(message) % len(responses)]}"

if __name__ == "__main__":
    # 主程序入口
    session = ChatSession()
    session.run()