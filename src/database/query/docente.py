from database.connection import create_connection
from mysql.connector import Error

# obtener todos los cursos que se les haya aplicado una prueba a un alumno
def get_courses_with_test(id_inst,id_doc):
    id_institucion = get_id_institucion (id_inst)
    id_docente = get_id_docente (id_doc)
    connection = create_connection()
    try:
        with connection.cursor() as cursor: # cambiar COUNT(asi.nombre) AS alumnos_totales por COUNT(cu.id AND pr.nombre) AS alumnos_totales
            sql = " SELECT \
                    	ev.id AS evento_id, \
                    	evcu.id AS evento_curso_id, \
                    	te.nombre AS tipo_enseñanza, \
                    	gr.nombre AS grado, \
                    	cu.id AS curso_id, \
                    	cu.letra AS curso, \
                    	pr.nombre AS aplicacion, \
                    	asi.nombre AS asignatura, \
                    	COUNT(asi.nombre) AS alumnos_totales, \
                    	COUNT(hr.nota >= 0) AS notas_puestas \
                    FROM \
                        curso AS cu \
                    	JOIN persona_curso AS pcu ON pcu.id_curso = cu.id \
                    	JOIN persona AS pe ON pe.id = pcu.id_persona \
                    	JOIN grado AS gr ON gr.id = cu.id_grado \
                    	JOIN tipo_ensenanza AS te ON te.id = gr.id_tipo_ensenanza \
                    	JOIN evento_curso AS evcu ON evcu.id_curso = cu.id \
                    	JOIN evento_prueba AS evpr ON evpr.id = evcu.id_evento_prueba \
                    	JOIN prueba AS pr ON pr.id = evpr.id_prueba \
                        JOIN asignatura as asi ON asi.id = pr.id_asignatura \
                    	JOIN evento AS ev ON ev.id = evpr.id_evento \
                    	JOIN hoja_respuesta AS hr ON hr.id_evento_prueba = evpr.id AND hr.id_persona_curso = pcu.id \
                    	JOIN establecimiento AS es ON es.id = cu.id_establecimiento \
                    WHERE \
                    	pcu.tipo = 1  \
                        AND evcu.se_evalua = 1 \
                    	AND ev.activo = 1 \
                    	AND (ev.fecha_inicio <= NOW() AND ev.fecha_fin >= NOW()) \
                    	AND hr.activo = 1 \
                    	AND hr.se_evalua = 1  \
                    	AND hr.activo = 1 \
                    	AND es.id_master_institucion = %s \
                    	AND evcu.id_docente = %s \
                    GROUP BY cu.id,pr.nombre ;"
            cursor.execute(sql, (id_institucion,id_docente))
            result = cursor.fetchall()
            data = []
            for row in result:
                dato = {
                    'id_evento': row[0],
                    'id_evento_curso': row[1],
                    'tipo_ensenanza': row[2],
                    'grado': row[3],
                    'id_curso': row[4],
                    'curso': row[5],
                    'aplicacion': row[6],
                    'asignatura': row[7],
                    'alumnos_curso': row[8],
                    'notas_puestas': row[9]
                }
                data.append(dato)
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")


