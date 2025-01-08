from scipy.optimize import linprog

# Define nutrient requirements for different poultry classes
nutrient_requirements = {
    'Broiler_chicken_0_6_weeks': {
        'ME_min': 2900, 'ME_max': 3000, 'CP_min': 22.0, 'CP_max': 24.0, 'Lys_min': 1.2, 'Lys_max': 1.2, 'Meth_min': 0.55, 'Meth_max': 0.55,
        'Ca_min': 1.25, 'Ca_min': 1.25, 'P': 0.85, 'Salt': 0.35, 'Premix': 0.25
    },
    'Broiler_chicken_6_9_weeks': {
        'ME_min': 2850, 'ME_max': 3000, 'CP_min': 19.0, 'CP_max': 21.0, 'Lys_min': 0.95, 'Lys_max': 0.95, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 1.00, 'Ca_max': 1.00, 'P': 0.70, 'Salt': 0.35, 'Premix': 0.25
    },
    'Broiler_chicken_9_12_weeks': {
        'ME_min': 2850, 'ME_max': 3000, 'CP_min': 17.0, 'CP_max': 18.0, 'Lys_min': 0.85, 'Lys_max': 0.85, 'Meth_min': 0.40, 'Meth_max': 0.40,
        'Ca_min': 0.95, 'Ca_max': 0.95, 'P': 0.85, 'Salt': 0.35, 'Premix': 0.25
    },

    'Pullets_chicken_0_8_weeks': { 'ME_min': 2500, 'ME_max': 2700, 'CP_min':18.0, 'CP_max': 20.0, 'Lys_min': 1.2, 'Lys_max': 1.2, 'Meth_min': 0.55, 'Meth_max': 0.55,
        'Ca_min': 1.25, 'Ca_max': 1.25, 'P': 0.85, 'Salt': 0.35, 'Premix': 0.25
    },
    'Pullets_chicken_8_20_weeks': {
        'ME_min': 2500, 'ME_max': 2700, 'CP_min': 15.0, 'CP_max':17.0, 'Lys_min': 0.95, 'Lys_max': 0.95, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 1.00, 'Ca_MAX': 1.00, 'P': 0.70, 'Salt': 0.35, 'Premix': 0.25
    },
    'Layers/Breeders_chicken': {'ME_min': 2500, 'ME_max': 2700, 'CP_min': 15.0, 'CP_max': 17.0, 'Lys_min': 0.85, 'Lys_max': 0.85, 'Meth_min': 0.40, 'Meth_max': 0.40,
        'Ca_min': 3.50, 'Ca_max': 3.50, 'P': 0.85, 'Salt': 0.35, 'Premix': 0.25
    },
    
    'Turkey_0_8_weeks': {
        'ME_min': 2800, 'ME_max': 3000, 'CP_min': 28.0, 'CP_max': 30.0, 'Lys_min': 1.60, 'Lys_max': 1.60, 'Meth_min': 0.65, 'Meth_max': 0.65,
        'Ca_min': 1.50, 'Ca_max': 1.50, 'P_min': 1.00, 'P_max': 1.00,
        'Salt': 0.35, 'Premix': 0.25
    },
    'Turkey_8_16_weeks': {
        'ME_min': 2600, 'ME_max': 2800, 'CP_min': 21.0, 'CP_max': 23.0, 'Lys_min': 1.20, 'Lys_max': 1.20, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 1.20, 'Ca_max': 1.20, 'P_min': 0.80, 'P_max': 0.80,
        'Salt': 0.35, 'Premix': 0.25
    },
    'Turkey_16_30_weeks': {
        'ME_min': 2600, 'ME_max': 2800, 'CP_min': 15.0, 'CP_max': 17.0, 'Lys_min': 0.90, 'Lys_max': 0.90, 'Meth_min': 0.35, 'Meth_max': 0.35,
        'Ca_min': 0.90, 'Ca_max': 0.90, 'P_min': 0.60, 'P_max': 0.60,
        'Salt': 0.35, 'Premix': 0.25
    },
    'Mature_Turkeys_and_Breeders': {
        'ME_min': 2450, 'ME_max': 2650, 'CP_min': 12.5, 'CP_max': 14.0,
        'Lys_min': 0.75, 'Lys_max': 0.75, 'Meth_min': 0.25, 'Meth_max': 0.25,'Ca_min': 2.75, 'Ca_max': 2.75, 'P_min': 0.90, 'P_max': 0.90,
        'Salt': 0.35, 'Premix': 0.25
    },
    'GuineaFowl_0_4_weeks': {
        'ME_min': 2900, 'ME_max': 3000, 'CP_min': 22.0, 'CP_max': 24.0, 'Lys_min': 1.20, 'Lys_max': 1.20, 'Meth_min': 0.53, 'Meth_max': 0.53,
        'Ca_min': 1.02, 'Ca_max': 1.02, 'P_min': 0.60, 'P_max': 0.60,
        'Salt': 0.15, 'Premix': 0.25
    },
    'GuineaFowl_4_8_weeks': {
        'ME_min': 2850, 'ME_max': 3000, 'CP_min': 18.0, 'CP_max': 20.0, 'Lys_min': 1.00, 'Lys_max': 1.00, 'Meth_min': 0.40, 'Meth_max': 0.40,
        'Ca_min': 0.94, 'Ca_max': 0.94, 'P_min': 0.60, 'P_max': 0.60,
        'Salt': 0.15, 'Premix': 0.25
    },
    'GuineaFowl_8_12_weeks': {
        'ME_min': 2850, 'ME_max': 3000, 'CP_min': 16.0, 'CP_max': 17.0,'Lys_min': 0.82, 'Lys_max': 0.82, 'Meth_min': 0.30, 'Meth_max': 0.30,
        'Ca_min': 0.82, 'Ca_max': 0.82, 'P_min': 0.55, 'P_max': 0.55,
        'Salt': 0.15, 'Premix': 0.25
    },
    'GuineaFowl_6_28_weeks': {
        'ME_min': 2600, 'ME_max': 2700, 'CP_min': 14.0, 'CP_max': 15.0, 'Lys_min': 0.65, 'Lys_max': 0.65, 'Meth_min': 0.31, 'Meth_max': 0.31,
        'Ca_min': 0.60, 'Ca_max': 0.60, 'P_min': 0.55, 'P_max': 0.55,
        'Salt': 0.15, 'Premix': 0.25
    },

    'GuineaFowl_Layers': {
        'ME_min': 2500, 'ME_max': 2700, 'CP_min': 14.0, 'CP_max': 16.0, 'Lys_min': 0.90, 'Lys_max': 0.90, 'Meth_min': 0.38, 'Meth_max': 0.38,
        'Ca_min': 2.75, 'Ca_max': 2.75, 'P_min': 0.55, 'P_max': 0.55,
        'Salt': 0.15, 'Premix': 0.25
    },

    'Duck_0_3_weeks': {
        'ME_min': 2600, 'ME_max': 2800, 'CP_min': 21.0, 'CP_max': 23.0, 'Lys_min': 1.20, 'Lys_max': 1.20, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 0.80, 'Ca_max': 0.80, 'P_min': 0.65, 'P_max': 0.65,
        'Salt': 0.25, 'Premix': 0.25
    },
    'Duck_3_8_weeks': {
        'ME_min': 2600, 'ME_max': 2800, 'CP_min': 15.0, 'CP_max': 17.0, 'Lys_min': 0.90, 'Lys_max': 0.90, 'Meth_min': 0.35, 'Meth_max': 0.35,
        'Ca_min': 0.65, 'Ca_max': 0.65, 'P_min': 0.55, 'P_max': 0.55,
        'Salt': 0.25, 'Premix': 0.25
    },
    'Duck_Layers': {
        'ME_min': 2500, 'ME_max': 2700, 'CP_min': 15.0, 'CP_max':17.0, 'Lys_min': 0.75, 'Lys_max': 0.75, 'Meth_min': 0.35, 'Meth_max': 0.35,
        'Ca_min': 3.00, 'Ca_max': 3.00, 'P_min': 0.65, 'P_max': 0.65,
        'Salt': 0.25, 'Premix': 0.25
    },

    'Quail_Broilers_0_2_weeks': {
        'ME_min': 2600, 'ME_max': 2800, 'CP_min': 26.0, 'CP_max': 27.0,'Lys_min': 1.20, 'Lys_max': 1.20, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 0.80, 'Ca_max': 0.80, 'P_min': 0.60, 'P_max': 0.60,
        'Salt': 0.15, 'Premix': 0.25
    },

    'Quail_Broilers_3_5_weeks': {
        'ME_min': 2800, 'ME_max': 2900, 'CP_min': 22.0, 'CP_max': 24.0,'Lys_min': 1.10, 'Lys_max': 1.10, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 0.60, 'Ca_max': 0.60, 'P_min': 0.60, 'P_max': 0.60,
        'Salt': 0.15, 'Premix': 0.25
    },

    'Quail_Layers_0_2_weeks': {
        'ME_min': 2850, 'ME_max': 2950, 'CP_min': 22.0, 'CP_max': 24.0,'Lys_min': 1.20, 'Lys_max': 1.20, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 0.80, 'Ca_max': 0.80, 'P_min': 0.30, 'P_max': 0.30,
        'Salt': 0.15, 'Premix': 0.25
    },

    'Quail_Layers_3_5_weeks': {
        'ME_min': 2600, 'ME_max': 2700, 'CP_min': 18.0, 'CP_max': 20.0, 'Lys_min': 1.10, 'Lys_max': 1.10, 'Meth_min': 0.45, 'Meth_max': 0.45,
        'Ca_min': 0.60, 'Ca_max': 0.60, 'P_min': 0.30, 'P_max': 0.30,
        'Salt': 0.15, 'Premix': 0.25
    },

    'Quail_Layers_5_6_weeks': {
        'ME_min': 2550, 'ME_max': 2650, 'CP_min': 17.0, 'CP_max': 19.0,'Lys_min': 0.80, 'Lys_max': 0.80, 'Meth_min': 0.33, 'Meth_max': 0.33,
        'Ca_min': 3.00, 'Ca_max': 3.00, 'P_min': 0.45, 'P_max': 0.45,
        'Salt': 0.15, 'Premix': 0.25
    }
}

