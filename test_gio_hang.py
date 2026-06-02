# ============================================================
# TEST CASE 2: KIỂM THỬ CHỨC NĂNG THÊM VÀO GIỎ HÀNG
# Mô tả: Tự động hóa việc chọn sản phẩm, bấm nút thêm vào
#         giỏ hàng, và kiểm tra số lượng trong giỏ.
# ============================================================

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestGioHang:
    """Bộ kiểm thử chức năng Giỏ hàng."""

    def test_them_san_pham_vao_gio(self, driver):
        """
        TC-04: Thêm một sản phẩm vào giỏ hàng thành công.
        Các bước:
          1. Cuộn đến sản phẩm cần mua
          2. Bấm nút "Thêm vào giỏ hàng"
          3. Kiểm tra badge số lượng trên icon giỏ hàng tăng lên
        """

        # --- Bước 1: Cuộn danh sách để tìm sản phẩm ---
        # Sử dụng UiScrollable (API Android) để cuộn tự động
        # Đây là kỹ thuật đặc biệt của UiAutomator2 cho Android
        san_pham = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            # Chuỗi UiSelector: cuộn đến khi tìm thấy text "Áo thun nam"
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().text("Áo thun nam"))'
        )
        print("🔍 Đã tìm thấy sản phẩm: Áo thun nam")

        # --- Bước 2: Bấm vào sản phẩm để mở chi tiết ---
        san_pham.click()
        print("👆 Đã bấm vào sản phẩm")

        # --- Bước 3: Bấm nút "Thêm vào giỏ hàng" ---
        wait = WebDriverWait(driver, 10)

        # Chờ nút "Thêm vào giỏ" xuất hiện (trang chi tiết cần thời gian load)
        btn_them_gio = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ID,
                "com.example.app:id/btn_add_to_cart"
            ))
        )
        btn_them_gio.click()
        print("🛒 Đã bấm nút 'Thêm vào giỏ hàng'")

        # --- Bước 4: Kiểm tra thông báo xác nhận ---
        # Chờ thông báo "Đã thêm vào giỏ hàng" xuất hiện
        thong_bao = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/txt_toast_message"
            ))
        )

        # ASSERT 1: Kiểm tra thông báo xác nhận
        assert "Đã thêm" in thong_bao.text, \
            f"❌ FAIL: Không thấy thông báo xác nhận. Thực tế: '{thong_bao.text}'"
        print(f"📢 Thông báo: '{thong_bao.text}'")

        # --- Bước 5: Kiểm tra badge số lượng giỏ hàng ---
        # Badge là con số nhỏ hiển thị trên icon giỏ hàng
        badge_gio_hang = driver.find_element(
            AppiumBy.ID,
            "com.example.app:id/txt_cart_badge"
        )

        # Lấy số lượng sản phẩm trong giỏ
        so_luong = int(badge_gio_hang.text)

        # ASSERT 2: Kiểm tra giỏ hàng có ít nhất 1 sản phẩm
        assert so_luong >= 1, \
            f"❌ FAIL: Giỏ hàng trống! Số lượng hiện tại: {so_luong}"

        print(f"✅ PASS: Giỏ hàng có {so_luong} sản phẩm")

    def test_xoa_san_pham_khoi_gio(self, driver):
        """
        TC-05: Xóa sản phẩm khỏi giỏ hàng.
        Kỳ vọng: Số lượng trong giỏ giảm xuống hoặc giỏ trống.
        """

        wait = WebDriverWait(driver, 10)

        # --- Bước 1: Mở giỏ hàng ---
        btn_gio_hang = driver.find_element(
            AppiumBy.ID, "com.example.app:id/btn_cart"
        )
        btn_gio_hang.click()
        print("🛒 Đã mở giỏ hàng")

        # --- Bước 2: Lấy số lượng sản phẩm trước khi xóa ---
        ds_san_pham = driver.find_elements(
            AppiumBy.ID, "com.example.app:id/item_product"
        )
        so_luong_truoc = len(ds_san_pham)
        print(f"📦 Số sản phẩm trước khi xóa: {so_luong_truoc}")

        # --- Bước 3: Bấm nút xóa sản phẩm đầu tiên ---
        btn_xoa = driver.find_element(
            AppiumBy.ID, "com.example.app:id/btn_remove_item"
        )
        btn_xoa.click()
        print("🗑️ Đã bấm xóa sản phẩm đầu tiên")

        # --- Bước 4: Chờ danh sách cập nhật ---
        import time
        time.sleep(1)  # Chờ animation xóa hoàn tất

        # Đếm lại số sản phẩm
        ds_san_pham_sau = driver.find_elements(
            AppiumBy.ID, "com.example.app:id/item_product"
        )
        so_luong_sau = len(ds_san_pham_sau)

        # --- ASSERT: Số lượng phải giảm đi 1 ---
        assert so_luong_sau == so_luong_truoc - 1, \
            f"❌ FAIL: Số lượng không giảm! Trước: {so_luong_truoc}, Sau: {so_luong_sau}"

        print(f"✅ PASS: Đã xóa thành công. Còn {so_luong_sau} sản phẩm")
