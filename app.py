# Importations et Configuration Initiale
import logging
from flask import Flask, jsonify, request      #retourner des réponses JSON
from models import Database
import os      #Pour accéder aux variables d'environnement
from bson.objectid import ObjectId    #Pour manipuler des identifiants MongoDB
from dotenv import load_dotenv    #Charge les variables d'environnement depuis un fichier .env
from datetime import datetime     #Pour manipuler les dates et heures
load_dotenv()
# Configuration du logging
logging.basicConfig(
    filename='api.log',  # Le fichier où les logs seront stockés
    level=logging.DEBUG,  # Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Format des messages de log
)
app = Flask(__name__)
db = Database()    #Instancie la connexion à la base de données à l'aide de la classe Database

VALID_STATUSES = ["à faire", "en cours", "terminé"] # Définit les statuts valides pour une tâche dans une liste

# endpoint de cration d'une tache
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() #recuperation des données json envoyé avec le requete

    # Validation des champs d'une tache
    if not isinstance(data.get('title'), str):
        logging.error("Titre invalide pour la tâche : %s", data.get('title'))
        return jsonify({"error": "le titre est invalide"}), 400
    if not isinstance(data.get('description'), str):
        logging.error("ddescription invalide pour la tâche : %s", data.get('title'))
        return jsonify({"error": "La description est invalide"}), 400
    try:
        assigned_to = ObjectId(data.get('assigned_to'))
    except Exception as e:
        return jsonify({"error": "L'ID utilisateur assigné est invalide"}), 400
    if data.get('status') not in VALID_STATUSES:
        logging.error("status invalide pour la tâche : %s", data.get('title'))
        return jsonify({"error": "Statut invalide. Les statuts valides sont 'à faire', 'en cours', ou 'terminé'"}), 400

    try:
        due_date = datetime.strptime(data.get('due_date'), "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "La date limite doit être au format YYYY-MM-DD"}), 400
    # Creation d'une tache  à insérer dans la base de données
    task = {
        "title": data.get('title'),
        "description": data.get('description'),
        "assigned_to": assigned_to,
        "status": data.get('status'),
        "due_date": due_date
    }

    #insertion d'une tache et retourne un message  de success
    task_id = db.tasks.insert_one(task).inserted_id
    return jsonify(
        {
            "msg": "task suceffull", 
            "task_id": str(task_id)
        }
    ), 201


# Endpoint pour modifier une tâche existante
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        task = db.tasks.find_one({"_id": ObjectId(task_id)})
        if not task:
            return jsonify(
                {"error": "Tâche non trouvée"}
            ), 404

        update_data = {}

        # Validation et mise à jour des champs
        if 'title' in data and isinstance(data.get('title'), str):
            update_data['title'] = data.get('title')

        if 'description' in data and isinstance(data.get('description'), str):
            update_data['description'] = data.get('description')

        if 'status' in data and data.get('status') in VALID_STATUSES:
            update_data['status'] = data.get('status')

        if 'due_date' in data:
            try:
                update_data['due_date'] = datetime.strptime(data.get('due_date'), "%Y-%m-%d")
            except ValueError:
                return jsonify(
                    {"error": "La date limite doit être au format YYYY-MM-DD"}
                ), 400
        db.tasks.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_data}
        )
        return jsonify(
            {"msg": "Task update succeful"}
        ), 200

    except:
        return jsonify(
            {"error": "Tasks invalid"}
        ), 400

#  endpoint de suppression d'une tâche
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        result = db.tasks.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Tâche non trouvée"}), 404
        return jsonify({"msg": "Task deleted successfully"}), 204

    except Exception as e:
        logging.error("Erreur lors de la suppression de la tâche : %s", str(e))
        return jsonify({"error": "Erreur lors de la suppression de la tâche"}), 400
#Récupérer les tâches d'un utilisateur a partir de son id
@app.route('/tasks/user/<user_id>', methods=['GET'])
def get_user_tasks(user_id):
    tasks = db.get_tasks_by_user(user_id)  
    for task in tasks:
        task['_id'] = str(task['_id'])
        task['assigned_to'] = str(task['assigned_to'])
    return jsonify(tasks), 200
# mise à jour d'une tache
@app.route('/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    status_data = request.json.get('status')
    
    # Vérifie si le statut a été fourni
    if not status_data:
        return jsonify({'error': 'Status is required'}), 400

    # Vérifie si le statut est valide
    if status_data not in VALID_STATUSES:
        return jsonify({'error': f'Status must be one of {VALID_STATUSES}'}), 400

    try:
        result = db.tasks.update_one(  
                                     
            {'_id': ObjectId(task_id)}, 
            {'$set': {'status': status_data}}
        )

        if result.matched_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({"msg": "Task status updated successfully"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