ingredient_db = {
    # Energy_Sources
    'Maize': {'type': 'energy', 'subtype': 'source', 'cost': 1.31, 'DM': 91.8, 'CP': 8.8, 'ME': 3510, 'CF': 2.1, 'EE': 4.1, 'Ash': 1.0, 'Ca': 0.01, 'P': 0.21, 'Lys': 0.31, 'Meth': 0.16, 'Cyst': 0.15},
    'Sorghum': {'type': 'energy', 'subtype': 'source', 'cost': 1.25, 'DM': 92.5, 'CP': 9.5, 'ME': 3270, 'CF': 2.7, 'EE': 2.5, 'Ash': 1.2, 'Ca': 0.03, 'P': 0.25, 'Lys': 0.28, 'Meth': 0.16, 'Cyst': 0.10},
    'Wheat': {'type': 'energy', 'subtype': 'source', 'cost': 1.50, 'DM': 89.0, 'CP': 13.0, 'ME': 3060, 'CF': 2.7, 'EE': 1.5, 'Ash': 1.2, 'Ca': 0.04, 'P': 0.35, 'Lys': 0.30, 'Meth': 0.20, 'Cyst': 0.22},
    'Rice': {'type': 'energy', 'subtype': 'source', 'cost': 1.19, 'DM': 89.1, 'CP': 8.6, 'ME': 2990, 'CF': 0.4, 'EE': 0.4, 'Ash': 0.6, 'Ca': 0.05, 'P': 0.22, 'Lys': 0.25, 'Meth': 0.22, 'Cyst': 0.08},
    'Millet': {'type': 'energy', 'subtype': 'source', 'cost': 1.38, 'DM': 89.5, 'CP': 12.0, 'ME': 2555, 'CF': 4.3, 'EE': 4.0, 'Ash': 3.0, 'Ca': 0.04, 'P': 0.30, 'Lys': 0.36, 'Meth': 0.22, 'Cyst': 0.20},
    'Barley': {'type': 'energy', 'subtype': 'source', 'cost': 1.44, 'DM': 89.0, 'CP': 11.2, 'ME': 2790, 'CF': 5.1, 'EE': 1.9, 'Ash': 2.5, 'Ca': 0.06, 'P': 0.38, 'Lys': 0.45, 'Meth': 0.27, 'Cyst': 0.18},
    'Oats': {'type': 'energy', 'subtype': 'source', 'cost': 1.56, 'DM': 89.0, 'CP': 11.2, 'ME': 2600, 'CF': 10.6, 'EE': 4.5, 'Ash': 2.9, 'Ca': 0.08, 'P': 0.33, 'Lys': 0.45, 'Meth': 0.18, 'Cyst': 0.18},
    'Rye': {'type': 'energy', 'subtype': 'source', 'cost': 1.44, 'DM': 89.0, 'CP': 11.7, 'ME': 2734, 'CF': 2.2, 'EE': 1.8, 'Ash': 1.7, 'Ca': 0.06, 'P': 0.32, 'Lys': 0.46, 'Meth': 0.20, 'Cyst': 0.20},
    'Maize Gluten Meal': {'type': 'energy', 'subtype': 'source', 'cost': 3.75, 'DM': 90.0, 'CP': 41.8, 'ME': 2875, 'CF': 4.3, 'EE': 2.3, 'Ash': 2.7, 'Ca': 0.15, 'P': 0.52, 'Lys': 0.81, 'Meth': 1.08, 'Cyst': 0.70},
    'Maize ByProduct Flour': {'type': 'energy', 'subtype': 'source', 'cost': 1.13, 'DM': 90.0, 'CP': 62.2, 'ME': 3780, 'CF': 2.0, 'EE': 2.3, 'Ash': 1.8, 'Ca': 0.02, 'P': 0.23, 'Lys': 1.00, 'Meth': 1.90, 'Cyst': 1.10},
    'Cassava Meal': {'type': 'energy', 'subtype': 'source', 'cost': 0.94, 'DM': 87.3, 'CP': 2.9, 'ME': 2900, 'CF': 1.2, 'EE': 0.7, 'Ash': 2.5, 'Ca': 0.12, 'P': 0.20, 'Lys': 0.08, 'Meth': 0.00, 'Cyst': 0.10},
    
    # Energy_Replacers
    'Wheat_Bran': {'type': 'energy', 'subtype': 'replacer', 'cost': 1.50, 'DM': 91.2, 'CP': 15.4, 'ME': 1145, 'CF': 10.0, 'EE': 3.4, 'Ash': 6.0, 'Ca': 0.07, 'P': 0.87, 'Lys': 0.87, 'Meth': 0.20, 'Cyst': 0.47},
    'Wheat_Middling': {'type': 'energy', 'subtype': 'replacer', 'cost': 1.56, 'DM': 90.0, 'CP': 16.0, 'ME': 1800, 'CF': 7.5, 'EE': 3.0, 'Ash': 2.5, 'Ca': 0.12, 'P': 0.90, 'Lys': 0.69, 'Meth': 0.21, 'Cyst': 0.32},
    'Maize_Gluten_Feed': {'type': 'energy', 'subtype': 'replacer', 'cost': 1.38, 'DM': 92.2, 'CP': 21.5, 'ME': 1700, 'CF': 9.0, 'EE': 2.3, 'Ash': 7.5, 'Ca': 0.30, 'P': 0.85, 'Lys': 0.63, 'Meth': 0.45, 'Cyst': 0.51},
    'Maize_Distillers_Dried_Grains': {'type': 'energy', 'subtype': 'replacer', 'cost': 3.13, 'DM': 89.0, 'CP': 9.9, 'ME': 1950, 'CF': 6.0, 'EE': 3.0, 'Ash': 7.5, 'Ca': 0.12, 'P': 0.41, 'Lys': 0.84, 'Meth': 0.37, 'Cyst': 0.28},
    'Rice_Bran': {'type': 'energy', 'subtype': 'replacer', 'cost': 1.19, 'DM': 92.0, 'CP': 19.8, 'ME': 1900, 'CF': 18.6, 'EE': 12.0, 'Ash': 8.6, 'Ca': 0.17, 'P': 0.70, 'Lys': 0.52, 'Meth': 0.37, 'Cyst': 0.49},
    'Rice_Polishing': {'type': 'energy', 'subtype': 'replacer', 'cost': 1.31, 'DM': 90.0, 'CP': 13.2, 'ME': 2100, 'CF': 11.5, 'EE': 13.2, 'Ash': 9.0, 'Ca': 0.05, 'P': 1.60, 'Lys': 0.52, 'Meth': 0.30, 'Cyst': 0.10},
    'Palm_Kernel_Meal': {'type': 'energy', 'subtype': 'replacer', 'cost': 3.44, 'DM': 89.0, 'CP': 21.3, 'ME': 2500, 'CF': 17.5, 'EE': 7.8, 'Ash': 5.6, 'Ca': 0.40, 'P': 0.40, 'Lys': 0.69, 'Meth': 0.47, 'Cyst': 0.32},
     
     # high Protein_Sources
    'Fish_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 10.00, 'DM': 92.8, 'CP': 66.1, 'ME': 2750, 'CF': 0.7, 'EE': 5.2, 'Ash': 22.3, 'Ca': 4.2, 'P': 2.4, 'Lys': 6.16, 'Meth': 2.23, 'Cyst': 1.40},
    'Anchovy_FM': {'type': 'protein', 'subtype': 'high', 'cost': 10.00, 'DM': 92.8, 'CP': 66.1, 'ME': 2750, 'CF': 0.7, 'EE': 5.2, 'Ash': 22.3, 'Ca': 4.2, 'P': 2.4, 'Lys': 6.16, 'Meth': 2.23, 'Cyst': 1.40},
    'Crayfish_FM': {'type': 'protein', 'subtype': 'high', 'cost': 9.38, 'DM': 92.8, 'CP': 67.9, 'ME': 2700, 'CF': 0.3, 'EE': 3.9, 'Ash': 12.3, 'Ca': 4.0, 'P': 2.4, 'Lys': 6.79, 'Meth': 2.04, 'Cyst': 2.04},
    'Herring_FM': {'type': 'protein', 'subtype': 'high', 'cost': 9.69, 'DM': 91.7, 'CP': 70.1, 'ME': 3000, 'CF': 0.5, 'EE': 10.0, 'Ash': 12.3, 'Ca': 2.2, 'P': 1.9, 'Lys': 6.67, 'Meth': 2.32, 'Cyst': 0.68},
    'Menhaden_FM': {'type': 'protein', 'subtype': 'high', 'cost': 10.00, 'DM': 94.0, 'CP': 60.4, 'ME': 2880, 'CF': 0.4, 'EE': 8.1, 'Ash': 21.9, 'Ca': 6.2, 'P': 2.9, 'Lys': 5.44, 'Meth': 2.22, 'Cyst': 1.1},
    'Blood_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 5.00, 'DM': 92.6, 'CP': 80.2, 'ME': 2844, 'CF': 1.5, 'EE': 1.5, 'Ash': 8.1, 'Ca': 0.50, 'P': 0.4, 'Lys': 9.10, 'Meth': 1.21, 'Cyst': 1.20},
    'Blood_Meal_2': {'type': 'protein', 'subtype': 'high', 'cost': 5.13, 'DM': 92.6, 'CP': 69.2, 'ME': 2600, 'CF': 1.0, 'EE': 0.5, 'Ash': 8.1, 'Ca': 0.3, 'P': 0.4, 'Lys': 8.48, 'Meth': 1.20, 'Cyst': 1.2},
    'Meat_and_Bone_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 4.38, 'DM': 92.8, 'CP': 55.0, 'ME': 2310, 'CF': 2.4, 'EE': 7.0, 'Ash': 28.8, 'Ca': 10.0, 'P': 5.0, 'Lys': 2.55, 'Meth': 0.70, 'Cyst': 0.77},
    'Meat_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 4.25, 'DM': 94.0, 'CP': 50.2, 'ME': 1955, 'CF': 2.5, 'EE': 10.0, 'Ash': 25.0, 'Ca': 7.5, 'P': 4.0, 'Lys': 3.0, 'Meth': 0.66, 'Cyst': 0.90},
    'Poultry_ByProduct_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 4.69, 'DM': 94.0, 'CP': 60.0, 'ME': 2840, 'CF': 2.5, 'EE': 12.5, 'Ash': 20.0, 'Ca': 5.0, 'P': 3.0, 'Lys': 2.60, 'Meth': 1.10, 'Cyst': 0.80},
    'Poultry_Feather_Meal': {'type': 'protein', 'subtype': 'high', 'cost': 4.06, 'DM': 93.0, 'CP': 85.7, 'ME': 2360, 'CF': 1.2, 'EE': 2.5, 'Ash': 3.9, 'Ca': 0.2, 'P': 0.7, 'Lys': 1.75, 'Meth': 0.6, 'Cyst': 3.20},


    # medium Protein_Sources
    'Beniseed_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 3.75, 'DM': 93.0, 'CP': 44.0, 'ME': 2100, 'CF': 10.0, 'EE': 6.5, 'Ash': 8.0, 'Ca': 0.20, 'P': 1.20, 'Lys': 0.30, 'Meth': 1.40, 'Cyst': 0.58},
    'Brewers_Yeast': {'type': 'protein', 'subtype': 'medium', 'cost': 3.75, 'DM': 93.0, 'CP': 44.7, 'ME': 1950, 'CF': 2.1, 'EE': 0.7, 'Ash': 0.7, 'Ca': 0.12, 'P': 1.40, 'Lys': 3.30, 'Meth': 0.85, 'Cyst': 0.50},
    'Canola_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 3.13, 'DM': 93.0, 'CP': 37.0, 'ME': 0, 'CF': 11.5, 'EE': 2.5, 'Ash': 7.2, 'Ca': 0.66, 'P': 1.10, 'Lys': 2.27, 'Meth': 0.68, 'Cyst': 0.47},
    'Cottonseed_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 2.81, 'DM': 90.3, 'CP': 42.3, 'ME': 2275, 'CF': 11.2, 'EE': 1.7, 'Ash': 7.7, 'Ca': 0.20, 'P': 1.0, 'Lys': 1.13, 'Meth': 0.85, 'Cyst': 0.47},
    'Groundnut_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 4.06, 'DM': 93.8, 'CP': 48.9, 'ME': 2275, 'CF': 12.2, 'EE': 4.3, 'Ash': 7.7, 'Ca': 0.21, 'P': 0.40, 'Lys': 1.13, 'Meth': 0.60, 'Cyst': 0.47},
    'Soybean': {'type': 'protein', 'subtype': 'medium', 'cost': 3.44, 'DM': 90.7, 'CP': 40.0, 'ME': 3750, 'CF': 7.5, 'EE': 19.3, 'Ash': 8.0, 'Ca': 0.20, 'P': 0.28, 'Lys': 2.90, 'Meth': 0.66, 'Cyst': 0.63},
    'Soybean_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 2.81, 'DM': 90.7, 'CP': 48.5, 'ME': 2240, 'CF': 6.3, 'EE': 1.5, 'Ash': 8.0, 'Ca': 0.28, 'P': 0.65, 'Lys': 2.75, 'Meth': 0.65, 'Cyst': 0.63},
    'Sunflowerseed': {'type': 'protein', 'subtype': 'medium', 'cost': 2.50, 'DM': 94.0, 'CP': 16.9, 'ME': 0, 'CF': 29.1, 'EE': 26.1, 'Ash': 8.0, 'Ca': 0.17, 'P': 0.53, 'Lys': 1.01, 'Meth': 0.46, 'Cyst': 0.54},
    'Sunflowerseed_Meal': {'type': 'protein', 'subtype': 'medium', 'cost': 2.81, 'DM': 90.3, 'CP': 39.6, 'ME': 2300, 'CF': 12.7, 'EE': 2.9, 'Ash': 8.4, 'Ca': 0.35, 'P': 0.9, 'Lys': 1.33, 'Meth': 0.6, 'Cyst': 0.7},


    #Protein_Replacers
    'Locust_Bean': {'type': 'protein', 'subtype': 'replacer', 'cost': 4.06, 'DM': 92.5, 'CP': 28.0, 'ME': 0, 'CF': 12.7, 'EE': 18.4, 'Ash': 5.6, 'Ca': 0.30, 'P': 0.40, 'Lys': 2.01, 'Meth': 0.18, 'Cyst': 0.58},
    'Beniseed': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.44, 'DM': 92.0, 'CP': 22.3, 'ME': 0, 'CF': 10.3, 'EE': 42.9, 'Ash': 5.6, 'Ca': 0.94, 'P': 0.70, 'Lys': 0.80, 'Meth': 0.86, 'Cyst': 0.35},
    'Canola_Seed': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.13, 'DM': 94.0, 'CP': 23.5, 'ME': 1820, 'CF': 14.2, 'EE': 39.2, 'Ash': 7.2, 'Ca': 0.39, 'P': 0.64, 'Lys': 1.38, 'Meth': 0.41, 'Cyst': 0.28},
    'Coconut_Oil_Meal': {'type': 'protein', 'subtype': 'replacer', 'cost': 2.81, 'DM': 92.0, 'CP': 21.0, 'ME': 0, 'CF': 12.5, 'EE': 4.1, 'Ash': 5.6, 'Ca': 0.40, 'P': 0.50, 'Lys': 0.69, 'Meth': 0.47, 'Cyst': 0.32},
    'Cottonseed': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.44, 'DM': 92.0, 'CP': 21.2, 'ME': 2069, 'CF': 22.1, 'EE': 18.5, 'Ash': 7.7, 'Ca': 0.14, 'P': 0.70, 'Lys': 1.68, 'Meth': 0.48, 'Cyst': 0.58},
    'Cowpeas': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.75, 'DM': 89.0, 'CP': 23.2, 'ME': 0, 'CF': 6.0, 'EE': 2.2, 'Ash': 7.7, 'Ca': 0.11, 'P': 0.40, 'Lys': 1.13, 'Meth': 0.49, 'Cyst': 0.47},
    'Groundnut': {'type': 'protein', 'subtype': 'replacer', 'cost': 4.06, 'DM': 92.9, 'CP': 24.8, 'ME': 0, 'CF': 9.3, 'EE': 46.5, 'Ash': 6.4, 'Ca': 0.10, 'P': 0.60, 'Lys': 2.13, 'Meth': 0.60, 'Cyst': 0.49},
    'Lima_Bean': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.75, 'DM': 89.6, 'CP': 23.7, 'ME': 0, 'CF': 4.6, 'EE': 1.4, 'Ash': 7.8, 'Ca': 0.11, 'P': 0.40, 'Lys': 1.13, 'Meth': 0.49, 'Cyst': 0.47},
    'Palm_Kernel_Meal': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.44, 'DM': 89.0, 'CP': 21.3, 'ME': 2500, 'CF': 17.5, 'EE': 7.8, 'Ash': 5.6, 'Ca': 0.40, 'P': 0.40, 'Lys': 0.69, 'Meth': 0.47, 'Cyst': 0.32},
    'Pigeon_Pea': {'type': 'protein', 'subtype': 'replacer', 'cost': 3.13, 'DM': 93.0, 'CP': 21.9, 'ME': 0, 'CF': 7.5, 'EE': 1.0, 'Ash': 4.1, 'Ca': 0.13, 'P': 0.60, 'Lys': 1.58, 'Meth': 0.54, 'Cyst': 0.27},
    'Sorghum_Distillers_Grains': {'type': 'protein', 'subtype': 'replacer', 'cost': 2.81, 'DM': 92.8, 'CP': 27.4, 'ME': 2500, 'CF': 12.1, 'EE': 3.2, 'Ash': 9.1, 'Ca': 0.09, 'P': 0.70, 'Lys': 0.52, 'Meth': 0.30, 'Cyst': 0.23},
    'Brewers_Dried_Grains': {'type': 'protein', 'subtype': 'replacer', 'cost': 1.38, 'DM': 92.5, 'CP': 22.5, 'ME': 2100, 'CF': 8.1, 'EE': 4.7, 'Ash': 2.8, 'Ca': 0.20, 'P': 0.45, 'Lys': 1.1, 'Meth': 0.27, 'Cyst': 0.17},
    
    #Essential Amino Acid 1
    'Lysine': {'type': 'Amino acid 1', 'subtype': 'Essential Amino Acid 1', 'cost': 29.00, 'CP': 0, 'ME': 0, 'Lys': 100, 'Meth': 0},
    
    #Essential Amino Acid 2
    'Methionine': {'type': 'Amino acid 2', 'subtype': 'Essential Amino Acid 2', 'cost': 45.00, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0},


    # fixed ingredients
    'Oyster Shell': {'type': 'mineral', 'cost': 0.63, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0, 'Ca': 38.0, 'P': 0.0},
    'Bone_Meal': {'type': 'mineral', 'cost': 0.94, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0, 'Ca': 24.0, 'P': 12.0},
    'Salt': {'type': 'mineral', 'cost': 0.31, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0},
    'Premix': {'type': 'additive', 'cost': 3.13, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0},
    'Lysine': {'type': 'Amino acid 1', 'subtype': 'Essential Amino Acid 1', 'cost': 29.00, 'CP': 0, 'ME': 0, 'Lys': 100, 'Meth': 0},
    'Methionine': {'type': 'Amino acid 2', 'subtype': 'Essential Amino Acid 2', 'cost': 45.00, 'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 100},
    }




