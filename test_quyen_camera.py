# ============================================================
# TEST CASE 3: KIỂM THỬ CHỨC NĂNG XIN QUYỀN CAMERA
# Mô tả: Tự động hóa việc kiểm tra luồng xin quyền truy cập
#         Camera trên Android (Runtime Permission).
# ============================================================

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestQuyenCamera:
    """Bộ kiểm thử chức năng xin quyền Camera."""

    def test_cho_phep_quyen_camera(self, driver):
        """
        TC-06: Cho phép quyền Camera khi hộp thoại hiện lên.
        Các bước:
          1. Bấm nút mở Camera trong app
          2. Chờ hộp thoại xin quyền (Permission Dialog) xuất hiện
          3. Bấm "Cho phép" (Allow)
          4. Xác nhận Camera đã mở thành công
        """

        wait = WebDriverWait(driver, 15)

        # --- Bước 1: Bấm nút mở Camera trong ứng dụng ---
        btn_camera = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ID,
                "com.example.app:id/btn_open_camera"
            ))
        )
        btn_camera.click()
        print("📷 Đã bấm nút mở Camera")

        # --- Bước 2: Xử lý hộp thoại xin quyền Android ---
        # Hộp thoại này là của HỆ THỐNG Android, không phải của app
        # Nên resource-id sẽ thuộc package: com.android.permissioncontroller
        # Hoặc có thể dùng package: com.android.packageinstaller (tuỳ phiên bản)

        # Chờ hộp thoại xin quyền xuất hiện
        btn_cho_phep = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ID,
                # ID của nút "Cho phép" trên dialog hệ thống Android
                "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
            ))
        )
        print("🔔 Hộp thoại xin quyền đã xuất hiện")

        # --- Bước 3: Bấm nút "Cho phép" (Allow) ---
        btn_cho_phep.click()
        print("✅ Đã bấm 'Cho phép' (Allow)")

        # --- Bước 4: Kiểm tra Camera đã mở thành công ---
        # Sau khi cấp quyền, app sẽ mở màn hình Camera/Preview
        camera_preview = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/camera_preview"
            ))
        )

        # ASSERT: Xác nhận phần tử Camera Preview tồn tại và hiển thị
        assert camera_preview.is_displayed(), \
            "❌ FAIL: Camera Preview không hiển thị sau khi cấp quyền!"

        print("✅ PASS: Camera đã mở thành công sau khi cấp quyền!")

    def test_tu_choi_quyen_camera(self, driver):
        """
        TC-07: Từ chối quyền Camera.
        Kỳ vọng: App hiển thị thông báo yêu cầu cấp quyền.
        """

        wait = WebDriverWait(driver, 15)

        # --- Bước 1: Bấm nút mở Camera ---
        btn_camera = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ID,
                "com.example.app:id/btn_open_camera"
            ))
        )
        btn_camera.click()
        print("📷 Đã bấm nút mở Camera")

        # --- Bước 2: Bấm nút "Từ chối" (Deny) trên hộp thoại hệ thống ---
        btn_tu_choi = wait.until(
            EC.element_to_be_clickable((
                AppiumBy.ID,
                # ID của nút "Từ chối" trên dialog hệ thống Android
                "com.android.permissioncontroller:id/permission_deny_button"
            ))
        )
        btn_tu_choi.click()
        print("🚫 Đã bấm 'Từ chối' (Deny)")

        # --- Bước 3: Kiểm tra app xử lý từ chối đúng cách ---
        # App tốt sẽ hiển thị thông báo giải thích tại sao cần quyền Camera
        txt_thong_bao = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ID,
                "com.example.app:id/txt_permission_denied"
            ))
        )

        # ASSERT 1: Thông báo phải hiển thị
        assert txt_thong_bao.is_displayed(), \
            "❌ FAIL: Không hiển thị thông báo khi từ chối quyền Camera!"

        # ASSERT 2: Nội dung thông báo phải liên quan đến quyền Camera
        assert "Camera" in txt_thong_bao.text or "quyền" in txt_thong_bao.text, \
            f"❌ FAIL: Nội dung thông báo không phù hợp: '{txt_thong_bao.text}'"

        print(f"✅ PASS: App xử lý từ chối đúng: '{txt_thong_bao.text}'")
