import paho.mqtt.client as mqtt
import mysql.connector as mysqli
import calendar
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("IoT_Sensor_Dananky")

def on_message(client, userdata, message):
    result = message.payload.decode("utf-8")

    mydb = mysqli.connect(
        host="localhost",
        user="root",
        password="",
        database="db_greenhouse"
    )

    mycursor = mydb.cursor()
    ts = calendar.timegm(time.gmtime())

    sql = "INSERT INTO sensor_dht11 (humidity,temperature,time) VALUES (%s, %s, %s)"
    val = (0,result, ts)

    mycursor.execute(sql, val)

    mydb.commit()
    print("Temperature :", result)
    print(mycursor.rowcount, "record inserted.")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.mqtt-dashboard.com", 1883, 60)

client.loop_forever()