# Fixed ingredients and their proportions in the diet
fixed_ingredients = {
    'Oyster Shell': 1.2,
    'Bone_Meal': 3.5,
    'Salt': 0.35,
    'Premix': 0.25,
    'Lysine': 0.8,
    'Methionine': 0.3
}

# Remaining proportion to be filled by variable ingredients
remaining_proportion = 100 - sum(fixed_ingredients.values())


def get_user_input(prompt, ingredient_type, subtype=None):
    """
    Prompts the user to select ingredients matching a specific type and optional subtype.
    Ensures the user selects ingredients where necessary and allows skipping optional categories.
    """
    available_ingredients = [
        name for name, details in ingredient_db.items()
        if details['type'] == ingredient_type and (subtype is None or details.get('subtype') == subtype)
    ]

    # Graceful skip when no ingredients exist
    if not available_ingredients:
        print(f"No ingredients found for '{ingredient_type}' with subtype '{subtype}'. Skipping category.")
        return []

    print(f"\nAvailable {subtype.capitalize()} {ingredient_type.capitalize()} Ingredients:" if subtype else f"\nAvailable {ingredient_type.capitalize()} Ingredients:")
    for idx, ingredient in enumerate(available_ingredients, start=1):
        print(f"{idx}. {ingredient}")

    # Prompt user for selection
    while True:
        print("\nEnter numbers separated by commas (e.g., 1,3,5), or type 'skip' to skip this category.")
        selected_indices = input(prompt).strip().lower()

        if selected_indices == 'skip':
            print(f"Skipping {ingredient_type} - {subtype} category.")
            return []

        try:
            selected_indices = [int(idx.strip()) for idx in selected_indices.split(',')]
            selected_ingredients = [available_ingredients[idx - 1] for idx in selected_indices if 0 < idx <= len(available_ingredients)]

            if len(selected_ingredients) > 0:
                return selected_ingredients
            else:
                print("Please select at least one valid ingredient.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas or 'skip' to skip.")

