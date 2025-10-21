import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Giúp in tiếng Việt không lỗi encoding
sys.stdout.reconfigure(encoding='utf-8')



# HÀM XỬ LÝ DỮ LIỆU CAR

def clean_car_data():
    print("Đang xử lý car_data.csv...")

    # Dùng Path để tránh lỗi đường dẫn tuyệt đối
    data_path = Path(__file__).resolve().parents[1] / "data_cleaned" / "car_data_cleaned.csv"
    df = pd.read_csv(data_path)
    print(f"Số dòng ban đầu: {len(df)}")

    # Loại bỏ dòng thiếu thông tin bắt buộc
    required_fields = ['Color', 'Seats', 'Gear', 'Price', 'Year']
    for field in required_fields:
        df = df[df[field].notna()]
        if field not in ['Price', 'Year']:
            df = df[df[field].astype(str).str.strip() != '']

    # Chuẩn hóa kiểu dữ liệu
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(',', ''), errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Seats'] = pd.to_numeric(df['Seats'], errors='coerce')

    # Loại bỏ NaN / vô cực
    df = df.dropna(subset=['Price', 'Year', 'Seats'])
    df = df[~df[['Price', 'Year', 'Seats']].apply(lambda x: np.isinf(x)).any(axis=1)]
    df[['Year', 'Seats']] = df[['Year', 'Seats']].astype(int)

    # Điền chuỗi rỗng cho cột text
    text_cols = [
        'Product_ID', 'Title', 'Manufacturer', 'Brand', 'Origin',
        'Figure', 'Gear', 'Fuel', 'Color', 'Shop_Slug'
    ]
    df[text_cols] = df[text_cols].fillna('').astype(str)

    # Ghi file kết quả ra thư mục data_cleaned
    output_path = Path(__file__).resolve().parents[1] / "data_cleaned" / "car_data_cleaned.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"Đã làm sạch car_data.csv → Còn lại {len(df)} dòng.")
    return df


# HÀM XỬ LÝ DỮ LIỆU SHOP

def clean_shop_data():
    print("Đang xử lý shop_data.csv...")

    data_path = Path(__file__).resolve().parents[1] / "data_cleaned" / "shop_data_cleaned.csv"
    df = pd.read_csv(data_path)
    print(f"Số dòng ban đầu: {len(df)}")

    # Xóa trùng slug
    df = df.drop_duplicates(subset='Shop_Slug', keep='first')

    # Chuyển ngày tạo về dạng chuẩn YYYY-MM-DD
    df['Shop_Created_At'] = pd.to_datetime(df['Shop_Created_At'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Ghi file
    output_path = Path(__file__).resolve().parents[1] / "data_cleaned" / "shop_data_cleaned.csv"
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"Đã làm sạch shop_data.csv → Còn lại {len(df)} dòng.")
    return df



# HÀM CHÍNH

def main():
    car_df = clean_car_data()
    shop_df = clean_shop_data()
    print(f"\n Hoàn thành! Cars: {len(car_df)}, Shops: {len(shop_df)}")


if __name__ == "__main__":
    main()
