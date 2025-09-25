import scrapy
# Создаем класс на питоне и наследуем в него внешний класс паука.
class QuotesSpider(scrapy.Spider):
    # Имя паука для вызова командой "scrapy crawl -->quotes<--"
    name = "quotes"
    # Задаем сайты с которыми будет работать паук.
    # Scrapy автоматически отправит GET-запрос на каждый URL и передаст ответ в parse
    start_urls = ['https://quotes.toscrape.com']
    def parse(self, response):
        # logger встроенн в паука. Делаем вывод информации
        self.logger.info('Hi, Its my spider')
        
        # Ищем все эл. <div class="quote">
        quotes = response.css('div.quote')
        for quote in quotes:
            # yield - возвращает словарь. Паук автоматом собирает все Yield и сохроняет.
            yield {
                #.text - берет данные из класса текст, ::text - выдать текстовое содержимое. 
                #.get() - берет первый эл. или выдает NONE если не найде    
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css('.tag::text').getall(),
            }
        #Поиск ссылки на следущую страницу.
        # Эл. <a> внутри <li class="next">, извлекает значение атрибута href
        next_page = response.css('li.next a::attr("href")').get()
        cnt = 0
        # есть ли ссылка или знач<10
        if next_page is not None or cnt<10:
            cnt+=1
            # Создает новый запрос на url из next_page и метод обработки
            yield response.follow(next_page, self.parse)
            
#Yeld - аналогия с конвеером
#yield {'text': ..., 'author': ...} - конвеер работает с данными
#На конвеер надо загрузить еще данных но он не закончил с yield {'text': ..., 'author': ...}
#Мы оставляем записку  yield response.follow(next_page, self.parse).
#Конвеер продолжает работать с данными yield {'text': ..., 'author': ...},
#Но держит в памяти что ему надо будет продолжить работу с yield response.follow(next_page, self.parse).
# Как только он закончит с 1 данными он перейде к следующим.
#Таким образом пока конвер обрабатывал первый Yield запрос, алгоритм успел просчитать последующие

   