def get_formulation(
    poultry_class, 
    energy_sources, 
    energy_replacers, 
    high_protein_sources,
    medium_protein_sources, 
    protein_replacers,
    Essential_Amino_Acids_1, 
    Essential_Amino_Acids_2,  
    tolerance=0.3
):
    """
    Generates 12 feed formulation options based on selected ingredients and highlights recommended ones.
    """
    print("\nStarting Feed Formulation Process...")

    # Validate inputs
    if len(medium_protein_sources) < 2 or len(energy_sources) < 2 or len(protein_replacers) < 2 or len(energy_replacers) < 2:
        print("Error: At least 2 medium protein sources, 2 energy sources, 2 energy replacers, and 2 protein replacers are required.")
        return None

    # Define proportions and replacement ratios based on poultry class
    if poultry_class == 'Broiler_chicken_0_6_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.15
        energy_replacement_ratio = 0.05
    elif poultry_class == 'Broiler_chicken_6_9_weeks':
        base_medium_protein_percentage = 35
        base_energy_percentage = 65
        protein_replacement_ratio = 0.40
        energy_replacement_ratio = 0.0

    elif poultry_class == 'Broiler_chicken_9_12_weeks':
        base_medium_protein_percentage = 30
        base_energy_percentage = 70
        protein_replacement_ratio = 0.45
        energy_replacement_ratio = 0.17
    elif poultry_class == 'Pullets_chicken_0_8_weeks':
        base_medium_protein_percentage = 38
        base_energy_percentage = 62
        protein_replacement_ratio = 0.55
        energy_replacement_ratio = 0.35
    elif poultry_class == 'Pullets_chicken_8_20_weeks':
        base_medium_protein_percentage = 50
        base_energy_percentage = 50
        protein_replacement_ratio = 0.95
        energy_replacement_ratio = 0.3
    elif poultry_class == 'Layers/Breeders_chicken':
        base_medium_protein_percentage = 28
        base_energy_percentage = 72
        protein_replacement_ratio = 0.7
        energy_replacement_ratio = 0.30
    elif poultry_class == 'Turkey_0_8_weeks':
        base_medium_protein_percentage = 50
        base_energy_percentage = 50
        protein_replacement_ratio = 0.05
        energy_replacement_ratio = 0.05
    elif poultry_class == 'Turkey_8_16_weeks':
        base_medium_protein_percentage = 50
        base_energy_percentage = 50
        protein_replacement_ratio = 0.50
        energy_replacement_ratio = 0.1
    elif poultry_class == 'Turkey_16_30_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.85
        energy_replacement_ratio = 0.3
    elif poultry_class == 'Mature_Turkeys_and_Breeders':
        base_medium_protein_percentage = 25
        base_energy_percentage = 75
        protein_replacement_ratio = 1
        energy_replacement_ratio = 0.7
    elif poultry_class == 'GuineaFowl_0_4_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.15
        energy_replacement_ratio = 0.05
    elif poultry_class == 'GuineaFowl_4_8_weeks':
        base_medium_protein_percentage = 35
        base_energy_percentage = 65
        protein_replacement_ratio = 0.40
        energy_replacement_ratio = 0.0
    elif poultry_class == 'GuineaFowl_8_12_weeks':
        base_medium_protein_percentage = 30
        base_energy_percentage = 70
        protein_replacement_ratio = 0.60
        energy_replacement_ratio = 0.10
    elif poultry_class == 'GuineaFowl_6_28_weeks':
        base_medium_protein_percentage = 35
        base_energy_percentage = 65
        protein_replacement_ratio = 4
        energy_replacement_ratio = 0.5
    elif poultry_class == 'GuineaFowl_Layers':
        base_medium_protein_percentage = 28
        base_energy_percentage = 70
        protein_replacement_ratio = 0.75
        energy_replacement_ratio = 0.30
    elif poultry_class == 'Duck_0_3_weeks':
        bbase_medium_protein_percentage = 50
        base_energy_percentage = 50
        protein_replacement_ratio = 0.50
        energy_replacement_ratio = 0.1
    elif poultry_class == 'Duck_3_8_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.85
        energy_replacement_ratio = 0.3
    elif poultry_class == 'Duck_Layers':
        base_medium_protein_percentage = 50
        base_energy_percentage = 50
        protein_replacement_ratio = 0.95
        energy_replacement_ratio = 0.3
    elif poultry_class == 'Quail_Broilers_0_2_weeks':
        base_medium_protein_percentage = 43
        base_energy_percentage = 57
        protein_replacement_ratio = 0
        energy_replacement_ratio = 0.2
    elif poultry_class == 'Quail_Broilers_3_5_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.15
        energy_replacement_ratio = 0.05
    elif poultry_class == 'Quail_Layers_0_2_weeks':
        base_medium_protein_percentage = 40
        base_energy_percentage = 60
        protein_replacement_ratio = 0.20
        energy_replacement_ratio = 0.1
    elif poultry_class == 'Quail_Layers_3_5_weeks':
        base_medium_protein_percentage = 36
        base_energy_percentage = 64
        protein_replacement_ratio = 0.56
        energy_replacement_ratio = 0.30
    elif poultry_class == 'Quail_Layers_5_6_weeks':
        base_medium_protein_percentage = 36
        base_energy_percentage = 64
        protein_replacement_ratio = 0.60
        energy_replacement_ratio = 0.31
    else:
        print(f"Error: Unknown poultry class '{poultry_class}'.")
        return None

     # Retrieve nutrient requirements for the selected class
    nutrient_req = nutrient_requirements[poultry_class]


    # Function to generate a formulation
    def create_formulation(medium_protein, energy, protein_replacer=None, energy_replacer=None):
        formulation = {}
        nutrients = {'CP': 0, 'ME': 0, 'Lys': 0, 'Meth': 0, 'Ca': 0, 'P': 0}  # Nutrient totals

        # Add fixed ingredients to the formulation
        for ingredient, proportion in fixed_ingredients.items():
            formulation[ingredient] = proportion
            for nutrient in nutrients:
                nutrients[nutrient] += (ingredient_db[ingredient].get(nutrient, 0) * proportion / 100)

        # Proportions of medium protein, energy, protein replacer, and energy replacer
        medium_protein_amount = base_medium_protein_percentage * (1 - protein_replacement_ratio)
        protein_replacer_amount = base_medium_protein_percentage * protein_replacement_ratio

        energy_amount = base_energy_percentage * (1 - energy_replacement_ratio)
        energy_replacer_amount = base_energy_percentage * energy_replacement_ratio

        # Add ingredients to the formulation
        formulation[medium_protein] = medium_protein_amount
        formulation[energy] = energy_amount
        if protein_replacer:
            formulation[protein_replacer] = protein_replacer_amount
        if energy_replacer:
            formulation[energy_replacer] = energy_replacer_amount

        # Update nutrient totals
        for nutrient in nutrients:
            nutrients[nutrient] += (ingredient_db[medium_protein].get(nutrient, 0) * medium_protein_amount / 100)
            nutrients[nutrient] += (ingredient_db[energy].get(nutrient, 0) * energy_amount / 100)
            if protein_replacer:
                nutrients[nutrient] += (ingredient_db[protein_replacer].get(nutrient, 0) * protein_replacer_amount / 100)
            if energy_replacer:
                nutrients[nutrient] += (ingredient_db[energy_replacer].get(nutrient, 0) * energy_replacer_amount / 100)

        # Attach calculated totals
        formulation['total_cp_content'] = nutrients['CP']
        formulation['total_me_content'] = nutrients['ME']
        formulation['lysine_content'] = nutrients['Lys']
        formulation['methionine_content'] = nutrients['Meth']
        formulation['calcium_content'] = nutrients['Ca']
        formulation['phosphorus_content'] = nutrients['P']

        return formulation

    # Generate formulations
    formulations = []
    for i in range(2):  # Iterate over selected medium protein sources
        for j in range(2):  # Iterate over selected energy sources
            formulations.append(create_formulation(
                medium_protein_sources[i], 
                energy_sources[j]
            ))
            formulations.append(create_formulation(
                medium_protein_sources[i], 
                energy_sources[j], 
                protein_replacers[0], 
                energy_replacers[0]
            ))
            formulations.append(create_formulation(
                medium_protein_sources[i], 
                energy_sources[j], 
                protein_replacers[1], 
                energy_replacers[1]
            ))

    # Display all formulations
    print("\nAll Generated Formulations:")
    for idx, formulation in enumerate(formulations, start=1):
        print(f"\nOption {idx}:")
        for ingredient, proportion in formulation.items():
            if not ingredient.endswith("_content"):
                print(f"  {ingredient}: {proportion:.2f}%")
        print(f"  Crude Protein (CP): {formulation['total_cp_content']:.2f}%")
        print(f"  Metabolizable Energy (ME): {formulation['total_me_content']:.2f} kcal/kg")
        print(f"  Lysine Content: {formulation['lysine_content']:.2f}%")
        print(f"  Methionine Content: {formulation['methionine_content']:.2f}%")
        print(f"  Calcium Content (Ca): {formulation['calcium_content']:.2f}%")
        print(f"  Phosphorus Content (P): {formulation['phosphorus_content']:.2f}%")

    # Identify recommended formulations
    recommended_formulations = [
        formulation for formulation in formulations
        if (
            nutrient_req['ME_min'] <= formulation['total_me_content'] <= nutrient_req['ME_max'] and
            nutrient_req['CP_min'] <= formulation['total_cp_content'] <= nutrient_req['CP_max']
        )
    ]

    # Display recommended formulations
    print("\nRecommended Formulations (meeting nutrient requirements):")
    if recommended_formulations:
        for idx, formulation in enumerate(recommended_formulations, start=1):
            print(f"\nRecommended Option {idx}:")
            for ingredient, proportion in formulation.items():
                if not ingredient.endswith("_content"):
                    print(f"  {ingredient}: {proportion:.2f}%")
            print(f"  Crude Protein (CP): {formulation['total_cp_content']:.2f}%")
            print(f"  Metabolizable Energy (ME): {formulation['total_me_content']:.2f} kcal/kg")
            print(f"  Lysine Content: {formulation['lysine_content']:.2f}%")
            print(f"  Methionine Content: {formulation['methionine_content']:.2f}%")
            print(f"  Calcium Content (Ca): {formulation['calcium_content']:.2f}%")
            print(f"  Phosphorus Content (P): {formulation['phosphorus_content']:.2f}%")
    else:
        print("No formulations meet the nutrient requirements.")

    return formulations


