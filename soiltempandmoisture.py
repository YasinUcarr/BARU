import serial
import time
import firebase_admin
from firebase_admin import credentials, db

# Firebase'e bağlanmak için Firebase Admin SDK'ya ihtiyacımız var
cred = credentials.Certificate("/home/pi/Downloads/raspberrypi7474-firebase-adminsdk-kqrrl-a642f17d92.json") # Firebase Console'dan indirdiğiniz JSON dosyasını belirtin
firebase_admin.initialize_app(cred, {'databaseURL': 'https://raspberrypi7474-default-rtdb.firebaseio.com/'})  # Bu URL'yi kendi Firebase proje URL'nizle değiştirin

# Serial port ayarları
ser = serial.Serial('/dev/ttyUSB1', 4800, timeout=1)

while True:
    try:
        # RS485 üzerinden veri okuma işlemi
        ser.write(b'\x01\x03\x00\x00\x00\x02\xC4\x0B')  #Bu komut sensör belgelerine göre ayarlanacaktır
        time.sleep(0.1)  # Gerekirse biraz bekleme ekleyin
        response = ser.read(9)

        # Gelen veriyi işleme
        if response:
            data = [int(byte) for byte in response]
            print(f"Sensor verisi (ondalık): {data}")


            nem = data[3] << 8 | data[4]
            sicaklik = data[5] << 8 | data[6]
            print(f"Nem: {nem / 10.0} %RH")
            print(f"Sıcaklık: {sicaklik / 10.0} °C")

            # Firebase'e veri gönderme
            ref = db.reference('/sensor_data')  # Firebase Realtime Database'deki bir referans
            ref.set({
                'nem': nem / 10.0,
                'sicaklik': sicaklik / 10.0
            })

        else:
            print("Sensörden veri alınamadı.")

    except serial.SerialException as e:
        print(f"Seri port hatası: {e}")

    # Bekleme süresi
    time.sleep(3)
