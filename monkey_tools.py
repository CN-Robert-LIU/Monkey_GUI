import glob
import json
import logging
import os
import re
import time
import tkinter as tk
from tkinter import ttk
from tkinter.constants import E
# import tkinter.messagebox

window = tk.Tk()

window.title("Demo APP")


# 设置窗口适应属性
window.resizable(width=True, height=True)
window.attributes("-alpha", 0.7)
window.attributes('-toolwindow', False,
                  '-alpha', 1,
                  '-fullscreen', False,
                  '-topmost', True)
# window.overrideredirect(True)

# 获取当前屏幕分辨率
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
# width = screenwidth
# height = screenheight * 0.92
width = 1680
height = 780


# 根据分辨率设置窗口大小
alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth-width)/2, (screenheight-height)/3)
window.geometry(alignstr)

# ----frame-----
frame_main1 = tk.Frame(window, bg="#F2F2F2", height=100, width=360)
frame_main1.grid(column=1, row=1, padx=10, pady=10)

frame_main2 = tk.Frame(window, bg="#F2F2F2", height=100, width=400)
frame_main2.grid(column=2, row=1)

frame_main3 = tk.Frame(window, bg="#F2F2F2", height=200, width=370)
frame_main3.grid(column=1, row=2)

frame_main4 = tk.Frame(window, bg="#F2F2F2", height=200, width=360)
frame_main4.grid(column=2, row=2)
frame_main5 = tk.Frame(window, bg="#F2F2F2",
                       height=height*0.8, width=width-400)
frame_main5.grid(column=3, columnspan=2, row=1, padx=15, pady=15, rowspan=3)

#

# -----menu菜单功能，暂时不要后续添加--------
# meun_main = tk.Menu()
# # meun_main.grid()
# filemenu = tk.Menu(meun_main, tearoff=1)
# meun_main.add_cascade(label='File', menu=filemenu)
# filemenu.add_command(label='Monkey')
# filemenu.add_command(label='Screen')
# filemenu.add_command(label='Instructions')
# filemenu.add_command(label='About')
# window.config(menu = filemenu)


def clear_log():
    text_log.delete("1.0", "end")


# text_log.insert("end","adasd21dadd")

# =================================================================
# ------主页lable显示引导---------------
# 刷新设备说明
# =================================================================
lable_main1 = tk.Label(frame_main1, justify="left", height=5, width=35, bg="#E5E5E5", font=(
    "微软雅黑", 10), text="准备工作：\n1.进入开发者选项打开测试机USB调试功能\n2.点击刷新设备\n3.手机端确认USB调试（若未提示则跳过此步骤）\n4.设备连接成功")
lable_main1.grid()
# monkey参数说明
lable_main2 = tk.Label(frame_main2, justify="left", height=5, width=40, bg="#E5E5E5", font=(
    "微软雅黑", 10), text="参数说明：\n1.Package：包名，可点击获取，也可以手动输入\n2.Seeds：随机值，默认取当天日期，也可手动输入\n3.Throttle：点击频率，默认300ms，可手动输入\n4.Count：总操作数，默认50万，可手动修改")
lable_main2.grid()
# =================================================================
# -------Log缓存区域，显示自定义日志--------
# =================================================================

label_log_h = tk.Label(frame_main5, bg="#E5E5E5", justify="left", text="0：触摸屏幕事件百分比，即参数–pct-touch\t 1：滑动事件百分比，即参数–pct-motion \
\t2：缩放事件百分比，即参数–pct-pinchzoom\n3：轨迹球的事件百分比，即参数–pct-trackball \
\t 4：屏幕旋转事件百分比，即参数–pct-rotation\t5：基本导航事件百分比，即参数–pct-nav \
\n6：主要导航事件百分比，即参数–pct-majornav\t 7：系统事件百分比，即参数–pct-syskeys \
\t8：Activity启动事件百分比，即参数–pct-appswitch\n9：键盘翻转事件百分比，即参数–pct-flip \
\t10：其他事件百分比，即参数–pct-anyevent")
label_log_h.grid(column=1, row=1)

