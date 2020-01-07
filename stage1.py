from linear_track_funcs import *
from sys_camera import *
	
def stage_1 (serial_ports = [r'/dev/ttyUSB0',r'/dev/ttyUSB1'],mouse_id=r"192137",note="train",description="no_description" video_record = False,
             according_to="Time",Time=1200,Trial=40,data_dir=r"C:\Users\Sabri\Desktop\test"):
    '''
    for lick learning and alternate lick learning, and will record timepoints including:
	nose_poke,
	context_Enter,
	context_Exit,
	choice,
	context Reverss Enter,
	context Reverse Exit
    '''
    #检查端口是否可用
    check_ports(serial_ports)
    ser_ctrl = serial.Serial(serial_ports[0],baudrate=9600,timeout=0.1)
    ser_motor = serial.Serial(serial_ports[1],baudrate=9600,timeout=0.1)
    countdown(3)
    print(serial_ports[1])
    #设置数据存放路径 年月日；设置log文件，视频文件的名字；
    data_dir = os.path.join(data_dir,time.strftime("%Y%m%d", time.localtime()))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"{data_dir} is created")
#    if not os.path.exists(data_dir):
#        print("path is wrong")
#        sys.exit()
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+note+'_log.csv')
    video_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+note+'.mp4')
    
    print(">>>>>>")
    ser_motor.write("4477".encode())#初始化时，给两个lick port出一点水
    print("<<<<<<")

    #开始实验
    #开始视频录制
    if video_record:
        input("请按Enter开始实验（倒计时3s之后开启，摄像头会率先启动:")
        video = video_recording(video_name)
        print(f'{os.path.basename(video_name)} is recording')
        countdown(3)
    else:
        input("请按Enter开始实验:")
    
    #在log文件中写入title
    with open(log_name, 'w',newline="",encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["mouse_id",mouse_id])
        writer.writerow(["stage2 learn to lick and alternate licking"])
        writer.writerow(["description",description])
        writer.writerow(["Trial_Num",])
    print(["Trial_Num","Nose_poke"])

    video_start_time = time.time()
    Trial_Num=[];
    A_NosePoke=[];A_ContextEnter=[];A_ContextExit=[];A_Choice=[];A_ContextREnter=[];A_ContextRExit=[]
    P_NosePoke=[];P_ContextEnter=[];P_ContextExit=[];P_Choice=[];P_ContextREnter=[];P_ContextRExit=[]
    shoe_info = "Ready"
    
    while True:
        info  = ser_ctrl.readline().decode("utf-8").strip().split(" ")#waiting for 0.1s
        time_elapse = time.time()-video_start_time
        if len(info)>:
            show_info = ''.join([i for i in info])
            #info.append(round(time_elapse,2))
            # 对位置进行判断，每当小鼠在左边触发红外时，进行是否切换context操作
            if "Stat1:" in info:
                P_NosePoke.append(time_elapse);ser_motor.write("4".encode())
            if "Stat2:" in info:
                P_ContextEnter.append(time_elapse)
            if "Stat3:" in info:
                P_ContextExit.append(time_elapse)
            if "Stat4:" in info:
                P_Choice.append(time_elapse);
                #print(info,end=" ")
            if "Stat5:" in info:
                P_ContextREnter.append(time_elapse)
            if "Stat6:" in info:
                P_ContextRExit.append(time_elapse)
            if "Sum:" in info:
                Trial_Num.append(info[1])
                A_NosePoke.append(info[4])
                A_ContextEnter.append(info[5])
                A_ContextExit.append(info[6])
                A_Choice.append(info[7])
                A_ContextREnter.append(info[8])
                A_ContextRExit.append(info[9])
                
                row=[Trial_Num[-1],
                     ,A_NosePoke[-1],A_ContextEnter[-1],A_ContextExit[-1],A_Choice[-1],A_ContextREnter[-1],A_ContextRExit[-1]
                     ,P_NosePoke[-1],P_ContextEnter[-1],P_ContextExit[-1],P_Choice[-1],P_ContextREnter[-1],P_ContextRExit[-1]]
                with open(log_name,"a",newline="\n",encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(row)
                print(row[0],row[7],row[12])
                show_info = "Ready "
        print(f"\r{show_info}".ljust(25),f"time elapses {round(time_elapse,1)}s  ",end="")
                
        #another situation: for certain number of trials
        if according_to == "Time":
            if time_elapse >=Time:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        elif according_to =="Trial":
            if len(info)>2:
                if info[1]==str(Trial):
                    if video_record:
                        time.sleep(1)
                        video.communicate('q')
                    break
        else:
            print("How do you decide to count down your experiments, 'Time'or'Trial'?")
            sys.exit()
    ser_ctrl.close()
    ser_motor.close()
    print(f"training log is saved in {os.path.basename(log_name)}")

    

    