def main():
    print("Welcome to the Least-Cost Feed Formulation Program!")

    print("\nAvailable poultry Classes:")
    for idx, poultry_class in enumerate(nutrient_requirements.keys(), start=1):
        print(f"{idx}. {poultry_class}")

    # Input validation for poultry Class
    while True:
        try:
            poultry_class_idx = int(input("\nSelect the poultry class by entering the corresponding number: "))
            if 1 <= poultry_class_idx <= len(nutrient_requirements):
                break
            print(f"Please enter a number between 1 and {len(nutrient_requirements)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    poultry_class = list(nutrient_requirements.keys())[poultry_class_idx - 1]

    print(f"\nYou selected '{poultry_class}'. Now, choose the ingredients for each category.")

    # Layer-specific poultry classes
    layer_classes = [
        'Layers/Breeders_chicken',
        'Mature_Turkeys_and_Breeders',
        'Duck_Layers',
        'GuineaFowl_Layers',
        'Quail_Layers_0_2_weeks',
        'Quail_Layers_3_5_weeks',
        'Quail_Layers_5_6_weeks'
    ]

    # Add extra oyster shell for layer classes
    if poultry_class in layer_classes:
        print("\nThis is a layers category. Adding an extra 5% Oyster Shell.")
        fixed_ingredients['Oyster Shell'] += 6

    # User-selected ingredients: prompt each category **only once**
    energy_sources = get_user_input("Enter the numbers for Energy Sources: ", "energy", "source")
    print(f"Selected Energy Sources: {energy_sources}")

    energy_replacers = get_user_input("Enter the numbers for Energy Replacers: ", "energy", "replacer")
    print(f"Selected Energy Replacers: {energy_replacers}")

    high_protein_sources = get_user_input("Enter the numbers for medium Protein Sources: ", "protein", "high")
    print(f"Selected High Protein Sources: {high_protein_sources}")

    medium_protein_sources = get_user_input("Enter the numbers for medium Protein Sources: ", "protein", "medium")
    print(f"Selected High Protein Sources: {medium_protein_sources}")

    protein_replacers = get_user_input("Enter the numbers for Protein Replacers: ", "protein", "replacer")
    print(f"Selected Protein Replacers: {protein_replacers}")

    Essential_Amino_Acids_1 = get_user_input("Enter the number for Essential Amino Acid 1: ", "Amino acid 1", "Essential Amino Acid 1")
    print(f"Selected Essential Amino Acid 1: {Essential_Amino_Acids_1}")

    Essential_Amino_Acids_2 = get_user_input("Enter the number for Essential Amino Acid 2: ", "Amino acid 2", "Essential Amino Acid 2")
    print(f"Selected Essential Amino Acid 2: {Essential_Amino_Acids_2}")

    print("\nGenerating feed formulations based on your inputs...")

    # Generate formulations
    formulations = get_formulation(
        poultry_class,
        energy_sources,
        energy_replacers,
        high_protein_sources,
        medium_protein_sources,
        protein_replacers,
        Essential_Amino_Acids_1,
        Essential_Amino_Acids_2
    )

    print("\nThank you for using the Least-Cost Feed Formulation Program!")


if __name__ == "__main__":
    main()

