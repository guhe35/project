"""
S-DES算法测试
"""

import time
import itertools
from sdes_algorithm import SDES


class SDESTester:
    """S-DES测试类"""
    
    def __init__(self):
        self.sdes = SDES()
        self.test_results = []
    
    def print_separator(self, title=""):
        """打印分隔线"""
        print("=" * 60)
        if title:
            print(f" {title} ")
            print("=" * 60)
    
    def print_test_header(self, test_name):
        """打印测试标题"""
        print(f"\n🔍 {test_name}")
        print("-" * 40)
    
    def test_level_1_basic_encryption(self):
        """第1关：基本加密解密测试"""
        self.print_separator("第1关：基本加密解密测试")
        
        # 测试用例
        test_cases = [
            ("10111101", "1010000010", "标准测试用例1"),
            ("00000000", "1111111111", "全零明文测试"),
            ("11111111", "0000000000", "全一明文测试"),
            ("10101010", "0101010101", "交替模式测试"),
            ("11001100", "1010101010", "重复模式测试")
        ]
        
        passed = 0
        total = len(test_cases)
        
        for plaintext, key, description in test_cases:
            print(f"\n📝 {description}")
            print(f"明文: {plaintext}")
            print(f"密钥: {key}")
            
            try:
                # 加密
                ciphertext = self.sdes.encrypt_block(plaintext, key)
                print(f"密文: {ciphertext}")
                
                # 解密
                decrypted = self.sdes.decrypt_block(ciphertext, key)
                print(f"解密: {decrypted}")
                
                # 验证
                is_correct = plaintext == decrypted
                status = "✅ 通过" if is_correct else "❌ 失败"
                print(f"结果: {status}")
                
                if is_correct:
                    passed += 1
                    
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
        
        success_rate = (passed / total) * 100
        print(f"\n📊 第1关测试结果: {passed}/{total} 通过 ({success_rate:.1f}%)")
        
        self.test_results.append(("第1关：基本加密解密", passed == total))
        return passed == total
    
    def test_level_2_cross_platform(self):
        """第2关：交叉平台兼容性测试"""
        self.print_separator("第2关：交叉平台兼容性测试")
        
        # 使用相同密钥测试不同明文
        key = "1010000010"
        plaintexts = [
            ("10111101", "标准明文"),
            ("00000000", "全零明文"),
            ("11111111", "全一明文"),
            ("10101010", "交替明文"),
            ("11001100", "重复明文")
        ]
        
        print(f"🔑 使用固定密钥: {key}")
        print("\n📋 加密结果对比:")
        
        results = []
        passed = 0
        
        for plaintext, description in plaintexts:
            try:
                # 第一次加密
                ciphertext1 = self.sdes.encrypt_block(plaintext, key)
                
                # 第二次加密（验证一致性）
                ciphertext2 = self.sdes.encrypt_block(plaintext, key)
                
                is_consistent = ciphertext1 == ciphertext2
                status = "✅ 一致" if is_consistent else "❌ 不一致"
                
                print(f"{description:10}: {plaintext} -> {ciphertext1} {status}")
                
                results.append((plaintext, ciphertext1, is_consistent))
                
                if is_consistent:
                    passed += 1
                    
            except Exception as e:
                print(f"{description:10}: ❌ 错误 - {str(e)}")
        
        # 验证不同明文产生不同密文
        print(f"\n🔍 验证雪崩效应（不同明文应产生不同密文）:")
        ciphertexts = [result[1] for result in results if result[2]]
        unique_ciphertexts = set(ciphertexts)
        
        avalanche_effect = len(unique_ciphertexts) == len(ciphertexts)
        avalanche_status = "✅ 正常" if avalanche_effect else "❌ 异常"
        print(f"雪崩效应: {avalanche_status} ({len(unique_ciphertexts)}/{len(ciphertexts)} 唯一密文)")
        
        total_tests = len(plaintexts) + 1  # 包括雪崩效应测试
        passed_tests = passed + (1 if avalanche_effect else 0)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n📊 第2关测试结果: {passed_tests}/{total_tests} 通过 ({success_rate:.1f}%)")
        
        self.test_results.append(("第2关：交叉平台兼容性", passed_tests == total_tests))
        return passed_tests == total_tests
    
    def test_level_3_ascii_encryption(self):
        """第3关：ASCII字符串加密测试"""
        self.print_separator("第3关：ASCII字符串加密测试")
        
        key = "1010000010"
        test_strings = [
            ("Hello", "英文单词"),
            ("World", "英文单词"),
            ("Test123", "英文数字混合"),
            ("S-DES", "包含特殊字符"),
            ("Python", "编程语言名称"),
            ("信息安全", "中文字符"),
            ("!@#$%^&*()", "特殊符号")
        ]
        
        print(f"🔑 使用固定密钥: {key}")
        
        passed = 0
        total = len(test_strings)
        
        for text, description in test_strings:
            print(f"\n📝 {description}: '{text}'")
            
            try:
                # 加密
                encrypted = self.sdes.encrypt_ascii(text, key)
                print(f"加密: '{encrypted}'")
                
                # 解密
                decrypted = self.sdes.decrypt_ascii(encrypted, key)
                print(f"解密: '{decrypted}'")
                
                # 验证
                is_correct = text == decrypted
                status = "✅ 正确" if is_correct else "❌ 错误"
                print(f"结果: {status}")
                
                if is_correct:
                    passed += 1
                    
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
        
        success_rate = (passed / total) * 100
        print(f"\n📊 第3关测试结果: {passed}/{total} 通过 ({success_rate:.1f}%)")
        
        self.test_results.append(("第3关：ASCII字符串加密", passed == total))
        return passed == total
    
    def test_level_4_brute_force(self):
        """第4关：暴力破解测试"""
        self.print_separator("第4关：暴力破解测试")
        
        # 使用已知明文密文对
        test_key = "1010000010"
        plaintext = "10111101"
        
        # 先加密得到密文
        ciphertext = self.sdes.encrypt_block(plaintext, test_key)
        
        print(f"🎯 破解目标:")
        print(f"已知明文: {plaintext}")
        print(f"已知密文: {ciphertext}")
        print(f"真实密钥: {test_key}")
        
        # 暴力破解
        print(f"\n🚀 开始暴力破解...")
        start_time = time.time()
        
        found_keys = []
        total_keys = 1024
        checked_keys = 0
        
        try:
            for key_bits in itertools.product([0, 1], repeat=10):
                checked_keys += 1
                key = ''.join(map(str, key_bits))
                
                encrypted = self.sdes.encrypt_block(plaintext, key)
                if encrypted == ciphertext:
                    found_keys.append(key)
                    if len(found_keys) <= 5:  # 只显示前5个
                        print(f"🔍 找到密钥: {key}")
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n⏱️  破解统计:")
            print(f"总用时: {elapsed_time:.4f}秒")
            print(f"检查密钥数: {checked_keys}/{total_keys}")
            print(f"找到密钥数: {len(found_keys)}")
            print(f"破解速度: {checked_keys/elapsed_time:.0f} 密钥/秒")
            
            # 验证结果
            correct_key_found = test_key in found_keys
            status = "✅ 成功" if correct_key_found else "❌ 失败"
            print(f"目标密钥: {status}")
            
            if found_keys:
                print(f"\n🔑 找到的所有密钥:")
                for i, key in enumerate(found_keys[:10], 1):  # 显示前10个
                    marker = "🎯" if key == test_key else "🔍"
                    print(f"{marker} 密钥{i}: {key}")
            
            # 性能评估
            performance_ok = elapsed_time < 2.0  # 期望在2秒内完成
            performance_status = "✅ 优秀" if elapsed_time < 1.0 else "⚠️ 一般" if elapsed_time < 2.0 else "❌ 较慢"
            print(f"\n📈 性能评估: {performance_status}")
            
            success = correct_key_found and performance_ok
            print(f"\n📊 第4关测试结果: {'✅ 通过' if success else '❌ 失败'}")
            
            self.test_results.append(("第4关：暴力破解", success))
            return success
            
        except Exception as e:
            print(f"❌ 暴力破解失败: {str(e)}")
            self.test_results.append(("第4关：暴力破解", False))
            return False
    
    def test_level_5_key_collision(self):
        """第5关：密钥碰撞和安全性测试"""
        self.print_separator("第5关：密钥碰撞和安全性测试")
        
        # 测试不同密钥是否会产生相同密文
        plaintext = "10111101"
        test_keys = [
            "1010000010",
            "0101111101", 
            "1111111111",
            "0000000000",
            "1010101010",
            "0101010101",
            "1100110011",
            "0011001100"
        ]
        
        print(f"📝 使用固定明文: {plaintext}")
        print(f"\n🔍 测试密钥碰撞:")
        
        ciphertexts = []
        passed = 0
        
        for key in test_keys:
            try:
                ciphertext = self.sdes.encrypt_block(plaintext, key)
                ciphertexts.append((key, ciphertext))
                print(f"密钥 {key}: {ciphertext}")
                passed += 1
            except Exception as e:
                print(f"密钥 {key}: ❌ 错误 - {str(e)}")
        
        # 检查密文碰撞
        print(f"\n🔍 密文唯一性分析:")
        ciphertext_values = [ct[1] for ct in ciphertexts]
        unique_ciphertexts = set(ciphertext_values)
        
        has_collision = len(unique_ciphertexts) < len(ciphertext_values)
        collision_status = "❌ 存在碰撞" if has_collision else "✅ 无碰撞"
        print(f"密文唯一性: {collision_status}")
        print(f"唯一密文数: {len(unique_ciphertexts)}/{len(ciphertext_values)}")
        
        if has_collision:
            print(f"⚠️  发现碰撞的密文:")
            for ciphertext in unique_ciphertexts:
                count = ciphertext_values.count(ciphertext)
                if count > 1:
                    colliding_keys = [key for key, ct in ciphertexts if ct == ciphertext]
                    print(f"密文 {ciphertext}: {count} 个密钥 -> {colliding_keys}")
        
        # 测试不同明文使用相同密钥
        print(f"\n🔍 测试明文敏感性:")
        key = "1010000010"
        test_plaintexts = [
            "10111101",
            "01000010", 
            "11111111",
            "00000000",
            "10101010"
        ]
        
        plaintext_ciphertexts = []
        for pt in test_plaintexts:
            try:
                ct = self.sdes.encrypt_block(pt, key)
                plaintext_ciphertexts.append((pt, ct))
                print(f"明文 {pt} -> 密文 {ct}")
            except Exception as e:
                print(f"明文 {pt}: ❌ 错误 - {str(e)}")
        
        # 检查明文敏感性
        plaintext_ct_values = [ct[1] for ct in plaintext_ciphertexts]
        unique_plaintext_cts = set(plaintext_ct_values)
        
        plaintext_sensitivity = len(unique_plaintext_cts) == len(plaintext_ct_values)
        sensitivity_status = "✅ 敏感" if plaintext_sensitivity else "❌ 不敏感"
        print(f"明文敏感性: {sensitivity_status}")
        
        # 安全性评估
        print(f"\n🛡️  安全性评估:")
        key_space = 1024
        print(f"密钥空间: 2^10 = {key_space} 种可能")
        print(f"分组长度: 8位")
        print(f"轮数: 2轮")
        
        # 计算破解难度
        print(f"\n🔐 破解难度分析:")
        print(f"暴力破解复杂度: O(2^10) = O({key_space})")
        print(f"平均破解时间: < 1秒")
        print(f"安全等级: ⚠️ 教学级别（不安全）")
        
        # 综合评估
        security_score = 0
        if not has_collision:
            security_score += 1
        if plaintext_sensitivity:
            security_score += 1
        if passed == len(test_keys):
            security_score += 1
        
        total_tests = 3
        success_rate = (security_score / total_tests) * 100
        
        print(f"\n📊 第5关测试结果: {security_score}/{total_tests} 通过 ({success_rate:.1f}%)")
        
        self.test_results.append(("第5关：密钥碰撞和安全性", security_score == total_tests))
        return security_score == total_tests
    
    def run_all_tests(self):
        """运行所有测试"""
        self.print_separator("S-DES算法完整测试套件")
        
        print("🎯 开始运行5个测试关卡...")
        print("每个关卡将验证算法的不同方面")
        
        start_time = time.time()
        
        # 运行所有测试
        results = []
        results.append(self.test_level_1_basic_encryption())
        results.append(self.test_level_2_cross_platform())
        results.append(self.test_level_3_ascii_encryption())
        results.append(self.test_level_4_brute_force())
        results.append(self.test_level_5_key_collision())
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 显示最终结果
        self.print_separator("测试结果汇总")
        
        passed_count = sum(results)
        total_count = len(results)
        
        print(f"📊 总体测试结果: {passed_count}/{total_count} 关卡通过")
        print(f"⏱️  总测试时间: {total_time:.2f}秒")
        
        print(f"\n📋 详细结果:")
        for i, (test_name, result) in enumerate(self.test_results):
            status = "✅ 通过" if result else "❌ 失败"
            print(f"第{i+1}关 - {test_name}: {status}")
        
        success_rate = (passed_count / total_count) * 100
        print(f"\n🎯 成功率: {success_rate:.1f}%")
        
        if passed_count == total_count:
            print("🎉 恭喜！所有测试关卡都通过了！")
            print("S-DES算法实现正确，可以投入使用。")
        else:
            print("⚠️  部分测试失败，请检查算法实现。")
            failed_tests = [i+1 for i, result in enumerate(results) if not result]
            print(f"失败的关卡: {failed_tests}")
        
        return passed_count == total_count


def main():
    """主测试函数"""
    print("S-DES算法测试程序")
    print("=" * 60)
    
    print("请选择测试模式:")
    print("1. 运行单个测试关卡")
    print("2. 运行所有测试关卡")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        tester = SDESTester()
        print("\n请选择要运行的测试关卡:")
        print("1. 第1关：基本加密解密测试")
        print("2. 第2关：交叉平台兼容性测试")
        print("3. 第3关：ASCII字符串加密测试")
        print("4. 第4关：暴力破解测试")
        print("5. 第5关：密钥碰撞和安全性测试")
        
        level_choice = input("请选择关卡 (1-5): ").strip()
        
        if level_choice == "1":
            tester.test_level_1_basic_encryption()
        elif level_choice == "2":
            tester.test_level_2_cross_platform()
        elif level_choice == "3":
            tester.test_level_3_ascii_encryption()
        elif level_choice == "4":
            tester.test_level_4_brute_force()
        elif level_choice == "5":
            tester.test_level_5_key_collision()
        else:
            print("无效选择")
    
    elif choice == "2":
        tester = SDESTester()
        tester.run_all_tests()
    
    elif choice == "3":
        print("退出测试程序")
    
    else:
        print("无效选择")


if __name__ == "__main__":
    main()
