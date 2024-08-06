from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for session

# Load data
DF = pd.read_excel("static/BPC Packszie Measurements - 2022 - FOR ROI.xlsx")

# Predefined DIMENSIONS
DIMENSIONS = {
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

IMAGES = {
    'Jif': ['image_2_2.png', 'image_3_2.png', 'image_4_2.png'],
    'Omo': ['image_18_2.png', 'image_6_2.png', 'image_19_2.png'],
    'Knorr': ['image_5_2.png', 'image_7_2.png', 'image_8_2.png'],
    'Comfort': ['image_6_2.png', 'image_25_2.png'],
    'Axe': ['image_35_1.png']
}

def calculate_blocks(length, width, blocks):
    area_rect = length * width
    results = []

    blocks = sorted(blocks, key=lambda block: block['length'] * block['width'])
    total_remaining_area = area_rect

    for block in blocks:
        block_length = block['length']
        block_width = block['width']
        block_percentage = block['percentage']
        
        area_block = (block_percentage / 100) * area_rect
        block_area = block_length * block_width
        
        num_blocks = area_block // block_area
        used_area = num_blocks * block_area
        remaining_area = area_block - used_area
        
        total_remaining_area -= used_area
        
        results.append({
            'block': block,
            'area_required': area_block,
            'num_blocks': num_blocks,
            'used_area': used_area,
            'remaining_area': remaining_area
        })

    smallest_block = blocks[0]
    smallest_block_area = smallest_block['length'] * smallest_block['width']
    num_smallest_extra = total_remaining_area // smallest_block_area

    results[0]['num_blocks'] += num_smallest_extra
    results[0]['used_area'] += num_smallest_extra * smallest_block_area

    return results

@app.route('/stands', methods=['GET', 'POST'])
def stands():
    if request.method == 'POST':
        session['selected_cards'] = request.form.getlist('selected_cards')[0].split(',')
        return redirect(url_for('stands'))
    return render_template('index.html', images=IMAGES)

@app.route('/get_images', methods=['POST'])
def get_images():
    selected_value = request.json.get('selection')
    return jsonify(IMAGES.get(selected_value, []))

@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        session['selected_images'] = request.form.getlist('selected_images')[0].split(',')
        return redirect(url_for('display'))
    return render_template('display.html', images=session.get('selected_images', []), cards=session.get('selected_cards', []))

@app.route('/', methods=['GET', 'POST'])
def items():
    items_dict = pickle.load(open("items.pickle", 'rb'))
    new_list = [i.replace("'", '') for i in items_dict.keys()]
    return render_template('items.html', items=new_list)

@app.route('/get_cards', methods=['POST'])
def get_cards():
    selected_value = request.json.get('selection')
    if selected_value == "CARTE DOR COMPLETE DESSERTS":
        selected_value = "CARTE D\'OR COMPLETE DESSERTS"

    filtered_DF = DF[DF['CPG'] == selected_value]
    final = [
        {"name": row["Material Number"], "tooltip": f"{row['Length']}, {row['Width']}, {row['Height']}"}
        for _, row in filtered_DF.iterrows()
    ]
    return jsonify(final)

@app.route('/calculate', methods=['POST'])
def calculate():
    submitted_data = request.form.to_dict()
    quantities = {key.replace('quantity_', ''): value for key, value in submitted_data.items() if key.startswith('quantity_')}
    
    all_results = []
    for image in session.get('selected_images', []):
        length = DIMENSIONS[image][1] * 100
        width = DIMENSIONS[image][2] * 100
        blocks = [
            {'length': int(filtered_DF.iloc[0]['Length']), 'width': int(filtered_DF.iloc[0]['Width']), 'percentage': int(quantity)}
            for card, quantity in quantities.items()
            for filtered_DF in [DF[DF['Material Number'] == card]]
        ]
        results = calculate_blocks(length, width, blocks)
        all_results.append(results)
    
    return jsonify(all_results)
    return render_template('calculate.html', all=all)

if __name__ == '__main__':
    app.run(debug=True)
