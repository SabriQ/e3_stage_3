#from func_train import stage_3
from stage1 import stage_1
from stage3 import stage_3_train
from stage3 import stage_3_test
from info import send_wechat_by_serverchan
import sys
if __name__ == "__main__":
    send_wechat = send_wechat_by_serverchan()
    stage_1(serial_ports=[r'/dev/ttyUSB1',r'/dev/ttyUSB0'],mouse_id=sys.argv[1],note="test",video_record = False,according_to="Time",Time=2400,Trial=60,data_dir=r"/home/qiushou/Documents/data/linear_track")
    send_wechat(f"{sys.argv[1]} finish training","nothing")
