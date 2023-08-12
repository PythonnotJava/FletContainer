from flet import (Page,
                  VerticalDivider,
                  colors,
                  PaintLinearGradient,
                  Container,
                  Text,
                  Column,
                  Row,
                  Tab,
                  app,
                  Tabs
                  )
from flet.canvas import Canvas, Fill

class CanvasTab(Tab):
    def __init__(self):

        self.paintContainer = Container()
        super().__init__(
            text='Canvas',
            content=self.paintContainer,
        )

def main(page : Page):
    cvs = CanvasTab()
    cvsTab = Tabs(tabs=[cvs])
    page.add(cvsTab)

if __name__ == '__main__':
    app(target=main)