from flask import jsonify, request, render_template
from src.models.student import Student
from src.config.db import SessionLocal
from flasgger import Swagger


def init_api_routes(app):
    swagger = Swagger(app)


    @app.route('/api/students', methods=['GET'])
    def get_students():
        """
        Obtener todos los estudiantes.

        ---
        responses:
          200:
            description: Una lista de estudiantes.
            schema:
              id: Estudiantes
              properties:
                students:
                  type: array
                  items:
                    $ref: '#/definitions/Student'
          404:
            description: No se encontraron estudiantes.
        """
        session = SessionLocal()
        students = session.query(Student).all()
        session.close()
        return jsonify([student.serialize() for student in students])

    @app.route('/api/students/<int:student_id>', methods=['GET'])
    def get_student_by_id(student_id):
        """
        Obtener un estudiante por ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID del estudiante a recuperar
            required: true
            type: integer
        responses:
          200:
            description: Estudiante encontrado.
            schema:
              $ref: '#/definitions/Student'
          404:
            description: Estudiante no encontrado.
        """
        session = SessionLocal()
        student = session.query(Student).filter_by(id=student_id).first()
        session.close()
        if student:
            return jsonify(student.serialize())
        else:
            return jsonify({"error": "Student not found"}), 404

    @app.route('/api/students', methods=['POST'])
    def add_student():
        """
        Agregar un nuevo estudiante.

        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Estudiante
              required:
                - name
                - age
                - spec
              properties:
                name:
                  type: string
                  description: Nombre del estudiante.
                age:
                  type: integer
                  description: Edad del estudiante.
                spec:
                  type: string
                  description: Especialización del estudiante.

        responses:
          201:
            description: Estudiante agregado exitosamente.
          400:
            description: Datos incompletos proporcionados.
        """
        data = request.json
        name = data.get('name')
        age = data.get('age')
        spec = data.get('spec')
        if name and age and spec:
            new_student = Student(name=name, age=age, spec=spec)
            session = SessionLocal()
            session.add(new_student)
            session.commit()
            session.close()
            return jsonify({"message": "Student added successfully"}), 201
        else:
            return jsonify({"error": "Incomplete data"}), 400

    @app.route('/api/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        """
        Actualizar un estudiante por ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID del estudiante a actualizar
            required: true
            type: integer
          - name: body
            in: body
            required: true
            schema:
              $ref: '#/definitions/Student'
        responses:
          200:
            description: Estudiante actualizado exitosamente.
          400:
            description: No se proporcionaron datos para actualizar.
          404:
            description: Estudiante no encontrado.
        """
        data = request.json
        name = data.get('name')
        age = data.get('age')
        spec = data.get('spec')
        if name or age or spec:
            session = SessionLocal()
            student = session.query(Student).filter_by(id=student_id).first()
            if student:
                student.name = name if name else student.name
                student.age = age if age else student.age
                student.spec = spec if spec else student.spec
                session.commit()
                session.close()
                return jsonify({"message": "Student updated successfully"}), 200
            else:
                return jsonify({"error": "Student not found"}), 404
        else:
            return jsonify({"error": "No data provided to update"}), 400

    @app.route('/api/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        """
        Eliminar un estudiante por ID.

        ---
        parameters:
          - name: student_id
            in: path
            description: ID del estudiante a eliminar
            required: true
            type: integer
        responses:
          200:
            description: Estudiante eliminado exitosamente.
          404:
            description: Estudiante no encontrado.
        """
        session = SessionLocal()
        student = session.query(Student).filter_by(id=student_id).first()
        if student:
            session.delete(student)
            session.commit()
            session.close()
            return jsonify({"message": "Student deleted successfully"}), 200
        else:
            session.close()
            return jsonify({"error": "Student not found"}), 404
