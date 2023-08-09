import flet as ft
import math
from typing import Union, Optional
from json import load as json_load, dump as json_dump
from flet_core.file_picker import FilePickerFile

class App:
    
    global_settings : dict = json_load(open('src/ui.json', 'r', encoding='U8'))
    
    def __init__(self, page : ft.Page) -> None:
        # 界面
        self.page = page
        
    
        # 内置核心控件
     
        
        # 内置功能的核心函数
        # self.selfCore()
        
        # 上方工具栏
        self.statusNow : bool = self.global_settings['statusNow'] 
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
            ]
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
        def open_url(e) : self.page.launch_url(e.data)
        self.tabBar = ft.Tabs(
            label_color=ft.colors.DEEP_PURPLE_ACCENT_700,
            divider_color=ft.colors.RED,
            unselected_label_color=ft.colors.WHITE70,
            overlay_color=ft.colors.TEAL_100,
            indicator_color=ft.colors.ON_SURFACE,
            indicator_border_radius=10,
        )
        self.longMdText = ft.Markdown(value='## FletEditor is a light file-editor created by Python and Flet.')
        self.defaultTabHome = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.HOME),
                            ft.Markdown(value='# Welcome to use FletEditor!'),
                            ]
                        ),
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.STAR),
                            self.longMdText     
                            ]
                        ),
                    ft.Row(
                        controls=[
                            ft.Icon(name=ft.icons.ADS_CLICK_OUTLINED),
                            ft.Markdown(
                                value='## Watch More. [Click Me!](https://github.com/PythonnotJava/)',
                                extension_set="gitHubWeb",
                                on_tap_link=open_url,
                                expand=True,  
                            ),
                        ],
                    ),
                ],
            ),
            margin=ft.Margin(100, 100, 0, 0),
        )
        self.defaultTab = ft.Tab(
            text='Home',
            content=self.defaultTabHome,
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
        self.page.bgcolor = ft.colors.TEAL if self.statusNow else None    
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
        self.tabBar.tabs.append(self.defaultTab)
        self.tabBar.selected_index = 0
        self.tabBar.scrollable = True
   
    # 窗口resize事件
    def page_resize(self, e):
        print("New page size:", self.page.window_width, self.page.window_height)
        if self.page.width <= 900:
            change_size = 900 - self.page.width 
            self.alphaSlider.width = 400 - change_size 
            self.longMdText.value = '## FletEditor is a light file-editor created\n ## by Python and Flet.'
        else:
            self.alphaSlider.width = 400
            self.longMdText.value = '## FletEditor is a light file-editor created by Python and Flet.'
        self.longMdText.update()
        self.alphaSlider.update()
    
    # 生成一个tab
    def createTab(self, e):
        newTab = ft.Tab(
            'New Tab',
            icon=ft.icons.NEW_LABEL,
            content=ft.Text("New!!!!!!!")
        )
        self.tabBar.tabs.append(newTab)
        self.tabBar.update()
     
    
main = lambda page : App(page=page)

ft.app(target=main)
        
        
