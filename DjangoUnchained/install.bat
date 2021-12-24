@echo off
echo Программа установки зависимостей. Сейчас будут установлены нехватающие зависимости на этото компьютер
pipenv install
pipenv shell
pip install numpy
pip install spacy
python -m spacy download ru_core_news_sm
py -m spacy download ru_core_news_sm
pip install nltk
pip install sklearn
pip install whitenoise
pip install mimetypes
pip install pandas
pip install pickle
pip install lxml
pip install json
pip install Django
pause
echo Теперь, Приложение попробует запуститься. Если всё пройдёт успешно, то в дальнейшем запуск будет осуществляться через 'start.bat'
echo Для выхода нажмите 'ctrl + c'
pause
py manage.py runserver
python manage.py runserver
echo Если вы видите это сообщение, а приложение не запустилось - значит у вас либо нет питона, либо его нет в path. Напишите в гугле запрос "Как добавить python в path" и не забудьте перезагрузить компьютер!
pause