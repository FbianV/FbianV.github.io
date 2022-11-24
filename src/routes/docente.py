from flask import Blueprint, jsonify, request
import database.query.docente as docente

docente_bp = Blueprint('docente_bp', __name__)

# obtener todos los cursos que se les haya aplicado una prueba a un alumno
@docente_bp.route('/app/v1/course/withTest', methods=['GET'])
def get_all_courses_Test():
    data = docente.get_courses_with_test(request.args.get('id_institucion'),request.args.get('id_docente'))
    return jsonify({'cursos': data, 'status': 'success'})

#obtener todas las asignaturas de las aplicaciones activas de un docente 
@docente_bp.route('/app/v1/subject/all', methods=['GET'])
def get_all_subjects():
    data = docente.get_all_subject(request.args.get('id_institucion'),request.args.get('id_docente'))
    return jsonify({'cursos': data, 'status': 'success'})


#obtener todas las aplicaciones activas de una asignatura
@docente_bp.route('/app/v1/subject/withTest', methods=['GET'])
def get_all_subject_test():
    data = docente.get_all_subject_test(request.args.get('id_institucion'),request.args.get('id_docente'), request.args.get('id_asignatura'))
    return jsonify({'cursos': data, 'status': 'success'})

# obtener todos los alumnos de una aplicacion
@docente_bp.route('/app/v1/subject/application', methods=['GET'])
def get_students_test ():
    data = docente.get_students_test(request.args.get('id_institucion'),request.args.get('id_docente'),request.args.get('id_aplicacion'))
    return jsonify({'alumnos': data, 'status': 'success'})
   
@docente_bp.route('/app/v1/xd', methods=['POST'])
def get_xd ():
    print("json")
    print(request.json)
    
    return jsonify({'status': 'success'})

