@echo off
echo �ணࠬ�� ��⠭���� ����ᨬ��⥩. ����� ���� ��⠭������ ��墠��騥 ����ᨬ��� �� ��� ��������
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
echo ������, �ਫ������ ���஡�� ����������. �᫨ ��� �ன��� �ᯥ譮, � � ���쭥�襬 ����� �㤥� �����⢫����� �१ 'start.bat'
echo ��� ��室� ������ 'ctrl + c'
pause
py manage.py runserver
echo �᫨ �� ����� �� ᮮ�饭��, � �ਫ������ �� �����⨫��� - ����� � ��� ���� ��� ��⮭�, ���� ��� ��� � path. ������ � �㣫� ����� "��� �������� python � path" � �� ������ ��१���㧨�� ��������!
pause