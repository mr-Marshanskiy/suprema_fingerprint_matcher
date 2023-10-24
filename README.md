# Suprema Fingerprint Enrollment and Matcher #

## Описание проекта ##
Демонстрационный проект на Django REST Framework, предназначенный для интеграции 
сканеров отпечатков пальцев `Suprema RealScan-G10` и `Suprema BioMini` в 
основной облачным WEB-сервис.

> Служит вспомогательным сервисом для работы с биометрическими персональными данными 
в пределах контролируемой зоны (КЗ).

### Задачи ###
Проект помогает выполнить задачи по сбору отпечатков данных с сотрудников с 
помощью устройства `Suprema RealScan-G10` и задачи по 
идентификации и верификации, используя устройство `Suprema BioMini`.

### Функциональные возможности ###
В проекте реализованы следующие  функциональные возможности:
* создание субъекта идентификационных данных (_далее - **СИД**_);
* парсинг данных, полученных со сканера и их добавление в базу данных (**Enrollment**);
* синхронизация Enrollment данных с основным облачным WEB-сервисом;
* удаление данных о СИД;
* верификация и идентификация СИД по шаблону отпечатка пальца (**Matcher**).

## Особенности проекта ##
### Реализация проекта ###

> Проект подходит для реализации только в демонстрационных целях.

Проект был реализован на территории страны **"Танзания"**, где не действуют требования 
ФСБ, ФСТЭК и других регулирующих органов в области информационной безопасности, 
поэтому данный проект не реализует взаимодействие с облачным сервисом через 
выделенный защищенный канал (VPN), и процесс хранения и обработки информации может 
не соответствовать необходимым требованиям ИБ. 

### Лицензионные ограничения ###

> Для использования библиотек необходим сканер `Suprema`, 
подключенный к серверу по USB, на котором развернут проект. По этой причине 
реализация проекта на облачном хостинге весьма проблематична.

Для матчинга (верификации и идентификации) используются поставляемые вместе с SDK библиотеки 
`UFMatcher.dll` (_Windows_) или `libNFiQ2.so` и `libUFMatcher.so` (_Linux_) в зависимости от 
операционной системы, на которой размещается данный проект.

Эти библиотеки требуют наличия лицензии и имеют следующий принцип проверки: 
при вызове методов из библиотеки 
происходит проверка подключенных USB устройств, среди которых должен быть найден 
сканер отпечатков пальцев Suprema, с него считывается уникальный UUID, который и 
является лицензионным ключом для библиотеки.

### Совместимость ###

> Для использования других устройств, возможно, придется изменить сериализатор 
для Enrollment.

Проект создавался под уже существующие решения и конкретные устройства,
которые предоставляют информацию в определенном формате через их собственные API:
* **Suprema RealScan-G10** для Enrollment; 
* **Suprema BioMini** для идентификации и верификации.

### Шаблонная схема взаимодействия

Схема взаимодействия содержит следующие элементы:
* Облачный web-сервис (`web.server.domain:443`);
* API Enrollment & Matcher (`192.168.0.10:443` / `biometry.local:443`);
* ПК пользователя с подключенными устройствами Suprema (`192.168.0.155`);
* API Suprema RealScan-G10 (`192.168.0.155:11121` / `127.0.0.1:11121`);
* API Suprema BioMini (`192.168.0.155:5678` / `127.0.0.1:5678`);

**API Suprema** становятся доступны после установки драйверов и запуска соответсвующей службы. 
Все запросы инициируются клиентом с ПК пользователя, поэтому API Suprema для клиента 
доступны через `localhost` (`127.0.0.1`).

### Описание технической реализации функционала
Выделяющимися в проекте являются следующие классы:
* `class FingerMatcher` (`fingerprints/tools/matcher/identification.py`)
* `class BoardSyncService` (`fingerprints/tools/board_sync.py`)

Описание механики находится в `fingerprints/tools/tools_description.md`
## Описание функциональных возможностей

### Enrollment

