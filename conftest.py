# ============================================================
# conftest.py - Cấu hình chung cho tất cả các bài kiểm thử
# File này được pytest tự động nhận diện và chạy trước mỗi test
# ============================================================

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# ---------- HẰNG SỐ CẤU HÌNH (chỉnh sửa theo máy của bạn) ----------

# URL của Appium Server (mặc định chạy local trên cổng 4723)
APPIUM_SERVER_URL = "http://127.0.0.1:4723"

# Tên thiết bị Android (lấy từ lệnh: adb devices)
DEVICE_NAME = "emulator-5554"

# Phiên bản Android trên thiết bị/giả lập
PLATFORM_VERSION = "14"

# Package name của ứng dụng cần test
# (Ví dụ dùng app demo "ApiDemos" của Appium - app mẫu phổ biến nhất)
APP_PACKAGE = "io.appium.android.apis"

# Activity khởi động của ứng dụng
APP_ACTIVITY = "io.appium.android.apis.ApiDemos"

# Đường dẫn tới file APK (nếu muốn cài app từ file)
# Để trống nếu app đã được cài sẵn trên thiết bị
APP_PATH = ""


@pytest.fixture(scope="function")
def driver():
    """
    Fixture khởi tạo driver Appium trước mỗi test case.
    - scope="function": Mỗi test case sẽ có một phiên driver riêng biệt
    - yield: Trả driver cho test case sử dụng, sau khi test xong sẽ tự đóng
    """

    # --- Bước 1: Thiết lập Desired Capabilities ---
    # Desired Capabilities là tập hợp các thông số mô tả thiết bị và ứng dụng
    options = UiAutomator2Options()

    # Tên nền tảng: Android hoặc iOS
    options.platform_name = "Android"

    # Tên thiết bị (giả lập hoặc thiết bị thật)
    options.device_name = DEVICE_NAME

    # Phiên bản hệ điều hành trên thiết bị
    options.platform_version = PLATFORM_VERSION

    # Automation engine: UiAutomator2 là engine phổ biến nhất cho Android
    options.automation_name = "UiAutomator2"

    # Package và Activity của ứng dụng cần khởi chạy
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY

    # Nếu có đường dẫn APK, thêm vào để Appium tự cài đặt
    if APP_PATH:
        options.app = APP_PATH

    # Không reset trạng thái app giữa các lần chạy (giữ dữ liệu)
    options.no_reset = True

    # Thời gian chờ khởi động app tối đa (mili-giây)
    options.new_command_timeout = 300

    # --- Bước 2: Khởi tạo phiên kết nối Appium ---
    # Tạo kết nối từ script Python tới Appium Server
    print("\n🚀 Đang kết nối tới Appium Server...")
    driver = webdriver.Remote(
        command_executor=APPIUM_SERVER_URL,
        options=options
    )

    # Đặt thời gian chờ ngầm định (implicit wait) là 10 giây
    # Appium sẽ chờ tối đa 10s để tìm phần tử trước khi báo lỗi
    driver.implicitly_wait(10)

    print("✅ Kết nối thành công! Bắt đầu kiểm thử...\n")

    # Trả driver cho test case sử dụng
    yield driver

    # --- Bước 3: Dọn dẹp sau khi test xong ---
    print("\n🧹 Đang đóng phiên kiểm thử...")
    driver.quit()
    print("✅ Đã đóng phiên thành công!\n")
