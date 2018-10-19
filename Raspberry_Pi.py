import socket
import Adafruit_PCA9685

#============================== PWM ========================
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
#===========================================================

Neutral = 290
Brake_Force = 140
Forward_Force = 440

#====================== Servo  =============================
servo_zero = 160
servo_90 = 370
servo_180 = 580

class servo:
        def __init__(self,pin):
                self.pin = pin
                self.pos = servo_90
                pwm.set_pwm(self.pin,0,self.pos)

        def Set_Servo_Pos(self,x):
                if x == 'u' and self.pos < servo_180:
                        self.pos += 21
                        pwm.set_pwm(self.pin,0,self.pos)
                elif x == 'd' and self.pos > servo_zero:
                        self.pos -= 21
                        pwm.set_pwm(self.pin,0,self.pos)

Camera_Servo = servo(6)
#===========================================================

class Motor:
        def __init__(self,pin_num):
                if pin_num >15 or pin_num <0:
                        print('error pin Num')
                        return
                self.__pin = pin_num
                self.__speed = 0

        def Set_Speed(self,speed):
                # convert the msg string to float
                Speed = float(speed)

                # check for repetition
                if Speed == self.__speed:
                        return
                # check for joystick error
                if Speed < Brake_Force  or Speed > Forward_Force :
                        return

                pwm.set_pwm(self.__pin,0,Speed)

Motors = []
# Motors 1 ,2 Front Motors
# Motors 3 ,4 Back Motors
# Motors 0 , 5 Z-Axis Motors
for i in range(6):
        Motors.append( Motor(i) )

#================== Movement Functions =======================
def Move(str_msg):

        # split the message by space to make a list of pwms
        pwms = str_msg.split()

        #Set Directions
        for i in range(1,5):
                Motors[i].Set_Speed(pwms[i])

        # Z-Axis Motors have the same PWM which is pwms[0] (Determined in QT)
        Motors[0].Set_Speed(pwms[0])
        Motors[5].Set_Speed(pwms[0])

#===========================================================

#================== Socket =================================
host = '111.111.111.111'
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
        s.bind((host, port))
        print('Waiting for QT Connection!')
except socket.error as m:
         print ('Bind failed. Error Code : ' + str(m[0]))
s.listen(5)
conn , addr = s.accept()
print ('Connected ya ray2')
#===========================================================

while True :
        msg = conn.recv(1024).decode()
        if not msg:
                conn.close()
                break
        if msg == 'u' or msg == 'd':
                Camera_Servo.Set_Servo_Pos(msg)
                continue

        print(msg)
        Move(msg)
