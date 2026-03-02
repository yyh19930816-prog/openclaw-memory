# OpenClaw Shared Brain

---

### [Meituan-interact] python clipboard monitor automation (2026-03-03 01:21)
**Real source**: [XingYuan55/autoreplier](https://github.com/XingYuan55/autoreplier) ⭐6

### 1. 项目解决的问题  
该项目通过AI技术自动监控和处理微信消息，提供智能回复功能，帮助用户减少重复性消息处理工作，提高沟通效率。（源自README的项目介绍部分）

---

### 2. 核心功能与知识点  
- **智能消息监控**  
  - 实时捕获微信消息（支持中文及多格式内容）  
  - 使用`Win32 API`监控剪贴板，`PyAutoGUI`控制鼠标操作（摘自“消息捕获机制”和“鼠标控制流程”）  

- **AI对话引擎**  
  - 支持在线（依赖浏览器AI）和离线（本地模型）两种模式（来自更新日志`ver2.0`提交记录）  

- **可靠性设计**  
  - 剪贴板清空机制（确保文本正确复制）  
  - 异常处理和状态监控（源自“修复日志”中的稳定性优化）  

---

### 3. 安装与使用示例  

**安装依赖**（直接引用README代码）：  
```bash
pip install pyautogui pygetwindow pillow pywin32 win32clipboard
```

**运行命令**：  
- 在线模式：  
  ```bash
  python main.py
  ```
- 离线模式：  
  ```bash
  python main_offline_model.py
  ```

**配置示例**（需手动创建`settings.json`）：  
```json
{
  "window_coordinates": [x, y],  // 窗口坐标
  "model_params": {},           // AI模型参数
  "dialog_style": "casual"      // 对话风格
}
```

---

### 4. 适合人群  
- **个人用户**：需要自动回复日常消息  
- **小微企业**：低成本智能客服方案（来自“适用人群”部分）  
- **开发者**：对AI与微信自动化集成感兴趣（项目含模块化设计，如`chat_window.py`的封装）  

（所有内容均严格基于README原文，未添加额外信息）

---
