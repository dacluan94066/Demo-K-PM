# ============================================================
# KIỂM THỰ ĐA THIẾT BỊ DI ĐỘNG ĐỒNG THỜI (MULTI-DEVICE TESTING)
# Công nghệ: Python + Appium (UiAutomator2) + Threading
# Mục tiêu: Tự động phát hiện toàn bộ thiết bị đang kết nối (máy thật/giả lập)
#          và khởi chạy kiểm thử song song trên tất cả thiết bị.
# ============================================================

import subprocess
import threading
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_connected_devices():
    """
    Tự động gọi lệnh 'adb devices' của hệ thống
    để quét và lấy danh sách ID của tất cả điện thoại/máy ảo đang kết nối.
    """
    try:
        output = subprocess.check_output("adb devices", shell=True).decode("utf-8")
        lines = output.strip().split("\n")[1:]
        devices = []
        for line in lines:
            if "device" in line and not line.startswith("*"):
                device_id = line.split()[0]
                devices.append(device_id)
        return devices
    except Exception as e:
        print(f"❌ Lỗi khi quét thiết bị adb: {e}")
        return []


def run_test_on_device(device_id, system_port):
    """
    Hàm chạy kịch bản kiểm thử trên một thiết bị cụ thể.
    Mỗi thiết bị sẽ chạy trên một luồng (Thread) riêng biệt.
    """
    print(f"\n🚀 [Thiết bị: {device_id}] Đang thiết lập phiên kết nối Appium...")

    # --- Bước 1: Khởi tạo Capabilities cho thiết bị ---
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = device_id
    options.udid = device_id  # Chỉ định đúng ID thiết bị để điều khiển
    options.automation_name = "UiAutomator2"

    # Để demo nhanh trên đa thiết bị mà không cần file APK,
    # chúng ta sẽ kiểm thử Web trên di động bằng trình duyệt Chrome tích hợp sẵn.
    options.browser_name = "Chrome"

    # CRITICAL: Mỗi thiết bị chạy song song CẦN một cổng giao tiếp hệ thống riêng biệt
    # để tránh bị xung đột lệnh (thiết bị 1 dùng port 8200, thiết bị 2 dùng port 8201...)
    options.set_capability("appium:systemPort", system_port)
    options.no_reset = True

    try:
        # --- Bước 2: Kết nối driver tới Appium Server ---
        # Cả 2 luồng đều gửi lệnh tới cùng 1 Appium Server (localhost:4723)
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        wait = WebDriverWait(driver, 15)

        print(f"🌐 [Thiết bị: {device_id}] Đã mở trình duyệt Chrome, truy cập saucedemo.com...")
        driver.get("https://www.saucedemo.com")
        time.sleep(2)

        # --- Bước 3: Đăng nhập ---
        txt_username = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        txt_username.send_keys("standard_user")
        print(f"📝 [Thiết bị: {device_id}] Đã nhập Username")
        time.sleep(1)

        txt_password = driver.find_element(By.ID, "password")
        txt_password.send_keys("secret_sauce")
        print(f"🔑 [Thiết bị: {device_id}] Đã nhập Password")
        time.sleep(1)

        btn_login = driver.find_element(By.ID, "login-button")
        btn_login.click()
        print(f"👆 [Thiết bị: {device_id}] Đã click nút Login")
        time.sleep(2)

        # --- Bước 4: Thêm sản phẩm vào giỏ hàng ---
        btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
        btn_add.click()
        print(f"🛒 [Thiết bị: {device_id}] Đã click nút 'Add to cart'")
        time.sleep(2)

        # --- Bước 5: Kiểm tra kết quả (Assert) ---
        badge_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        so_luong = badge_cart.text

        assert so_luong == "1", f"Sai số lượng giỏ hàng! Thực tế: {so_luong}"
        print(f"✅ [Thiết bị: {device_id}] PASS: Giỏ hàng hiển thị chính xác 1 sản phẩm!")
        time.sleep(2)

    except Exception as e:
        print(f"❌ [Thiết bị: {device_id}] THẤT BẠI: {str(e)}")
    finally:
        # --- Bước 6: Đóng trình duyệt ---
        print(f"🧹 [Thiết bị: {device_id}] Đang đóng phiên làm việc...")
        driver.quit()


if __name__ == "__main__":
    # Lấy danh sách toàn bộ thiết bị đang kết nối
    devices = get_connected_devices()

    if not devices:
        print("❌ Không tìm thấy thiết bị Android nào!")
        print("💡 Hãy bật ít nhất 2 máy ảo Emulator (hoặc cắm 2 điện thoại thật đã bật USB Debugging).")
        exit()

    print(f"📱 Quét thành công: Phát hiện {len(devices)} thiết bị đang hoạt động: {devices}")
    print("🚦 Bắt đầu chạy kịch bản đồng thời trên tất cả thiết bị...")

    threads = []
    # Cổng bắt đầu cho UIAutomator2 Server trên các thiết bị
    start_port = 8200

    # Tạo luồng (Thread) chạy song song cho từng thiết bị
    for index, device_id in enumerate(devices):
        system_port = start_port + index
        thread = threading.Thread(
            target=run_test_on_device,
            args=(device_id, system_port)
        )
        threads.append(thread)
        thread.start()

    # Chờ tất cả thiết bị chạy xong
    for thread in threads:
        thread.join()

    print("\n🏁 Hoàn thành quá trình kiểm thử tự động trên Đa thiết bị!")