![Enrollment scheme](https://github.com/mr-Marshanskiy/suprema_fingerprint_matcher/tree/main/media/Enrollment.jpg)

Для процедуры записи (Enrollment) используется сканер `Suprema RealScan-G10`. 

1. Клиент отправляет запрос на web-сервис для получения информации о целевом сотруднике
2. Web-сервис возвращает ответ с данными
3. Клиент отправляет запрос на API RealScan-G10
```
GET http://127.0.0.1:11121/rswas/DeviceInfo - Проверка доступности устройства
POST http://127.0.0.1:11121/rswas/Capture - Начало процедуры сканирования
GET http://127.0.0.1:11121/rswas/CanvasInfo - Получение отпечатков
```

4. API RealScan-G10 возвращает ответ, в котором содержится информация о
всех отсканированных пальцах по отдельности и об отпечатках ладоней
```
200 OK
{
   {
     "captureMode": "string",
     "captureType": "string",
     "errCode": 0,
     "errMsg": "string",
     "fingers": [
       {
         "fingerNo": "string",
         "imgQuality": 0,
         "wsqData": "string",
         "imgType": "string",
         "imgData": "string",
         "isoFMRType": "string",
         "isoFMRData": "string",
         "isoFIRType": "string",
         "isoFIRData": "string"
       }
     ],
     "slaps": [
       {
         "slapType": "string",
         "wsqData": "string",
         "imgType": "string",
         "imgData": "string",
         "isoFIRType": "string",
         "isoFIRData": "string"
       }
     ]
   }
}
```

5. Клиент добавляет к полученным данным информацию из web-сервиса в ключ `person`
и отправляет запрос на **API Enrollment & Matcher**
```
Добавить к ответу:
  
"person": {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "board_id": 100,
    "status": "employee"
}
 
POST https:biometry.local/api/fingerprints/enrollment/
   body = [полученный JSON]
```

6. **API Enrollment & Matcher** выполняет следующие шаги:
* получает запрос от клиента;
* создает объект модели `persons.Person` из значений по ключу `person` в body;
* создает `fingerprints.Enrollment`;
* создает объекты `fingerprints.Slap` из массива по ключу `slaps` в body;
* создает объекты `fingerprints.Fingerprint` из массива по ключу ключа `fingers` в body;
* запускает процесс синхронизации с web-сервисом: генериррует и отправляет информацию 
о UUID созданных отпечатков. В заголовке передается Токен для авторизации.
```
POST https://web.server.domain/api/api/biometry/fingerprints/enrollment/employee/
body = {
  "person": "string",
  "fingers": [
    "eb23dcda-71dc-11ee-b962-0242ac120002",
    "6845f385-0cfd-492e-9d1e-e8010de862b4",
    ....
   ]
}
```

7. **Web-сервис** связывает полученные UUID с объектом целевого сотрудника
8. **API Enrollment & Matcher** отправляет ответ клиенту об успешном создании объектов
```
   201 CREATED
```
9. Клиент запрашивает у web-сервиса обновленную информацию о сотруднике
10. Web-сервис возвращает информацию с массивом пальцев, на которые есть отпечатки 
в базе данных API Enrollment & Matcher. Информация отрисовывается на клиенте.

### Identification

![Enrollment scheme](https://github.com/mr-Marshanskiy/suprema_fingerprint_matcher/tree/main/media/Identify.jpg)

Для процедуры идентификации используется сканер `Suprema BioMini`. 

1. Клиент отправляет запрос на `API BioMini`. 
В качестве параметра`dummy` передается псевдорандомное число
```
GET http://localhost:5678/api/initDevice?dummy=${dummy}
GET http://localhost:5678/api/setParameters?dummy=${dummy}&sHandle=${device_handle}&templateType=${type}
GET http://localhost:5678/api/getScannerStatus?dummy=${dummy}&sHandle=${device_handle}
GET http://localhost:5678/api/captureSingle?dummy=${dummy}&sHandle=${device_handle}&id=0
GET http://localhost:5678/api/getTemplateData?dummy=${dummy}&sHandle=${device_handle}&id=0&encrypt=0&qualityLevel=1&encryptKey&extractEx=0
```

2. `API BioMini` возвращает Template полученного отпечатка пальца
3. Клиент отправляет запрос на `API Enrollment & Matcher` и передает полученный Template
```
POST https://biometry.local/api/fingerprints/identify/
body={
  "template": "template_info_in_base_64",
  "status": "employee"
}
```

4. `API Enrollment & Matcher` определяет, какому отпечатку, хранящемуся в базе данных 
соответствуюет переданный Template. Если совпадений не найдено, то ответ будет:
```
400 NOT_FOUND
```
Если совпадение было найдено, то происходит поиск объекта `persons.Person` и 
возвращает информацию о нем в ответе:
```
200 OK
{
  "full_name": "Ivan Ivanov",
  "status": "employee",
  "board_id": 100
}
```

5. Если клиент получает статус 200 в ответ, то отправляет запрос на web-сервис на получение 
информации о сотруднике, в качестве `id` используется значения по ключу `board_id`
```
GET https://web.server.domain/api/employees/{id}/
```
6. Web-сервис возвращает информацию о сотруднике. Клиент отрисовывает профиль 
сотрудника.

### Verification

![Enrollment scheme](https://github.com/mr-Marshanskiy/suprema_fingerprint_matcher/tree/main/media/Verify.jpg)

Для процедуры верификации используется сканер `Suprema BioMini`. 

1. Клиент отправляет запрос на web-сервис на получение профиля сотрудника
2. Web-сервис возвращает информацию клиенту
3. Клиент отправляет запрос на `API BioMini`. 
В качестве параметра`dummy` передается псевдорандомное число
```
GET http://localhost:5678/api/initDevice?dummy=${dummy}
GET http://localhost:5678/api/setParameters?dummy=${dummy}&sHandle=${device_handle}&templateType=${type}
GET http://localhost:5678/api/getScannerStatus?dummy=${dummy}&sHandle=${device_handle}
GET http://localhost:5678/api/captureSingle?dummy=${dummy}&sHandle=${device_handle}&id=0
GET http://localhost:5678/api/getTemplateData?dummy=${dummy}&sHandle=${device_handle}&id=0&encrypt=0&qualityLevel=1&encryptKey&extractEx=0
```

4. `API BioMini` возвращает Template полученного отпечатка пальца
5. Клиент отправляет запрос на `API Enrollment & Matcher` и передает 
ID сотрудника и полученный Template
```
POST https://biometry.local/api/fingerprints/verify/
body={
  "template": "template_info_in_base_64",
  "status": "employee",
  "board_id": 100
}
```

6. `API Enrollment & Matcher` выбирает отпечатки, принадлежащие субъекту 
с соответствующим значением `board_id` и определяет, существует ли совпадение 
в выборке с переданным Template. Если совпадений не найдено, то ответ будет:
```
400 NOT_FOUND
{'detail': 'Not verified'}
```
Если совпадение было найдено, то ответ будет:
```
200 OK
{'detail': 'Verified'}
```

Клиент отражает полученную информацию, верифицирован ли выбранный сотрудник 
по отсканированному отпечатку


### Удаление записей
Запрос на удаление данных:
```
DELTE /api/fingerprints/destroy/{board_id}/
```
По значению `board_id` находится объект persons.Person и каскадно удаляются 
все объекты `Enrollment`, `Slap`, `Finger` из приложения `fingerprints`. После 
происходит синхронизация с web-сервисом, откуда также удаляется информация о 
наличии отпечатков для сотрдудника.

## Используемые технологии

- **Django**: Основной фреймворк для веб-разработки.
- **Django REST framework (DRF)**: Используется для разработки API.
- **libusb:** библиотека, которая предоставляет приложениям доступ для управления передачей данных на USB-устройства.
- **psycopg2:** библиотека для взаимодействия с PostgreSQL.
- **libUFMatcher.so:** библиотека для матчинга для Linux от Suprema.
- **libNFIQ2.so:** библиотека для матчинга для Linux от Suprema.
- **UFMatcher.dll:** библиотека для матчинга для Windows от Suprema.
- **Drf-spectacular** - библиотека генерации схем OpenAPI 3 с явным акцентом на расширяемость, настраиваемость и генерацию клиентов.
- **[Другие библиотеки и инструменты]**: [Список других технологий и инструментов, используемых в проекте].

## Установка и запуск

1. **Клонирование репозитория**:

   ```bash
   git clone [URL-репозитория]
   ```

2. **Создание виртуальной среды** (рекомендуется использовать [инструмент виртуальной среды]):

   ```bash
   virtualenv venv
   ```

3. **Активация виртуальной среды**:

   ```bash
   source venv/bin/activate
   ```

4. **Установка зависимостей**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Установка библиотек для Suprema Matcher**:
   ```bash
   добавить в fingerprints/tools/matcher/ следующие библиотеки

   (для Windows)
   UFMatcher.dll
   
   (для Linux)
   libUFMatcher.so
   libNFIQ2.so
   ```

6. Создание .env:
   - скопировать `example.env` в `.env`
   - заменить в файле '.env' значения

7. **Настройка базы данных**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Сгенерировать токен для клиента:
   ```bash
   python manage.py generate_api_token
   ```

6. **Запуск проекта**:

   ```bash
   python manage.py runserver
   ```

## Документация API

Документация по API доступна по `/api`.

## Вклад и разработка

Если вы хотите внести вклад в проект, пожалуйста, ознакомьтесь с [руководством по внесению вклада] и отправьте запрос на объединение (Pull Request).

## Лицензия

Подробности см. в файле LICENSE.

## Авторы

- Маршанский Николай
