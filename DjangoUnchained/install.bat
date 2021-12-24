@echo off
echo Программа установки зависимостей. Сейчас будут установлены нехватающие зависимости на этото компьютер
mkdir %1 
cd %1
pip install virtualenv
virtualenv env
call env\Scripts\activate
pip install django
pip install numpy
pip install spacy
py -m spacy download ru_core_news_sm
pip install nltk
pip install sklearn
pip install whitenoise
pip install pandas
pip install lxml
pip install django_extensions
pause
cls
echo Теперь, Приложение попробует запуститься. Если всё пройдёт успешно, то в дальнейшем запуск будет осуществляться через 'start.bat'
echo Для выхода нажмите 'ctrl + c'
pause
py manage.py runserver
echo Если вы видите это сообщение, а приложение не запустилось - значит у вас либо нет питона, либо его нет в path. Напишите в гугле запрос "Как добавить python в path" и не забудьте перезагрузить компьютер!
pause