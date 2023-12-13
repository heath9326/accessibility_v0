from processing.models import AItem, Url
from processing.processors import ATypeProcessor, FormTypeProcessor
from processing.tasks import AutomaticAItemCrawler, AutomaticFormCrawler


class AutomaticCrawlerService:
    crawlers: set = (AutomaticFormCrawler,)
    url_to_process: str = None
    url_id: str = None

    def __init__(self, url_to_process: str, url_id: int):
        print("Initializing AutomaticCrawlerService...")
        self.url_to_process = url_to_process
        self.url_id = url_id

    def __call__(self):
        print("AutomaticCrawlerService is being called...")
        for crawler in self.crawlers:
            try:
                active_crawler = crawler(self.url_to_process, self.url_id)
                active_crawler.scrape_page()
            except Exception as exc:
                print(f"While scraping the page using {crawler.name} exeption occurred, exeption: {exc}")
                print(f"Fix the error and repeat the process")
                return


class AccessibilityProcessingService:
    processors: set = (FormTypeProcessor, )
    url_to_process: str = None
    url_id: int = None
    context: dict = {}

    def __init__(self, url_to_process: str,  url_id: int):
        print("Initializing AccessibilityProcessingService...")
        self.url_to_process = url_to_process
        self.url_id = url_id

    def __call__(self):
        print("AccessibilityProcessingService is called...")
        for processor in self.processors:
            try:
                active_processor = processor(self.url_id)
                elements = active_processor.process_elements()
                self.context[processor.name] = elements
            except Exception as exc:
                print(f"Exception occurred while processing and items, exception: '{exc}'")
        return self.context

    def clear_db(self):
        url = Url.objects.get(url=self.url_to_process)
        url.delete()

