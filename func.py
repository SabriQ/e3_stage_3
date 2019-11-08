import serial
import serial.tools.list_ports
import csv
import time
import os, sys
import subprocess
import platform
from sys_camera import *
import numpy as np
 #%% functions
def countdown(seconds):
    i=0
    while True:
        sys.stdout.write("%.1is in total %ss"%(i,seconds))
        sys.stdout.write("\r")
        time.sleep(1)
        i += 1
        if i >= seconds:
            #sys.stdout.write("%s countdown finished"%seconds)
            break

def check_ports(*serial_ports):
    ports = [i.device for i in serial.tools.list_ports.comports()]
    if len(ports) == 0:
        sys.exit("There is no ports avilable")
    else:
        for i in serial_ports:
            if i in ports:
                print(f'{i} is available')
            else:
                print(f'{i} is unavailable, please choose from{ports}')
                sys.exit()
#check_ports(r'/dev/ttyUSB0')

def RandomContextOrder(context_nu=2,trials=30,blocks=3):
    np.random.seed(12) # 取值12，
    return np.random.randint(1,context_nu+1,(blocks,trials))
#p.sum(np.where(RandomContextOrder(2,30,3)==1,1,0),axis=1)

#%% stage_1
def stage_1 (serial_port = r'/dev/ttyUSB0',mouse_id=r"192137",video_record = True,
             according_to="Time",Time=1200,Trial=40,data_dir=r"E:\e1_stage_1"):
    '''
    stage_1a is round-trip lick-flows in fixed context
    Variables:
        serual_port (control board), relying on which monitoring two pairs of ared light pair tubes and delivering reward(waters);
        mouse_id
        video_record, if True,video will be recorded.
        according_to: programme will be terminated according to what you define {"Tiem","Trial"}
        data_dir: where your video and log file get saved

    '''
    check_ports(serial_port)


    data_dir = os.path.join(data_dir,time.strftime("%Y%m%d", time.localtime()))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
