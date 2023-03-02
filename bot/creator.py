from playwright.async_api import async_playwright


# This class here will be in charge of one browser.... The orchestrator has several of this one
class Creator:

    def __init__(self, id: int) -> None:
        self._id = id

    async def create():
        async with async_playwright() as p:
            browser = await p.chrome.launch()
            page = await browser.new_page()
            await page.goto("http://127.0.0.1:8080/")
