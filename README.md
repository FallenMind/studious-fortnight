1. Склонировать/скачать данный репозиторий.
2. Для запуска сервера без тестов, запустите start_without_test.bat(docker-compose up в данной директории). Всё будет работать сразу, после автоматической подготовки.
3. Для запуска сервера с тестированием, запустите start_with_test.bat(docker-compose -f start_with_test up в данной директории). Примечание - перед запуском одного, необходимо выключить другой из-за использования одинаковых портов.
4. Все результаты тестов, запросы на сервер будут выведены в консоль.
5. Тестовый и не тестовые сервера используют разные базы данных.
5.1. Для того, чтоб не отчищать базу данных для docker-compose_test, измените переменную среды TEST_CHECK на любую, не являющуюся YES_I_WANT_TO_DELETE_MY_DATA (К примеру, 1)
