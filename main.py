# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import cv2
import pyautogui
import win32api
import win32gui
import numpy
import time
from PIL import ImageGrab

# 窗口标题和窗口坐标
windows_tittle = '天天象棋'
game_pos = (0,0,0,0,)

# 获取游戏窗口坐标
def getGameWindow():
    # FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
    window = win32gui.FindWindow(None, windows_tittle)

    # 没有定位到游戏窗体
    while not window:
        print('Failed to locate the game window , reposition the game window after 10 seconds...')
        time.sleep(10)
        window = win32gui.FindWindow(None, windows_tittle)

    # 定位到游戏窗体
    # 置顶游戏窗口
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)
    # print(pos)
    print("Game windows at " + str(pos))
    return (pos[0], pos[1], pos[2], pos[3])

# 根据坐标截取游戏画面
def getGameImage(game_pos):
    print('shot game screen')
    games_screen_img=ImageGrab.grab(bbox=(game_pos))
    games_screen_img.save('./img/games_screen_img.png')

# 对比找出需要点击的位置坐标
def get_click_positon(img_model_path):
    img_background=cv2.imread('./img/games_screen_img.png')
    img_point = cv2.imread(img_model_path)
    height, width = img_point.shape[:2]
    position = cv2.matchTemplate(img_background,img_point,cv2.TM_SQDIFF_NORMED)
    # min_val, max_Val, minLoc, maxLoc = cv2.minMaxLoc(position)
    minLoc = cv2.minMaxLoc(position)[2]
    maxLoc=(minLoc[0]+width, minLoc[1]+height)
    center_position=(int((minLoc[0]+maxLoc[0])/2),int((minLoc[1]+maxLoc[1])/2))
    # print(center_position)
    return center_position

# 自动点击坐标位置
def auto_click(var_avg):
    # 待点击位置相对游戏窗口坐标+游戏窗口左上角坐标 = 待点击位置绝对坐标
    pyautogui.click(var_avg[0]+game_pos[0], var_avg[1]+game_pos[1],button='left')

# 传入指定路径图片调用上面的方法进行点击
def auto_find_click(img_model_path,name):
    avg = get_click_positon(img_model_path)
    print(f'clicking{name}')
    # pyautogui.moveTo(avg)
    auto_click(avg)
    time.sleep(2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i= 1
    # 死循环 持续点击
    while True:
        game_pos = getGameWindow()
        game_img = getGameImage(game_pos)
        # center_positions=get_click_positon()
        # auto_find_click("./img/quick_start.png","快速开始")
        # auto_find_click("./img/start.png","开始")
        auto_find_click("./img/yes.png","确定")
        auto_find_click('./img/change.png','切换对手')
        print(f'sleep 60 second，running total {i}'+' minutes')
        i =i+1
        if i>600:sys.exit(0)
        time.sleep(60)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
