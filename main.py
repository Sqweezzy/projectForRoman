from sqlalchemy import null, text
from database.database import start_db, orm_db
from flask import Flask, jsonify, request, json
from database.models import User, Client, Freelancer, Category, Tasks, Transactions

CACHE = dict()


app = Flask(__name__)

@app.route('/')
def home():
    return "Выполнил Брюшинкин Роман"

#-------------------------------------------USERS---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    data = CACHE.get('all_users')
    if data is None:
        data = orm_db.session.query(User).all()
        if data == []:
            return jsonify({'error': 'No users found'})
        CACHE['all_users'] = data
    return jsonify({'result': [[f'id - {user.id}', f'username - {user.username}',
                                f'email - {user.email}', f'first_name - {user.first_name}', f'last_name - {user.last_name}',
                                f'bio - {user.bio}', f'rating - {user.rating}', f'balance - {user.balance}',
                                f'is_client - {user.is_client}', f'is_freelancer - {user.is_freelancer}',
                                f'is_verified - {user.is_verified}', f'created_at - {user.created_at}',
                                f'updated_at - {user.updated_at}'] for user in data]})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = orm_db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'result': {'id': user.id, 'username': user.username, 'email': user.email,
                               'first_name': user.first_name, 'last_name': user.last_name, 'bio': user.bio,
                               'rating': user.rating, 'balance': user.balance, 'is_client': user.is_client,
                               'is_freelancer': user.is_freelancer, 'is_verified': user.is_verified,
                               'created_at': user.created_at, 'updated_at': user.updated_at}}), 200

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    required_fields = ['username', 'email', 'password']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        user = User(**data)
        orm_db.session.add(user)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_users'] = None
    return jsonify({'message': 'User created successfully',
                    'data': data}), 201