lable_log = tk.Label(frame_main5, justify="left",
                     text="日志区", font=("微软雅黑", 14))
lable_log.grid(column=1, row=2, padx=1, pady=1)

text_log = tk.Text(frame_main5, bg="#5B5B5B",
                   fg="#FFFFFF", width=140, height=40)
text_log.grid(column=1, row=3, rowspan=2)

button_clearLog = tk.Button(frame_main5, text="清除", font=(
    "微软雅黑", 8), bg="#836FFF", fg="#FFFFFF", command=clear_log)
button_clearLog.grid(column=2, row=2, sticky="n")


# ----listbox用于显示当前设备列表-----
lb = tk.Listbox(frame_main3, height=30, width=28, bg="#CDCDB4", fg="#551A8B")
lb.grid(column=0, row=0, padx=10, pady=10)


# -----frame4上的参数配置-----
lab1 = tk.Label(frame_main4, text="配置项", bg="#F2F2F2", font=(11))
lab2 = tk.Label(frame_main4, text="Package", bg="#F2F2F2")
lab3 = tk.Label(frame_main4, text="Seeds", bg="#F2F2F2")
lab4 = tk.Label(frame_main4, text="Throttle", bg="#F2F2F2")
lab5 = tk.Label(frame_main4, text="Count", bg="#F2F2F2")
label_pct_1 = tk.Label(frame_main4, text="pct_touch", bg="#F2F2F2")
label_pct_2 = tk.Label(frame_main4, text="pct_motion", bg="#F2F2F2")
label_pct_3 = tk.Label(frame_main4, text="pct_trackball", bg="#F2F2F2")
label_pct_4 = tk.Label(frame_main4, text="pct_syskeys", bg="#F2F2F2")
label_pct_5 = tk.Label(frame_main4, text="pct_nav", bg="#F2F2F2")
label_pct_6 = tk.Label(frame_main4, text="pct_majornav", bg="#F2F2F2")
label_pct_7 = tk.Label(frame_main4, text="pct_appswitch", bg="#F2F2F2")
label_pct_8 = tk.Label(frame_main4, text="pct_flip", bg="#F2F2F2")
label_pct_9 = tk.Label(frame_main4, text="pct_anyevent", bg="#F2F2F2")
label_pct_10 = tk.Label(frame_main4, text="pct_pinchzoom", bg="#F2F2F2")
label_pct_11 = tk.Label(frame_main4, text="pct_permission", bg="#F2F2F2")

lab6 = tk.Label(frame_main4, text="参数", bg="#F2F2F2", font=(11))  # 第二列标题哦


lab1.grid(column=1, row=1, padx=5, pady=5)
lab2.grid(column=1, row=2, padx=5, pady=5, sticky="w")
lab3.grid(column=1, row=3, padx=5, pady=5, sticky="w")
lab4.grid(column=1, row=4, padx=5, pady=5, sticky="w")
lab5.grid(column=1, row=5, padx=5, pady=5, sticky="w")
label_pct_1.grid(column=1, row=6, padx=5, pady=5, sticky="w")
label_pct_2.grid(column=1, row=7, padx=5, pady=5, sticky="w")
label_pct_3.grid(column=1, row=8, padx=5, pady=5, sticky="w")
label_pct_4.grid(column=1, row=9, padx=5, pady=5, sticky="w")
label_pct_5.grid(column=1, row=10, padx=5, pady=5, sticky="w")
label_pct_6.grid(column=1, row=11, padx=5, pady=5, sticky="w")
label_pct_7.grid(column=1, row=12, padx=5, pady=5, sticky="w")
label_pct_8.grid(column=1, row=13, padx=5, pady=5, sticky="w")
label_pct_9.grid(column=1, row=14, padx=5, pady=5, sticky="w")
label_pct_10.grid(column=1, row=15, padx=5, pady=5, sticky="w")
label_pct_11.grid(column=1, row=16, padx=5, pady=5, sticky="w")
lab6.grid(column=2, row=1, padx=1, pady=1)

