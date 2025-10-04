# ===============================
# models/models.py - MODELOS (VERSIÓN FINAL CORREGIDA)
# ===============================

from models.database import get_db
import json

class Mapa:
    @staticmethod
    def crear(nombre, descripcion=None):
        """Crea un nuevo mapa en la tabla 'Mapas'."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO Mapas (nombre, descripcion) VALUES (%s, %s)',
            (nombre, descripcion)
        )
        mapa_id = cursor.lastrowid
        db.commit()
        return mapa_id

    @staticmethod
    def obtener_todos():
        """Obtiene todos los mapas."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT id_mapa as id, nombre, descripcion, fecha_creacion FROM Mapas ORDER BY fecha_creacion DESC')
        mapas = cursor.fetchall()
        return mapas

    @staticmethod
    def obtener_por_id(mapa_id):
        """Obtiene un mapa por su ID."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT id_mapa as id, nombre FROM Mapas WHERE id_mapa = %s', (mapa_id,))
        mapa = cursor.fetchone()
        return mapa

    @staticmethod
    def eliminar(mapa_id):
        """Elimina un mapa y sus relaciones en cascada."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Mapas WHERE id_mapa = %s', (mapa_id,))
        db.commit()
        return cursor.rowcount > 0

class Contenido:
    @staticmethod
    def crear(color, detalle, imagen):
        """Crea un nuevo registro de contenido y devuelve su ID."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO Contenidos (color, detalle, imagen) VALUES (%s, %s, %s)',
            (color, detalle, imagen)
        )
        contenido_id = cursor.lastrowid
        db.commit()
        return contenido_id

class Municipio:
    @staticmethod
    def vincular_contenido(id_mapa, id_municipio, nombre_municipio, id_contenido):
        """Crea o actualiza el vínculo entre un mapa, municipio y su contenido."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''
            INSERT INTO Municipios (id_mapa, id_municipio, nombre, id_contenido)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id_contenido = VALUES(id_contenido)
            ''',
            (id_mapa, id_municipio, nombre_municipio, id_contenido)
        )
        db.commit()

    @staticmethod
    def obtener_configuraciones_por_mapa(mapa_id):
        """Obtiene todas las configuraciones de municipios para un mapa específico."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT 
                m.id_municipio as municipio_id,
                m.nombre as municipio_nombre,
                c.color,
                c.detalle AS informacion,
                c.imagen AS imagen_url
            FROM Municipios m
            LEFT JOIN Contenidos c ON m.id_contenido = c.id_contenido
            WHERE m.id_mapa = %s
            ''',
            (mapa_id,)
        )
        return cursor.fetchall()

    @staticmethod
    def eliminar_configuraciones_por_mapa(mapa_id):
        """Elimina todas las filas de la tabla Municipios para un mapa_id."""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM Municipios WHERE id_mapa = %s", (mapa_id,))
        db.commit()

    @staticmethod
    def obtener_todos():
        """Obtiene el catálogo de todos los municipios base."""
        # Esta es la función que faltaba. Devuelve una lista estática.
        return [
            {'id': 'amealcoDeBonfil', 'nombre': 'Amealco de Bonfil'},
            {'id': 'arroyoSeco', 'nombre': 'Arroyo Seco'},
            {'id': 'cadereytaDeMontes', 'nombre': 'Cadereyta de Montes'},
            {'id': 'colon', 'nombre': 'Colón'},
            {'id': 'corregidora', 'nombre': 'Corregidora'},
            {'id': 'elMarques', 'nombre': 'El Marqués'},
            {'id': 'ezequielMontes', 'nombre': 'Ezequiel Montes'},
            {'id': 'huimilpan', 'nombre': 'Huimilpan'},
            {'id': 'jalpanDeSerra', 'nombre': 'Jalpan de Serra'},
            {'id': 'landaDeMatamoros', 'nombre': 'Landa de Matamoros'},
            {'id': 'pedroEscobedo', 'nombre': 'Pedro Escobedo'},
            {'id': 'penamiller', 'nombre': 'Peñamiller'},
            {'id': 'pinalDeAmoles', 'nombre': 'Pinal de Amoles'},
            {'id': 'queretaro', 'nombre': 'Querétaro'},
            {'id': 'sanJoaquin', 'nombre': 'San Joaquín'},
            {'id': 'sanJuanDelRio', 'nombre': 'San Juan del Río'},
            {'id': 'tequisquiapan', 'nombre': 'Tequisquiapan'},
            {'id': 'toliman', 'nombre': 'Tolimán'}
        ]

class TablaDatos:
    # ... (El código de TablaDatos permanece igual) ...
    pass