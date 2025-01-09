# The primary goal of this work is to build up a Model of Skin Cancer Detection System utilizing Machine Learning Algorithms. After experimenting with many different architectures for the CNN model It is found that adding the BatchNormalization layer after each Dense, and MaxPooling2D layer can help increase the validation accuracy. In future, a mobile application can be made.
from flask import Flask, request, render_template,jsonify
from PIL import Image
import numpy as np
import skin_cancer_detection as SCD

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def runhome():

    return render_template("home.html")


# The primary goal of this work is to build up a Model of Skin Cancer Detection System utilizing Machine Learning Algorithms. After experimenting with many different architectures for the CNN model It is found that adding the BatchNormalization layer after each Dense, and MaxPooling2D layer can help increase the validation accuracy. In future, a mobile application can be made.


@app.route("/showresult", methods=["GET", "POST"])
def show():
    pic = request.files["pic"]
    inputimg = Image.open(pic)
    inputimg = inputimg.resize((28, 28))
    img = np.array(inputimg).reshape(-1, 28, 28, 3)
    result = SCD.model.predict(img)

    result = result.tolist()
    print(result)
    max_prob = max(result[0])
    class_ind = result[0].index(max_prob)
    print(class_ind)
    result = SCD.classes[class_ind]

    if class_ind == 0:
        info = "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion."

    elif class_ind == 1:
        info = "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells — a type of cell within the skin that produces new skin cells as old ones die off.Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck"
    elif class_ind == 2:
        info = "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL)1"
    elif class_ind == 3:
        info = "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years. They are firm and often feel like a stone under the skin. "
    elif class_ind == 4:
        info = "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with ‘melanocytic nevus’, but there are also sources that equate the term mole with any nevus form."
    elif class_ind == 5:
        info = "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum."
    elif class_ind == 6:
        info = "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."

    return render_template("results.html", result=result, info=info)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


# The primary goal of this work is to build up a Model of Skin Cancer Detection System utilizing Machine Learning Algorithms. After experimenting with many different architectures for the CNN model It is found that adding the BatchNormalization layer after each Dense, and MaxPooling2D layer can help increase the validation accuracy. In future, a mobile application can be made.

# The primary goal of this work is to build up a Model of Skin Cancer Detection System utilizing Machine Learning Algorithms. After experimenting with many different architectures for the CNN model It is found that adding the BatchNormalization layer after each Dense, and MaxPooling2D layer can help increase the validation accuracy. In future, a mobile application can be made.
# from flask import Flask, render_template, request, jsonify



# Function to calculate risk

def calculate_risk(uv_exposure, sunscreen_use, family_history, skin_type, moles_or_freckles):
    risk_score = 0

    if uv_exposure == "Always":
        risk_score += 3
    elif uv_exposure == "Often":
        risk_score += 2
    elif uv_exposure == "Sometimes":
        risk_score += 1

    if sunscreen_use == "Never":
        risk_score += 3
    elif sunscreen_use == "Sometimes":
        risk_score += 2
    elif sunscreen_use == "Often":
        risk_score += 1

    if family_history == "Yes":
        risk_score += 3

    if skin_type in ["Very Fair", "Fair"]:
        risk_score += 3
    elif skin_type == "Medium":
        risk_score += 2
    elif skin_type in ["Dark", "Very Dark"]:
        risk_score += 1

    if moles_or_freckles == "Many":
        risk_score += 3
    elif moles_or_freckles == "Moderate":
        risk_score += 2
    elif moles_or_freckles == "Few":
        risk_score += 1

    risk_percentage = (risk_score / 15) * 100

    if risk_score >= 12:
        risk_level = "High"
        suggestion = (
            "You are at high risk for skin cancer. "
            "Limit sun exposure, avoid tanning beds, use sunscreen daily, and consult a dermatologist regularly."
        )
    elif 6 <= risk_score < 12:
        risk_level = "Moderate"
        suggestion = (
            "You are at moderate risk for skin cancer. "
            "Use sunscreen regularly, monitor your skin for changes, and schedule a skin check-up annually."
        )
    else:
        risk_level = "Low"
        suggestion = (
            "You are at low risk for skin cancer. "
            "Maintain good sun protection habits and monitor your skin for any unusual changes."
        )

    return risk_percentage, risk_level, suggestion

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        uv_exposure = data.get('1', '')
        sunscreen_use = data.get('2', '')
        family_history = data.get('3', '')
        skin_type = data.get('4', '')
        moles_or_freckles = data.get('5', '')

        risk_percentage, risk_level, suggestion = calculate_risk(
            uv_exposure, sunscreen_use, family_history, skin_type, moles_or_freckles
        )

        return jsonify({
            'risk_percentage': risk_percentage,
            'risk_level': risk_level,
            'suggestion': suggestion
        })

    return render_template('index.html')
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port)

