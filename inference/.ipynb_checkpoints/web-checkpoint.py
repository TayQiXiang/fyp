import base64
import io
import os
import time
from zipfile import ZipFile

import numpy as np
from flask import Flask, render_template, request, flash, make_response, send_from_directory

from inference.indexer import Indexer
from utils.misc import pil_loader

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'webp', 'tif', 'jfif'}

def allowed_format(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def combine(*args):
    x = zip(*args)
    
    # analyse the tuple from label (group by label)
    # return a dictionary with key as label and value as a list of tuples
    # each tuple contains distance, name, label
    result = {}
    for i in x:
        if i[2] not in result:
            result[i[2]] = []
        result[i[2]].append(i)

    #sort based on the length of the list
    for key in result:
        result[key] = sorted(result[key], key = lambda x: x[0])

    #calculate the confidence score for label
    # the confidence score should consider the number of tuples in the list, the sum and average distance between the tuples, combined with weightage
    # the confidence score should be between 0 and 1

    unsure = 0.0
    total_distance = 0.1
    total_tuples = 0.1
    for key in result:
        total_tuples += len(result[key])
        for i in result[key]:
            total_distance += i[0]

    for key in result:
        sum_distance = 0
        for i in result[key]:
            sum_distance += i[0]
        # confidence_score = len(result[key])/average_distance
        average_distance = sum_distance / total_distance
        confidence_score =  len(result[key]) * (1- sum_distance/total_distance)

        #when the average distance is too high, the unsure score will be higher


        result[key] = (result[key], confidence_score)
        print(key, confidence_score)


    # make all confidence score sum to 1
    total_confidence = 0
    for key in result:
        total_confidence += result[key][1]

    for key in result:
        result[key] = (result[key][0], result[key][1] / total_confidence)

    #sort based on the confidence score
    result = dict(sorted(result.items(), key = lambda x: x[1][1], reverse = True))

    #replace one hot with actual
    d_new= {
        0: "PCR-3222",
        1: "PCR-2611",
        2: "PCR-3132",
        3: "PCR-3268",
        4: "PCR-2894",
        5: "PCR-3009",
        6: "PCR-3167",
        7: "PCR-3008",
        8: "PCR-3168",
        9: "PCR-3040",
        10: 'unknown',
        11: "PCR-3066",
        12: "PCR-3028",
        13: "PCR-2919",
        14: "PCR-3265"
    }
    replaced_result= dict((d_new[key], value) for (key, value) in result.items())

    # get minimum distance 
    min_distance = 1000000
    for key in result:
        if result[key][0][0][0] < min_distance:
            min_distance = result[key][0][0][0]

    return replaced_result, min_distance

def process_query(f, indexer: Indexer):
    assert indexer, 'Indexer not initialize'
    start_time = time.time()
    img_ = pil_loader(f)

    dist, ind, query_code = indexer.query_with_image(img_)
    img_paths = indexer.get_img_path(ind)
    img_labels = indexer.get_img_labels(ind)

    end_time = time.time()
    flash("Upload successfully.")

    data = io.BytesIO()
    img_.save(data, "JPEG")

    encoded_img_data = base64.b64encode(data.getvalue())  # convert to base64 in byte
    encoded_img_data = encoded_img_data.decode('utf-8')  # convert to base64 in utf-8

    time_string = f'Time taken: {(end_time - start_time):.3f}s\n'
    code_string = "".join(str(np.unpackbits(query_code)).split())[1:-2]
    code_string = '\n'.join(code_string[i:i + 8] for i in range(0, len(code_string), 8))
    # return dist, img_paths, code_string, encoded_img_data, img_, time_string
    return dist, img_labels, img_paths, code_string, encoded_img_data, img_, time_string
    
def get_web_app(log_path, device='cpu', top_k=10):
    indexer = Indexer(log_path, device=device, top_k=top_k)
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = 'my_secret_key'

    @app.route('/', methods=['GET'])
    def index():
        return render_template('main.html',page_status=2,count = 46787, class_count=15)

    @app.route('/', methods=['POST'])
    def predict():
        f = request.files['image']
        if f.filename == '':
            flash("Please select a file")
            return index()
        elif not allowed_format(f.filename):
            flash("Invalid file type")
            return index()
    
        dist, img_labels, img_paths, code_string, encoded_img_data, img_, time_string = process_query(f, indexer)
        results,min_dist = combine(dist[0],img_paths[0],img_labels[0])

    
        return render_template('main.html',results=results,page_status=1,count = 46787, class_count=15, min_dist= min_dist,
                                   code=code_string,
                                   query_img=encoded_img_data,
                                   query_img_full=img_,
                                   time_string=time_string,
                                   extra_data=indexer.get_info())
    
    @app.route('/zip', methods=['POST'])
    def generate_zip():
        f = request.files['file']
        try:
            img_ = pil_loader(f)
        except:
            flash("Invalid file type")
            return index()
        dists, ind, query_code = indexer.query_with_image(img_)
        img_paths = indexer.get_img_path(ind)
        img_labels = indexer.get_img_labels(ind)[0]
        dists = dists[0]
    
        data = io.BytesIO()
        img = io.BytesIO()
        img_.save(img, "JPEG")
        with ZipFile(data, 'w') as zip:
            # f'retr_rank{i}_{dists[i]}_{path.split("/")[-1].split("_")[0]}.{path.split(".")[-1]}')
            for i, path in enumerate(img_paths[0]):
                zip.write(os.path.abspath(path), 
                          f'retr_rank{i}_{img_labels[i]}_{path.split("/")[-1].split("_")[0]}.{path.split(".")[-1]}')
            zip.writestr(f'query.jpg', img.getvalue())
        data.seek(0)
        response = make_response(data.read())
        response.headers.set('Content-Type', 'zip')
        response.headers.set('Content-Disposition', 'attachment', filename='%s.zip' % 'out')
        return response
    
    @app.route('/img/<path:filename>')
    def get_image(filename):
        path, file = os.path.split(filename)
        print(os.path.abspath(filename))
        return send_from_directory(os.path.abspath(path), file)
    
    return app