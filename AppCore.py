import flet as ft
import math
from typing import Union, Optional
from json import load as json_load, dump as json_dump
from flet_core.file_picker import FilePickerFile
from flet_core.control_event import ControlEvent
from TabsComponent import HomeTab, CanvasTab
from Utility import AudioPlayer
from Source import UI_JSON

class App:
    global_settings: dict = json_load(open(UI_JSON, 'r', encoding='U8'))

    def __init__(self, page: ft.Page) -> None:

        # 界面
        self.page = page

        # 内置核心控件
        # 打开的新选项卡
        self.newTabWithField: list[ft.Tab] = []
        
        # 内置播放器
        self.audioPlayer = AudioPlayer()
        
        # 内置通用字体配置
        self.commonFont = {
            'size' : 12,
            'weight' : ft.FontWeight.W_900,
            'family' : 'Consolas',
            'color' : ft.colors.BLACK
        }

        # 内置功能的核心函数
        self.selfCore()

        # 上方工具栏
        self.statusNow: bool = self.global_settings['statusNow']
        self.statusIcon = ft.Icon(
            name=ft.icons.WB_SUNNY_OUTLINED if self.statusNow else ft.icons.MODE_NIGHT
        )
        self.swtichBtn = ft.Switch(
            value=self.statusNow
        )

        self.openBtn = ft.ElevatedButton(
            text='Open',
            icon=ft.icons.FILE_OPEN,
            icon_color=ft.colors.DEEP_PURPLE_900,
        )
        self.createOne = ft.ElevatedButton(
            text='Create One',
            icon=ft.icons.CREATE,
            icon_color=ft.colors.SHADOW,
            on_click=self.createTab
        )
        self.settingsBtn = ft.ElevatedButton(
            text='Settings',
            icon=ft.icons.SETTINGS,
            icon_color=ft.colors.INDIGO,
        )
        self.alphaSlider = ft.Slider(
            height=10,
            min=10,
            max=100,
            value=100,
            divisions=20,
            round=5,
            width=400,
            thumb_color=ft.colors.RED,
            active_color=ft.colors.GREEN_900,
            inactive_color=ft.colors.YELLOW,
        )
        self.topTools = ft.Row(
            controls=[self.swtichBtn, self.statusIcon,
                      self.openBtn, self.createOne,
                      self.settingsBtn, self.alphaSlider
            ],
        )

        # 上方工具栏函数
        self.setTopTools()

        # 中间分割线
        self.dividerLine = ft.Divider(
            height=10,
            thickness=5,
            color=ft.colors.BLACK87 if self.statusNow else ft.colors.LIGHT_BLUE_900,
        )

        # 下方tab
        # 默认主界面
        self.defaultTab = HomeTab()
        # 画板
        self.drawBoard = CanvasTab()
        
        self.tabBar = ft.Tabs(
            label_color=ft.colors.DEEP_PURPLE_ACCENT_700,
            divider_color=ft.colors.RED,
            unselected_label_color=ft.colors.WHITE70,
            overlay_color=ft.colors.TEAL_100,
            indicator_color=ft.colors.ON_SURFACE,
            indicator_border_radius=10,
            selected_index=0,
            scrollable=True
        )

        # 下方控件函数
        self.tabBarFuncs()

        # 界面核心函数
        self.setPage()
        self.setWidgets()

    def setPage(self):
        self.page.on_resize = self.page_resize
        self.page.window_opacity = 1
        self.page.title = "FlexEditor"
        self.page.theme_mode = None if self.statusNow else ft.ThemeMode.DARK
        self.page.window_min_width = self.global_settings['window_min_width']
        self.page.window_min_height = self.global_settings['window_min_height']
        self.page.bgcolor = ft.colors.TEAL if self.statusNow else None
        self.page.overlay.append(self.audioPlayer)
        self.page.window_center()
        self.page.update()

    def setWidgets(self):
        self.page.add(self.topTools, self.dividerLine, self.tabBar)

    def setTopTools(self):
        # 主题模式
        def swtichBtn_on_change(e):
            self.statusNow = not self.statusNow
            self.page.theme_mode = None if self.statusNow else ft.ThemeMode.DARK
            self.swtichBtn.value = self.statusNow
            self.statusIcon.name = ft.icons.WB_SUNNY_OUTLINED if self.statusNow else ft.icons.MODE_NIGHT
            self.dividerLine.color = ft.colors.BLACK87 if self.statusNow else ft.colors.LIGHT_BLUE_900
            self.page.bgcolor = ft.colors.TEAL if self.statusNow else None
            self.page.update()

        # 透明度
        def alpha_on_change(e):
            self.page.window_opacity = self.alphaSlider.value / 100
            self.page.update()

        self.alphaSlider.on_change = alpha_on_change
        self.swtichBtn.on_change = swtichBtn_on_change

    def tabBarFuncs(self):
        def open_url(e):
            self.page.launch_url(e.data)
        self.defaultTab.defaultTabHome.content.controls[2].controls[1].on_tap_link = open_url
        self.tabBar.tabs.append(self.defaultTab)
        self.tabBar.tabs.append(self.drawBoard)
        def tabBar_on_change(e : ControlEvent):
            self.tabBar.selected_index = e.data
        self.tabBar.on_change = tabBar_on_change

    # 窗口resize事件
    def page_resize(self, e):
        print("New page size:", self.page.window_width, self.page.window_height)
        # 重置透明度进度条长度、Home字体区     
        if self.page.width <= 900:
            change_size = 900 - self.page.width
            self.alphaSlider.width = 400 - change_size - 20
            self.defaultTab.longMdText.value = '## FletEditor is a light file-editor created\n ## by Python and Flet.'
        else:
            self.alphaSlider.width = 400
            self.defaultTab.longMdText.value = '## FletEditor is a light file-editor created by Python and Flet.'

        # 重置Text编辑器最大行
        height_change_ratio = self.page.height / 720
        for eachEditor in self.newTabWithField:
            eachEditor.content.max_lines = int(25 * height_change_ratio)
        self.page.update()

    # 生成一个tab
    def createTab(self, e):
        length = self.newTabWithField.__len__()
        if length < 3:
            newTab = ft.Tab(
                text="New Editor %d" % (1 + length),
                icon=ft.icons.EDIT,
                content=ft.TextField(
                    multiline=True,
                    text_size=self.commonFont['size'],
                    max_lines=25,
                    cursor_width=5,
                    border_color=ft.colors.LIGHT_BLUE_900,
                    cursor_color=ft.colors.RED_900,
                ),
            )
            self.tabBar.tabs.append(newTab)
            self.newTabWithField.append(newTab)
            if self.tabBar.selected_index == 0:
                self.tabBar.selected_index += 2
            else:
                self.tabBar.selected_index += 1
            self.tabBar.update()
            
        else:
            self.flyDlg(1)

    #  弹出框
    def flyDlg(self, from_where: int):
        # 参数表示弹出框来源
        # 创建超过3个文本框
        if from_where == 1:
            def close1(e):
                alert1.open = False
                self.page.update()

            alert1 = ft.AlertDialog(
                actions=[ft.TextButton("I Konw.", on_click=close1)],
                modal=True,
                title=ft.Text("Warning"),
                content=ft.Text("Counts of Text Editor cannot exceed three!"),
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda _: ...
            )
            self.page.dialog = alert1
            alert1.open = True
            self.audioPlayer.play()
            self.page.update()
        elif from_where == 2:
            ...
        else:
            ...
            
    def selfCore(self):
        ...
        

main = lambda page: App(page=page)

ft.app(target=main)
