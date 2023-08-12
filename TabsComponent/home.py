from flet import Page, Column, Icon, Markdown, Container, Row, MarkdownExtensionSet, Margin, Tab, app, Tabs, icons

class HomeTab(Tab):
    def __init__(self):

        self.longMdText = Markdown(value='## FletEditor is a light file-editor created by Python and Flet.')
        self.defaultTabHome = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Icon(name=icons.HOME),
                            Markdown(value='# Welcome to use FletEditor!'),
                        ]
                    ),
                    Row(
                        controls=[
                            Icon(name=icons.STAR),
                            self.longMdText
                        ]
                    ),
                    Row(
                        controls=[
                            Icon(name=icons.ADS_CLICK_OUTLINED),
                            Markdown(
                                value='## Watch More. [Click Me!](https://github.com/PythonnotJava/)',
                                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                                expand=True,
                            ),
                        ],
                    ),
                ],
            ),
            margin=Margin(100, 100, 0, 0),
        )

        super().__init__(
            text='Home',
            content=self.defaultTabHome
        )

def main(page : Page):
    home = HomeTab()
    home.defaultTabHome.content.controls[2].controls[1].on_tap_link = lambda _ : page.launch_url(_.data)
    homeTab = Tabs(tabs=[home])
    page.add(homeTab)

if __name__ == '__main__':
    app(target=main)