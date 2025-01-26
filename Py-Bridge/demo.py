import serial

# Configure serial connection
ser = serial.Serial('COM', 9600, timeout=1)  # Replace COM3 with your port

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")