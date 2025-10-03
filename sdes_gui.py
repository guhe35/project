"""
S-DES图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from sdes_algorithm import SDES


class SDESGUI:
    """S-DES图形界面类"""
    
    def __init__(self):
        self.sdes = SDES()
        self.root = tk.Tk()
        self.root.title("S-DES加密解密工具 v2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 暴力破解相关变量
        self.brute_force_thread = None
        self.stop_brute_force = False
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 9), foreground='#7f8c8d')
        style.configure('Success.TLabel', font=('Arial', 10), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#e74c3c')
        
        # 按钮样式
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Arial', 9))
        style.configure('Danger.TButton', font=('Arial', 9), foreground='#e74c3c')
    
    def create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="S-DES加密解密工具", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # 基本加密解密选项卡
        self.create_basic_tab()
        
        # ASCII处理选项卡
        self.create_ascii_tab()
        
        # 暴力破解选项卡
        self.create_brute_force_tab()
        
        # 算法信息选项卡
        self.create_info_tab()
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_basic_tab(self):
        """创建基本加密解密选项卡"""
        basic_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(basic_frame, text="基本加密/解密")
        
        # 配置网格
        basic_frame.columnconfigure(1, weight=1)
        
        # 密钥输入区域
        key_frame = ttk.LabelFrame(basic_frame, text="密钥设置", padding="10")
        key_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        key_frame.columnconfigure(1, weight=1)
        
        ttk.Label(key_frame, text="密钥 (10位二进制):", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=2)
        self.key_var = tk.StringVar()
        key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=30, font=('Courier', 10))
        key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # 密钥信息显示
        self.key_info_label = ttk.Label(key_frame, text="", style='Info.TLabel')
        self.key_info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # 绑定密钥变化事件
        self.key_var.trace('w', self.update_key_info)
        
        # 数据输入区域
        data_frame = ttk.LabelFrame(basic_frame, text="数据处理", padding="10")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        data_frame.columnconfigure(1, weight=1)
        
        # 明文输入
        ttk.Label(data_frame, text="明文 (8位二进制):", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.plaintext_var = tk.StringVar()
        plaintext_entry = ttk.Entry(data_frame, textvariable=self.plaintext_var, width=30, font=('Courier', 10))
        plaintext_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 密文输入
        ttk.Label(data_frame, text="密文 (8位二进制):", style='Heading.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ciphertext_var = tk.StringVar()
        ciphertext_entry = ttk.Entry(data_frame, textvariable=self.ciphertext_var, width=30, font=('Courier', 10))
        ciphertext_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 操作按钮
        button_frame = ttk.Frame(data_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        encrypt_btn = ttk.Button(button_frame, text="🔒 加密", command=self.encrypt, style='Primary.TButton')
        encrypt_btn.grid(row=0, column=0, padx=5)
        
        decrypt_btn = ttk.Button(button_frame, text="🔓 解密", command=self.decrypt, style='Primary.TButton')
        decrypt_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ 清空", command=self.clear_basic, style='Secondary.TButton')
        clear_btn.grid(row=0, column=2, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(basic_frame, text="操作结果", padding="10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        basic_frame.rowconfigure(2, weight=1)
        
        self.basic_result_text = scrolledtext.ScrolledText(result_frame, height=8, width=70, font=('Courier', 9))
        self.basic_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def create_ascii_tab(self):
        """创建ASCII处理选项卡"""
        ascii_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(ascii_frame, text="ASCII文本处理")
        
        # 配置网格
        ascii_frame.columnconfigure(1, weight=1)
        
        # 密钥输入
        ttk.Label(ascii_frame, text="密钥 (10位二进制):", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ascii_key_var = tk.StringVar()
        ascii_key_entry = ttk.Entry(ascii_frame, textvariable=self.ascii_key_var, width=30, font=('Courier', 10))
        ascii_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 文本输入
        ttk.Label(ascii_frame, text="ASCII文本:", style='Heading.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ascii_text_var = tk.StringVar()
        ascii_text_entry = ttk.Entry(ascii_frame, textvariable=self.ascii_text_var, width=50)
        ascii_text_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 操作按钮
        ascii_button_frame = ttk.Frame(ascii_frame)
        ascii_button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ascii_encrypt_btn = ttk.Button(ascii_button_frame, text="🔒 ASCII加密", command=self.ascii_encrypt, style='Primary.TButton')
        ascii_encrypt_btn.grid(row=0, column=0, padx=5)
        
        ascii_decrypt_btn = ttk.Button(ascii_button_frame, text="🔓 ASCII解密", command=self.ascii_decrypt, style='Primary.TButton')
        ascii_decrypt_btn.grid(row=0, column=1, padx=5)
        
        ascii_clear_btn = ttk.Button(ascii_button_frame, text="🗑️ 清空", command=self.clear_ascii, style='Secondary.TButton')
        ascii_clear_btn.grid(row=0, column=2, padx=5)
        
        # 结果显示
        ascii_result_frame = ttk.LabelFrame(ascii_frame, text="ASCII处理结果", padding="10")
        ascii_result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        ascii_result_frame.columnconfigure(0, weight=1)
        ascii_result_frame.rowconfigure(0, weight=1)
        ascii_frame.rowconfigure(3, weight=1)
        
        self.ascii_result_text = scrolledtext.ScrolledText(ascii_result_frame, height=10, width=70, font=('Courier', 9))
        self.ascii_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def create_brute_force_tab(self):
        """创建暴力破解选项卡"""
        brute_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(brute_frame, text="暴力破解")
        
        # 配置网格
        brute_frame.columnconfigure(1, weight=1)
        
        # 说明文字
        info_label = ttk.Label(brute_frame, text="输入已知的明文密文对，程序将尝试所有可能的密钥", style='Info.TLabel')
        info_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 已知数据输入
        data_frame = ttk.LabelFrame(brute_frame, text="已知数据对", padding="10")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        data_frame.columnconfigure(1, weight=1)
        
        ttk.Label(data_frame, text="已知明文 (8位二进制):", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.known_plaintext_var = tk.StringVar()
        ttk.Entry(data_frame, textvariable=self.known_plaintext_var, width=30, font=('Courier', 10)).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(data_frame, text="已知密文 (8位二进制):", style='Heading.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.known_ciphertext_var = tk.StringVar()
        ttk.Entry(data_frame, textvariable=self.known_ciphertext_var, width=30, font=('Courier', 10)).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 控制按钮
        control_frame = ttk.Frame(brute_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        self.start_brute_btn = ttk.Button(control_frame, text="🚀 开始破解", command=self.start_brute_force, style='Primary.TButton')
        self.start_brute_btn.grid(row=0, column=0, padx=5)
        
        self.stop_brute_btn = ttk.Button(control_frame, text="⏹️ 停止破解", command=self.stop_brute_force_func, style='Danger.TButton', state='disabled')
        self.stop_brute_btn.grid(row=0, column=1, padx=5)
        
        clear_brute_btn = ttk.Button(control_frame, text="🗑️ 清空", command=self.clear_brute_force, style='Secondary.TButton')
        clear_brute_btn.grid(row=0, column=2, padx=5)
        
        # 进度显示
        progress_frame = ttk.Frame(brute_frame)
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="等待开始...")
        ttk.Label(progress_frame, textvariable=self.progress_var, style='Info.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 结果显示
        brute_result_frame = ttk.LabelFrame(brute_frame, text="破解结果", padding="10")
        brute_result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        brute_result_frame.columnconfigure(0, weight=1)
        brute_result_frame.rowconfigure(0, weight=1)
        brute_frame.rowconfigure(4, weight=1)
        
        self.brute_result_text = scrolledtext.ScrolledText(brute_result_frame, height=8, width=70, font=('Courier', 9))
        self.brute_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def create_info_tab(self):
        """创建算法信息选项卡"""
        info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(info_frame, text="算法信息")
        
        # 创建滚动文本区域
        self.info_text = scrolledtext.ScrolledText(info_frame, height=20, width=80, font=('Arial', 10))
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # 填充算法信息
        self.fill_algorithm_info()
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 版本信息
        version_label = ttk.Label(status_frame, text="v2.0", relief=tk.SUNKEN, anchor=tk.E)
        version_label.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
    
    def fill_algorithm_info(self):
        """填充算法信息"""
        info_text = """