# -----entry monkey参数配置-------
entry1 = tk.Entry(frame_main4)
# combox_1 = ttk.Combobox(frame_main4)
# combox_1.grid(column=2, row=2, padx=5, pady=1, sticky="w")
entry2 = tk.Entry(frame_main4)
entry3 = tk.Entry(frame_main4)
entry4 = tk.Entry(frame_main4)

entry_1 = tk.Entry(frame_main4)
entry_2 = tk.Entry(frame_main4)
entry_3 = tk.Entry(frame_main4)
entry_4 = tk.Entry(frame_main4)
entry_5 = tk.Entry(frame_main4)
entry_6 = tk.Entry(frame_main4)
entry_7 = tk.Entry(frame_main4)
entry_8 = tk.Entry(frame_main4)
entry_9 = tk.Entry(frame_main4)
entry_10 = tk.Entry(frame_main4)
entry_11 = tk.Entry(frame_main4)

entry1.grid(column=2, row=2, padx=5, pady=1, sticky="w")
entry2.grid(column=2, row=3, padx=5, pady=1, sticky="w")
entry3.grid(column=2, row=4, padx=5, pady=1, sticky="w")
entry4.grid(column=2, row=5, padx=5, pady=1, sticky="w")


entry_1.grid(column=2, row=6, padx=5, pady=1, sticky="w")
entry_2.grid(column=2, row=7, padx=5, pady=1, sticky="w")
entry_3.grid(column=2, row=8, padx=5, pady=1, sticky="w")
entry_4.grid(column=2, row=9, padx=5, pady=1, sticky="w")
entry_5.grid(column=2, row=10, padx=5, pady=1, sticky="w")
entry_6.grid(column=2, row=11, padx=5, pady=1, sticky="w")
entry_7.grid(column=2, row=12, padx=5, pady=1, sticky="w")
entry_8.grid(column=2, row=13, padx=5, pady=1, sticky="w")
entry_9.grid(column=2, row=14, padx=5, pady=1, sticky="w")
entry_10.grid(column=2, row=15, padx=5, pady=1, sticky="w")
entry_11.grid(column=2, row=16, padx=5, pady=1, sticky="w")


# ------一些可能用到的全局变量------
select_var = ""
pkg_details = ""
button_state = "disabled"
model_name = ""
close_all_cmd = True

# ------百分比------
glb_pct_touch = ""
glb_pct_motion = ""
glb_pct_trackball = ""
glb_pct_syskeys = ""
glb_pct_nav = ""
glb_pct_majornav = ""
glb_pct_appswitch = ""
glb_pct_flip = ""
glb_pct_anyevent = ""
glb_pct_pinchzoom = ""
glb_pct_permission = ""
glb_package_name = ""

# 创建一个空list存储设备
list_device = []
# 创建一个空的包项目
list_packages = []
# monkey配置残水
p = ""
s = ""
t = ""
c = ""


def monitor_monkey(deviceIDs, resuld_dir):
    print("Init Check DOS")
    # time.sleep(5)
    loop_check = True
    time_epoch_check = 0
    time_sleep_len = 10
    for devid in deviceIDs:
        while(loop_check):
            time.sleep(time_sleep_len)
            cur = os.popen(
                F"adb -s {devid} shell ps -ef|grep monkey").readline()
            ps_monkey = re.findall("shell.*?", cur)
            if(ps_monkey):
                time_epoch_check += 1
                print(F'\n第{time_epoch_check}次检查Monkey状态:')
                print(cur)
                text_log.insert('end', F'\n第{time_epoch_check}次检查Monkey状态')
                continue
            else:
                loop_check = False
    cur_cmd = os.popen('tasklist|grep cmd').readlines()
    cmd_v_len = 4 * len(deviceIDs)
    cur_cmd.reverse()
    close_cmd_index = 0
    cur_index = 0
    while(close_cmd_index < cmd_v_len):
        cmd_pid = re.findall(
            "cmd.exe\s*(\d*) Console.*?", cur_cmd[cur_index])
        cur_index += 1
        if len(cmd_pid) < 1:
            continue
        time.sleep(0.5)
        os.popen(F'taskkill /pid {int(cmd_pid[0])}')
        print(F'close cmd dos for {cmd_pid}')
        close_cmd_index += 1
    text_log.insert("end", F'\n{resuld_dir}')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    resuld_dir = resuld_dir.replace('/', '\\')
    window.wm_attributes('-topmost', False)
    os.system(F"explorer {resuld_dir}")
    print(F'打开目录\t{resuld_dir}')


