#from func_train import stage_3
from func_test import stage_3
from info import send_wechat_by_serverchan
import sys
if __name__ == "__main__":
    send_wechat = send_wechat_by_serverchan()
    stage_3(serial_ports=[r'/dev/ttyUSB0',r'/dev/ttyUSB1'],mouse_id=sys.argv[1],note="test",video_record = False,according_to="Trial",Time=1200,Trial=60,data_dir=r"/home/qiushou/Documents/data/linear_track")
    send_wechat(f"{sys.argv[1]} finish training","nothing")
