import serial
import time
import firebase_admin
from firebase_admin import credentials, db

# Firebase'e bağlanmak için Firebase Admin SDK'ya ihtiyacımız var
cred = credentials.Certificate("/home/pi/Downloads/raspberrypi7474-firebase-adminsdk-kqrrl-a642f17d92.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://raspberrypi7474-default-rtdb.firebaseio.com/'})

# Serial port ayarları
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Baud rate 9600 olarak değiştirildi

while True:
    try:
        # RS485 üzerinden veri okuma işlemi
        ser.write(b'\x01\x03\x00\x00\x00\x01\x84\x0A')  # RK400-01 için örneğin bu komutu kullanabilirsiniz
        time.sleep(0.1)
        response = ser.read(9)  # RK400-01 için beklenen byte sayısı 7'dir

        # Gelen veriyi işleme
        if response:
            data = [int(byte) for byte in response]
            print(f"Sensör verisi (hex): {data}")

            # Daha fazla işlem yapmak için buraya kod ekleyebilirsiniz
            yağmur_miktarı = (data[3] << 8 | data[4]) / 10.0
            print(f"Yağmur Miktarı: {yağmur_miktarı} mm")

            # Firebase'e veri gönderme
            ref = db.reference('/sensor_data2')  # Firebase Realtime Database'deki bir referans belirtin
            ref.set({
                'yağmur_miktarı': yağmur_miktarı
            })

        else:
            print("Sensörden veri alınamadı.")

    except serial.SerialException as e:
        print(f"Seri port hatası: {e}")

    # Belirli bir süre bekleyin (örneğin, 3 saniye)
    time.sleep(3)
