# ============================================================
# TEST CASE 1: KIỂM THỬ CHỨC NĂNG ĐĂNG NHẬP
# Mô tả: Tự động hóa việc nhập username, password và bấm
#         nút đăng nhập, sau đó kiểm tra kết quả.
# ============================================================

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestDangNhap:
    """Bộ kiểm thử chức năng Đăng nhập."""

    def test_dang_nhap_thanh_cong(self, driver):
        """
        TC-01: Đăng nhập thành công với tài khoản hợp lệ.
        Các bước:
          1. Mở màn hình đăng nhập
          2. Nhập username hợp lệ
          3. Nhập password hợp lệ
          4. Bấm nút Đăng nhập
          5. Xác nhận chuyển sang màn hình chính
        """

        # --- Bước 1: Tìm và nhập Username ---
        # Sử dụng AppiumBy.ID để tìm phần tử theo resource-id
        # (resource-id tương tự như id trong HTML)
        txt_username = driver.find_element(
            AppiumBy.ID,                          # Phương thức định vị
            "com.example.app:id/edt_username"     # Resource ID của ô nhập
        )
        txt_username.clear()                       # Xóa nội dung cũ (nếu có)
        txt_username.send_keys("admin")            # Nhập username: "admin"
        print("📝 Đã nhập username: admin")

        # --- Bước 2: Tìm và nhập Password ---
        txt_password = driver.find_element(
            AppiumBy.ID,
            "com.example.app:id/edt_password"
        )
        txt_password.clear()
        txt_password.send_keys("123456")           # Nhập password: "123456"
        print("🔑 Đã nhập password: ******")

        # --- Bước 3: Bấm nút Đăng nhập ---
        btn_login = driver.find_element(
            AppiumBy.ID,
            "com.example.app:id/btn_login"
        )
        btn_login.click()                          # Thực hiện bấm nút
        print("👆 Đã bấm nút Đăng nhập")

        # --- Bước 4: Chờ và kiểm tra kết quả ---
        # Sử dụng WebDriverWait (chờ tường minh) thay vì time.sleep()
        # Ưu điểm: Chờ đúng điều kiện, không chờ cứng => test nhanh hơn
        wait = WebDriverWait(driver, 10)           # Chờ tối đa 10 giây

        # Chờ cho đến khi phần tử "Xin chào" xuất hiện trên màn hình
        txt_welcome = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/txt_welcome"
            ))
        )

        # --- Bước 5: ASSERT - Đánh giá kết quả PASS/FAIL ---
        # Kiểm tra nội dung text có chứa "Xin chào" hay không
        assert "Xin chào" in txt_welcome.text, \
            f"❌ FAIL: Không tìm thấy lời chào. Nội dung thực tế: '{txt_welcome.text}'"

        print(f"✅ PASS: Đăng nhập thành công! Hiển thị: '{txt_welcome.text}'")

    def test_dang_nhap_that_bai_sai_mat_khau(self, driver):
        """
        TC-02: Đăng nhập thất bại với mật khẩu sai.
        Kỳ vọng: Hiển thị thông báo lỗi "Sai mật khẩu".
        """

        # --- Nhập username đúng ---
        txt_username = driver.find_element(
            AppiumBy.ID, "com.example.app:id/edt_username"
        )
        txt_username.clear()
        txt_username.send_keys("admin")
        print("📝 Đã nhập username: admin")

        # --- Nhập password SAI ---
        txt_password = driver.find_element(
            AppiumBy.ID, "com.example.app:id/edt_password"
        )
        txt_password.clear()
        txt_password.send_keys("wrong_password")   # Mật khẩu sai
        print("🔑 Đã nhập password sai: wrong_password")

        # --- Bấm nút Đăng nhập ---
        btn_login = driver.find_element(
            AppiumBy.ID, "com.example.app:id/btn_login"
        )
        btn_login.click()
        print("👆 Đã bấm nút Đăng nhập")

        # --- Chờ thông báo lỗi xuất hiện ---
        wait = WebDriverWait(driver, 10)

        # Tìm phần tử hiển thị thông báo lỗi (Toast hoặc TextView)
        txt_error = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/txt_error"
            ))
        )

        # --- ASSERT: Xác nhận thông báo lỗi đúng nội dung ---
        assert txt_error.is_displayed(), \
            "❌ FAIL: Không hiển thị thông báo lỗi khi nhập sai mật khẩu"

        assert "Sai mật khẩu" in txt_error.text, \
            f"❌ FAIL: Thông báo lỗi không đúng. Thực tế: '{txt_error.text}'"

        print(f"✅ PASS: Hiển thị thông báo lỗi chính xác: '{txt_error.text}'")

    def test_dang_nhap_de_trong_username(self, driver):
        """
        TC-03: Đăng nhập khi để trống Username.
        Kỳ vọng: Hiển thị thông báo "Vui lòng nhập tên đăng nhập".
        """

        # --- Để trống username ---
        txt_username = driver.find_element(
            AppiumBy.ID, "com.example.app:id/edt_username"
        )
        txt_username.clear()                       # Đảm bảo ô trống
        print("📝 Để trống username")

        # --- Nhập password bất kỳ ---
        txt_password = driver.find_element(
            AppiumBy.ID, "com.example.app:id/edt_password"
        )
        txt_password.clear()
        txt_password.send_keys("123456")
        print("🔑 Đã nhập password: 123456")

        # --- Bấm nút Đăng nhập ---
        btn_login = driver.find_element(
            AppiumBy.ID, "com.example.app:id/btn_login"
        )
        btn_login.click()
        print("👆 Đã bấm nút Đăng nhập")

        # --- ASSERT: Kiểm tra thông báo validation ---
        wait = WebDriverWait(driver, 5)
        txt_error = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/txt_error"
            ))
        )

        assert "Vui lòng nhập" in txt_error.text, \
            f"❌ FAIL: Thông báo validation không đúng. Thực tế: '{txt_error.text}'"

        print(f"✅ PASS: Validation hoạt động đúng: '{txt_error.text}'")
