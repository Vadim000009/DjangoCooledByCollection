@echo off
echo �ணࠬ�� ��⠭���� ����ᨬ��⥩. ����� ���� ��⠭������ ��墠��騥 ����ᨬ��� �� ��� ��������
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
echo ������, �ਫ������ ���஡�� ����������. �᫨ ��� �ன��� �ᯥ譮, � � ���쭥�襬 ����� �㤥� �����⢫����� �१ 'start.bat'
echo ��� ��室� ������ 'ctrl + c'
pause
py manage.py runserver
python manage.py runserver
echo �᫨ �� ����� �� ᮮ�饭��, � �ਫ������ �� �����⨫��� - ����� � ��� ���� ��� ��⮭�, ���� ��� ��� � path. ������ � �㣫� ����� "��� �������� python � path" � �� ������ ��१���㧨�� ��������!
pause