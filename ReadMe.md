先简单写着 之后用Markdown再编辑好

install dependencies(需要得包和环境）
terminal 中
创建环境 (ComplexEquipKGQA) python3.6的版本应该都可以:

conda create -n ComplexEquipKGQA python==3.6.13
conda activate ComplexEquipKGQA

pip install itchat
pip install sanic
pip install sklearn
pip install numpy
pip install -U sanic-cors
pip install sanic-openapi
pip install fuzzywuzzy
pip install xlrd ==1.2.0
pip install pandas
pip install jieba
pip install thefuzz
pip install pickle
pip install numpy

运行lacal.py:
python local.py