def find_and_init():
    # def find_devices():
    global list_device, model_name
    list_device.clear()
    logging.basicConfig(level=logging.INFO)
    try:
        d_lists = os.popen("adb devices -l").readlines()

    except IndexError:
        logging.error("d_lists  ->  IndexError")

    except TypeError:
        logging.error("d_lists  ->  TypeError")

    else:
        pass
    logging.error(d_lists)
    d_lists.remove(d_lists[len(d_lists)-1])
    d_lists.remove(d_lists[0])
    lb.delete("0", "end")
    logging.info(d_lists)
    # time.sleep(3)
    if len(d_lists) == 0:
        lb.insert("end", "未检测到设备，请连接测试机...")
        text_log.insert("end", "未检测到设备，请连接测试机...\n")
        text_log.yview_moveto(1)
        text_log.update()
    elif "unauthorized" in d_lists[0]:
        lb.insert("end", "请在手机上点击允许USB调试...")
        text_log.insert("end", "请在手机上点击允许USB调试...\n")
        text_log.yview_moveto(1)
        text_log.update()
    else:

        text_log.insert("end", "设备已连接，请选择设备进行后续操作！\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        for i in d_lists:
            reg_serial = re.findall("(.*?)device", i)
            model_org = os.popen(
                "adb -s "+str(reg_serial[0])+" shell getprop ro.product.model").readlines()
            logging.info(reg_serial[0].replace(
                "\t", "")+"："+model_org[0].replace("\n", ""))

            # 将设备信息添加到listbox中
            per_list = reg_serial[0].replace("\t", "")
            print("设备列表为：", per_list)
            os.system("adb -s "+str(per_list)+" logcat -c")
            lb.insert("end", model_org[0].replace(
                "\n", "").replace(" ", "")+"："+per_list)
            model_name = model_org[0].replace("\n", "").replace(" ", "")
            list_device.append(per_list)


# ------读写配置文件-----------
    # def init_config():
    entry1.delete(0, "end")
    entry2.delete(0, "end")
    entry3.delete(0, "end")
    entry4.delete(0, "end")
    # time.sleep(3)
    if os.path.exists("config.json"):
        with open('config.json', encoding="utf-8") as ff:
            json_data = json.load(ff)
            print(json_data.keys())
            entry1.insert("end", json_data["pkg"])
            # entry2.insert("end", time.strftime(
            #     "%Y%m%d%H%M%S", time.localtime())[2:8])
            entry2.insert("end", json_data["seed"])
            entry3.insert("end", json_data["thr"])
            entry4.insert("end", json_data["total"])

    else:
        config_file = open('config.json', 'w', encoding='utf-8')
        # json_data = {"pkg":"请在此处填写包名...","sd":time.strftime("%Y%m%d%H%M%S", time.localtime())[2:8],"thr":"300","total":"500000"}
        json_data = {"pkg": "请在此处填写包名...", "thr": "300", "total": "500000"}
        json.dump(json_data, config_file, ensure_ascii=False)
        config_file.close()

    # p=entry1.get()
    # s=entry2.get()
    # t=entry3.get()
    # c=entry4.get()


#  -----------按钮事件--------
# 刷新设备按钮
button = tk.Button(frame_main3, text="刷新设备", font=(
    "微软雅黑", 15), bg="#8FBC8F", fg="#FFFFFF", command=find_and_init)
button.grid(column=0, row=1)


# --------获取当前包名---------
def get_pkg():
    global select_var
    global pkg_details
    global button_state
    logging.info(select_var)
    # global select_var
    if len(lb.curselection()) == 0:
        tk.messagebox.showerror(title='设备选取异常', message='请先选取设备')
        return
    selected = lb.get(lb.curselection())

    print("我也不知道这里会不会报错 ", selected)

    print("原始的", selected, type(selected))
    reg_device = ".*?：(.*)"
    select_device = re.findall(reg_device, selected)
    print("选择的设备是", select_device[0])
    select_var = select_device[0]

    try:
        cur = os.popen("adb -s "+str(select_var) +
                       " shell dumpsys window | findstr mCurrentFocus").readline()
        result = re.findall("mCurrentFocus=Window{.*?u0 (.*?)/.*?}", cur)
        if result == '':
            result = re.findall("mCurrentFocus=Window{.*?u0 (.*?)}", cur)
        print(result)
        pkg_details = ''
        if result == '':
            pkg_details = ''
        elif len(result) > 1:
            pkg_details = result[-1]
        else:
            pkg_details = result
        entry1.delete(0, "end")
        entry1.insert("end", F"{pkg_details}")
        logging.info(cur)

        # cur1 = os.popen("adb -s "+str(select_var) +
        #                 " shell pm list packages -3").readlines()
        # result1 = []
        # for cur1_0 in cur1:
        #     result_1 = re.findall("package:(.*?)\n", cur1_0)
        #     if result_1:
        #         result1.append(result_1)
        # if len(result1):
        #     combox_1['values'] = result1
        # else:
        #     combox_1['values'] = ''
        # # for result1_0 in result1:
        # #     logging.info(result1_0)
        # combox_1.set(result1[0])
        cur1 = os.popen("adb -s "+str(select_var) +
                        " shell pm list packages -3").readlines()
        text_log.insert("end", "\n第三方安装包列表:\n")
        for cur1_0 in cur1:
            result_1 = re.findall("package:(.*?)\n", cur1_0)
            if result_1:
                text_log.insert("end", F"\r{result_1}\n")

        button_runmonkey['bg'] = "#8FBC8F"
        button_runmonkey['state'] = 'normal'

    except IndexError:
        entry1.delete(0, "end")
        entry1.insert("end", "获取失败...")
        tk.messagebox.showerror(
            "Error了吧，哈哈哈！", "请注意：\n  1.确认设备已经连接。\n  2.需要获取包名的应用处于前台状态！")
        entry1.delete(0, "end")
        entry1.insert("end", "点击重试...")

    except TypeError:
        entry1.delete(0, "end")
        entry1.insert("end", "未选择设备哦！")
        tk.messagebox.showerror("Error，这个不是Bug...", "没有选择设备哦！")
        entry1.delete(0, "end")
        entry1.insert("end", "点击重试...")

    else:

        entry1.delete(0, "end")
        entry1.insert("end", pkg_details)
        text_log.insert("end", "获取包名成功！！！\n\n")
        text_log.insert("end", F"{pkg_details}\n\n")

        text_log.yview_moveto(1)
        text_log.update()


def check_pct():
    global glb_pct_touch
    global glb_pct_motion
    global glb_pct_trackball
    global glb_pct_syskeys
    global glb_pct_nav
    global glb_pct_majornav
    global glb_pct_appswitch
    global glb_pct_flip
    global glb_pct_anyevent
    global glb_pct_pinchzoom
    global glb_pct_permission

    glb_pct_touch = entry_1.get()
    glb_pct_motion = entry_2.get()
    glb_pct_trackball = entry_3.get()
    glb_pct_syskeys = entry_4.get()
    glb_pct_nav = entry_5.get()
    glb_pct_majornav = entry_6.get()
    glb_pct_appswitch = entry_7.get()
    glb_pct_flip = entry_8.get()
    glb_pct_anyevent = entry_9.get()
    glb_pct_pinchzoom = entry_10.get()
    glb_pct_permission = entry_11.get()

    sum = 0
    varList = [glb_pct_touch, glb_pct_motion, glb_pct_trackball,
               glb_pct_syskeys, glb_pct_nav, glb_pct_majornav,
               glb_pct_appswitch, glb_pct_flip, glb_pct_anyevent,
               glb_pct_pinchzoom, glb_pct_permission]
    # lableList = ["glb_pct_touch", "glb_pct_motion", "glb_pct_trackball",
    #              "glb_pct_syskeys", "glb_pct_nav", "glb_pct_majornav",
    #              "glb_pct_appswitch", "glb_pct_flip", "glb_pct_anyevent",
    #              "glb_pct_pinchzoom", "glb_pct_permission"]
    labelValueDict = {
        "pct_touch": glb_pct_touch,
        "pct_motion": glb_pct_motion,
        "pct_trackball": glb_pct_trackball,
        "pct_syskeys": glb_pct_syskeys,
        "pct_nav": glb_pct_nav,
        "pct_majornav": glb_pct_majornav,
        "pct_appswitch": glb_pct_appswitch,
        "pct_flip": glb_pct_flip,
        "pct_anyevent": glb_pct_anyevent,
        "pct_pinchzoom": glb_pct_pinchzoom,
        "pct_permission": glb_pct_permission,
    }
    for label, value in labelValueDict.items():
        if value.isdigit():
            value = int(value)
            if value > 100:
                tk.messagebox.showerror(
                    title=F"{label}信息", message=F"{label}为{value}，超过100")
                return 1
            else:
                sum += value
        elif value == '':
            continue
        else:
            tk.messagebox.showerror(
                title=F"{label}信息", message=F"{label}为{value}，不属于整数")
            return 1

    if sum > 100:
        tk.messagebox.showerror(title="百分比综合异常", message="pct超过100了，请重新分配哦")
        return 1
    else:
        return 0


def run_monkey():
    global glb_pct_touch
    global glb_pct_motion
    global glb_pct_trackball
    global glb_pct_syskeys
    global glb_pct_nav
    global glb_pct_majornav
    global glb_pct_appswitch
    global glb_pct_flip
    global glb_pct_anyevent
    global glb_pct_pinchzoom
    global glb_pct_permission
    global select_var
    check_pct_val = check_pct()
    if(check_pct_val):
        return
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())[4:12]

    if not os.path.exists("./Result/"+str(now_time)):
        text_log.insert("end", "创建必要资源文件夹....\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        os.makedirs("./Result/"+str(now_time))

    if not os.path.exists("./script/"+str(now_time)):
        text_log.insert("end", "创建必要资源文件夹....\n\n")
        text_log.yview_moveto(1)
        text_log.update()
        os.makedirs("./script/"+str(now_time))
    global p, s, t, c
    p = entry1.get()
    # p = combox_1.get()
    s = entry2.get()
    t = entry3.get()
    c = entry4.get()

    global button_state
    button_state = "disabled"
    print(pkg_details)
    text_log.insert("end", "即将开始初始化资源，请稍等...\n")
    labelValueDict = {
        "pct_touch": glb_pct_touch,
        "pct_motion": glb_pct_motion,
        "pct_trackball": glb_pct_trackball,
        "pct_syskeys": glb_pct_syskeys,
        "pct_nav": glb_pct_nav,
        "pct_majornav": glb_pct_majornav,
        "pct_appswitch": glb_pct_appswitch,
        "pct_flip": glb_pct_flip,
        "pct_anyevent": glb_pct_anyevent,
        "pct_pinchzoom": glb_pct_pinchzoom,
        "pct_permission": glb_pct_permission,
    }
    if len(select_var) > 0:

        if entry1.get() in (u"请在此处填写包名...", ""):
            tk.messagebox.showerror("你又错了！！！", "不出意外的话你包名肯定不对！！")

        else:

            for d in [select_var]:
                bat_monkey = str(d[:8])+"_monkey_"+str(pkg_details)+".bat"
                with open("script\\"+str(now_time)+"\\"+bat_monkey, "w") as f:
                    text_log.insert("end", "生成"+str(d)+"---monkey脚本...\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    str_file = ''
                    str_file = '@echo off\necho start  monkey test\ntitle Monkey\nadb -s ' + \
                        str(d)+' shell monkey -s '+str(s) + \
                        ' -p '+str(p)+' --throttle '+str(t)
                    for label, value in labelValueDict.items():
                        if value != '':
                            label_new = label.replace('_', '-')
                            str_file += f" --{label_new} {value}"
                    resuld_dir = './Result/'+str(now_time)
                    str_file += ' --ignore-crashes --ignore-native-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v -v ' + \
                        str(c)+' > '+resuld_dir + \
                        '/'+str(d[:8])+'_monkey.log'
                    # f.write('@echo off\necho start  monkey test\ntitle Monkey\nadb -s '+str(d)+' shell monkey -s '+str(s)+' -p '+str(p)+' --throttle '+str(t) +
                    # ' --ignore-crashes --ignore-native-crashes --ignore-security-exceptions --ignore-timeouts --monitor-native-crashes -v -v -v '+str(c)+' > ./Result/'+str(now_time)+'/'+str(d[:8])+'_monkey.log')
                    f.write(str_file)
                bat_fc = str(d[:8])+"_fc_"+str(pkg_details)+".bat"
                with open("script\\"+str(now_time)+"\\"+bat_fc, "w") as ff:
                    text_log.insert("end", "生成"+str(d)+"---crash监控脚本...\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    ff.write('@echo off\necho Start collecting crash logs\ntitle Crash\nadb -s '+str(
                        d)+' logcat -s AndroidRuntime > ./Result/'+str(now_time)+'/'+str(d[:8])+'_crash.log')
                bat_memory = str(d[:8])+"_memory_"+str(pkg_details)+".bat"
                with open("script\\"+str(now_time)+"\\"+bat_memory, "w") as fff:
                    text_log.insert("end", "生成"+str(d)+"---内存监控脚本...\n\n")
                    text_log.yview_moveto(1)
                    text_log.update()
                    fff.write('@echo off\necho Start collecting memory logs\ntitle Memory\n:memory\nadb -s '+str(d)+' shell dumpsys meminfo '+str(
                        p)+' | findstr TOTAL: > ./Result/'+str(now_time)+'/'+str(d[:8])+'_memory.log\nping -n 30 127.0.0.1>nul\ngoto memory')

            bat_finally = glob.glob("script\\"+str(now_time)+"\\*.bat")
            print("最终的bat有", bat_finally)
            time.sleep(2)
            text_log.insert("end", "一切准备就绪，即将启动所有骚操作！！！\n\n")
            text_log.yview_moveto(1)
            text_log.update()

            text_log.insert("end", F"\n{str_file}")
            text_log.insert("end", "\n包名："+p)
            text_log.insert("end", "\nseeds值："+s)
            text_log.insert("end", "\nthrottle值："+t)
            text_log.insert("end", "\n总测试数："+c)
            for label, value in labelValueDict.items():
                if value != '':
                    text_log.insert("end", F"\n{label}:\t{value}")

            for gogo in bat_finally:
                os.system("start "+gogo)
                time.sleep(1)
            monitor_monkey([select_var], resuld_dir)

    else:
        # len(list_device)==0:
        tk.messagebox.showerror(
            "你又错了！！！", "请注意：\n  1.确认设备已经连接。\n  2.确认包名不为空！！")


# 获取包名按钮
button_getpkg = tk.Button(frame_main4, text="获取包名", fg="#FFFFFF", font=(
    "", 9), bg="#8FBC8F", command=get_pkg)
button_getpkg.grid(column=3, row=2, padx=5, pady=5, sticky="w")
notice_lable = tk.Label(
    frame_main4, text="获取包名前，\n先选择设备。", justify="left", fg="red")
notice_lable.grid(column=3, row=3)

button_make_res = tk.Button()


# Monkey启动按钮
if button_state == "disabled":
    button_runmonkey = tk.Button(frame_main4, text="Run!!!", state="disabled", fg="#5B5B5B", font=(
        "微软雅黑", 15), bg="#FFFFFF", command=run_monkey)
    button_runmonkey.grid(column=2, row=19, padx=25, pady=5, sticky="w")
else:
    button_runmonkey = tk.Button(frame_main4, text="Run!!!", fg="#FFFFFF", font=(
        "微软雅黑", 15), bg="#8FBC8F", command=run_monkey)
    button_runmonkey.grid(column=2, row=19, padx=25, pady=5, sticky="w")
    button_state = "disabled"

window.mainloop()
