"""
S-DES算法核心实现
"""

from typing import List, Tuple


class SDES:
    """S-DES算法核心实现类"""
    
    def __init__(self):
        # 初始置换盒 (IP)
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        
        # 最终置换盒 (IP^-1)
        self.IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
        
        # 扩展置换盒 (EP)
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        
        # SP置换盒
        self.SP = [2, 4, 3, 1]
        
        # S盒1
        self.S1 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 0, 2]
        ]
        
        # S盒2
        self.S2 = [
            [0, 1, 2, 3],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [2, 1, 0, 3]
        ]
        
        # P8置换盒（用于密钥扩展）
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        
        # P10置换盒（用于密钥扩展）
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    
    def permute(self, data: List[int], permutation: List[int]) -> List[int]:
        """执行置换操作"""
        return [data[i-1] for i in permutation]
    
    def left_shift(self, data: List[int], shift: int) -> List[int]:
        """左移操作"""
        return data[shift:] + data[:shift]
    
    def generate_keys(self, key: str) -> Tuple[List[int], List[int]]:
        """生成子密钥K1和K2"""
        # 将10位密钥转换为列表
        key_bits = [int(bit) for bit in key.zfill(10)]
        
        # P10置换
        key_p10 = self.permute(key_bits, self.P10)
        
        # 分割为左右两部分
        left = key_p10[:5]
        right = key_p10[5:]
        
        # 左移1位
        left_shifted_1 = self.left_shift(left, 1)
        right_shifted_1 = self.left_shift(right, 1)
        
        # 合并并P8置换得到K1
        combined_1 = left_shifted_1 + right_shifted_1
        k1 = self.permute(combined_1, self.P8)
        
        # 左移2位
        left_shifted_2 = self.left_shift(left_shifted_1, 2)
        right_shifted_2 = self.left_shift(right_shifted_1, 2)
        
        # 合并并P8置换得到K2
        combined_2 = left_shifted_2 + right_shifted_2
        k2 = self.permute(combined_2, self.P8)
        
        return k1, k2
    
    def s_box(self, data: List[int], s_box: List[List[int]]) -> List[int]:
        """S盒替换"""
        row = data[0] * 2 + data[3]
        col = data[1] * 2 + data[2]
        result = s_box[row][col]
        return [result // 2, result % 2]
    
    def f_function(self, right: List[int], key: List[int]) -> List[int]:
        """轮函数F"""
        # 扩展置换
        expanded = self.permute(right, self.EP)
        
        # 与密钥异或
        xor_result = [expanded[i] ^ key[i] for i in range(8)]
        
        # 分割为两部分
        left_part = xor_result[:4]
        right_part = xor_result[4:]
        
        # S盒替换
        s1_result = self.s_box(left_part, self.S1)
        s2_result = self.s_box(right_part, self.S2)
        
        # 合并结果
        combined = s1_result + s2_result
        
        # SP置换
        return self.permute(combined, self.SP)
    
    def encrypt_block(self, plaintext: str, key: str) -> str:
        """加密单个8位数据块"""
        # 将明文转换为8位二进制
        plaintext_bits = [int(bit) for bit in plaintext.zfill(8)]
        
        # 生成子密钥
        k1, k2 = self.generate_keys(key)
        
        # 初始置换
        ip_result = self.permute(plaintext_bits, self.IP)
        
        # 分割为左右两部分
        left = ip_result[:4]
        right = ip_result[4:]
        
        # 第一轮：使用K1
        f_result = self.f_function(right, k1)
        new_right = [left[i] ^ f_result[i] for i in range(4)]
        new_left = right
        
        # 第二轮：使用K2
        f_result2 = self.f_function(new_right, k2)
        final_left = [new_left[i] ^ f_result2[i] for i in range(4)]
        final_right = new_right
        
        # 合并
        combined = final_left + final_right
        
        # 最终置换
        ciphertext = self.permute(combined, self.IP_INV)
        
        return ''.join(map(str, ciphertext))
    
    def decrypt_block(self, ciphertext: str, key: str) -> str:
        """解密单个8位数据块"""
        # 将密文转换为8位二进制
        ciphertext_bits = [int(bit) for bit in ciphertext.zfill(8)]
        
        # 生成子密钥
        k1, k2 = self.generate_keys(key)
        
        # 初始置换
        ip_result = self.permute(ciphertext_bits, self.IP)
        
        # 分割为左右两部分
        left = ip_result[:4]
        right = ip_result[4:]
        
        # 第一轮：使用K2（解密时密钥顺序相反）
        f_result = self.f_function(right, k2)
        new_right = [left[i] ^ f_result[i] for i in range(4)]
        new_left = right
        
        # 第二轮：使用K1
        f_result2 = self.f_function(new_right, k1)
        final_left = [new_left[i] ^ f_result2[i] for i in range(4)]
        final_right = new_right
        
        # 合并
        combined = final_left + final_right
        
        # 最终置换
        plaintext = self.permute(combined, self.IP_INV)
        
        return ''.join(map(str, plaintext))
    
    def encrypt_ascii(self, text: str, key: str) -> str:
        """加密文本字符串（使用UTF-8编码处理）"""
        result = ""
        # 将文本编码为UTF-8字节序列
        utf8_bytes = text.encode('utf-8')
        
        for byte_val in utf8_bytes:
            # 将字节转换为8位二进制
            binary = format(byte_val, '08b')
            # 加密
            encrypted = self.encrypt_block(binary, key)
            # 转换回ASCII字符
            encrypted_ascii_val = int(encrypted, 2)
            result += chr(encrypted_ascii_val)
        
        return result
    
    def decrypt_ascii(self, text: str, key: str) -> str:
        """解密文本字符串（使用UTF-8编码处理）"""
        result_bytes = []
        
        for char in text:
            # 将字符转换为ASCII码，再转换为8位二进制
            ascii_val = ord(char)
            binary = format(ascii_val, '08b')
            # 解密
            decrypted = self.decrypt_block(binary, key)
            # 转换回字节值
            byte_val = int(decrypted, 2)
            result_bytes.append(byte_val)
        
        # 将字节序列解码为UTF-8字符串
        return bytes(result_bytes).decode('utf-8')
    
    def validate_key(self, key: str) -> bool:
        """验证密钥格式"""
        if not key or len(key) != 10:
            return False
        return all(c in '01' for c in key)
    
    def validate_block(self, block: str) -> bool:
        """验证数据块格式"""
        if not block or len(block) != 8:
            return False
        return all(c in '01' for c in block)
    
    def get_key_info(self, key: str) -> dict:
        """获取密钥信息"""
        if not self.validate_key(key):
            return {"valid": False}
        
        k1, k2 = self.generate_keys(key)
        return {
            "valid": True,
            "key": key,
            "k1": ''.join(map(str, k1)),
            "k2": ''.join(map(str, k2))
        }