#obtener todas las asignaturas de eventos activos de un docente 
def get_all_subject(id_inst, id_doc):
    id_institucion = get_id_institucion(id_inst)
    id_docente = get_id_docente(id_doc)
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = " SELECT \
                        asignatura, \
                        color_asignatura, \
                    	notas_puestas, \
                    	SUM(alumnos_cursos)AS alumnos_totales, \
                    	Count(*)  AS cant_eventos, \
                    	eventos_completados \
                    FROM(SELECT \
                            evento_id, \
                    		evento_curso_id, \
                    		asignatura, \
                    		color_asignatura, \
                    		notas_puestas, \
                    		alumnos_cursos, \
                    		curso_id, \
                    		aplicacion, \
                    		COUNT(notas_puestas = alumnos_cursos) AS eventos_completados \
                    	FROM(SELECT \
                                ev.id AS evento_id, \
                    			evcu.id AS evento_curso_id, \
                    			te.nombre AS tipo_enseñanza, \
                    			gr.nombre AS grado, \
                    			cu.id AS curso_id, \
                    			cu.letra AS curso, \
                    			pr.nombre AS aplicacion, \
                    			asi.nombre AS asignatura, \
                    			asi.color AS color_asignatura, \
                    			COUNT(cu.id AND pr.nombre) AS alumnos_cursos, \
                    			COUNT(hr.nota >= 0) AS notas_puestas \
                    		FROM \
                    			curso AS cu \
                    			JOIN persona_curso AS pcu ON pcu.id_curso = cu.id \
                    			JOIN persona AS pe ON pe.id = pcu.id_persona \
                    			JOIN grado AS gr ON gr.id = cu.id_grado \
                    			JOIN tipo_ensenanza AS te ON te.id = gr.id_tipo_ensenanza \
                    			JOIN evento_curso AS evcu ON evcu.id_curso = cu.id \
                    			JOIN evento_prueba AS evpr ON evpr.id = evcu.id_evento_prueba \
                    			JOIN prueba AS pr ON pr.id = evpr.id_prueba \
                    			JOIN asignatura as asi ON asi.id = pr.id_asignatura \
                    			JOIN evento AS ev ON ev.id = evpr.id_evento \
                    			JOIN hoja_respuesta AS hr ON hr.id_evento_prueba = evpr.id AND hr.id_persona_curso = pcu.id \
                    			JOIN establecimiento AS es ON es.id = cu.id_establecimiento \
                    		WHERE \
                    			pcu.tipo = 1  \
                    			AND evcu.se_evalua = 1 \
                    			AND ev.activo = 1 \
                    			AND (ev.fecha_inicio <= NOW() AND ev.fecha_fin >= NOW()) \
                    			AND hr.activo = 1 \
                    			AND hr.se_evalua = 1 \
                    			AND hr.activo = 1 \
                    			AND es.id_master_institucion = %s \
                    			AND evcu.id_docente = %s \
                    		GROUP BY cu.id,pr.nombre) AS c	 \
                    	GROUP BY  curso_id, aplicacion) AS cc  \
                    GROUP BY asignatura;"
            cursor.execute(sql, (id_institucion, id_docente))
            result = cursor.fetchall()
            data = []
            for row in result:
                dato = {
                    'asignatura': row[0],
                    'color_asignatura': row[1],
                    'notas_puestas': row[2],
                    'alumnos_totales': int(row[3]),
                    'cant_eventos': row[4],
                    'eventos_completados': row[5]
                }
                data.append(dato)
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")


#obtener todas las aplicaciones de una asignatura
def get_all_subject_test(id_inst, id_doc, id_asignatura):
    id_institucion = get_id_institucion(id_inst)
    id_docente = get_id_docente(id_doc)
    connection = create_connection()
    try:
        with connection.cursor() as cursor: # cambiar COUNT(asi.nombre) AS alumnos_totales por COUNT(cu.id AND pr.nombre) AS alumnos_totales
            sql = " SELECT \
                        asi.nombre AS asignatura, \
                    	gr.nombre AS grado, \
                        te.nombre AS tipo_enseñanza, \
                        cu.letra AS curso, \
                    	cu.id AS curso_id, \
                    	pr.nombre AS aplicacion, \
                    	COUNT(asi.nombre) AS alumnos_totales, \
                    	COUNT(hr.nota >= 0) AS notas_puestas \
                    FROM \
                        curso AS cu \
                    	JOIN persona_curso AS pcu ON pcu.id_curso = cu.id \
                    	JOIN persona AS pe ON pe.id = pcu.id_persona \
                    	JOIN grado AS gr ON gr.id = cu.id_grado \
                    	JOIN tipo_ensenanza AS te ON te.id = gr.id_tipo_ensenanza \
                    	JOIN evento_curso AS evcu ON evcu.id_curso = cu.id \
                    	JOIN evento_prueba AS evpr ON evpr.id = evcu.id_evento_prueba \
                    	JOIN prueba AS pr ON pr.id = evpr.id_prueba \
                        JOIN asignatura as asi ON asi.id = pr.id_asignatura \
                    	JOIN evento AS ev ON ev.id = evpr.id_evento \
                    	JOIN hoja_respuesta AS hr ON hr.id_evento_prueba = evpr.id AND hr.id_persona_curso = pcu.id \
                    	JOIN establecimiento AS es ON es.id = cu.id_establecimiento \
                    WHERE \
                    	pcu.tipo = 1  \
                        AND evcu.se_evalua = 1 \
                    	AND ev.activo = 1 \
                    	AND (ev.fecha_inicio <= NOW() AND ev.fecha_fin >= NOW()) \
                    	AND hr.activo = 1 \
                    	AND hr.se_evalua = 1 \
                    	AND hr.activo = 1 \
                    	AND es.id_master_institucion = %s \
                    	AND evcu.id_docente = %s \
                        AND asi.nombre = %s \
                    GROUP BY cu.id,pr.nombre;"
            cursor.execute(sql, (id_institucion, id_docente,id_asignatura))
            result = cursor.fetchall()
            data = []
            for row in result:
                dato = {
                    'asignatura': row[0],
                    'grado': row[1],
                    'tipo_enseñanza': row[2],
                    'curso': row[3],
                    'curso_id': row[4],
                    'aplicacion': row[5],
                    'alumnos_totales': row[6],
                    'notas_puestas': row[7]
                }
                data.append(dato)
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")



