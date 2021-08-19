import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    # ホームページのURLを格納する
    TARGET_URL = "https://suumo.jp/chintai/tokyo/sc_shinjuku/"

    PAGE_NUM = 3

    all_data = []

    for num in range(PAGE_NUM):
        print(len(all_data))

        # アクセスするためのURLを格納する
        url = TARGET_URL
        payload = {"page": num + 1}

        try:
            # アクセス結果を格納
            res = requests.get(url, params=payload)
            res.raise_for_status()
            # 結果解析
            soup = BeautifulSoup(res.text, features="lxml")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print("error", e)

        # すべての物件情報を取得
        contents = soup.findAll("div", class_="cassetteitem")
        # content = contents[0]

        # ページ内の各物件情報をfor文で取得
        for content in contents:
            # 物件情報と部屋情報を取得
            detail = content.find("div", class_="cassetteitem-detail")
            room = content.find("table", class_="cassetteitem_other")
            # 物件情報から個別の情報を取得
            title = detail.find("div", class_="cassetteitem_content-title").text
            address = detail.find("li", class_="cassetteitem_detail-col1").text
            access = detail.find("li", class_="cassetteitem_detail-col2").text
            age = detail.find("li", class_="cassetteitem_detail-col3").text

            # 部屋情報ブロックから各部屋情報を取得
            tr_tags = room.find_all("tr", class_="js-cassette_link")

            # 物件内の各部屋情報をfor文で取得
            for tr_tag in tr_tags:
                # 部屋情報から詳細情報を取得
                floor, price, first_fee, capacity = tr_tag.find_all("td")[2:6]
                rent, management_fee = price.find_all("li")
                deposit, gratuity = first_fee.find_all("li")
                room_layout, area = capacity.find_all("li")

                # データ整形
                property_information = {
                    "title": title,
                    "address": address,
                    "access": access,
                    "age": age,
                    "floor": floor.text.replace("\t", ""),
                    "rent": rent.text,
                    "management_fee": management_fee.text,
                    "deposit": deposit.text,
                    "gratuity": gratuity.text,
                    "room_layout": room_layout.text,
                    "area": area.text,
                }

                all_data.append(property_information)

    # データフレーム作成
    df = pd.DataFrame(all_data)

    # データをcsvで保存
    df.to_csv("suumo_room_info.csv", index=None, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
