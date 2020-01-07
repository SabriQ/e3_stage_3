from linear_track_funcs import *
from sys_camera import *
def stage_3_train(serial_ports=[r'/dev/ttyUSB0',r'/dev/ttyUSB1'],mouse_id=r"192137",video_record = False,
             according_to="Trial",Time=1200,Trial=60,data_dir=r"C:\Users\Sabri\Desktop\test"):
    '''
    stage3 is shuttle run ...
    '''
    #检查端口是否可用
    check_ports(serial_ports)
    ser_ctrl = serial.Serial(serial_ports[0],baudrate=9600,timeout=0.1)
    ser_motor = serial.Serial(serial_ports[1],baudrate=9600,timeout=0.1)
    countdown(3)
    print(serial_ports[1])
    #设置数据存放路径 年月日；设置log文件，视频文件的名字；context_orders
    data_dir = os.path.join(data_dir,time.strftime("%Y%m%d", time.localtime()))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"{data_dir} is created")
#    if not os.path.exists(data_dir):
#        print("path is wrong")
#        sys.exit()
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+"train"+'_log.csv')
    video_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+"train"+'.mp4')
    context_orders = RandomContextOrder()
    current_context_orders = context_orders.pop()
    #初始化context的位置
    # case 48 0 move to context 1
    # case 51 3 move to context 2
    # case 52 4 pump ll
    # case 53 5 pump lr
    # case 54 6 pump rl
    # case 55 7 pump rr
    print(">>>>>>")
    ser_motor.write("0".encode())
    ser_motor.write("55".encode())
    current_context = "1"
    print("<<<<<<")

    #开始实验
    #开始视频录制
    if video_record:
        input("请按Enter开始实验（倒计时3s之后开启，摄像头会率先启动）：")
        video = video_recording(video_name)
        print(f'{os.path.basename(video_name)} is recording')
        countdown(3)
    else:
        input("请按Enter开始实验:")
        #video = video_online_play()
    #在log文件中写入title
    with open(log_name, 'w',newline="",encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Trial_Num","Choice","Choice_Count","Choice_Class","A_NosePoke","A_ContextEnter","A_ContextExit","A_Choice","A_ContextREnter","A_ContextRExit","P_NosePoke","P_ContextEnter","P_ContextExit","P_Choice","P_ContextREnter","P_ContextRExit"])
    print(["Trial_Num","Choice","Choice_Count","Choice_Class"])
    
    video_start_time = time.time()
    
    Trial_Num=[];Choice=[];Choice_Class=[]
    A_NosePoke=[];A_ContextEnter=[];A_ContextExit=[];A_Choice=[];A_ContextREnter=[];A_ContextRExit=[]
    P_NosePoke=[];P_ContextEnter=[];P_ContextExit=[];P_Choice=[];P_ContextREnter=[];P_ContextRExit=[]
    show_info = "Ready "
    while True:
        info = ser_ctrl.readline().decode("utf-8").strip().split(" ")# waiting for 0.1s
        time_elapse = time.time()-video_start_time
        if len(info)>1:
            show_info = ''.join([i for i in info])
            if "Stat1:" in info:
                P_NosePoke.append(time_elapse);
                ser_motor.write("5".encode())
                if len(current_context_orders) == 0: 
                    if len(context_orders) != 0:
                        current_context_orders = context_orders.pop()
                    else:
                        time.sleep(1)
                        if video_record:
                            video.communicate('q')
                        print("all blocks are already done!")
                        break
                #获取下一个conext 
                if len(Choice_Class)>0:
                    if Choice_Class[-1]=="correct":
                        next_context = str(current_context_orders.pop())
                    else:
                        next_context = current_context
                else:                    
                    next_context = str(current_context_orders.pop())
                #print(current_context,next_context)
                #切换context
                if current_context != next_context:
                    if next_context == "1":
                        ser_motor.write("0".encode())
                    if next_context == "2":
                        ser_motor.write("3".encode())               
                current_context = next_context                        
            if "Stat2:" in info:
                P_ContextEnter.append(time_elapse)
            if "Stat3:" in info:
                P_ContextExit.append(time_elapse)
            if "Stat4:" in info:
                P_Choice.append(time_elapse);
                print(info,end=" ")
                if next_context  == "1" and info[-1]=="choice_r":
                    ser_motor.write("77".encode())
                    Choice_Class.append("correct")
                elif next_context == "2" and info[-1] == "choice_l":
                    ser_motor.write("66".encode())
                    Choice_Class.append("correct")
                else:
                    Choice_Class.append("wrong")
            if "Stat5:" in info:
                P_ContextREnter.append(time_elapse)
            if "Stat6:" in info:
                P_ContextRExit.append(time_elapse)
            if "Sum:" in info:
                Trial_Num.append(info[1])
                Choice.append(info[2])
                Choice_count = info[3]
                A_NosePoke.append(info[4])
                A_ContextEnter.append(info[5])
                A_ContextExit.append(info[6])
                A_Choice.append(info[7])
                A_ContextREnter.append(info[8])
                A_ContextRExit.append(info[9])
                
                row=[Trial_Num[-1],Choice[-1],Choice_count,Choice_Class[-1]
                     ,A_NosePoke[-1],A_ContextEnter[-1],A_ContextExit[-1],A_Choice[-1],A_ContextREnter[-1],A_ContextRExit[-1]
                     ,P_NosePoke[-1],P_ContextEnter[-1],P_ContextExit[-1],P_Choice[-1],P_ContextREnter[-1],P_ContextRExit[-1]]
                with open(log_name,"a",newline="\n",encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(row)
                print(row[0:4])
        #时间进度输出
            if "Sum" in show_info:
                show_info = "Ready "
        print(f"\r{show_info}".ljust(25),f"current_context: {current_context}".ljust(20),f"time elapses {round(time_elapse,1)}s  ",end="")
        #sys.stdout.write("time elapses %.1fs"%(time_elapse))
        #sys.stdout.write("\r")
        #another situation: for certain number of trials
        if according_to == "Time":
            if time_elapse >=Time:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        elif according_to =="Trial": # trial <= 90 
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
def stage_3_test(serial_ports=[r'/dev/ttyUSB0',r'/dev/ttyUSB1'],mouse_id=r"192137",video_record = False,
             according_to="Trial",Time=1200,Trial=60,data_dir=r"C:\Users\Sabri\Desktop\test"):
    '''
    stage3 is shuttle run ...
    '''
    #检查端口是否可用
    check_ports(serial_ports)
    ser_ctrl = serial.Serial(serial_ports[0],baudrate=9600,timeout=0.1)
    ser_motor = serial.Serial(serial_ports[1],baudrate=9600,timeout=0.1)
    countdown(3)
    print(serial_ports[1])
    #设置数据存放路径 年月日；设置log文件，视频文件的名字；context_orders
    data_dir = os.path.join(data_dir,time.strftime("%Y%m%d", time.localtime()))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"{data_dir} is created")
#    if not os.path.exists(data_dir):
#        print("path is wrong")
#        sys.exit()
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())

    log_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+"test"+'_log.csv')
    video_name = os.path.join(data_dir,current_time+"-"+mouse_id+"-"+"test"+'.mp4')
    context_orders = RandomContextOrder()
    current_context_orders = context_orders.pop()
    #初始化context的位置
    # case 48 0 move to context 1
    # case 51 3 move to context 2
    # case 52 4 pump ll
    # case 53 5 pump lr
    # case 54 6 pump rl
    # case 55 7 pump rr
    print(">>>>>>")
    ser_motor.write("0".encode())
    ser_motor.write("55".encode())
    current_context = "1"
    print("<<<<<<")

    #开始实验
    #开始视频录制
    if video_record:
        input("请按Enter开始实验（倒计时3s之后开启，摄像头会率先启动）：")
        video = video_recording(video_name)
        print(f'{os.path.basename(video_name)} is recording')
        countdown(3)
    else:
        input("请按Enter开始实验:")
        #video = video_online_play()
    #在log文件中写入title
    with open(log_name, 'w',newline="",encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Trial_Num","Choice","Choice_Count","Choice_Class","A_NosePoke","A_ContextEnter","A_ContextExit","A_Choice","A_ContextREnter","A_ContextRExit","P_NosePoke","P_ContextEnter","P_ContextExit","P_Choice","P_ContextREnter","P_ContextRExit"])
    print(["Trial_Num","Choice","Choice_Count","Choice_Class"])
    
    video_start_time = time.time()
    
    Trial_Num=[];Choice=[];Choice_Class=[]
    A_NosePoke=[];A_ContextEnter=[];A_ContextExit=[];A_Choice=[];A_ContextREnter=[];A_ContextRExit=[]
    P_NosePoke=[];P_ContextEnter=[];P_ContextExit=[];P_Choice=[];P_ContextREnter=[];P_ContextRExit=[]
    show_info = "Ready "
    while True:
        info = ser_ctrl.readline().decode("utf-8").strip().split(" ")# waiting for 0.1s
        time_elapse = time.time()-video_start_time
        if len(info)>1:
            show_info = ''.join([i for i in info])
            if "Stat1:" in info:
                P_NosePoke.append(time_elapse);
                ser_motor.write("5".encode())
                if len(current_context_orders) == 0: 
                    if len(context_orders) != 0:
                        current_context_orders = context_orders.pop()
                    else:
                        time.sleep(1)
                        if video_record:
                            video.communicate('q')
                        print("all blocks are already done!")
                        break
                #获取下一个conext 
                next_context = str(current_context_orders.pop())
                #print(current_context,next_context)
                #切换context
                if current_context != next_context:
                    if next_context == "1":
                        ser_motor.write("0".encode())
                    if next_context == "2":
                        ser_motor.write("3".encode())               
                current_context = next_context
                        
            if "Stat2:" in info:
                P_ContextEnter.append(time_elapse)
            if "Stat3:" in info:
                P_ContextExit.append(time_elapse)
            if "Stat4:" in info:
                P_Choice.append(time_elapse);
                print(info,end=" ")
                if next_context  == "1" and info[-1]=="choice_r":
                    ser_motor.write("77".encode())
                    Choice_Class.append("correct")
                elif next_context == "2" and info[-1] == "choice_l":
                    ser_motor.write("66".encode())
                    Choice_Class.append("correct")
                else:
                    Choice_Class.append("wrong")
            if "Stat5:" in info:
                P_ContextREnter.append(time_elapse)
            if "Stat6:" in info:
                P_ContextRExit.append(time_elapse)
            if "Sum:" in info:
                Trial_Num.append(info[1])
                Choice.append(info[2])
                Choice_count = info[3]
                A_NosePoke.append(info[4])
                A_ContextEnter.append(info[5])
                A_ContextExit.append(info[6])
                A_Choice.append(info[7])
                A_ContextREnter.append(info[8])
                A_ContextRExit.append(info[9])
                
                row=[Trial_Num[-1],Choice[-1],Choice_count,Choice_Class[-1]
                     ,A_NosePoke[-1],A_ContextEnter[-1],A_ContextExit[-1],A_Choice[-1],A_ContextREnter[-1],P_ContextRExit[-1]
                     ,P_NosePoke[-1],P_ContextEnter[-1],P_ContextExit[-1],P_Choice[-1],P_ContextREnter[-1],P_ContextRExit[-1]]
                with open(log_name,"a",newline="\n",encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(row)
                print(row[0:4])
        #时间进度输出
            if "Sum" in show_info:
                show_info = "Ready "
        print(f"\r{show_info}".ljust(25),f"current_context: {current_context}".ljust(20),f"time elapses {round(time_elapse,1)}s  ",end="")
        #sys.stdout.write("time elapses %.1fs"%(time_elapse))
        #sys.stdout.write("\r")
        #another situation: for certain number of trials
        if according_to == "Time":
            if time_elapse >=Time:
                if video_record:
                    time.sleep(1)
                    video.communicate('q')
                break
        elif according_to =="Trial": # trial <= 90 
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
