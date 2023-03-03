from playwright.async_api import async_playwright
from playwright.async_api import Browser, Page

from data import DataManager


# This class here will be in charge of one browser.... The orchestrator has several of this one
class Creator:

    def __init__(self, id: int, data_manager: DataManager) -> None:
        self.data_manager = data_manager
        self._id = id

    async def _produce_new(self, page: Page):
        return

    async def create():
        async with async_playwright() as p:
            browser: Browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("http://127.0.0.1:8080/")
