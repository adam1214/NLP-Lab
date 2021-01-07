from flask import Flask, render_template
from flask import request
import json
import Word2Morphemes

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/here/js_get', methods=['GET'])
def js_get():
    r = {'Status': 'Search not found'}
    # request.values就是前端傳過來的幾個關鍵引數
    # 以request.values['query']為例，如果這個欄位是字串，直接獲取即可
    # 如果是字典或者陣列，切記要用json.loads(request.values['...'])將其格式轉換後再進行python程式碼中的邏輯處理
    # param = {query: request.values['query']}
    
    print(request.values['query'])
    dict2 = Word2Morphemes.Word2Morphemes(request.values['query'])
    result = json.dumps(dict2)
    
    '''
    if request.values['query'] == '123':
        r = {'Prefix': {'功能1:':123, '功能2:':456,'功能3:':789}, 'Affix': {'功能1:':111, '功能2:':"222", '功能3:':333}}
    result = json.dumps(r)
    '''
    return result


if __name__ == '__main__':
    app.run("0.0.0.0")  # Flask應用不限制訪問ip地址
