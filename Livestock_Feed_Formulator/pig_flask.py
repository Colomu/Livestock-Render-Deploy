from flask import Flask, render_template, request, jsonify
from pig_formulation import get_formulation, nutrient_requirements, ingredient_db

app = Flask(__name__)

@app.route('/')
def home():
    # Pass data for pig classes and ingredient categories to the template
    pig_classes = nutrient_requirements.keys()
    ingredient_options = {
        "energy_sources": [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'source'],
        "energy_replacers": [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'replacer'],
        "high_protein_sources": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'high'],
        "medium_protein_sources": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'medium'],
        "protein_replacers": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'replacer'],
        "amino_acid_1": [name for name, details in ingredient_db.items() if details['type'] == 'Amino acid 1'],
        "amino_acid_2": [name for name, details in ingredient_db.items() if details['type'] == 'Amino acid 2']
    }

    return render_template('index2.html', pig_classes=pig_classes, ingredient_options=ingredient_options)

@app.route('/formulate', methods=['POST'])
def formulate():
    # Handle AJAX request and return JSON response 
    data = request.get_json()

    pig_class = data.get('pig_class')
    energy_sources = data.get('energy_sources', [])
    energy_replacers = data.get('energy_replacers', [])
    high_protein_sources = data.get('high_protein_sources', [])
    medium_protein_sources = data.get('medium_protein_sources', [])
    protein_replacers = data.get('protein_replacers', [])
    amino_acid_1 = data.get('amino_acid_1', [])
    amino_acid_2 = data.get('amino_acid_2', [])

    # Validate inputs
    if not pig_class or pig_class not in nutrient_requirements:
        return jsonify({'error': 'Invalid or missing pig class. Please select a valid class.'})

    if len(energy_sources) < 2 or len(medium_protein_sources) < 2 or len(protein_replacers) < 2 or len(energy_replacers) < 2:
        return jsonify({'error': 'Please select at least 2 items for energy sources, medium protein sources, energy replacers, and protein replacers.'})

    # Fetch nutrient requirements for the selected pig class
    requirements = nutrient_requirements[pig_class]
    me_min, me_max = requirements['ME_min'], requirements['ME_max']
    cp_min, cp_max = requirements['CP_min'], requirements['CP_max']

    # Generate formulations using the selected inputs
    formulations = get_formulation(
        pig_class,
        energy_sources,
        energy_replacers,
        high_protein_sources,
        medium_protein_sources,
        protein_replacers,
        amino_acid_1,  
        amino_acid_2
    )

    # Add a tolerance margin to include near-matching formulations
    tolerance = 0.01  # 1% tolerance for nutrient requirements
    recommended_formulations = [
        formulation for formulation in formulations
        if (me_min * (1 - tolerance)) <= formulation['total_me_content'] <= (me_max * (1 + tolerance)) and
           (cp_min * (1 - tolerance)) <= formulation['total_cp_content'] <= (cp_max * (1 + tolerance))
    ]

    # Return formulations in JSON format
    return jsonify({'formulations': formulations, 'recommended_formulations': recommended_formulations})


if __name__ == '__main__':
    app.run(debug=True, port=5006)
