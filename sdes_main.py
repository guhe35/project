"""
启动S-DES图形用户界面
"""

import sys
from sdes_gui import SDESGUI


def check_dependencies():
    """检查依赖项"""
    print("🔍 检查系统依赖...")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ Python版本过低，需要Python 3.6或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version.split()[0]}")
    
    # 检查必要的模块
    try:
        import tkinter
        print("✅ tkinter模块可用")
    except ImportError:
        print("❌ tkinter模块不可用，GUI功能将无法使用")
        return False
    
    try:
        from sdes_algorithm import SDES
        print("✅ S-DES算法模块可用")
    except ImportError as e:
        print(f"❌ S-DES算法模块加载失败: {e}")
        return False
    
    print("✅ 系统检查完成")
    return True


def main():
    """主函数"""
    
    # 检查依赖项
    if not check_dependencies():
        print("❌ 系统依赖检查失败，程序无法运行")
        input("按回车键退出...")
        return
    
    # 启动GUI
    print("\n🖥️  正在启动图形界面...")
    print("请稍候...")
    
    try:
        gui = SDESGUI()
        print("✅ GUI界面加载成功！")
        print("💡 提示：请在图形界面中进行操作")
        gui.run()
    except Exception as e:
        print(f"❌ GUI启动失败: {str(e)}")
        print("请检查Python环境和tkinter库是否正确安装")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
