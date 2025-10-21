import pandas as pd
import pyodbc
import sys

sys.stdout.reconfigure(encoding='utf-8')

df_shop = pd.read_csv('shop_data_cleaned.csv', encoding='utf-8-sig')
df_car = pd.read_csv('car_data_cleaned.csv', encoding='utf-8-sig')

df_car = df_car.where(pd.notnull(df_car), None)

conn = pyodbc.connect(
   'DRIVER={ODBC Driver 17 for SQL Server};'
   'SERVER=localhost;'
   'DATABASE=datawarehouse;'
   'Trusted_Connection=yes;'
)
cursor = conn.cursor()

print("Xoá dữ liệu cũ...")
cursor.execute("DELETE FROM Car")
cursor.execute("DELETE FROM Shop")
conn.commit()

print("Insert Shop...")
for index, row in df_shop.iterrows():
   cursor.execute("""
   INSERT INTO Shop (Shop_Slug, Shop_Name, Shop_Province, Shop_Created_At)
   VALUES (?, ?, ?, ?)
   """, row['Shop_Slug'], row['Shop_Name'], row['Shop_Province'], row['Shop_Created_At'])
conn.commit()

print("Insert Car...")
for index, row in df_car.iterrows():
   cursor.execute("""
   INSERT INTO Car (Product_ID, Title, Price, Year, Manufacturer, Brand, Origin, Figure, Seats, Gear, Fuel, Color, Shop_Slug)
   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   """, row['Product_ID'], row['Title'], row['Price'], row['Year'],
   row['Manufacturer'], row['Brand'], row['Origin'], row['Figure'],
   row['Seats'], row['Gear'], row['Fuel'], row['Color'], row['Shop_Slug'])
   
   if index % 100 == 0:
       print(f"Processed {index} rows...")

conn.commit()
cursor.close()
conn.close()
print("Done.")