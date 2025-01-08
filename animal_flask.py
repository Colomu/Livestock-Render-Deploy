from flask import Flask, render_template, request, jsonify
from importlib import import_module

app = Flask(__name__)

# Dictionary mapping animal types to their respective modules
animal_modules = {
    'catfish': 'catfish_formulation',
    'pig': 'pig_formulation',
    'poultry': 'poultry_formulation'
}

@app.route('/')
def home():
    # Animal types available
    animal_types = list(animal_modules.keys())

    # Default to catfish data
    default_animal = 'catfish'
    module = import_module(animal_modules[default_animal])
    nutrient_requirements = module.nutrient_requirements
    ingredient_db = module.ingredient_db

    # Prepare ingredient options for the default animal
    ingredient_options = {
        "energy_sources": [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'source'],
        "energy_replacers": [name for name, details in ingredient_db.items() if details['type'] == 'energy' and details['subtype'] == 'replacer'],
        "high_protein_sources": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'high'],
        "medium_protein_sources": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'medium'],
        "protein_replacers": [name for name, details in ingredient_db.items() if details['type'] == 'protein' and details['subtype'] == 'replacer'],
        "amino_acid_1": [name for name, details in ingredient_db.items() if details['type'] == 'Amino acid 1'],
        "amino_acid_2": [name for name, details in ingredient_db.items() if details['type'] == 'Amino acid 2']
    }

    return render_template('index.html', animal_types=animal_types, catfish_classes=nutrient_requirements.keys(), ingredient_options=ingredient_options)

@app.route('/get_classes', methods=['POST'])
def get_classes():
    # Handle AJAX request to fetch classes for the selected animal type
    data = request.get_json()
    selected_animal = data.get('animal_type')

    if selected_animal not in animal_modules:
        return jsonify({'error': 'Invalid animal type selected.'})

    # Dynamically import the appropriate module
    module = import_module(animal_modules[selected_animal])
    nutrient_requirements = module.nutrient_requirements

    # Return the classes as a list
    return jsonify({'classes': list(nutrient_requirements.keys())})

@app.route('/formulate', methods=['POST'])
def formulate():
    # Handle AJAX request and return JSON response
    data = request.get_json()

    # Get selected animal type
    selected_animal = data.get('animal_type')
    if selected_animal not in animal_modules:
        return jsonify({'error': 'Invalid animal type selected.'})

    # Dynamically import the appropriate module
    module = import_module(animal_modules[selected_animal])
    nutrient_requirements = module.nutrient_requirements
    ingredient_db = module.ingredient_db
    get_formulation = module.get_formulation

    # Extract inputs from the request
    catfish_class = data.get('catfish_class')
    energy_sources = data.get('energy_sources', [])
    energy_replacers = data.get('energy_replacers', [])
    high_protein_sources = data.get('high_protein_sources', [])
    medium_protein_sources = data.get('medium_protein_sources', [])
    protein_replacers = data.get('protein_replacers', [])
    amino_acid_1 = data.get('amino_acid_1', [])
    amino_acid_2 = data.get('amino_acid_2', [])

    # Validate inputs
    if not catfish_class or catfish_class not in nutrient_requirements:
        return jsonify({'error': 'Invalid or missing class. Please select a valid class.'})

    if len(energy_sources) < 2 or len(medium_protein_sources) < 2 or len(protein_replacers) < 2 or len(energy_replacers) < 2:
        return jsonify({'error': 'Please select at least 2 items for energy sources, medium protein sources, energy replacers, and protein replacers.'})

    # Fetch nutrient requirements for the selected class
    requirements = nutrient_requirements[catfish_class]
    me_min, me_max = requirements['ME_min'], requirements['ME_max']
    cp_min, cp_max = requirements['CP_min'], requirements['CP_max']

    # Generate formulations using the selected inputs
    formulations = get_formulation(
        catfish_class,
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
    app.run(debug=True, port=5008)
