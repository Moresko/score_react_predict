link https://github.com/datasets/football-datasets/blob/main/datasets/bundesliga/season-2526.csv

ako spustit bakckedn:
python3 -m venv venv
source venv/bin/activate
pip3 install fastapi pandas joblib scikit-learn "uvicorn[standard]"
(venv) martinmores@other-16-34 src % python3 -m uvicorn main:app --reload