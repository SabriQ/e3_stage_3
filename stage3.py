from func import stage_3
from info import send_email
import sys
if __name__ == "__main__":
    stage_3(serial_ports=[r'/dev/ttyUSB1',r'/dev/ttyUSB0'],mouse_id=sys.argv[1],video_record = False,according_to="Trial",Time=1200,Trial=60,data_dir=r"/home/qiushou/Documents/data/linear_track")
    send_email("sqiu@ion.ac.cn","info from python",f"{sys.argv[1] finish training}")
