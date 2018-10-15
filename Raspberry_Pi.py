import socket
#============================== PWM ========================
pwm = PWM(0x40)
# Read Data Sheet of Brushless Motor for frequancy
pwm.setPWMFreq(60)
#===========================================================


# just assumtion
Neutral = 2000
Brake_Force = 0
Forward_Force = 4000

class Motor:
        def __init__(self,pin_num)
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

                pwm.SetPWM(self.__pin,0,Speed)

Motors = []
# Motors 1 ,2 Front Motors
# Motors 3 ,4 Back Motors
# Motors 0 , 5 Z-Axis Motors
for i in range(6):
        Motors[i] = Motor(i)

#================== Movment Functions =======================
def Move(str_msg):

        # split the messge by space to make a list of pwms
        pwms = str_msg.split()

        #Set Directions
        for i in range(1,5):
                Motors[i].Set_Speed(pwms[i])

        # Z-Axis Motors have the same PWM which is pwms[0] (Determined in QT)
        Motors[0].Set_Speed(pwms[0])
        Motors[5].Set_Speed(pwms[0])

#===========================================================

#================== Socket =================================
host = '111.111.111.111' port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
        s.bind((host, port))
        print('Waiting for QT Connection!')
except socket.error as m:
         print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
         s.bind((host,8082))
s.listen(5)
conn , addr = s.accept()
print ('Connected ya ray2')
#===========================================================

while True :
        msg = conn.recv(1024).decode()
        if not msg:
                conn.close()
                break
        print(msg)
        Move(msg)

