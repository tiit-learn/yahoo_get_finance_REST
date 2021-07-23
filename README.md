# Yahoo get finance REST

Для запускка контейнера - docker run --publish 5000:5000 <conteiner_name>
Для получения данных любой имеющейся компании в Yahoo Finance, необходимо использовать /api/1.0/get/<string:symbol_name>