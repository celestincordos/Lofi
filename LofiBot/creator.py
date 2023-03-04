from playwright.async_api import async_playwright
from playwright.async_api import Browser, Page, Locator, Playwright, Download
import asyncio
import os

from data import DataManager, Track


# This class here will be in charge of one browser.... The orchestrator has several of this one
class Creator:

    def __init__(self, id: int, data_manager: DataManager) -> None:
        self.track: Track
        self.data_manager = data_manager
        self._id = id
        self.p: Playwright
        self._finished: bool = False

    async def _delete_pre_existing(self, page: Page):
        old = await page.query_selector_all(".track-actions > button")
        for button in old:
            await button.click()

    async def _generate_and_save(self, page: Page):
        generate_button = await page.query_selector("#generate-button")
        await generate_button.click()

    async def _produce_new(self, page: Page):
        await self._delete_pre_existing(page=page)
        while True:
            rand = await page.query_selector("#refresh-button")
            await rand.click()
            inputs_vector = await page.evaluate('''() => {
            const inputs = Array.from(document.querySelectorAll('#sliders > input'));
            return inputs.map(input => input.value);
            }''')
            features = [float(x)for x in inputs_vector]
            track = Track(features=features)
            if not self.data_manager.track_exists(track):
                self.track = track
                return  # This breaks the while loop

    async def _handle_download(self, download: Download):
        # await download._finished_future

        # Get the suggested filename and save the download to the download path
        suggested_filename = download.suggested_filename
        server_hash = suggested_filename.split('.')[0]
        if server_hash != self.track.id:
            self._finished = True
            raise Exception(
                f"My hash ({self.track.id}) does not match the one that was received from the server ({server_hash}) !!")
        path = self.track.prepare_download()
        await download.save_as(path)
        await download.delete()
        self._finished = True
        # await self.p.stop()

    async def _has_finished(self, page: Page):
        while not self._finished:
            await page.wait_for_timeout(500)

    async def create(self):
        # will have to close this...
        # self.p: Playwright = await async_playwright().start()
        async with async_playwright() as p:
            self.p = p
            browser: Browser = await self.p.chromium.launch(headless=False)
            page = await browser.new_page()
            page.on('download', lambda download: asyncio.create_task(
                self._handle_download(download)))

            await page.goto("http://127.0.0.1:8080/")
            await self._produce_new(page=page)
            await self._generate_and_save(page=page)
            await self._has_finished(page)
