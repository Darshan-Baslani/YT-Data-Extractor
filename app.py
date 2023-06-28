from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
import logging
import re

logging.basicConfig(filename='scrapper.log', level=logging.INFO)
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
            # task-1 get the raw code ready 
            search = request.form['name']
            main_url = 'https://www.youtube.com/@' + search + '/videos'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = requests.get(main_url,headers=headers)
            raw_code = response.text
            logging.info('Response Got Successfully!')

            ## creating csv
            filename = search + '.csv'
            file_csv = open(filename, 'w')
            headers = 'title, url, thumbnail, views, posted \n'
            file_csv.write(headers)

            # task-2 get video url's
            try:
                pattern = r'/watch\?v=[\w]+'
                url_list = re.findall(pattern, raw_code)
                vid_url = []
                for index in range(5):
                    vid_url.append('https://www.youtube.com'+url_list[index])
                logging.info('URL fetched successfully!')
            except Exception as e:
                logging.warning(e)

            # task-3 get thumbnail url's
            try:
                pattern = r'https://i.ytimg.com/vi/[\w-]+/hqdefault.jpg?'
                vid_thumbnail = re.findall(pattern, raw_code)
                logging.info('Thumbails fetched successfully!')
            except Exception as e:
                logging.warning(e)

            # task-4 get title
            try:
                pattern = r'"title":{"runs":\[{"text":".*?"'
                titles = re.findall(pattern, raw_code)
                vid_title = []
                for title in titles:
                    temp = title.split(':')[3]
                    vid_title.append(temp)
                logging.info('Title fetched successfully')
            except Exception as e:
                logging.warning(e)

            # task-5 get no of views
            try:
                pattern = r'"viewCountText":{"simpleText":".*?"'
                views = re.findall(pattern, raw_code)
                vid_view = []
                for view in views:
                    temp = view.split(':')[2]
                    vid_view.append(temp)
                logging.info('No of views fetched successfully')
            except Exception as e:
                logging.warning(e)

            # task-6 time of posting
            try:
                pattern = r'"publishedTimeText":{"simpleText":".*?"'
                posts = re.findall(pattern, raw_code)
                vid_post = []
                for post in posts:
                    temp = post.split(':')[2]
                    vid_post.append(temp)
                logging.info('Time of Post fetched successfully')
            except Exception as e:
                logging.warning(e)
            

             # task-7 filter data
            for i in range(5):
                final_data.append(vid_title[i].strip('"'))
                file_csv.write(vid_title[i].strip('"'))
                file_csv.write(',')

                final_data.append(vid_url[i].strip('"'))
                file_csv.write(vid_url[i].strip('"'))
                file_csv.write(',')

                final_data.append(vid_thumbnail[i].strip('"'))
                file_csv.write(vid_thumbnail[i].strip('"'))
                file_csv.write(',')

                final_data.append(vid_view[i].strip('"'))
                file_csv.write(vid_view[i].strip('"'))
                file_csv.write(',')

                final_data.append(vid_post[i].strip('"'))
                file_csv.write(vid_post[i].strip('"'))
                file_csv.write(',')
                file_csv.write('\n')

            logging.info(f'Final Data: {final_data}')
            
            return render_template('results.html', data=final_data)

        except Exception as e:
            logging.warning(e)
            file_csv.close()
            return str(e)
    else:
        return render_template('in.html')

if __name__ == '__main__':
    app.run()