from playwright.async_api import async_playwright
from playwright.async_api import Browser, Page

from data import DataManager, Track


# This class here will be in charge of one browser.... The orchestrator has several of this one
class Creator:

    def __init__(self, id: int, data_manager: DataManager) -> None:
        self.data_manager = data_manager
        self._id = id

    async def _delete_pre_existing(self, page: Page):
        old = await page.query_selector_all(".track-actions > button")
        for button in old:
            await button.click()

    async def _produce_new(self, page: Page):
        self._delete_pre_existing(page=page)
        track = Track("TODO... get here the track that is present in the form of features and check if it exists.... then generate another one from the server until it is actually a new one ")

    async def create():
        async with async_playwright() as p:
            browser: Browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("http://127.0.0.1:8080/")
