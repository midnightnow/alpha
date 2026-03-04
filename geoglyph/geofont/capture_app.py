import asyncio
import os
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 800})
        
        # Absolute path to your map file
        file_path = "file://" + os.path.abspath("alphabet-resonance-map.html")
        print(f"Opening: {file_path}")
        
        await page.goto(file_path)
        # Wait for SVG to render
        await page.wait_for_selector("#main-svg")
        
        # Take screenshot of the visualizer card
        await page.locator("#viz-card").screenshot(path="screenshot.png")
        print("Success: screenshot.png generated.")
        
        await browser.close()

if __name__ == "__main__":
    print("Installing playwright if needed: pip install playwright && playwright install chromium")
    try:
        asyncio.run(capture())
    except Exception as e:
        print(f"Error: {e}")
