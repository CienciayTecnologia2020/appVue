from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS
import openai
import json
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'database': 'probono',
    'pool_name': 'mypool',
    'pool_size': 5
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.before_request
def before_request():
    request.db = get_db_connection()
    request.cursor = request.db.cursor(dictionary=True)

@app.teardown_request
def teardown_request(exception):
    if hasattr(request, 'cursor'):
        request.cursor.close()
    if hasattr(request, 'db'):
        request.db.close()

# Define your API key
openai.api_key = "sk-proj-1bVzZFgVIjSa0dkiYHu6T3BlbkFJCnnEKPcuBLmJaySn3DGG"

def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the random level of the model
    )
    return response.choices[0].message['content']


# Ruta para servir la imagen
@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    # Ruta a la carpeta donde están las imágenes
    image_folder = os.path.join(app.root_path, './static/images')
    try:
        # Devuelve la imagen solicitada
        return send_from_directory(image_folder, filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/labs', methods=['GET'])
def get_labs():
    problem_id = request.args.get('selectedProblem')  # Obtener el ID del problema seleccionado de los parámetros de la solicitud

    sql = "SELECT id, name FROM location"
    request.cursor.execute(sql)

    labs = request.cursor.fetchall()
    return jsonify(labs)

@app.route('/map/<int:location>', methods=['GET'])
def get_map(location):
    
    sql = "SELECT latitude, longitude FROM location WHERE id = %s"
    request.cursor.execute(sql, (location,))

    map = request.cursor.fetchall()
    return jsonify(map)

@app.route('/update_problem_location', methods=['POST'])
def update_problem_location():
    try:
        data = request.json
        problem_id = data.get('problem_id')
        context_id = data.get('context_id')
        
        sql = """
            UPDATE problem
            SET context_id = %s
            WHERE id = %s
        """
        request.cursor.execute(sql, (context_id, problem_id))
        request.db.commit()
        return jsonify({"message": "Problem location updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/lab_data', methods=['POST'])
def get_lab_data():
    problem_id = request.json.get('selectedProblem')
    sql = """
        SELECT location.*
        FROM location
        INNER JOIN problem ON location.id = problem.context_id
        WHERE problem.id = %s
    """
    request.cursor.execute(sql, (problem_id,))
    lab_info = request.cursor.fetchall()
    return jsonify(lab_info)


@app.route('/kpi/<int:problem_id>', methods=['GET'])
def get_kpis_by_lab(problem_id):
    try:
        sql = """
            SELECT 
                k.*,
                cf.frequency AS calculationFrequency,
                CASE WHEN pk.problem_id IS NOT NULL THEN TRUE ELSE FALSE END AS selectedKpi,
                GROUP_CONCAT(lc.name SEPARATOR ', ') AS lifecycle
            FROM 
                kpi k
            LEFT JOIN
                calculationfrequency cf ON k.calculationfrequency_id = cf.id
            LEFT JOIN
                problem_kpi pk ON k.id = pk.kpi_id AND pk.problem_id = %s
            LEFT JOIN
                kpi_lifecycle klc ON k.id = klc.kpi_id
            LEFT JOIN
                lifecycle lc ON klc.lifecycle_id = lc.id
            GROUP BY
                k.id,cf.frequency, pk.problem_id
        """
        request.cursor.execute(sql, (problem_id,))
        kpis = request.cursor.fetchall()
        return jsonify(kpis)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/lifecycle/<int:kpi_id>', methods=['PUT'])
def put_lifeCycle(kpi_id):
    try:
        # Obtener el lifecycle_id del cuerpo de la solicitud
        lifecycle = request.json
        
        # Verificar si la relación ya existe
        sql_check = "SELECT * FROM kpi_lifecycle WHERE kpi_id = %s AND lifecycle_id = %s"
        request.cursor.execute(sql_check, (kpi_id, lifecycle['lifecycle_id']))
        existing_relation = request.cursor.fetchone()
        
        if existing_relation:
            # Si la relación existe, no hacer nada
            return jsonify({"message": "Relation already exists"}), 200
        else:
            # Si la relación no existe, crear una nueva relación
            sql_insert = "INSERT INTO kpi_lifecycle (kpi_id, lifecycle_id) VALUES (%s, %s)"
            request.cursor.execute(sql_insert, (kpi_id, lifecycle['lifecycle_id']))
            request.db.commit()
            
            return jsonify({"message": "Relation created successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/lifecycle', methods=['GET'])
def get_lifeCycle():
    try:
        sql = "SELECT * FROM lifecycle"
        request.cursor.execute(sql)
        lifeCycles = request.cursor.fetchall()
        return jsonify(lifeCycles), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lifecycle/<int:kpi_id>', methods=['DELETE'])
def delete_lifeCycle(kpi_id):
    try:
        # Obtener el life_cycle_id del cuerpo de la solicitud
        data = request.json
        print(data["lifecycle_id"])
        
        # Consulta para eliminar la relación en kpi_lifecycle
        sql = """
            DELETE FROM kpi_lifecycle
            WHERE kpi_id = %s AND lifecycle_id = %s
        """
        
        # Ejecutar la consulta con los parámetros proporcionados
        request.cursor.execute(sql, (kpi_id, data['lifecycle_id']))
        request.db.commit()  # Asegúrate de confirmar la transacción
        
        return jsonify({"message": "Relation deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/lifecycle-kpi/<int:kpi_id>', methods=['GET'])
def get_lifeCycle_for_kpi(kpi_id):
    try:
        # Consulta para obtener los nombres de los lifecycle relacionados con el kpi_id
        sql = """
            SELECT lc.id, lc.name 
            FROM lifecycle lc
            JOIN kpi_lifecycle klc ON lc.id = klc.lifecycle_id
            JOIN kpi k ON klc.kpi_id = k.id
            WHERE k.id = %s
        """
        # Ejecutar la consulta con el kpi_id proporcionado
        request.cursor.execute(sql, (kpi_id,))
        lifeCycles = request.cursor.fetchall()
        
       
        
        return jsonify(lifeCycles), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@app.route('/kpi/<int:kpi_id>', methods=['PUT'])
def update_kpi(kpi_id):
    try:
        kpi_data = request.json
        sql = """
            UPDATE kpi
            SET name = %s, impact =%s, description=%s, formula = %s, responsibilityDefinition = %s, baseLineDataNeeded = %s, pillar= %s, unit= %s
            WHERE id = %s
        """
        request.cursor.execute(sql, (
            kpi_data['name'],
            kpi_data['impact'],
            kpi_data['description'],
            kpi_data['formula'],
            kpi_data['responsibilityDefinition'], 
            kpi_data['baseLineDataNeeded'],
            kpi_data['pillar'],
            kpi_data['unit'], 
            kpi_id
        ))
        
       
    
        
        request.db.commit()
        return jsonify({"message": "KPI updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/kpi', methods=['POST'])
def manage_kpi():
    try:
        kpi_data = request.json
        sql_get_last_id = "SELECT MAX(id) FROM kpi"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1

        sql_insert_kpi = """
            INSERT INTO kpi (
            id, unit, pillar, calculationfrequency_id, name, impact, baseLineDataNeeded, 
            responsibilityDefinition, responsibilityCalculation, description, dataRequirements, formula
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        kpi_values = (
            new_id, kpi_data.get('unit_id', ''), kpi_data.get('pillar_id', ''), kpi_data.get('calculationfrequency_id', 1),
            kpi_data.get('name', 'name'), kpi_data.get('impact', "H"), kpi_data.get('baseLineDataNeeded', 'baseLineDataNeeded'), 
            kpi_data.get('responsibilityDefinition', "3333"), kpi_data.get('responsibilityCalculation', "333"), 
            kpi_data.get('description', "rrrr"), kpi_data.get('dataRequirements', "some"), kpi_data.get('formula', 'formula')
            )


        
        request.cursor.execute(sql_insert_kpi, kpi_values)
        print(new_id)
        
        sql_insert = "INSERT INTO problem_kpi (problem_id, kpi_id) VALUES (%s, %s)"
        request.cursor.execute(sql_insert, (kpi_data['selectedProblem'], new_id))
        request.db.commit()


        return jsonify({"message": "KPI created successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/kpi/<int:kpi_id>', methods=['DELETE'])
def delete_kpi(kpi_id):
    try:
        data = request.json
        
        sql_delete_relation = "DELETE FROM problem_kpi WHERE kpi_id = %s AND problem_id = %s"
        
        request.cursor.execute(sql_delete_relation, (kpi_id, data['selectedProblem']))

        sql_delete_relation_2 = "DELETE FROM kpi_lifecycle WHERE kpi_id = %s"
        
        request.cursor.execute(sql_delete_relation_2, (kpi_id,))
        
       
        sql_delete_kpi = "DELETE FROM kpi WHERE id = %s"
        request.cursor.execute(sql_delete_kpi, (kpi_id,))

        
        request.db.commit()
        
        return jsonify({"message": "KPI deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/delete-kpi/<int:kpi_id>', methods=['DELETE'])
def delete_kpi_in_list(kpi_id):
    try:
        sql_delete_problem_kpi = "DELETE FROM problem_kpi WHERE kpi_id = %s"
        request.cursor.execute(sql_delete_problem_kpi, (kpi_id,))
        
        request.db.commit()
        
        return jsonify({"message": "Building deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/add-kpi/<int:kpi_id>', methods=['PUT'])
def update_kpi_list(kpi_id):
    try:
        kpi_data = request.json

        sql_insert_problem_kpi = """
            INSERT INTO problem_kpi (problem_id, kpi_id) 
            VALUES (%s, %s)
        """
        lab_values = (kpi_data['selectedProblem'], kpi_id)
       
        request.cursor.execute(sql_insert_problem_kpi, lab_values)

        request.db.commit()


        return jsonify({"message": "Building updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    


    
@app.route('/stakeholder/<int:problem_id>', methods=['GET'])
def get_stakeholder_by_lab(problem_id):
    try:
        # Consulta para obtener los stakeholders y establecer la columna selectedStakeholder
        sql = """
            SELECT 
                s.*,
                CASE WHEN ps.problem_id IS NOT NULL THEN TRUE ELSE FALSE END AS selectedStakeholder
            FROM 
                stakeholder s
            LEFT JOIN 
                problem_stakeholder ps ON s.id = ps.stakeholder_id AND ps.problem_id = %s
        """
        request.cursor.execute(sql, (problem_id,))
        stakeholders = request.cursor.fetchall()
        return jsonify(stakeholders)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/stakeholder/<int:stakeholder_id>', methods=['PUT'])
def update_stakeholder(stakeholder_id):
    try:
        stakeholder_data = request.json
        sql = """
            UPDATE stakeholder
            SET name = %s, specificities = %s, requirements = %s, general_description = %s, related_kpi = %s
            WHERE id = %s
        """
        request.cursor.execute(sql, (
            stakeholder_data['name'],
            stakeholder_data['specificities'], 
            stakeholder_data['requirements'], 
            stakeholder_data['general_description'], 
            stakeholder_data['related_kpi'], 
            stakeholder_id
        ))
        
        selected_problem = stakeholder_data['selectedProblem']
        selected_stakeholders = stakeholder_data['selectedStakeholders']

        # Limpiar las relaciones existentes del problema en ejecución
        sql_delete_existing = "DELETE FROM problem_stakeholder WHERE problem_id = %s"
        request.cursor.execute(sql_delete_existing, (selected_problem,))

        # Agregar relaciones únicas en la tabla problem_stakeholder
        for index in range(len(selected_stakeholders)):
            selected_stakeholder_id = selected_stakeholders[index]
            # Verificar si la relación ya existe
            sql_check = "SELECT * FROM problem_stakeholder WHERE problem_id = %s AND stakeholder_id = %s"
            request.cursor.execute(sql_check, (selected_problem, selected_stakeholder_id))
            existing_relation = request.cursor.fetchone()
            if not existing_relation:
                # Si la relación no existe, insertarla
                sql_insert = "INSERT INTO problem_stakeholder (problem_id, stakeholder_id) VALUES (%s, %s)"
                request.cursor.execute(sql_insert, (selected_problem, selected_stakeholder_id))

        request.db.commit()
        return jsonify({"message": "Stakeholder updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/gpt-stakeholder', methods=['POST'])
def gpt_stakeholder():
    try:
        data = request.get_json()

        # Consulta para obtener el 'need' del problema
        sql_get_need = "SELECT need FROM problem WHERE id = %s"
        request.cursor.execute(sql_get_need, (data['selectedProblem'],))
        need_result = request.cursor.fetchone()

        # Consulta para obtener el 'name' y 'description' del lab
        sql_get_lab_info = "SELECT name, description FROM location WHERE id = %s"
        request.cursor.execute(sql_get_lab_info, (data['selectedLab'],))
        lab_info_result = request.cursor.fetchone()

        sql_get_building_info = """
            SELECT b.*
            FROM building b
            JOIN problem_building pb ON b.id = pb.building_id
            JOIN location_building lb ON b.id = lb.building_id
            WHERE pb.problem_id = %s AND lb.general_id = %s
        """
        request.cursor.execute(sql_get_building_info, (data['selectedProblem'], data['selectedLab']))
        buildings = request.cursor.fetchall()

        

        living_lab = lab_info_result['name']
        living_lab_description = lab_info_result['description']
        current_need = need_result['need']

        #buildings = [{"name":"Building10","description":""},{"name":"Kitchen 2.0","description":"The Kitchen 2.0 will be housed in the former boiler house and laundry and will, as now, function as Aarhus University's entrepreneurial factory, where students and researchers can bridge the gap between research and business."},{"name":"Building4","description":""}]
        # Convertir la información de los edificios a un string secuencial
        building_list = "\n".join([f"- {building['name']}: {building['description']}" for building in buildings])
        print(building_list)
        limit = 4
        prompt = f"""
            The context is inside ###

            ###
            You are assisting the development of a sustainable neighborhood.

            Location: {living_lab}
            Location details: {living_lab_description}
            
            Problem faced and decision to take: {current_need}
            
            Buildings and infrastructure involved : 
            {building_list}

            ###

            What are the stakeholders and stakeholder requirements to take into account?

            Give the result just as a JSON array without headers:
            [
            1) name: "stakeholder name",
            2) general_description: "description of the stakeholder", 
            3) requirements: "requirements of the stakeholder",
            ]
            Limit the result to {limit} stakeholders
        """
    
        response = get_completion(prompt)
        print(response)
        stakeholders = json.loads(response)

        sql_get_last_id = "SELECT MAX(id) FROM stakeholder"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
    
        for i, stakeholder in enumerate(stakeholders[:4]):  # Limit to first 4 stakeholders
            new_id = last_id + 1 + i  # Increment id based on index
            
            sql_insert_stakeholder = """
                INSERT INTO stakeholder (id,name, specificities, requirements, general_description) 
                VALUES (%s, %s, %s, %s, %s)
            """
            stakeholder_values = (
                new_id,
                stakeholder.get('name', ''),
                "Stakeholder generated with GPT-4o",
                stakeholder.get('requirements', ''),
                stakeholder.get('general_description', ''),
            
            )
            
            request.cursor.execute(sql_insert_stakeholder, stakeholder_values)
            
            sql_insert_problem_stakeholder = """
                INSERT INTO problem_stakeholder (problem_id, stakeholder_id) VALUES (%s, %s)
            """
            request.cursor.execute(sql_insert_problem_stakeholder, (data['selectedProblem'], new_id))
        
        request.db.commit()
        return jsonify({"message": "Stakeholders created successfully"}), 201
    
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)},), 500

@app.route('/gpt-recomendation', methods=['POST'])
def gpt_recomendation():
    try:
        data = request.get_json()

        # Consulta para obtener el 'need' del problema
        sql_get_need = "SELECT need FROM problem WHERE id = %s"
        request.cursor.execute(sql_get_need, (data['selectedProblem'],))
        need_result = request.cursor.fetchone()

        # Consulta para obtener el 'name' y 'description' del lab
        sql_get_lab_info = "SELECT name, description FROM location WHERE id = %s"
        request.cursor.execute(sql_get_lab_info, (data['selectedLab'],))
        lab_info_result = request.cursor.fetchone()

        sql_get_building_info = """
            SELECT b.*
            FROM building b
            JOIN problem_building pb ON b.id = pb.building_id
            JOIN location_building lb ON b.id = lb.building_id
            WHERE pb.problem_id = %s AND lb.general_id = %s
        """
        request.cursor.execute(sql_get_building_info, (data['selectedProblem'], data['selectedLab']))
        buildings = request.cursor.fetchall()

        living_lab = lab_info_result['name']
        living_lab_description = lab_info_result['description']
        current_need = need_result['need']

        #buildings = [{"name":"Building10","description":""},{"name":"Kitchen 2.0","description":"The Kitchen 2.0 will be housed in the former boiler house and laundry and will, as now, function as Aarhus University's entrepreneurial factory, where students and researchers can bridge the gap between research and business."},{"name":"Building4","description":""}]
        # Convertir la información de los edificios a un string secuencial
        building_list = "\n".join([f"- {building['name']}: {building['description']}" for building in buildings])
       
        sql_get_stakeholder_info = """
            SELECT s.*
            FROM stakeholder s
            JOIN problem_stakeholder ps ON s.id = ps.stakeholder_id
            WHERE ps.problem_id = %s
        """
        request.cursor.execute(sql_get_stakeholder_info, (data['selectedProblem'],))
        stakeholder= request.cursor.fetchall()
        stakeholder_list = "\n".join([f"- {stakeholder['name']}: {stakeholder['general_description']}" for stakeholder in stakeholder])
        
        limit = 4
        prompt = f"""
            The context is inside ###

            ###
            Location selected: {living_lab}
            Location details: {living_lab_description}
            
            Problem faced and decision to take: {current_need}
            
            Buildings and infrastructure involved: 
            {building_list}

            Stakeholders considered:
            {stakeholder_list}
            #
            Which digital tools would you suggest to use and why?
            It can be commercial tools or tools from academic research.
            Provide a URL for each tool.
            Make sure that each URL is correct.

            Give the result just as a JSON array without headers:
            [
            1) name: "name of the tool",
            2) explanation: "why you would suggest to use this tool"
            3) url: "URL of the tool"
            ]
            Limit the result to {limit} tools
        """
    
        response = get_completion(prompt)
        
        simulation_tools = json.loads(response)

        
        
        return jsonify(simulation_tools)
    
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/gpt-recomendation-selection', methods=['POST'])
def gpt_recomendation_selection():
    try:
        data = request.get_json()

        # Consulta para obtener el 'need' del problema
        sql_get_need = "SELECT need FROM problem WHERE id = %s"
        request.cursor.execute(sql_get_need, (data['selectedProblem'],))
        need_result = request.cursor.fetchone()

        # Consulta para obtener el 'name' y 'description' del lab
        sql_get_lab_info = "SELECT name, description FROM location WHERE id = %s"
        request.cursor.execute(sql_get_lab_info, (data['selectedLab'],))
        lab_info_result = request.cursor.fetchone()

        sql_get_building_info = """
            SELECT b.*
            FROM building b
            JOIN problem_building pb ON b.id = pb.building_id
            JOIN location_building lb ON b.id = lb.building_id
            WHERE pb.problem_id = %s AND lb.general_id = %s
        """
        request.cursor.execute(sql_get_building_info, (data['selectedProblem'], data['selectedLab']))
        buildings = request.cursor.fetchall()

        living_lab = lab_info_result['name']
        living_lab_description = lab_info_result['description']
        current_need = need_result['need']

        #buildings = [{"name":"Building10","description":""},{"name":"Kitchen 2.0","description":"The Kitchen 2.0 will be housed in the former boiler house and laundry and will, as now, function as Aarhus University's entrepreneurial factory, where students and researchers can bridge the gap between research and business."},{"name":"Building4","description":""}]
        # Convertir la información de los edificios a un string secuencial
        building_list = "\n".join([f"- {building['name']}: {building['description']}" for building in buildings])
       
        sql_get_stakeholder_info = """
            SELECT s.*
            FROM stakeholder s
            JOIN problem_stakeholder ps ON s.id = ps.stakeholder_id
            WHERE ps.problem_id = %s
        """
        request.cursor.execute(sql_get_stakeholder_info, (data['selectedProblem'],))
        stakeholder= request.cursor.fetchall()
        stakeholder_list = "\n".join([f"- {stakeholder['name']}: {stakeholder['general_description']}" for stakeholder in stakeholder])
        
        limit = 3
        prompt = f"""
            The context is inside ###

            ###
            Location selected: {living_lab}
            Location details: {living_lab_description}
            
            Problem faced and decision to take: {current_need}
            
            Buildings and infrastructure involved: 
            {building_list}

            Stakeholders considered:
            {stakeholder_list}
            #
            Among these digital tools, which ones would you suggest to use and why?

            - Name : Ventilation Assessment Tool
            - Description : User-friendly semi-automated CFD simulation for thermal comfort in buildings; Takes into account heaters, doors, windows or weather; Used for Kitchen 2.0 in Aarhus and for Pragues.
            
            - Name : Virtual Comfort Sensor
            - Description : Reduced CFD model for real-time simulation of building thermal comfort; The model inputs must be provided by on-site sensors; Used for Kitchen 2.0 in Aarhus.

            - Name : Demand&Response Platform
            - Description : Helps choose new energy solutions (installation of solar panels, replacement of a water heater, ...) by comparing their installation and operating costs for a given energy consumptions profile; Used for Brussels.

            - Name : Particle Propagation
            - Description : Simulates the propagation of particles and polluants in the air given data such as the geometry of the city and weather forecasts; Can for example help schedule the demolition of a building to limit air pollution; Used for Madrid.

            - Name : Urban Heat Island
            - Description : Helps identify urban heat islands; urban heat islands are city areas which become uncomfortably hot because of heat accumulation (typically because of concrete); Green neighborhood must avoid urban heat islands; Used for Madrid.

            - Name : Energy anomaly detection
            - Description : Helps detect anomalies in energy consumptions; Used for Brussels.

            - Name : Mobility
            - Description : Helps distinguish good and problematic areas on a map given traffic related data (speed, accidents, etc.); Can improve urban choices such as speed limits, sidewalk width or sign size; Used for Brussels.

            - Name : Green roof
            - Description : Simulation a green roof properties such as humidity and heat insulation; Permits to optimize water irrigation, using weather forecasts.

            Give the result just as a JSON array without headers:
            [
            1) name: "name of the tool",
            2) description: "description of the tool",
            3) explanation: "why you would suggest to use this tool"
            ]

            Limit the result to {limit} tools

        """
    
        response = get_completion(prompt)
        
        simulation_tools = json.loads(response)

        
        
        return jsonify(simulation_tools)
    
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/stakeholder', methods=['POST'])
def manage_stakeholder():
    try:
        stakeholder_data = request.json
        sql_get_last_id = "SELECT MAX(id) FROM stakeholder"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1

        sql_insert_stakeholder = """
            INSERT INTO stakeholder (id, name, specificities, requirements, general_description, related_kpi) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        stakeholder_values = (
            new_id,
            stakeholder_data['name'],
            stakeholder_data['specificities'], 
            stakeholder_data['requirements'], 
            stakeholder_data['general_description'], 
            stakeholder_data['related_kpi'],
        )
        request.cursor.execute(sql_insert_stakeholder, stakeholder_values)
        

        sql_insert = "INSERT INTO problem_stakeholder (problem_id, stakeholder_id) VALUES (%s, %s)"
        request.cursor.execute(sql_insert, (stakeholder_data['selectedProblem'], new_id))
        
        request.db.commit()
        return jsonify({"message": "Stakeholder created successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/stakeholder/<int:stakeholder_id>', methods=['DELETE'])
def delete_stakeholder(stakeholder_id):
    try:
        
        
        sql_delete_relation = "DELETE FROM problem_stakeholder WHERE stakeholder_id = %s"
        
        request.cursor.execute(sql_delete_relation, (stakeholder_id,))
        
        sql_delete_stakeholder = "DELETE FROM stakeholder WHERE id = %s"
        request.cursor.execute(sql_delete_stakeholder, (stakeholder_id,))
        request.db.commit()
        
        return jsonify({"message": "Stakeholder and related relations deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

        


@app.route('/save-stakeholders', methods=['POST'])
def save_stakeholders():
    try:
        data = request.json
        selected_problem = data['selectedProblem']
        selected_stakeholders = data['selectedStakeholders']

        # Inserta los registros en la tabla problem_stakeholder
        for stakeholder_id in selected_stakeholders:
            sql = "INSERT INTO problem_stakeholder (problem_id, stakeholder_id) VALUES (%s, %s)"
            request.cursor.execute(sql, (selected_problem, stakeholder_id))
        
        request.db.commit()
        
        return jsonify({"message": "Stakeholders saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/delete-stakeholder/<int:stakeholder_id>', methods=['DELETE'])
def delete_stakeholder_in_list(stakeholder_id):
    try:
        sql_delete_problem_stakeholder = "DELETE FROM problem_stakeholder WHERE stakeholder_id = %s"
        request.cursor.execute(sql_delete_problem_stakeholder, (stakeholder_id,))
        
        request.db.commit()
        
        return jsonify({"message": "Building deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/add-stakeholder/<int:stakeholder_id>', methods=['PUT'])
def update_stakeholder_list(stakeholder_id):
    try:
        stakeholder_data = request.json

        sql_insert_problem_building = """
            INSERT INTO problem_stakeholder (problem_id, stakeholder_id) 
            VALUES (%s, %s)
        """
        lab_values = (stakeholder_data['selectedProblem'], stakeholder_id)
        request.cursor.execute(sql_insert_problem_building, lab_values)

        request.db.commit()


        return jsonify({"message": "Building updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/building/<int:lab_id>', methods=['GET'])
def get_building_by_lab(lab_id):
    try:
        selectedProblem = request.args.get('selectedProblem')
        sql = """
            SELECT 
                b.*,
                CASE 
                    WHEN pb.building_id IS NOT NULL THEN true
                    ELSE false
                END AS selectedBuilding
            FROM 
                location_building gb 
            INNER JOIN 
                building b ON gb.building_id = b.id 
            LEFT JOIN 
                problem_building pb ON b.id = pb.building_id AND pb.problem_id = %s
            WHERE 
                gb.general_id = %s
            """
        request.cursor.execute(sql, (selectedProblem, lab_id))
        buildings = request.cursor.fetchall()
        return jsonify(buildings)
    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/building/<int:building_id>', methods=['PUT'])
def update_building(building_id):
    try:
        building_data = request.json
        sql = """
            UPDATE building
            SET name = %s, description = %s, address = %s
            WHERE id = %s
        """
        request.cursor.execute(sql, (
            building_data['name'],
            building_data['description'],
            building_data['address'],
            building_id
        ))
       
        request.db.commit()
        return jsonify({"message": "Building updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/building', methods=['POST'])
def manage_building():
    try:
        building_data = request.json
        sql_get_last_id = "SELECT MAX(id) FROM building"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1
        
        sql_insert_building = """
            INSERT INTO building (id, name, description, address, gps, filename, date, version) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        building_values = (
            new_id,
            building_data['name'],
            building_data['description'],
            building_data['address'],
            building_data['gps'],
            building_data['filename'],
            building_data['date'],
            building_data['version']
        )
      
        request.cursor.execute(sql_insert_building, building_values)
        
        sql_insert_general_building = """
            INSERT INTO location_building (general_id, building_id) 
            VALUES (%s, %s)
        """
        lab_values = (building_data['selectedLab'], new_id)
        request.cursor.execute(sql_insert_general_building, lab_values)
        
        sql_insert_problem_building = """
            INSERT INTO problem_building (problem_id, building_id) 
            VALUES (%s, %s)
        """
        lab_values = (building_data['selectedProblem'], new_id)
        request.cursor.execute(sql_insert_problem_building, lab_values)

        request.db.commit()
        return jsonify({"message": "Building created successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/building/<int:building_id>', methods=['DELETE'])
def delete_building(building_id):
    try:
        print(building_id)
        sql_delete_general_building = "DELETE FROM location_building WHERE building_id = %s"
        request.cursor.execute(sql_delete_general_building, (building_id,))

        sql_delete_problem_building = "DELETE FROM problem_building WHERE building_id = %s"
        request.cursor.execute(sql_delete_problem_building, (building_id,))
        
        
        sql_delete_building = "DELETE FROM building WHERE id = %s"
        request.cursor.execute(sql_delete_building, (building_id,))
        request.db.commit()
        
        return jsonify({"message": "Building deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/delete-building/<int:building_id>', methods=['DELETE'])
def delete_building_in_list(building_id):
    try:
        sql_delete_problem_building = "DELETE FROM problem_building WHERE building_id = %s"
        request.cursor.execute(sql_delete_problem_building, (building_id,))
        
        request.db.commit()
        
        return jsonify({"message": "Building deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/add-building/<int:building_id>', methods=['PUT'])
def update_building_list(building_id):
    try:
        building_data = request.json

        sql_insert_problem_building = """
            INSERT INTO problem_building (problem_id, building_id) 
            VALUES (%s, %s)
        """
        lab_values = (building_data['selectedProblem'], building_id)
        request.cursor.execute(sql_insert_problem_building, lab_values)

        request.db.commit()


        return jsonify({"message": "Building updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/output/<int:problem_id>', methods=['GET'])
def get_output(problem_id):
    try:
        sql = """
            SELECT 
                o.*
            FROM 
                problem_output po 
            INNER JOIN 
                output o ON po.output_id = o.id 
            WHERE 
                po.problem_id = %s
            """
        request.cursor.execute(sql, (problem_id,))
        outputs = request.cursor.fetchall()
        return jsonify(outputs)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/output', methods=['POST'])
def manage_output():
    try:
        output_data = request.json
        sql_get_last_id = "SELECT MAX(id) FROM output"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1

        sql_insert_output = """
            INSERT INTO output (id, name, math_relation, threshold) 
            VALUES (%s, %s, %s, %s)
        """
        output_values = (
            new_id,
            output_data['name'],
            output_data['math_relation'],
            output_data['threshold']
        )

        request.cursor.execute(sql_insert_output, output_values)

        sql_insert_problem_output = """
            INSERT INTO problem_output (problem_id, output_id) 
            VALUES (%s, %s)
        """
        problem_values = (output_data['problemId'], new_id)
        request.cursor.execute(sql_insert_problem_output, problem_values)

        request.db.commit()
        return jsonify({"message": "Output created successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/output/<int:output_id>', methods=['PUT'])
def update_output(output_id):
    try:
        output_data = request.json
        sql = """
            UPDATE output
            SET name = %s, math_relation = %s, threshold = %s
            WHERE id = %s
        """
        request.cursor.execute(sql, (
            output_data['name'],
            output_data['math_relation'],
            output_data['threshold'],
            output_id
        ))
        request.db.commit()
        return jsonify({"message": "Output updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/output/<int:output_id>', methods=['DELETE'])
def delete_output(output_id):
    try:
        sql_delete_problem_output = "DELETE FROM problem_output WHERE output_id = %s"
        request.cursor.execute(sql_delete_problem_output, (output_id,))
        request.db.commit()

        sql_delete_output = "DELETE FROM output WHERE id = %s"
        request.cursor.execute(sql_delete_output, (output_id,))
        request.db.commit()

        return jsonify({"message": "Output deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/scenario/<int:problem_id>', methods=['GET'])
def get_scenario(problem_id):
    try:
        sql = """
            SELECT 
                s.id as scenario_id,
                s.name as scenario_name,
                p.id as parameter_id,
                p.value as parameter_name,
                sp.value as scenario_value,
                sp.uncertained,
                sp.optimized
            FROM 
                problem pr
            INNER JOIN 
                problem_scenario ps ON pr.id = ps.problem_id
            INNER JOIN 
                scenario s ON ps.scenario_id = s.id
            INNER JOIN 
                scenario_parameter sp ON s.id = sp.scenario_id
            INNER JOIN 
                parameter p ON sp.parameter_id = p.id
            INNER JOIN 
                problem_parameter pp ON p.id = pp.parameter_id
            WHERE 
                pr.id = %s
                AND pp.problem_id = %s;
            """
        request.cursor.execute(sql, (problem_id, problem_id))
        results = request.cursor.fetchall()
        
        # Organizar el resultado en un JSON estructurado
        scenarios = {}
        
        for row in results:
            scenario_id = row['scenario_id']
            if scenario_id not in scenarios:
                scenarios[scenario_id] = {
                    'id_scenario': scenario_id,
                    'name_scenario': row['scenario_name'],
                    'id_parameter': [],
                    'name_parameter': [],
                    'parameter_optimized': [],
                    'parameter_uncertained': [],
                    'scenario_value': []  # Añadir nueva columna para scenario_value
                }
            
            scenarios[scenario_id]['id_parameter'].append(row['parameter_id'])
            scenarios[scenario_id]['name_parameter'].append(row['parameter_name'])
            scenarios[scenario_id]['parameter_optimized'].append(row['optimized'])
            scenarios[scenario_id]['parameter_uncertained'].append(row['uncertained'])
            scenarios[scenario_id]['scenario_value'].append(row['scenario_value'])  # Añadir valor a scenario_value
        
        # Convertir el diccionario de escenarios en una lista para el JSON
        scenario_list = list(scenarios.values())
        
        return jsonify(scenario_list)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/delete-parameter/<int:parameter_id>', methods=['DELETE'])
def delete_parameter(parameter_id):
    try:
        
        # Eliminar relaciones de scenario_parameter
        sql_delete_scenario_parameter = "DELETE FROM scenario_parameter WHERE parameter_id = %s"
        request.cursor.execute(sql_delete_scenario_parameter, (parameter_id,))
        
        # Eliminar relaciones de problem_parameter
        sql_delete_problem_parameter = "DELETE FROM problem_parameter WHERE parameter_id = %s"
        request.cursor.execute(sql_delete_problem_parameter, (parameter_id,))
        
        
        
        # Eliminar el parámetro de la tabla 'parameter'
        sql_delete_parameter = "DELETE FROM parameter WHERE id= %s"
        request.cursor.execute(sql_delete_parameter, (parameter_id,))
        
        # Commit de la transacción
        request.db.commit()
        
        return jsonify({"message": "Parameter deleted successfully"}), 200
    except Exception as e:
        request.db.rollback()  # Rollback en caso de error
        return jsonify({"error": str(e)}), 400

    
@app.route('/delete-scenario/<int:scenario_id>', methods=['DELETE'])
def delete_scenario(scenario_id):
    try:
        # Eliminar relaciones de problem_scenario
        sql_delete_problem_scenario = "DELETE FROM problem_scenario WHERE scenario_id = %s"
        request.cursor.execute(sql_delete_problem_scenario, (scenario_id,))
        
        # Eliminar relaciones de scenario_parameter
        sql_delete_scenario_parameter = "DELETE FROM scenario_parameter WHERE scenario_id = %s"
        request.cursor.execute(sql_delete_scenario_parameter, (scenario_id,))
        
        # Eliminar el escenario de la tabla 'scenario'
        sql_delete_scenario = "DELETE FROM scenario WHERE id = %s"
        request.cursor.execute(sql_delete_scenario, (scenario_id,))
        
        # Commit de la transacción
        request.db.commit()
        
        return jsonify({"message": "Scenario deleted successfully"}), 200
    except Exception as e:
        request.db.rollback()  # Rollback en caso de error
        return jsonify({"error": str(e)}), 400



@app.route('/parameter', methods=['POST'])
def create_paramater():
    try:
        data = request.json
        
        # Obtener el último id de la tabla parameter
        sql_get_last_id = "SELECT MAX(id) FROM parameter"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1

        # Primera inserción en la tabla parameter
        sql_insert_parameter = "INSERT INTO parameter (id, value) VALUES (%s, %s)"
        combined_value = f"{data['name']}_{new_id}"
        parameter_values = (new_id, combined_value)
        request.cursor.execute(sql_insert_parameter, parameter_values)
        request.db.commit()  # Asegurarse de que la primera inserción se ejecute y se confirme

        # Segunda inserción en la tabla problem_parameter
        
        sql_insert_problem_parameter = "INSERT INTO problem_parameter (problem_id, parameter_id) VALUES (%s, %s)"
        problem_parameter_values = (data['problem_id'], new_id)
        request.cursor.execute(sql_insert_problem_parameter, problem_parameter_values)

        # Tercera inserción: Verificar escenarios asociados y crear relaciones si no existen
        sql_select_scenarios = """
            SELECT s.id 
            FROM scenario s
            JOIN problem_scenario ps ON ps.scenario_id = s.id
            WHERE ps.problem_id = %s
        """
        request.cursor.execute(sql_select_scenarios, (data['problem_id'],))
        scenario_ids = [row['id'] for row in request.cursor.fetchall()]

        # Si no existen escenarios, crear uno nuevo llamado "scenario 1"
        if not scenario_ids:
            sql_insert_scenario = "INSERT INTO scenario (name) VALUES ('Scenario 1')"
  
            request.cursor.execute(sql_insert_scenario)
            
            # Obtener el ID del nuevo escenario creado
            new_scenario_id = request.cursor.lastrowid
            
            # Crear la relación problem_scenario con el nuevo escenario
            sql_insert_problem_scenario = "INSERT INTO problem_scenario (problem_id, scenario_id) VALUES (%s, %s)"
            request.cursor.execute(sql_insert_problem_scenario, (data['problem_id'], new_scenario_id))
            
            # Añadir el nuevo escenario al array de scenario_ids
            scenario_ids = [new_scenario_id]

        if scenario_ids:
            # Verificar si ya existe la relación scenario_parameter
            for scenario_id in scenario_ids:
                sql_check_scenario_parameter = """
                    SELECT COUNT(*) 
                    FROM scenario_parameter 
                    WHERE scenario_id = %s AND parameter_id = %s
                """
                request.cursor.execute(sql_check_scenario_parameter, (scenario_id, new_id))
                if request.cursor.fetchone()['COUNT(*)'] == 0:
                    # Crear la relación si no existe
                    sql_insert_scenario_parameter = "INSERT INTO scenario_parameter (scenario_id, parameter_id, value) VALUES (%s, %s,%s)"
                    request.cursor.execute(sql_insert_scenario_parameter, (scenario_id, new_id,"default_value"))
   

        request.db.commit()  # Confirmar todas las inserciones restantes que no fallaron
        return jsonify({"message": "Simulation requirement created successfully"}), 201
    
    except Exception as e:
        request.db.rollback()  # Deshacer la transacción principal si falla
        return jsonify({"error": str(e)}), 400


@app.route('/scenario', methods=['POST'])
def create_scenario():
    try:
        data = request.json
        
        # Obtener el último ID de scenario y generar el nuevo ID
        sql_get_last_id = "SELECT COALESCE(MAX(id), 0) AS max_id FROM scenario"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['max_id']
        new_id = last_id + 1
        
        # Insertar el nuevo escenario en la tabla 'scenario'
        sql_insert_scenario = """
            INSERT INTO scenario (id, name) 
            VALUES (%s, %s)
        """
        values = (new_id, data['name'])
        request.cursor.execute(sql_insert_scenario, values)
        
        # Insertar la relación en la tabla 'problem_scenario'
        sql_insert_problem_scenario = """
            INSERT INTO problem_scenario (problem_id, scenario_id) 
            VALUES (%s, %s)
        """
        values = (data['problem_id'], new_id)
        request.cursor.execute(sql_insert_problem_scenario, values)
        
        # Verificar si hay parámetros asociados al problem_id
        sql_select_parameters = """
            SELECT p.id 
            FROM parameter p
            JOIN problem_parameter pp ON pp.parameter_id = p.id
            WHERE pp.problem_id = %s
        """

        request.cursor.execute(sql_select_parameters, (data['problem_id'],))
        parameter_ids = [row['id'] for row in request.cursor.fetchall()]

        # Si no hay parámetros existentes, crear uno nuevo llamado "New Parameter"
        if not parameter_ids:
            sql_insert_parameter = """
                INSERT INTO parameter (value) 
                VALUES (%s)
            """
            request.cursor.execute(sql_insert_parameter, ("New Parameter",))
            new_parameter_id = request.cursor.lastrowid
            
            # Insertar la relación en problem_parameter
            sql_insert_problem_parameter = """
                INSERT INTO problem_parameter (problem_id, parameter_id)
                VALUES (%s, %s)
            """
            request.cursor.execute(sql_insert_problem_parameter, (data['problem_id'], new_parameter_id))
            
        
       
        # Obtener todos los IDs de los parámetros desde la tabla 'parameter'
        sql_select_parameters = "SELECT id FROM parameter"
        request.cursor.execute(sql_select_parameters)
        parameter_ids = [row['id'] for row in request.cursor.fetchall()]

        # Preparar la consulta SQL para la inserción en 'scenario_parameter'
        sql_insert_scenario_parameter = "INSERT INTO scenario_parameter (scenario_id, parameter_id) VALUES (%s, %s)"

        # Iterar sobre cada ID de parámetro y ejecutar la inserción
        for index in range(len(parameter_ids)):
            parameter_id = parameter_ids[index]
            values = (new_id, parameter_id)
            request.cursor.execute(sql_insert_scenario_parameter, values)

        # Commit de la transacción
        request.db.commit()

        return jsonify({"message": "Simulation requirement created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/scenario/<int:scenario_id>', methods=['PUT'])
def update_scenario(scenario_id):
    try:
        data = request.json
        
        # Validar que el escenario existe
        sql_check_scenario = "SELECT COUNT(*) FROM scenario WHERE id = %s"
        request.cursor.execute(sql_check_scenario, (scenario_id,))
        if request.cursor.fetchone()['COUNT(*)'] == 0:
            return jsonify({"error": "Scenario not found"}), 404

        # Actualizar el nombre del escenario
        sql_update_scenario = """
            UPDATE scenario 
            SET name = %s 
            WHERE id = %s
        """
        values = (data['name'], scenario_id)
        request.cursor.execute(sql_update_scenario, values)
        

        
        request.db.commit()
        return jsonify({"message": "Scenario updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/parameter/<int:parameter_id>', methods=['PUT'])
def update_parameter(parameter_id):
    try:
        data = request.json
        print(data)
        
        # Validar que el parámetro existe
        sql_check_parameter = "SELECT COUNT(*) FROM parameter WHERE id = %s"
        request.cursor.execute(sql_check_parameter, (parameter_id,))
        if request.cursor.fetchone()['COUNT(*)'] == 0:
            return jsonify({"error": "Parameter not found"}), 404

        # Validar que los campos 'name' y 'problem_id' están presentes
        if 'name' not in data or 'problem_id' not in data:
            return jsonify({"error": "Missing required fields 'name' or 'problem_id'"}), 400

        # Actualizar el nombre y el problem_id del parámetro
        sql_update_parameter = "UPDATE parameter SET value = %s WHERE id = %s"
        values = (data['name'], parameter_id)
        request.cursor.execute(sql_update_parameter, values)
        
        # Si 'value' y 'scenario_id' están presentes, actualizar también la tabla scenario_parameter
        if 'value' in data and 'scenario_id' in data:
            sql_update_scenario_parameter = """
                UPDATE scenario_parameter 
                SET value = %s
                WHERE scenario_id = %s AND parameter_id = %s
            """
            values = (data['value'], data['scenario_id'], parameter_id)
            request.cursor.execute(sql_update_scenario_parameter, values)
        
        request.db.commit()
        return jsonify({"message": "Parameter updated successfully"}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

    

@app.route('/save-table', methods=['POST'])
def save_table():
    
    try:
        data = request.json
        problem_id = data.get('problem_id')
        scenarios = data.get('scenarios', [])

        # Delete existing scenario_parameters for the given problem_id
        sql_delete_scenario_parameters = """
            DELETE sp FROM scenario_parameter sp
            INNER JOIN scenario s ON sp.scenario_id = s.id
            WHERE s.id IN (
                SELECT id FROM scenario WHERE id IN (
                    SELECT scenario_id FROM problem_scenario WHERE problem_id = %s
                )
            )
        """
        request.cursor.execute(sql_delete_scenario_parameters, (problem_id,))

        sql_delete_problem_scenario = """
            DELETE FROM problem_scenario WHERE problem_id = %s
        """
        request.cursor.execute(sql_delete_problem_scenario, (problem_id,))

        # 3. Eliminar los registros de la tabla scenario
        sql_delete_scenarios = """
            DELETE FROM scenario WHERE id IN (
                SELECT scenario_id FROM problem_scenario WHERE problem_id = %s
            )
        """
        request.cursor.execute(sql_delete_scenarios, (problem_id,))

        # 4. Eliminar los registros de la tabla problem_parameter
        sql_delete_problem_parameter = """
            DELETE FROM problem_parameter WHERE problem_id = %s
        """
        request.cursor.execute(sql_delete_problem_parameter, (problem_id,))

        # 5. Eliminar los registros de la tabla parameter
        sql_delete_parameters = """
            DELETE FROM parameter WHERE id IN (
                SELECT parameter_id FROM problem_parameter WHERE problem_id = %s
            )
        """
        request.cursor.execute(sql_delete_parameters, (problem_id,))

         # 6. Eliminar parámetros que no están asociados a ningún problema
        sql_delete_orphan_parameters = """
            DELETE FROM parameter WHERE id NOT IN (
                SELECT parameter_id FROM problem_parameter
            )
        """
        request.cursor.execute(sql_delete_orphan_parameters)

        # 7. Eliminar scenarios que no están asociados a ningún problema
        sql_delete_orphan_scenarios = """
            DELETE FROM scenario WHERE id NOT IN (
                SELECT scenario_id FROM problem_scenario
            )
        """
        request.cursor.execute(sql_delete_orphan_scenarios)



        

        # Start transaction
        request.cursor.execute("BEGIN")

        # Insert scenarios and their parameters
        for scenario in scenarios:
            scenario_id = scenario['id_scenario']
            scenario_name = scenario['name_scenario']

            if scenario_id.startswith('temp_'):
                # Insert new scenario
                sql_insert_scenario = """
                    INSERT INTO scenario (name) VALUES (%s)
                """
                request.cursor.execute(sql_insert_scenario, (scenario_name,))
                scenario_id = request.cursor.lastrowid
                scenario['id_scenario'] = scenario_id

                # Insert into problem_scenario
                sql_insert_problem_scenario = """
                    INSERT INTO problem_scenario (problem_id, scenario_id) VALUES (%s, %s)
                """
                request.cursor.execute(sql_insert_problem_scenario, (problem_id, scenario_id))

            # Insert parameters for the scenario
            for parameter in scenario['parameters']:
                parameter_id = None
                parameter_name = parameter['name']
                parameter_value = parameter['value']

                # Check if parameter already exists
                sql_check_parameter = """
                    SELECT id FROM parameter WHERE value = %s
                """
                request.cursor.execute(sql_check_parameter, (parameter_name,))
                existing_parameter = request.cursor.fetchone()

                if existing_parameter:
                    parameter_id = existing_parameter['id']
                else:
                    # Insert new parameter
                    sql_insert_parameter = """
                        INSERT INTO parameter (value) VALUES (%s)
                    """
                    request.cursor.execute(sql_insert_parameter, (parameter_name,))
                    parameter_id = request.cursor.lastrowid

                    # Insert into problem_parameter
                    sql_insert_problem_parameter = """
                        INSERT INTO problem_parameter (problem_id, parameter_id) VALUES (%s, %s)
                    """
                    request.cursor.execute(sql_insert_problem_parameter, (problem_id, parameter_id))

                # Insert into scenario_parameter
                sql_insert_scenario_parameter = """
                    INSERT INTO scenario_parameter (scenario_id, parameter_id, value) VALUES (%s, %s, %s)
                """
                request.cursor.execute(sql_insert_scenario_parameter, (scenario_id, parameter_id, parameter_value))

        # Commit transaction
        request.db.commit()

        return jsonify({"message": "Table saved successfully"}), 200
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 400






@app.route('/problem', methods=['GET'])
def get_problems():
    sql = "SELECT * FROM problem"
    request.cursor.execute(sql)
    problems = request.cursor.fetchall()
    return jsonify(problems)

@app.route('/problem_data', methods=['POST'])
def get_problem_data():
    problem_id = request.json.get('problemId')
    sql = "SELECT * FROM problem WHERE id = %s"
    request.cursor.execute(sql, (problem_id,))
    problem_info = request.cursor.fetchone()
    return jsonify(problem_info)

@app.route('/problem', methods=['POST'])
def create_problem():
    try:
                
        sql_get_last_id = "SELECT MAX(id) FROM problem"
        request.cursor.execute(sql_get_last_id)
        last_id = request.cursor.fetchone()['MAX(id)'] or 0
        new_id = last_id + 1

        # Crear un nuevo problema
        sql_insert_problem = """INSERT INTO problem (id, need) VALUES (%s,'New Problem')"""
        request.cursor.execute(sql_insert_problem, (new_id,))
  

        
        request.db.commit()
        
        return jsonify({"message": "Problem created successfully", "problemId": new_id})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/problem/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    try:
        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations = "DELETE FROM problem_stakeholder WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations, (problem_id,))

        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations_1 = "DELETE FROM problem_building WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations_1, (problem_id,))

        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations_2 = "DELETE FROM problem_kpi WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations_2, (problem_id,))

        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations_3 = "DELETE FROM problem_objective WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations_3, (problem_id,))

        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations_4 = "DELETE FROM problem_parameter WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations_4, (problem_id,))

        # Eliminar relaciones en problem_stakeholder
        sql_delete_stakeholder_relations_5 = "DELETE FROM problem_scenario WHERE problem_id = %s"
        request.cursor.execute(sql_delete_stakeholder_relations_5, (problem_id,))        




        # Eliminar el problema
        sql_delete_problem = "DELETE FROM problem WHERE id = %s"
        request.cursor.execute(sql_delete_problem, (problem_id,))

        request.db.commit()
        return jsonify({"message": "Problem deleted successfully"})
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)})


@app.route('/need/<int:problem_id>', methods=['GET'])
def get_need(problem_id):
    print(problem_id, "problem_id")
    try:
        sql = """
            SELECT 
                p.*, 
                GROUP_CONCAT(o.description SEPARATOR ', ') AS objectives
            FROM 
                problem p
            LEFT JOIN 
                problem_objective po ON p.id = po.problem_id
            LEFT JOIN 
                objective o ON po.objective_id = o.id
            WHERE
                p.id = %s
            GROUP BY 
                p.id
            """
        request.cursor.execute(sql, (problem_id,))
        outputs = request.cursor.fetchall()
        if not outputs:
            return jsonify({"message": "No problem found with the given ID"}), 404
        return jsonify(outputs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/need/<int:problem_id>', methods=['PUT'])
def update_need(problem_id):
    try:
        data = request.get_json()

        # Actualiza la tabla 'problem'
        sql_update_problem = """
            UPDATE problem 
            SET  
                accepted_risk = %s 
            WHERE 
                id = %s
        """
        request.cursor.execute(sql_update_problem, (
            data['accepted_risk'],
            problem_id
        ))

        
        # Confirma la transacción
        request.db.commit()
        print("Need updated successfully")
        return jsonify({"message": "Problem updated successfully"}), 200
    except Exception as e:
        request.db.rollback()
        print("Error occurred:", str(e))  # Añade un print para depurar el error
        return jsonify({"error": str(e)}), 500

@app.route('/update_need/<int:problem_id>', methods=['PUT'])
def update_need_field(problem_id):
    try:
        data = request.get_json()
        need = data.get('need')

        # Verifica que el campo need no esté vacío
        if not need:
            return jsonify({"error": "The 'need' field is required"}), 400

        # Actualiza la tabla 'problem'
        sql_update_need = """
            UPDATE problem 
            SET 
                need = %s
            WHERE 
                id = %s
        """
        request.cursor.execute(sql_update_need, (
            need,
            problem_id
        ))

        # Confirma la transacción
        request.db.commit()
        print("Need updated successfully")
        return jsonify({"message": "Need updated successfully"}), 200
    except Exception as e:
        request.db.rollback()
        print("Error occurred:", str(e))  # Añade un print para depurar el error
        return jsonify({"error": str(e)}), 500

@app.route('/objective', methods=['GET'])
def get_objectives():
    sql = "SELECT * FROM objective"
    request.cursor.execute(sql)
    problems = request.cursor.fetchall()
    return jsonify(problems)

@app.route('/attribute', methods=['GET'])
def get_attributs():
    sql = "SELECT * FROM attribute"
    request.cursor.execute(sql)
    problems = request.cursor.fetchall()
    return jsonify(problems)

@app.route('/test/<int:selectedProblem>', methods=['GET'])
def get_simulations(selectedProblem):
    try:
        sql = """
            SELECT 
                sr.id, 
                sr.text, 
                a.name AS attribute,
                sr.problem_id
            FROM 
                testrequirements sr
            JOIN 
                attribute a ON sr.attribute_id = a.id
            WHERE 
                sr.problem_id = %s
        """
        request.cursor.execute(sql, (selectedProblem,))
        simulations = request.cursor.fetchall()
        return jsonify(simulations)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/test', methods=['POST'])
def create_simulation():
    try:
        data = request.json
        sql = """
            INSERT INTO testrequirements (attribute_id, text, problem_id) 
            VALUES (%s, %s, %s)
        """
        values = (data['attribute_id'], data['text'], data['problem_id'])
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/test/<int:requirement_id>', methods=['PUT'])
def update_simulation(requirement_id):
    try:
        data = request.json
        sql = """
            UPDATE testrequirements 
            SET text = %s 
            WHERE id = %s
        """
        values = (data['text'], requirement_id)
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/test/<int:requirement_id>', methods=['DELETE'])
def delete_simulation(requirement_id):
    try:
        sql = "DELETE FROM testrequirements WHERE id = %s"
        request.cursor.execute(sql, (requirement_id,))
        request.db.commit()
        return jsonify({"message": "Simulation requirement deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/modeling/<int:selectedProblem>', methods=['GET'])
def get_modelingchoices(selectedProblem):
    try:
        sql = """
            SELECT* FROM modelchoice        
            WHERE 
                problem_id = %s
        """
        request.cursor.execute(sql, (selectedProblem,))
        simulations = request.cursor.fetchall()
        return jsonify(simulations)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/modeling', methods=['POST'])
def create_modelingchoices():
    try:
        data = request.json
        sql = """
            INSERT INTO modelchoice (text, problem_id) 
            VALUES (%s, %s)
        """
        values = (data['text'], data['problem_id'])
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/modeling/<int:choice_id>', methods=['PUT'])
def update_modelingchoices(choice_id):
    try:
        data = request.json
        sql = """
            UPDATE modelchoice 
            SET text = %s 
            WHERE id = %s
        """
        values = (data['text'], choice_id)
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/modeling/<int:choice_id>', methods=['DELETE'])
def delete_modelingchoices(choice_id):
    try:
        sql = "DELETE FROM modelchoice WHERE id = %s"
        request.cursor.execute(sql, (choice_id,))
        request.db.commit()
        return jsonify({"message": "Simulation requirement deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/verification/<int:selectedProblem>', methods=['GET'])
def get_verifications(selectedProblem):
    try:
        sql = """
            SELECT* FROM verification        
            WHERE 
                id_problem = %s
        """
        request.cursor.execute(sql, (selectedProblem,))
        simulations = request.cursor.fetchall()
        return jsonify(simulations)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/verification', methods=['POST'])
def create_verification():
    try:
        data = request.json
        sql = """
            INSERT INTO verification (aspect, note, date, id_problem) 
            VALUES (%s, %s, %s, %s)
        """
        values = (data['aspect'], data['note'], data['date'], data['problem_id'])
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/verification/<int:verification_id>', methods=['PUT'])
def update_verification(verification_id):
    try:
        data = request.json
        sql = """
            UPDATE verification
            SET aspect = %s, note = %s, date = %s 
            WHERE id = %s
        """
        values = (data['aspect'], data['note'], data['date'], verification_id)
        request.cursor.execute(sql, values)
        request.db.commit()
        return jsonify({"message": "Simulation requirement updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/verification/<int:verification_id>', methods=['DELETE'])
def delete_verification(verification_id):
    try:
        sql = "DELETE FROM verification WHERE id = %s"
        request.cursor.execute(sql, (verification_id,))
        request.db.commit()
        return jsonify({"message": "Simulation requirement deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download-db-structure/<int:problem_id>', methods=['GET'])
def download_db_structure(problem_id):
    try:
        # Configurar el cursor para devolver diccionarios
        request.cursor = request.db.cursor(dictionary=True)

        # Crear la estructura base del JSON
        db_structure = {}

        # Obtener información principal del problema
        sql = """SELECT id, need AS decision, accepted_risk
                 FROM problem
                 WHERE id = %s"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        problem = request.cursor.fetchone()  # Cambié a fetchone para obtener un solo resultado
        if not problem:
            return jsonify({"error": "Problem not found"}), 404
        db_structure['problem'] = problem

        # Obtener la ubicación
        sql = """SELECT *
                 FROM location
                 WHERE id = (SELECT context_id FROM problem WHERE id = %s)"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        location = request.cursor.fetchone()  # Cambié a fetchone para obtener un solo resultado
        if location:
            db_structure['location'] = location

        # Obtener los edificios
        sql = """SELECT building.id, building.name, building.description, building.filename, 
                        building.lifecycle_id, lifecycle.name AS lifecycle
                 FROM building
                 LEFT JOIN lifecycle ON building.lifecycle_id = lifecycle.id
                 WHERE building.id IN (SELECT building_id FROM problem_building WHERE problem_id = %s)"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        buildings = request.cursor.fetchall()
        db_structure['buildings'] = buildings if buildings else []

        # Obtener los stakeholders
        sql = """SELECT id, general_description AS description, requirements
                 FROM stakeholder
                 WHERE stakeholder.id IN (SELECT stakeholder_id FROM problem_stakeholder WHERE problem_id = %s)"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        stakeholders = request.cursor.fetchall()
        db_structure['stakeholders'] = stakeholders if stakeholders else []

        # Obtener los KPIs 
        sql = """SELECT kpi.id, kpi.name, kpi.unit AS unit, kpi.description, kpi.baseLineDataNeeded, 
                kpi.dataRequirements AS dataRequirements, kpi.formula, kpi.impact, 
                kpi.pillar AS pillar, kpi.responsibilityDefinition AS responsibilityDefinition, 
                kpi.responsibilityCalculation AS responsibilityCalculation
         FROM kpi
         WHERE kpi.id IN (SELECT kpi_id FROM problem_kpi WHERE problem_id = %s)"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        kpis = request.cursor.fetchall()
        db_structure['kpis'] = kpis if kpis else []

        for kpi in kpis:
            sql = """SELECT *
                     FROM lifecycle
                     WHERE id IN (SELECT lifecycle_id FROM kpi_lifecycle WHERE kpi_id = %s)"""
            params = (kpi['id'],)
            request.cursor.execute(sql, params)
            lifecycle = request.cursor.fetchall()
            kpi['lifecycle'] = lifecycle if lifecycle else []
        
        # Obtener los escenarios
        sql = """SELECT *
                 FROM scenario
                 WHERE id IN (SELECT scenario_id FROM problem_scenario WHERE problem_id = %s)"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        scenarios = request.cursor.fetchall()
        db_structure['scenarios'] = scenarios if scenarios else []

        if scenarios:
            df_scenarios = pd.DataFrame(scenarios)
            df_scenarios.set_index('id', inplace=True)

            # Obtener los parámetros de los escenarios
            sql = """SELECT scenario_parameter.scenario_id, parameter.value AS parameter, scenario_parameter.value
                     FROM scenario_parameter
                     INNER JOIN parameter ON scenario_parameter.parameter_id = parameter.id
                     WHERE scenario_id IN (SELECT scenario_id FROM problem_scenario WHERE problem_id = %s)
                     AND parameter_id IN (SELECT parameter_id FROM problem_parameter WHERE problem_id = %s)"""
            params = (problem_id, problem_id)
            request.cursor.execute(sql, params)
            parameters = request.cursor.fetchall()

            if parameters:
                df_parameters = pd.DataFrame(parameters)
                df_parameters = df_parameters.pivot(index='parameter', columns='scenario_id')

                summary_scenarios = ""

                for (columnName, columnValues) in df_parameters.items():
                    text_scenario = '#' + str(columnName[1]) + ' ' + df_scenarios.loc[columnName[1]]['name']
                    table_parameters = df_parameters.index.values + ' = ' + columnValues.values
                    text_parameters = '\n'.join(table_parameters)
                    summary_scenarios += text_scenario + '\n' + text_parameters + '\n'

                db_structure['scenarios_summary'] = summary_scenarios 

        # Obtener los requerimientos de datos
        sql = """SELECT testrequirements.id, attribute.name AS attribute, 
                        testrequirements.attribute_id AS attribute_id, testrequirements.text AS requirement
                 FROM testrequirements
                 LEFT JOIN attribute ON testrequirements.attribute_id = attribute.id
                 WHERE problem_id = %s"""
        params = (problem_id,)
        request.cursor.execute(sql, params)
        dataRequirements = request.cursor.fetchall()
        db_structure['dataRequirements'] = dataRequirements if dataRequirements else []

        return jsonify(db_structure)

    except Exception as e:
        return jsonify({"error": str(e)}), 400




if __name__ == '__main__':
    app.run(debug=True)


 
 