from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
import re


app = Flask(__name__)

@app.route('/', methods=["GET"])
@cross_origin()
def homepage():
    return render_template('in.html')

@app.route('/data', methods=["POST", "GET"])
@cross_origin()
def result():
    if request.method == 'POST':
        final_data = []
        try:
            # Task-1: Get the raw code ready
            search = request.form['name']
            main_url = 'https://www.youtube.com/@' + search + '/videos'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(main_url, headers=headers)
            raw_code = response.text

            # Creating CSV
            filename = search + '.csv'
            file_csv = open(filename, 'w')
            headers = 'title, url, thumbnail, views, posted \n'
            file_csv.write(headers)

            # Task-2: Get video URLs
            try:
                pattern = r'/watch\?v=[\w]+'
                url_list = re.findall(pattern, raw_code)
                vid_url = []
                for index in range(5):
                    vid_url.append('https://www.youtube.com'+url_list[index])
            except Exception as e:

            # ... (rest of the code remains unchanged)

            # Task-7: Filter data
            for i in range(5):
                final_data.append(vid_title[i].strip('"'))
                file_csv.write(vid_title[i].strip('"'))
                file_csv.write(',')

                # ... (similar lines for other data)

                file_csv.write('\n')

            
            return render_template('results.html', data=final_data)

        except Exception as e:
            file_csv.close()
            return str(e)
    else:
        return render_template('in.html')

if __name__ == '__main__':
    app.run()
