# ============================================================
# GIẢI PHÁP CHẠY TEST ĐA THIẾT BỊ DI ĐỘNG KHÔNG CẦN ĐIỆN THOẠI/MÁY ẢO
# Công nghệ: Python + Selenium (Chrome Mobile Emulation) + Threading
# Giải thích: Sử dụng tính năng giả lập thiết bị di động (Responsive Mode)
#             có sẵn của Google Chrome để kiểm thử giao diện di động
#             trên nhiều dòng máy khác nhau (ví dụ: Pixel 7 vs iPhone 12 Pro).
# ============================================================

import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def run_test_on_emulated_device(device_name, window_position, is_locked_user=False):
    """
    Hàm chạy kịch bản kiểm thử trên một thiết bị giả lập của Chrome.
    Mỗi thiết bị chạy song song trên một luồng (Thread) riêng biệt.
    """
    print(f"\n🚀 [Thiết bị: {device_name}] Đang khởi tạo trình duyệt Chrome giả lập...")

    # --- Bước 1: Cấu hình Chrome giả lập thiết bị di động ---
    chrome_options = webdriver.ChromeOptions()
    
    # Kích hoạt tính năng giả lập thiết bị của Chrome DevTools
    mobile_emulation = {"deviceName": device_name}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Tắt các thông báo tự động hóa phiền phức của Chrome
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Khởi tạo driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Đặt vị trí và kích thước cửa sổ trên màn hình để khi chạy 2 máy không bị đè lên nhau
    driver.set_window_rect(x=window_position[0], y=window_position[1], width=390, height=844)
    
    wait = WebDriverWait(driver, 15)

    try:
        # --- Bước 2: Truy cập trang web ---
        print(f"🌐 [Thiết bị: {device_name}] Đang mở Saucedemo...")
        driver.get("https://www.saucedemo.com")
        time.sleep(2)

        # --- Bước 3: Nhập Username (Tùy theo cấu hình test Pass hay Fail) ---
        txt_username = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        username = "locked_out_user" if is_locked_user else "standard_user"
        txt_username.send_keys(username)
        print(f"📝 [Thiết bị: {device_name}] Đã nhập Username: {username}")
        time.sleep(1)

        # --- Bước 4: Nhập Password ---
        txt_password = driver.find_element(By.ID, "password")
        txt_password.send_keys("secret_sauce")
        print(f"🔑 [Thiết bị: {device_name}] Đã nhập Password: ******")
        time.sleep(1)

        # --- Bước 5: Click nút Login ---
        btn_login = driver.find_element(By.ID, "login-button")
        btn_login.click()
        print(f"👆 [Thiết bị: {device_name}] Đã click nút Login")
        time.sleep(2)

        if is_locked_user:
            # KỊCH BẢN THẤT BẠI: Mong đợi đăng nhập thành công vào trang sản phẩm (inventory.html)
            # Nhưng do tài khoản bị khoá, trình duyệt vẫn ở trang chủ => Lệnh assert này SẼ THẤT BẠI.
            url_hien_tai = driver.current_url
            print(f"🔎 [Thiết bị: {device_name}] URL thực tế sau đăng nhập: {url_hien_tai}")
            
            assert "inventory.html" in url_hien_tai, \
                f"Lỗi: Đăng nhập thất bại do tài khoản bị khóa! URL thực tế là: {url_hien_tai}"
        else:
            # KỊCH BẢN THÀNH CÔNG: Thêm sản phẩm vào giỏ hàng
            btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
            btn_add.click()
            print(f"🛒 [Thiết bị: {device_name}] Đã thêm sản phẩm vào giỏ")
            time.sleep(2)

            # Kiểm tra kết quả (Assert)
            badge_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            so_luong = badge_cart.text

            assert so_luong == "1", f"Sai số lượng giỏ hàng! Thực tế: {so_luong}"
            print(f"✅ [Thiết bị: {device_name}] PASS: Giỏ hàng hiển thị chính xác 1 sản phẩm!")
            time.sleep(3)

    except Exception as e:
        print(f"❌ [Thiết bị: {device_name}] THẤT BẠI: {str(e)}")
    finally:
        # --- Đóng trình duyệt ---
        print(f"🧹 [Thiết bị: {device_name}] Đang đóng phiên làm việc...")
        driver.quit()


if __name__ == "__main__":
    # Cấu hình danh sách các dòng điện thoại giả lập
    # iPhone 12 Pro: chạy thành công (standard_user)
    # Pixel 7: chạy thất bại (locked_out_user) để demo đồng thời cả 2 trạng thái
    target_devices = [
        {"name": "iPhone 12 Pro", "position": (150, 50), "is_locked": False},
        {"name": "Pixel 7", "position": (650, 50), "is_locked": True}
    ]

    print("🚦 Bắt đầu chạy test song song trên các thiết bị di động giả lập...")
    
    threads = []
    for device in target_devices:
        thread = threading.Thread(
            target=run_test_on_emulated_device, 
            args=(device["name"], device["position"], device["is_locked"])
        )
        threads.append(thread)
        thread.start()

    # Chờ tất cả luồng chạy xong
    for thread in threads:
        thread.join()

    print("\n🏁 Hoàn thành quá trình kiểm thử tự động trên Đa thiết bị di động giả lập!")