#    if not os.path.exists(data_dir):
#        print("path is wrong")
#        sys.exit()
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_name = os.path.join(data_dir,mouse_id+"-"+current_time+'_log.csv')
    if video_record:
        video_name = os.path.join(data_dir,mouse_id+"-"+current_time+'.mp4')

    input("请按Enter开始实验（按Enter之后倒计时3s之后开启，摄像头会率先启动）：")

    #开始实验
    #开始视频录制
    if video_record:
        video = video_recording(video_name)
        print(f'{os.path.basename(video_name)} is recording')
    else:
        video = video_online_play()
    countdown(3)


    #在log文件中写入title
    with open(log_name, 'w',newline="",encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Arduino_time(ms)","Event","Count","Python_time(s)"])
    print("Arduino_time(ms)","Event","Count","Python_time(s)")

    ser1 = serial.Serial(serial_port,baudrate=9600,timeout=0.1)
    #print(ser1.name, ser1.port, ser1.timeout,ser1.bytesize)

    video_start_time = time.time()

    while True:
        info  = ser1.readline().decode("utf-8").strip().split(" ")#waiting for 0.1s
        time_elapse = time.time()-video_start_time
        if len(info)>2:
            info.append(round(time_elapse,2))
            with open(log_name,'a',newline="\n",encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(info)
                print(info)

        sys.stdout.write("time elapses %.1fs"%(time_elapse))
        sys.stdout.write("\r")
        #another situation: for certain number of trials
        if according_to == "Time":
            if time_elapse >=Time:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        elif according_to =="Trial":
            if info[2]==Trial+1:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        else:
            print("How do you decide to count down your experiments, 'Time'or'Trial'?")
            sys.exit()

  #  print(f"{os.path.basename(video_name)} is saved.")
    print(f"training log is saved in {os.path.basename(log_name)}")
#%% stage_2
def stage_2a (serial_ports = [r'/dev/ttyUSB0',r'/dev/ttyUSB1'],mouse_id=r"192137",video_record = True,
             according_to="Time",Time=1200,Trial=40,data_dir=r"C:\Users\Sabri\Desktop\test"):
    '''
    stage_2a is round-trip lick-flows in auto-switching contexts
    Variables:
        serual_ports (control_port & motor_port ),
            control port: monitoring pairs of ared light pair tubes and delivering reward(waters);
            motor_port: change context. there are 2 contexts in total.
        mouse_id
        video_recording, if True,video will be recorded.
        according_to: programme will be terminated according to what you define {"Tiem","Trial"}
        data_dir: where your video and log file get saved
    '''
    #检查端口是否可用
    check_ports(serial_ports)
    ser_ctrl = serial.Serial(serial_ports[0],baudrate=9600,timeout=0.1)
    ser_motor = serial.Serial(serial_ports[1],baudrate=9600,timeout=0.1)

    #设置数据存放路径 年月日；设置log文件，视频文件的名字；context_orders
    data_dir = os.path.join(data_dir,time.strftime("%Y%m%d", time.localtime()))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"{data_dir} is created")
#    if not os.path.exists(data_dir):
#        print("path is wrong")
#        sys.exit()
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_name = os.path.join(data_dir,mouse_id+"-"+current_time+'_log.csv')
    video_name = os.path.join(data_dir,mouse_id+'-'+current_time+'.mp4')
    context_orders = RandomContextOrder().tolists()
    current_context_orders = context_orders.pop()
    #初始化context的位置
    ##case 54 6 move to context A, approaching stepper(left)
    #case 55 7 move to context A, leaving stepper(right)
    #case 56 8 move to context B, approaching stepper(left)
    ##case 57 9 move to context B, leaving stepper(right)
    ser_motor.write('7') ; context = 1

    input("请按Enter开始实验（倒计时3s之后开启，摄像头会率先启动）：")

    #开始实验
    #开始视频录制
    if video_record:
        video = video_recording(video_name)
        print(f'{os.path.basename(video_name)} is recording')
    else:
        video = video_online_play()
    countdown(3)
    #在log文件中写入title
    with open(log_name, 'w',newline="",encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Arduino_time(ms)","Event","Count","Python_time(s)","Context"])
    print(["Arduino_time(ms)","Event","Count","Python_time(s)","Context"])

    video_start_time = time.time()

    while True:
        info  = ser_ctrl.readline().decode("utf-8").strip().split(" ")#waiting for 0.1s
        time_elapse = time.time()-video_start_time
        if len(info)>2:
            info.append(round(time_elapse,2))
            # 对位置进行判断，每当小鼠在左边触发红外时，进行是否切换context操作
            if "left" in info:
                if len(current_context_orders) > 0:
                    current_context = current_context_orders.pop()
                else:
                    current_context_orders = context_orders.pop()
                    current_context = current_context_orders.pop()
                info.append(current_context)
                with open(log_name,'a',newline="\n",encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(info)
                print(info)
                if current_context == 1:
                    ser_motor.write("7")
                if current_context == 2:
                    ser_motor.write("8")
        # 时间输出
        sys.stdout.write("time elapses %.1fs"%(time_elapse))
        sys.stdout.write("\r")
        #another situation: for certain number of trials
        if according_to == "Time":
            if time_elapse >=Time:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        elif according_to =="Trial":
            if info[2]==Trial+1:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        else:
            print("How do you decide to count down your experiments, 'Time'or'Trial'?")
            sys.exit()

  #  print(f"{os.path.basename(video_name)} is saved.")
    print(f"training log is saved in {os.path.basename(log_name)}")
    
if __name__ == "__main__":

    stage_1(serial_port = sys.argv[1]
    ,mouse_id=sys.argv[2]
    ,video_record = True
    , according_to="Time"
    ,Time=1400
    ,Trial=40
    ,data_dir=r"/home/qiushou/Documents/data/linear_track")