S-DES算法详细信息

1. 算法规格
   - 分组长度: 8位
   - 密钥长度: 10位
   - 轮数: 2轮
   - 子密钥数: 2个(K1, K2)

2. 置换盒定义

   初始置换盒 (IP): [2, 6, 3, 1, 4, 8, 5, 7]
   最终置换盒 (IP^-1): [4, 1, 3, 5, 7, 2, 8, 6]
   扩展置换盒 (EP): [4, 1, 2, 3, 2, 3, 4, 1]
   P4置换盒 (SP): [2, 4, 3, 1]
   P8置换盒: [6, 3, 7, 4, 8, 5, 10, 9]
   P10置换盒: [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

3. S盒定义

   S盒1:
       0  1  2  3
   0   1  0  3  2
   1   3  2  1  0
   2   0  2  1  3
   3   3  1  0  2

   S盒2:
       0  1  2  3
   0   0  1  2  3
   1   2  3  1  0
   2   3  0  1  2
   3   2  1  0  3

4. 加密流程
   1. 密钥扩展生成K1和K2
   2. 初始置换 (IP)
   3. 第一轮：使用K1的F函数
   4. 第二轮：使用K2的F函数
   5. 最终置换 (IP^-1)

5. 解密流程
   解密过程与加密相同，但密钥使用顺序相反（K2, K1）

6. 安全特性
   - 密钥空间: 2^10 = 1024种可能
   - 支持暴力破解攻击

7. 使用说明
   - 密钥必须是10位二进制数（只包含0和1）
   - 数据块必须是8位二进制数
   - ASCII文本会自动转换为二进制处理
   - 暴力破解会尝试所有可能的密钥

        """
        
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state='disabled')
    
    def update_key_info(self, *args):
        """更新密钥信息显示"""
        key = self.key_var.get().strip()
        if key:
            key_info = self.sdes.get_key_info(key)
            if key_info["valid"]:
                self.key_info_label.config(text=f"✓ 密钥有效 - K1: {key_info['k1']}, K2: {key_info['k2']}", style='Success.TLabel')
            else:
                self.key_info_label.config(text="✗ 密钥格式错误", style='Error.TLabel')
        else:
            self.key_info_label.config(text="请输入10位二进制密钥", style='Info.TLabel')
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def encrypt(self):
        """加密功能"""
        try:
            key = self.key_var.get().strip()
            plaintext = self.plaintext_var.get().strip()
            
            if not key or not plaintext:
                messagebox.showerror("错误", "请输入密钥和明文")
                return
            
            if not self.sdes.validate_key(key):
                messagebox.showerror("错误", "密钥必须是10位二进制")
                return
            
            if not self.sdes.validate_block(plaintext):
                messagebox.showerror("错误", "明文必须是8位二进制")
                return
            
            self.update_status("正在加密...")
            ciphertext = self.sdes.encrypt_block(plaintext, key)
            self.ciphertext_var.set(ciphertext)
            
            result_msg = f"[{time.strftime('%H:%M:%S')}] 加密成功\n"
            result_msg += f"明文: {plaintext}\n"
            result_msg += f"密钥: {key}\n"
            result_msg += f"密文: {ciphertext}\n"
            result_msg += "-" * 50 + "\n"
            
            self.basic_result_text.insert(tk.END, result_msg)
            self.basic_result_text.see(tk.END)
            self.update_status("加密完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")
            self.update_status("加密失败")
    
    def decrypt(self):
        """解密功能"""
        try:
            key = self.key_var.get().strip()
            ciphertext = self.ciphertext_var.get().strip()
            
            if not key or not ciphertext:
                messagebox.showerror("错误", "请输入密钥和密文")
                return
            
            if not self.sdes.validate_key(key):
                messagebox.showerror("错误", "密钥必须是10位二进制")
                return
            
            if not self.sdes.validate_block(ciphertext):
                messagebox.showerror("错误", "密文必须是8位二进制")
                return
            
            self.update_status("正在解密...")
            plaintext = self.sdes.decrypt_block(ciphertext, key)
            self.plaintext_var.set(plaintext)
            
            result_msg = f"[{time.strftime('%H:%M:%S')}] 解密成功\n"
            result_msg += f"密文: {ciphertext}\n"
            result_msg += f"密钥: {key}\n"
            result_msg += f"明文: {plaintext}\n"
            result_msg += "-" * 50 + "\n"
            
            self.basic_result_text.insert(tk.END, result_msg)
            self.basic_result_text.see(tk.END)
            self.update_status("解密完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")
            self.update_status("解密失败")
    
    def ascii_encrypt(self):
        """ASCII加密功能"""
        try:
            key = self.ascii_key_var.get().strip()
            text = self.ascii_text_var.get().strip()
            
            if not key or not text:
                messagebox.showerror("错误", "请输入密钥和ASCII文本")
                return
            
            if not self.sdes.validate_key(key):
                messagebox.showerror("错误", "密钥必须是10位二进制")
                return
            
            self.update_status("正在加密ASCII文本...")
            encrypted = self.sdes.encrypt_ascii(text, key)
            
            result_msg = f"[{time.strftime('%H:%M:%S')}] ASCII加密成功\n"
            result_msg += f"原文: '{text}'\n"
            result_msg += f"密钥: {key}\n"
            result_msg += f"密文: '{encrypted}'\n"
            result_msg += "-" * 50 + "\n"
            
            self.ascii_result_text.insert(tk.END, result_msg)
            self.ascii_result_text.see(tk.END)
            self.update_status("ASCII加密完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"ASCII加密失败: {str(e)}")
            self.update_status("ASCII加密失败")
    
    def ascii_decrypt(self):
        """ASCII解密功能"""
        try:
            key = self.ascii_key_var.get().strip()
            text = self.ascii_text_var.get().strip()
            
            if not key or not text:
                messagebox.showerror("错误", "请输入密钥和ASCII文本")
                return
            
            if not self.sdes.validate_key(key):
                messagebox.showerror("错误", "密钥必须是10位二进制")
                return
            
            self.update_status("正在解密ASCII文本...")
            decrypted = self.sdes.decrypt_ascii(text, key)
            
            result_msg = f"[{time.strftime('%H:%M:%S')}] ASCII解密成功\n"
            result_msg += f"密文: '{text}'\n"
            result_msg += f"密钥: {key}\n"
            result_msg += f"明文: '{decrypted}'\n"
            result_msg += "-" * 50 + "\n"
            
            self.ascii_result_text.insert(tk.END, result_msg)
            self.ascii_result_text.see(tk.END)
            self.update_status("ASCII解密完成")
            
        except Exception as e:
            messagebox.showerror("错误", f"ASCII解密失败: {str(e)}")
            self.update_status("ASCII解密失败")
    
    def start_brute_force(self):
        """开始暴力破解"""
        try:
            plaintext = self.known_plaintext_var.get().strip()
            ciphertext = self.known_ciphertext_var.get().strip()
            
            if not plaintext or not ciphertext:
                messagebox.showerror("错误", "请输入已知的明文和密文")
                return
            
            if not self.sdes.validate_block(plaintext) or not self.sdes.validate_block(ciphertext):
                messagebox.showerror("错误", "明文和密文都必须是8位二进制")
                return
            
            # 启动暴力破解线程
            self.stop_brute_force = False
            self.start_brute_btn.config(state='disabled')
            self.stop_brute_btn.config(state='normal')
            self.progress_bar.start()
            
            self.brute_force_thread = threading.Thread(target=self.brute_force_worker, args=(plaintext, ciphertext))
            self.brute_force_thread.daemon = True
            self.brute_force_thread.start()
            
            self.progress_var.set("正在破解中...")
            self.update_status("暴力破解已启动")
            
            result_msg = f"[{time.strftime('%H:%M:%S')}] 开始暴力破解\n"
            result_msg += f"已知明文: {plaintext}\n"
            result_msg += f"已知密文: {ciphertext}\n"
            result_msg += "-" * 50 + "\n"
            
            self.brute_result_text.insert(tk.END, result_msg)
            self.brute_result_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("错误", f"暴力破解启动失败: {str(e)}")
            self.update_status("暴力破解启动失败")
    
    def brute_force_worker(self, plaintext: str, ciphertext: str):
        """暴力破解工作线程"""
        import itertools
        
        start_time = time.time()
        found_keys = []
        total_keys = 1024
        checked_keys = 0
        
        try:
            # 生成所有可能的10位密钥
            for key_bits in itertools.product([0, 1], repeat=10):
                if self.stop_brute_force:
                    break
                
                checked_keys += 1
                key = ''.join(map(str, key_bits))
                
                # 测试这个密钥
                encrypted = self.sdes.encrypt_block(plaintext, key)
                if encrypted == ciphertext:
                    found_keys.append(key)
                    self.root.after(0, lambda k=key: self.brute_result_text.insert(tk.END, f"找到密钥: {k}\n"))
                    self.root.after(0, lambda: self.brute_result_text.see(tk.END))
                
                # 更新进度
                if checked_keys % 100 == 0:
                    progress = (checked_keys / total_keys) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(f"进度: {p:.1f}% ({checked_keys}/{total_keys})"))
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 更新UI
            self.root.after(0, self.brute_force_completed)
            self.root.after(0, lambda: self.progress_var.set(f"破解完成，用时: {elapsed_time:.2f}秒"))
            self.root.after(0, lambda: self.update_status(f"暴力破解完成，找到{len(found_keys)}个密钥"))
            
            if not self.stop_brute_force:
                self.root.after(0, lambda: self.brute_result_text.insert(tk.END, f"破解完成！用时: {elapsed_time:.2f}秒\n"))
                self.root.after(0, lambda: self.brute_result_text.insert(tk.END, f"找到 {len(found_keys)} 个匹配的密钥\n"))
                self.root.after(0, lambda: self.brute_result_text.see(tk.END))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"暴力破解失败: {str(e)}"))
            self.root.after(0, self.brute_force_completed)
    
    def brute_force_completed(self):
        """暴力破解完成后的UI更新"""
        self.progress_bar.stop()
        self.start_brute_btn.config(state='normal')
        self.stop_brute_btn.config(state='disabled')
    
    def stop_brute_force_func(self):
        """停止暴力破解"""
        self.stop_brute_force = True
        self.brute_result_text.insert(tk.END, "用户停止暴力破解\n")
        self.brute_result_text.see(tk.END)
        self.update_status("暴力破解已停止")
    
    def clear_basic(self):
        """清空基本选项卡"""
        self.key_var.set("")
        self.plaintext_var.set("")
        self.ciphertext_var.set("")
        self.basic_result_text.delete(1.0, tk.END)
        self.update_status("基本选项卡已清空")
    
    def clear_ascii(self):
        """清空ASCII选项卡"""
        self.ascii_key_var.set("")
        self.ascii_text_var.set("")
        self.ascii_result_text.delete(1.0, tk.END)
        self.update_status("ASCII选项卡已清空")
    
    def clear_brute_force(self):
        """清空暴力破解选项卡"""
        self.known_plaintext_var.set("")
        self.known_ciphertext_var.set("")
        self.brute_result_text.delete(1.0, tk.END)
        self.progress_var.set("等待开始...")
        self.update_status("暴力破解选项卡已清空")
    
    def run(self):
        """运行GUI"""
        self.update_status("S-DES工具已启动")
        self.root.mainloop()


if __name__ == "__main__":
    gui = SDESGUI()
    gui.run()
