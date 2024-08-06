from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import pandas as pd
app = Flask(__name__)

df = pd.read_excel("static\BPC Packszie Measurements - 2022 - FOR ROI.xlsx")

dimensions = {
    'image_2_2.png': [4, 1.2, 0.8],
    'image_3_2.png': [3, 2.4, 1.6],
    'image_4_2.png': [3, 1.2, 0.8],
    'image_18_2.png': [3, 2.4, 1.6],
    'image_6_2.png': [3, 1.2, 0.8],
    'image_19_2.png': [3, 1.2, 0.8],
    'image_5_2.png': [4, 1.2, 0.8],
    'image_7_2.png': [4, 1.2, 0.8],
    'image_8_2.png': [4, 2.4, 1.6],
    'image_25_2.png': [4, 2.4, 1.6],
    'image_35_1.png': [4, 1, 1]
}

selected_cards = ''
@app.route('/stands', methods=['GET', 'POST'])
def stands():
    global selected_cards
    selected_cards = request.form.getlist('selected_cards')
    selected_cards = selected_cards[0].split(',')
    images = {
        'Jif': ['image_2_2.png', 'image_3_2.png', 'image_4_2.png'],
        'Omo': ['image_18_2.png', 'image_6_2.png', 'image_19_2.png'],
        'Knorr': ['image_5_2.png', 'image_7_2.png', 'image_8_2.png'],
        'Comfort': ['image_6_2.png', 'image_25_2.png'],
        'Axe': ['image_35_1.png']
    }
    return render_template('index.html', images=images)

@app.route('/get_images', methods=['POST'])
def get_images():
    selected_value = request.json.get('selection')
    images = {
        'Jif': ['image_2_2.png', 'image_3_2.png', 'image_4_2.png'],
        'Omo': ['image_18_2.png', 'image_6_2.png', 'image_19_2.png'],
        'Knorr': ['image_5_2.png', 'image_7_2.png', 'image_8_2.png'],
        'Comfort': ['image_6_2.png', 'image_25_2.png'],
        'Axe': ['image_35_1.png']
    }
    return jsonify(images.get(selected_value, []))

@app.route('/display', methods=['POST'])
def display():
    selected_images = ''
    selected_images = request.form.getlist('selected_images')
    selected_images = selected_images[0].split(',')
    return render_template('display.html', images=selected_images, cards=selected_cards)

@app.route('/', methods=['GET', 'POST'])
def items():
    items_dict = pickle.load(open("items.pickle", 'rb'))
    new_list = []
    for i in items_dict.keys():
        new_list.append(i.replace("\'", ''))
    return render_template('items.html', items=new_list)


@app.route('/get_cards', methods=['POST'])
def get_cards():
    global df
    selected_value = request.json.get('selection')
    items_dict = pickle.load(open("items.pickle", 'rb'))
    if selected_value == "CARTE DOR COMPLETE DESSERTS":
        selected_value = "CARTE D\'OR COMPLETE DESSERTS"
    # Value to filter by
    value_to_filter = selected_value

    # Filter rows where the Material column matches the value_to_filter
    filtered_df = df[df['CPG'] == value_to_filter]
    final = []
    for i in range(len(filtered_df)):
        final.append({"name" : filtered_df.iloc[i]["Material Number"], "tooltip" : str(filtered_df.iloc[i]["Length"]) + ', ' + str(filtered_df.iloc[i]["Width"]) + ', ' + str(filtered_df.iloc[i]["Height"])})
    # print('==============', items_dict[selected_value])
    return jsonify(final)

@app.route('/calculate', methods=['POST'])
def calculate():
    selected_cards = ''
    selected_cards = request.form.getlist('selected_cards')
    selected_cards = selected_cards[0].split(',')
    
    return render_template('calculate.html', cards=selected_cards)
if __name__ == '__main__':
    app.run(debug=True)