# obtener todos los alumnos de una aplicacion
def get_students_test(id_inst, id_doc, id_application):
    id_institucion = get_id_institucion(id_inst)
    id_docente = get_id_docente(id_doc)
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = " SELECT \
                        ev.id, \
                    	evcu.id, \
                        te.nombre AS tipo_enseñanza, \
                        gr.nombre AS grado, \
                        cu.id, \
                        cu.letra AS curso, \
                        pr.nombre AS aplicacion, \
                        pe.run AS RUN, \
                        CONCAT(pe.nombres,' ',pe.ap_paterno,' ',pe.ap_materno) AS alumno, \
                        hr.id, \
                        hr.nota as nota \
                    FROM \
                        curso AS cu \
                    	JOIN persona_curso AS pcu ON pcu.id_curso = cu.id \
                    	JOIN persona AS pe ON pe.id = pcu.id_persona \
                    	JOIN grado AS gr ON gr.id = cu.id_grado \
                    	JOIN tipo_ensenanza AS te ON te.id = gr.id_tipo_ensenanza \
                    	JOIN evento_curso AS evcu ON evcu.id_curso = cu.id \
                    	JOIN evento_prueba AS evpr ON evpr.id = evcu.id_evento_prueba \
                    	JOIN prueba AS pr ON pr.id = evpr.id_prueba \
                    	JOIN evento AS ev ON ev.id = evpr.id_evento \
                    	JOIN hoja_respuesta AS hr ON hr.id_evento_prueba = evpr.id AND hr.id_persona_curso = pcu.id \
                    	JOIN establecimiento AS es ON es.id = cu.id_establecimiento \
                    WHERE \
                    	pcu.tipo = 1  \
                        AND evcu.se_evalua = 1 \
                    	AND ev.activo = 1 \
                    	AND (ev.fecha_inicio <= NOW() AND ev.fecha_fin >= NOW()) \
                    	AND hr.activo = 1 \
                    	AND hr.se_evalua = 1 \
                    	AND hr.activo = 1 \
                    	AND es.id_master_institucion = %s \
                    	AND evcu.id_docente = %s \
                    	AND pr.nombre = %s ;"
            cursor.execute(sql, (id_institucion, id_docente, id_application))
            result = cursor.fetchall()
            data = []
            for row in result:
                dato = {
                    'id_evento': row[0],
                    'id_evento_curso': row[1],
                    'tipo_ensenanza': row[2],
                    'grado': row[3],
                    'id_curso': row[4],
                    'curso': row[5],
                    'aplicacion': row[6],
                    'run': row[7],
                    'alumno': row[8],
                    'id_hoja_respuesta': row[9],
                    'nota': row[10]
                }
                data.append(dato)
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

#obtener id persona del docente a partir de dato entregado por API de PIL
def get_id_docente (id_docente):
    connection = create_connection()
    id_empresa = 30
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM persona WHERE id_master_persona = %s and id_empresa = %s; "
            cursor.execute(sql, (id_docente, id_empresa))
            result = cursor.fetchone()
            return result[0]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")


#obtener id_master_institucion a partir de la id de la institucion dada por API de PIL
def get_id_institucion (id_institucion):
    cod = get_cod_colegio(id_institucion)
    id_empresa = 30
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id_master_institucion FROM establecimiento WHERE cod_colegio  = %s and id_empresa = %s;"
            cursor.execute(sql, (cod,id_empresa))
            result = cursor.fetchone()
            return result[0]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

#obtener cod_colegio a partir de la id de la institucion dada por API de PIL
def get_cod_colegio (id_institucion):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "select cod_colegio from establecimiento where id_master_institucion = '{0}';".format(id_institucion)
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
      if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")
