from flask import Flask, render_template, request
import base64, json, requests, os

def encode_file(file):
  file_content = file.read()
  return base64.b64encode(file_content)

def get_text_to_img(path):
    contest = ""
    with open(path, "rb") as image_file:
        text = str(encode_file(image_file))[2:][:-1]
        res = {"folderId": os.environ["folder_id"], "analyze_specs": [{"content": text, "features": [{"type": "TEXT_DETECTION", "text_detection_config": {"language_codes": ["*"]}}]}]}
        iam = requests.post("https://iam.api.cloud.yandex.net/iam/v1/tokens", json.dumps({"yandexPassportOauthToken": os.environ["OAuth"]})).json()["iamToken"]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {iam}"}
        result = requests.post("https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze", data = json.dumps(res), headers = headers).json()
        result = result['results'][0]['results'][0]['textDetection']['pages'][0]['blocks']
        for i in range(len(result)):
            res = result[i]['lines']
            for j in range(len(res)):
                r = res[j]["words"] 
                for k in range(len(r)):
                    #coordinate = r[k]['boundingBox']['vertices']
                    text = r[k]["text"]
                    contest += text + " "
    os.remove(path)
    return contest	

app = Flask(__name__)
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/file", methods = ["post"])
def file():
    if request.method == 'POST':
        file1 = request.files['photo']
        path = os.path.join('uploads', file1.filename)
        file1.save(path)
    return render_template("index.html", contest = get_text_to_img(path))


if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 5000)