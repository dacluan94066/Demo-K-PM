# ============================================================
# DEMO KIỂM THỬ TỰ ĐỘNG TRANG WEB (SELENIUM + PYTHON)
# Trang web test: https://www.saucedemo.com (Trang mua sắm demo)
# ============================================================

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    """
    Fixture khởi tạo trình duyệt Chrome trước khi chạy test case
    và tự động đóng trình duyệt sau khi test xong.
    """
    print("\n🌐 Đang mở trình duyệt Chrome...")
    # Tự động tải và cấu hình ChromeDriver tương thích với phiên bản Chrome trên máy bạn
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Phóng to cửa sổ trình duyệt tối đa
    driver.maximize_window()
    
    # Trả driver về cho test case sử dụng
    yield driver
    
    # Dọn dẹp sau khi test xong
    print("\n🧹 Đang đóng trình duyệt...")
    time.sleep(2) # Chờ 2 giây để bạn kịp nhìn thấy trạng thái cuối cùng trước khi đóng
    driver.quit()


def test_dang_nhap_va_them_gio_hang(driver):
    """
    Kịch bản kiểm thử: Đăng nhập thành công và thêm sản phẩm vào giỏ hàng.
    Các bước:
      1. Truy cập vào trang web saucedemo.com
      2. Nhập username hợp lệ (standard_user)
      3. Nhập password hợp lệ (secret_sauce)
      4. Click nút Login
      5. Xác nhận đã vào trang chính (chứa danh sách sản phẩm)
      6. Click "Add to cart" sản phẩm đầu tiên
      7. Xác nhận số lượng giỏ hàng hiển thị số '1'
    """
    wait = WebDriverWait(driver, 10)

    # --- Bước 1: Truy cập trang web ---
    driver.get("https://www.saucedemo.com")
    print("🤖 Đã truy cập trang: https://www.saucedemo.com")
    time.sleep(1) # Thêm time.sleep để người xem kịp theo dõi khi thuyết trình

    # --- Bước 2: Nhập Username ---
    # Tìm ô input username bằng ID
    txt_username = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    txt_username.send_keys("standard_user")
    print("📝 Đã nhập Username: standard_user")
    time.sleep(1)

    # --- Bước 3: Nhập Password ---
    # Tìm ô input password bằng ID
    txt_password = driver.find_element(By.ID, "password")
    txt_password.send_keys("secret_sauce")
    print("🔑 Đã nhập Password: ******")
    time.sleep(1)

    # --- Bước 4: Click nút Login ---
    btn_login = driver.find_element(By.ID, "login-button")
    btn_login.click()
    print("👆 Đã click nút Login")
    time.sleep(1)

    # --- Bước 5: Xác nhận đăng nhập thành công (Assert 1) ---
    # Kiểm tra xem tiêu đề trang sản phẩm "Products" có xuất hiện không
    txt_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
    
    assert txt_title.text == "Products", \
        f"❌ FAIL: Đăng nhập thất bại. Tiêu đề thực tế: '{txt_title.text}'"
    print(f"✅ PASS: Đăng nhập thành công! Tiêu đề trang: '{txt_title.text}'")

    # --- Bước 6: Thêm sản phẩm đầu tiên vào giỏ hàng ---
    # Tìm nút Add to cart của sản phẩm "Sauce Labs Backpack"
    btn_add_to_cart = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    btn_add_to_cart.click()
    print("🛒 Đã click thêm sản phẩm 'Sauce Labs Backpack' vào giỏ hàng")
    time.sleep(1)

    # --- Bước 7: Kiểm tra giỏ hàng hiển thị số 1 (Assert 2) ---
    # Tìm badge hiển thị số lượng trên icon giỏ hàng (chờ xuất hiện)
    badge_cart = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    so_luong_gio_hang = badge_cart.text

    assert so_luong_gio_hang == "1", \
        f"❌ FAIL: Số lượng giỏ hàng sai. Thực tế: {so_luong_gio_hang}"
    print(f"✅ PASS: Giỏ hàng hiển thị chính xác: {so_luong_gio_hang} sản phẩm")
    time.sleep(2)


def test_dang_nhap_that_bai_locked_out(driver):
    """
    TC-02: Test case CỐ TÌNH THẤT BẠI (Để demo trạng thái FAILED trong báo cáo)
    Các bước:
      1. Truy cập trang web
      2. Nhập tài khoản bị khoá (locked_out_user)
      3. Nhập password đúng
      4. Click nút Login
      5. Mong đợi vào được trang sản phẩm (inventory.html)
      6. Assert: Thực tế trang web báo lỗi và giữ lại ở trang chủ,
                 lệnh assert phát hiện ra và báo lỗi FAIL.
    """
    wait = WebDriverWait(driver, 10)

    # --- Bước 1: Truy cập trang web ---
    driver.get("https://www.saucedemo.com")
    print("\n🤖 Đã truy cập trang để test lỗi FAILED")
    time.sleep(1)

    # --- Bước 2: Nhập Username bị khoá ---
    txt_username = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    txt_username.send_keys("locked_out_user") # Đây là user bị hệ thống khóa
    print("📝 Đã nhập Username bị khóa: locked_out_user")
    time.sleep(1)

    # --- Bước 3: Nhập Password ---
    txt_password = driver.find_element(By.ID, "password")
    txt_password.send_keys("secret_sauce")
    print("🔑 Đã nhập Password: ******")
    time.sleep(1)

    # --- Bước 4: Click nút Login ---
    btn_login = driver.find_element(By.ID, "login-button")
    btn_login.click()
    print("👆 Đã click nút Login")
    time.sleep(1)

    # --- Bước 5 & 6: ASSERT - Kiểm tra URL hiện tại ---
    url_hien_tai = driver.current_url
    print(f"🔎 URL thực tế sau khi bấm đăng nhập: {url_hien_tai}")

    # Chúng ta mong đợi vào được trang sản phẩm 'inventory.html'
    # Nhưng vì user bị khóa, trang web vẫn giữ ta ở trang chủ, assert này SẼ SAI => Báo FAILED.
    assert "inventory.html" in url_hien_tai, \
        f"❌ FAIL: Đăng nhập thất bại do tài khoản bị khóa! Trang hiện tại vẫn là: {url_hien_tai}"