@app.route('/api/v1/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    user = orm_db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    for key, value in data.items():
        setattr(user, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_users'] = None
    return jsonify({'message': 'User updated successfully',
                    'data': data}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = orm_db.session.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        orm_db.session.delete(user)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_users'] = None
    return jsonify({'message': 'User deleted successfully'}), 200

#-------------------------------------------------------Client---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/clients', methods=['GET'])
def get_clients():
    data = CACHE.get('all_clients')
    if data is None:
        data = orm_db.session.query(Client).all()
        if data == []:
            return jsonify({'error': 'No clients found'})
        CACHE['all_clients'] = data
    return jsonify({'result': [[f'id - {client.id}', f'user_id - {client.user_id}',
                                f'projects_posted - {client.projects_posted}', f'succes_rate - {client.succes_rate}',
                                f'hires_count - {client.hires_count}', f'active_projects - {client.active_projects}',
                                f'status - {client.status}'] for client in data]})

@app.route('/api/v1/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = orm_db.session.query(Client).filter(Client.id == client_id).first()
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({'result': {'id': client.id, 'user_id': client.user_id, 'projects_posted': client.projects_posted,
                               'succes_rate': client.succes_rate, 'hires_count': client.hires_count,
                               'active_projects': client.active_projects, 'status': client.status}}), 200

@app.route('/api/v1/clients', methods=['POST'])
def create_client():
    required_fields = ['user_id']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        client = Client(**data)
        orm_db.session.add(client)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_clients'] = None
    return jsonify({'message': 'Client created successfully',
                    'data': data}), 201

@app.route('/api/v1/clients/<int:client_id>', methods=['PATCH'])
def update_client(client_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    client = orm_db.session.query(Client).filter(Client.id == client_id).first()
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    for key, value in data.items():
        setattr(client, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_clients'] = None
    return jsonify({'message': 'Client updated successfully',
                    'data': data}), 200

@app.route('/api/v1/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = orm_db.session.query(Client).filter(Client.id == client_id).first()
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    try:
        orm_db.session.delete(client)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_clients'] = None
    return jsonify({'message': 'Client deleted successfully'}), 200

#-------------------------------------------------------Freelancer---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/freelancers', methods=['GET'])
def get_freelancers():
    data = CACHE.get('all_freelancers')
    if data is None:
        data = orm_db.session.query(Freelancer).all()
        if data == []:
            return jsonify({'error': 'No freelancers found'})
        CACHE['all_freelancers'] = data
    return jsonify({'result': [[f'id - {freelancer.id}', f'user_id - {freelancer.user_id}',
                                f'succes_rate - {freelancer.succes_rate}', f'completed_projects - {freelancer.completed_projects}',
                                f'reviews_count - {freelancer.reviews_count}', f'status - {freelancer.status}'] for freelancer in data]})
    
@app.route('/api/v1/freelancers/<int:freelancer_id>', methods=['GET'])
def get_freelancer(freelancer_id):
    freelancer = orm_db.session.query(Freelancer).filter(Freelancer.id == freelancer_id).first()
    if not freelancer:
        return jsonify({'error': 'Freelancer not found'}), 404
    return jsonify({'result': {'id': freelancer.id, 'user_id': freelancer.user_id, 'succes_rate': freelancer.succes_rate,
                               'completed_projects': freelancer.completed_projects, 'reviews_count': freelancer.reviews_count,
                               'status': freelancer.status}}), 200

@app.route('/api/v1/freelancers', methods=['POST'])
def create_freelancer():
    required_fields = ['user_id']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        freelancer = Freelancer(**data)
        orm_db.session.add(freelancer)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_freelancers'] = None
    return jsonify({'message': 'Freelancer created successfully',
                    'data': data}), 201

@app.route('/api/v1/freelancers/<int:freelancer_id>', methods=['PATCH'])
def update_freelancer(freelancer_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    freelancer = orm_db.session.query(Freelancer).filter(Freelancer.id == freelancer_id).first()
    if not freelancer:
        return jsonify({'error': 'Freelancer not found'}), 404
    for key, value in data.items():
        setattr(freelancer, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_freelancers'] = None
    return jsonify({'message': 'Freelancer updated successfully',
                    'data': data}), 200

@app.route('/api/v1/freelancers/<int:freelancer_id>', methods=['DELETE'])
def delete_freelancer(freelancer_id):
    freelancer = orm_db.session.query(Freelancer).filter(Freelancer.id == freelancer_id).first()
    if not freelancer:
        return jsonify({'error': 'Freelancer not found'}), 404
    try:
        orm_db.session.delete(freelancer)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_freelancers'] = None
    return jsonify({'message': 'Freelancer deleted successfully'}), 200

#--------------------------------------------------------Category---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    data = CACHE.get('all_categories')
    if data is None:
        data = orm_db.session.query(Category).all()
        if data == []:
            return jsonify({'error': 'No categories found'})
        CACHE['all_categories'] = data
    return jsonify({'result': [[f'id - {category.id}', f'name - {category.name}',
                                f'tasks_count - {category.tasks_count}'] for category in data]})

@app.route('/api/v1/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = orm_db.session.query(Category).filter(Category.id == category_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({'result': {'id': category.id, 'name': category.name, 'tasks_count': category.tasks_count}}), 200

@app.route('/api/v1/categories', methods=['POST'])
def create_category():
    required_fields = ['name']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        category = Category(**data)
        orm_db.session.add(category)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_categories'] = None
    return jsonify({'message': 'Category created successfully',
                    'data': data}), 201

@app.route('/api/v1/categories/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    category = orm_db.session.query(Category).filter(Category.id == category_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    for key, value in data.items():
        setattr(category, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_categories'] = None
    return jsonify({'message': 'Category updated successfully',
                    'data': data}), 200

@app.route('/api/v1/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = orm_db.session.query(Category).filter(Category.id == category_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    try:
        orm_db.session.delete(category)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_categories'] = None
    return jsonify({'message': 'Category deleted successfully'}), 200

#---------------------------------------------------------Tasks---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    data = CACHE.get('all_tasks')
    if data is None:
        data = orm_db.session.query(Tasks).all()
        if data == []:
            return jsonify({'error': 'No tasks found'})
        CACHE['all_tasks'] = data
    return jsonify({'result': [[f'id - {task.id}', f'client_id - {task.client_id}',
                                f'freelancer_id - {task.freelancer_id}', f'category_id - {task.category_id}', f'title - {task.title}',
                                f'full_text - {task.full_text}', f'price_min - {task.price_min}',
                                f'price_max - {task.price_max}', f'deadline - {task.deadline}',
                                f'status - {task.status}', f'created_at - {task.created_at}', f'updated_at - {task.updated_at}',
                                f'published_at - {task.published_at}'] for task in data]})

@app.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = orm_db.session.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'result': {'id': task.id, 'client_id': task.client_id, 'freelancer_id': task.freelancer_id,
                               'category_id': task.category_id, 'title': task.title, 'full_text': task.full_text,
                               'price_min': task.price_min, 'price_max': task.price_max, 'deadline': task.deadline,
                               'status': task.status, 'created_at': task.created_at, 'updated_at': task.updated_at,
                               'published_at': task.published_at}}), 200

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    required_fields = ['client_id', 'category_id', 'title', 'full_text', 'price_min', 'price_max', 'deadline']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        task = Tasks(**data)
        orm_db.session.add(task)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_tasks'] = None
    return jsonify({'message': 'Task created successfully',
                    'data': data}), 201

@app.route('/api/v1/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    task = orm_db.session.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    for key, value in data.items():
        setattr(task, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_tasks'] = None
    return jsonify({'message': 'Task updated successfully',
                    'data': data}), 200

@app.route('/api/v1/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = orm_db.session.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    try:
        orm_db.session.delete(task)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_tasks'] = None
    return jsonify({'message': 'Task deleted successfully'}), 200

#---------------------------------------------------------Transactions---------------------------------------------------------------------------------------------------------

@app.route('/api/v1/transactions', methods=['GET'])
def get_transactions():
    data = CACHE.get('all_transactions')
    if data is None:
        data = orm_db.session.query(Transactions).all()
        if data == []:
            return jsonify({'error': 'No transactions found'})
        CACHE['all_transactions'] = data
    return jsonify({'result': [[f'id - {transaction.id}', f'user_id - {transaction.user_id}', f'related_user_id - {transaction.related_user_id}',
                                f'transaction_type - {transaction.transaction_type}',
                                f'processed_at - {transaction.processed_at}', f'amount - {transaction.amount}',
                                f'description - {transaction.description}'] for transaction in data]})

@app.route('/api/v1/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = orm_db.session.query(Transactions).filter(Transactions.id == transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify({'result': {'id': transaction.id, 'user_id': transaction.user_id,
                               'related_user_id': transaction.related_user_id, 'transaction_type': transaction.transaction_type,
                               'processed_at': transaction.processed_at, 'amount': transaction.amount,
                               'description': transaction.description}}), 200

@app.route('/api/v1/transactions', methods=['POST'])
def create_transaction():
    required_fields = ['user_id', 'transaction_type', 'amount']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        transaction = Transactions(**data)
        orm_db.session.add(transaction)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_transactions'] = None
    return jsonify({'message': 'Transaction created successfully',
                    'data': data}), 201

@app.route('/api/v1/transactions/<int:transaction_id>', methods=['PATCH'])
def update_transaction(transaction_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    transaction = orm_db.session.query(Transactions).filter(Transactions.id == transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    for key, value in data.items():
        setattr(transaction, key, value)
    try:
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_transactions'] = None
    return jsonify({'message': 'Transaction updated successfully',
                    'data': data}), 200
    
@app.route('/api/v1/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = orm_db.session.query(Transactions).filter(Transactions.id == transaction_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    try:
        orm_db.session.delete(transaction)
        orm_db.commit_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    CACHE['all_transactions'] = None
    return jsonify({'message': 'Transaction deleted successfully'}), 200

if __name__ == '__main__':
    if False: # Чтобы зарестарить бд - заменить на True
        start_db.reset_db()
    else:
        start_db.init_db()
    app.run(debug=True) 
