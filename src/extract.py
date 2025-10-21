import random
import requests
import time
import pandas as pd

BASE_URL = "https://api-ecom.carpla.vn/app-server/search/car"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_car_data(item):
    """Trích xuất dữ liệu ô tô từ phản hồi API"""
    additional = item.get("additional", {})
    return {
        "Product_ID": item.get("id", ""),
        "Title": item.get("title", ""),
        "Price": item.get("price", ""),
        "Year": additional.get("year", ""),
        "Manufacturer": additional.get("manufacturer", {}).get("name", ""),
        "Brand": additional.get("brand", {}).get("name", ""),
        "Origin": additional.get("origin", {}).get("source", ""),
        "Figure": additional.get("figure", {}).get("name", ""),
        "Seats": additional.get("seats", ""),
        "Gear": additional.get("gear", {}).get("name", ""),
        "Fuel": additional.get("fuel", {}).get("type", ""),
        "Color": additional.get("color", {}).get("color", ""),
        "Shop_Slug": item.get("shop", {}).get("slug", "")
    }


def extract_shop_data(shop):
    """Trích xuất dữ liệu cửa hàng từ phản hồi API"""
    address = shop.get("shop", {}).get("address", {})
    return {
        "Shop_Slug": shop.get("slug", ""),
        "Shop_Name": shop.get("name", ""),
        "Shop_Province": address.get("province", {}).get("label", ""),
        "Shop_Created_At": shop.get("createdAt", "")
    }


def scrape_carpla_data():
    """Gọi API và lưu dữ liệu xe và cửa hàng ra file CSV"""
    session = requests.Session()
    car_data, shop_data = [], []
    seen_shop_slugs = set()

    params = {"status": 2, "limit": 15, "saleState": 1, "type": 1}

    for offset in range(0, 1111, 15):
        params["offset"] = offset
        try:
            response = session.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
            data = response.json()

            if not data.get("data"):
                print(f"No more data at offset {offset}")
                break

            for item in data["data"]:
                car_data.append(extract_car_data(item))

                shop = item.get("shop", {})
                shop_slug = shop.get("slug", "")
                if shop_slug and shop_slug not in seen_shop_slugs:
                    seen_shop_slugs.add(shop_slug)
                    shop_data.append(extract_shop_data(shop))

            print(f"Processed offset {offset}")
            time.sleep(random.uniform(1, 2.5))

        except Exception as e:
            print(f"Error at offset {offset}: {e}")
            continue

    # Ghi dữ liệu ra file CSV
    pd.DataFrame(car_data).to_csv('car_data.csv', index=False, encoding='utf-8-sig')
    pd.DataFrame(shop_data).to_csv('shop_data.csv', index=False, encoding='utf-8-sig')

    print(f"Finished! Scraped {len(car_data)} cars and {len(shop_data)} shops.")


if __name__ == "__main__":
    scrape_carpla_data()
