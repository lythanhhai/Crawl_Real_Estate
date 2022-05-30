import requests
from bs4 import BeautifulSoup
import csv

# def convertUnitPrice(price, unitPrice):
#     if unitPrice.find("Triệu") != -1:
#         price = float(price) / 1000
    
#     return str(price)

# def removeComma(input):
#     if input.find(",") != -1:
#         input = input.replace(",", ".")
#     return str(input)

# danh sach luu giu tat ca du lieu 
allData = []

# xu ly gia ca
def handlePrice(price, unitPrice):
    # xu ly chuyen doi phay thay cham
    if price.find(",") != -1:
        price = price.replace(",", ".")
    
    # xu ly doi trieu thanh ty
    if unitPrice.find("Triệu") != -1:
        price = float(price) / 1000
    
    return str(price)

# them du lieu den file csv
def writeDataCsv():
    header = ['title', 'address', 'area', 'price', 'number_bedroom', 'number_wc', 'number_floor', 'direction', 'entrance', 'facade', 'number_parking', 'id_estate']
    with open('Ck/Data.csv', 'w', encoding='UTF8') as f:
        # tao writer
        writer = csv.writer(f)

        # tao header
        writer.writerow(header)

        # them du lieu
        writer.writerows(allData)

# lay thong tin chi tiet cua nhung bai dang trong 1 trang
def getDataFromLink(links):
    for link in links:  
        
        infor = requests.get('https://nhadat24h.net' + link)
            
        soup = BeautifulSoup(infor.content, "html.parser")
        global title, address, area, unitPrice, price_prev, price, detail_infor, number_bedroom, number_wc, number_floor, direction, entrance, facade, number_parking, id_estate

        # lay thong tin co ban cua bai dang
        # check ngoai le la nonetype
        try:
            # chu de bai dang
            title = soup.find("h1", id= "txtcontenttieudetin").text.replace("\n", "")

            # Dia chi
            address = soup.find("label", id= 'ContentPlaceHolder1_ctl00_lbTinhThanh').text.replace("\n", "")

            # dien tich (m^2)
            area = soup.find("label", class_= 'strong2').text

            # gia (ty)
            unitPrice = soup.find("label", id= "ContentPlaceHolder1_ctl00_lbGiaDienTich").text
            price_prev = soup.find("label", class_= "strong1").text
            price = handlePrice(price_prev, unitPrice)

            # lay thong tin chi tiet cua bai dang
            detail_infor = soup.select('.dv-tb-tsbds table tbody tr')

            # so phong ngu
            number_bedroom = detail_infor[0].select('td')[1].text.replace("\n", "")

            # so nha ve sinh
            number_wc = detail_infor[1].select('td')[1].text.replace("\n", "")

            # so tang 
            number_floor = detail_infor[2].select('td')[1].text.replace("\n", "").split(" ")[0]

            # huong
            direction = soup.find("label", id= 'ContentPlaceHolder1_ctl00_lbHuong').text.replace("\n", "")

            # duong vao (m)
            entrance = detail_infor[4].select('td')[1].text.replace("\n", "").split(" ")[0]

            # mat tien (m)
            facade = detail_infor[5].select('td')[1].text.replace("\n", "").split(" ")[0]

            # cho de xe (cho)
            number_parking = detail_infor[6].select('td')[1].text.replace("\n", "").split(" ")[0]

            # ma bat dong san
            id_estate = detail_infor[7].select('td')[1].text.replace("\n", "")

        except:
            # loi nonetype
            pass
        
        allData.append([title, address, area, price, number_bedroom, number_wc, number_floor, direction, entrance, facade, number_parking, id_estate])

        # viet vao file csv
        # data = [title, address, area, price, number_bedroom, number_wc, number_floor, direction, entrance, facade, number_parking, id_estate]
        # with open('Ck/Data.csv', 'w', encoding='UTF8') as f:
        #     # create the csv writer
        #     writer = csv.writer(f)
        #     # write the header
        #     writer.writerow(data)

        # write the data
        # writer.writerow(data)

    # return array

# lay du lieu tu cac trang
def getData():
    for index in range(1, 135):
        # tao duong link theo tung trang
        if index == 1:
            url = 'https://nhadat24h.net/ban-can-ho-chung-cu'
        else:
            url = 'https://nhadat24h.net/ban-can-ho-chung-cu/page' + str(index)

        # gui request den trang web
        response = requests.get(url)

        # lay noi dung html bang thu vien beautifulsoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)

        body_part = soup.findAll('body')
        # print(body_part)

        # lay tat ca bai dang
        items = soup.findAll('div', class_="dv-item")
        # print(items)

        # lay link cho tung thuoc tinh trong the <a>
        links = [link.find('a').attrs["href"] for link in items]
        #print(links)
        
        # lay thong tin chi tiet cua moi bai dang
        getDataFromLink(links)
        # print(array)
        
    writeDataCsv()
    # print(allData)


def main():
    getData()

main()