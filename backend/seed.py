from database import SessionLocal, engine, Base
import models
from datetime import date

def seed():
    db = SessionLocal()

    # ── Evita correr el seed dos veces ──────────────────────────────
    if db.query(models.KnowledgeActivity).count() > 0:
        print("Seed ya fue ejecutado. Saliendo.")
        db.close()
        return

    print("Iniciando seed...")

    # ────────────────────────────────────────────────────────────────
    # 1. MISIONES FIJAS
    # ────────────────────────────────────────────────────────────────
    missions = [
        # Nutrición — todos los estados
        {"name": "3 comidas con proteína", "description": "Desayuno, comida y cena con fuente de proteína (pollo, res, huevo, atún)", "mission_type": "daily_nutrition", "xp_reward": 60, "coins_reward": 5, "evolution_state_required": 0},
        {"name": "2 litros de agua", "description": "Completar 2 litros de agua durante el día", "mission_type": "daily_nutrition", "xp_reward": 50, "coins_reward": 5, "evolution_state_required": 0},
        {"name": "Sin comida procesada", "description": "No comer comida rápida ni ultra-procesada", "mission_type": "daily_nutrition", "xp_reward": 40, "coins_reward": 5, "evolution_state_required": 0},
        {"name": "Dormir 7+ horas", "description": "Dormir al menos 7 horas esta noche", "mission_type": "daily_nutrition", "xp_reward": 40, "coins_reward": 5, "evolution_state_required": 0},

        # Ejercicio — Estado 0 (antes del despertar, solo referencia)
        {"name": "Caminar 20 minutos", "description": "Caminata ligera de al menos 20 minutos", "mission_type": "daily_exercise", "xp_reward": 50, "coins_reward": 5, "evolution_state_required": 0},

        # Ejercicio — Estado 1 (niveles 1-10)
        {"name": "Entrenamiento de fuerza 30 min", "description": "Rutina de pesas o bandas de resistencia, mínimo 30 minutos", "mission_type": "daily_exercise", "xp_reward": 80, "coins_reward": 5, "evolution_state_required": 1},
        {"name": "Cardio 30 minutos", "description": "Caminata rápida, trote o cardio continuo 30 min", "mission_type": "daily_exercise", "xp_reward": 60, "coins_reward": 5, "evolution_state_required": 1},

        # Ejercicio — Estado 2 (niveles 11-20)
        {"name": "Entrenamiento de fuerza 40 min", "description": "Rutina A/B de fuerza, mínimo 40 minutos", "mission_type": "daily_exercise", "xp_reward": 90, "coins_reward": 5, "evolution_state_required": 2},
        {"name": "Cardio 30 min continuo", "description": "Cardio sin pausas durante 30 minutos", "mission_type": "daily_exercise", "xp_reward": 60, "coins_reward": 5, "evolution_state_required": 2},

        # Ejercicio — Estado 3 (niveles 21-35)
        {"name": "Entrenamiento de fuerza 50 min", "description": "Rutina A/B de fuerza, mínimo 50 minutos", "mission_type": "daily_exercise", "xp_reward": 100, "coins_reward": 5, "evolution_state_required": 3},
        {"name": "Cardio 30 min continuo", "description": "Cardio sin pausas durante 30 minutos", "mission_type": "daily_exercise", "xp_reward": 60, "coins_reward": 5, "evolution_state_required": 3},

        # Ejercicio — Estado 4 (niveles 36-55)
        {"name": "Entrenamiento 60 min rutina 4 días", "description": "Sesión de 60 minutos, 4 días por semana", "mission_type": "daily_exercise", "xp_reward": 110, "coins_reward": 5, "evolution_state_required": 4},
        {"name": "HIIT 20 minutos", "description": "Entrenamiento de intervalos de alta intensidad, 20 min", "mission_type": "daily_exercise", "xp_reward": 70, "coins_reward": 5, "evolution_state_required": 4},

        # Ejercicio — Estado 5 (niveles 56-75)
        {"name": "Entrenamiento 60 min con técnica", "description": "Sesión de 60 minutos enfocada en técnica correcta", "mission_type": "daily_exercise", "xp_reward": 115, "coins_reward": 5, "evolution_state_required": 5},
        {"name": "Cardio mixto 35 min", "description": "Combinación de cardio (trote + saltos + bici), 35 min", "mission_type": "daily_exercise", "xp_reward": 75, "coins_reward": 5, "evolution_state_required": 5},

        # Ejercicio — Estado 6 (niveles 76-90)
        {"name": "Entrenamiento 60 min con progresión", "description": "Sesión de 60 min aumentando peso o repeticiones vs semana anterior", "mission_type": "daily_exercise", "xp_reward": 120, "coins_reward": 5, "evolution_state_required": 6},
        {"name": "Cardio 40 min libre", "description": "40 minutos de cardio a elección", "mission_type": "daily_exercise", "xp_reward": 80, "coins_reward": 5, "evolution_state_required": 6},

        # Ejercicio — Estado 7 (niveles 91-100)
        {"name": "Entrenamiento 60 min libre", "description": "60 minutos de entrenamiento — el usuario diseña su rutina", "mission_type": "daily_exercise", "xp_reward": 120, "coins_reward": 5, "evolution_state_required": 7},
        {"name": "Cardio 40 min libre", "description": "40 minutos de cardio a elección", "mission_type": "daily_exercise", "xp_reward": 80, "coins_reward": 5, "evolution_state_required": 7},

        # Misiones semanales de ejercicio
        {"name": "Acumular 5 km", "description": "Sumar 5 km caminando o trotando durante la semana", "mission_type": "weekly_exercise", "xp_reward": 150, "coins_reward": 30, "evolution_state_required": 1},
        {"name": "Acumular 10 km", "description": "Sumar 10 km durante la semana — desbloquea recompensa cerveza", "mission_type": "weekly_exercise", "xp_reward": 200, "coins_reward": 30, "evolution_state_required": 3},
        {"name": "Acumular 15 km", "description": "Sumar 15 km durante la semana", "mission_type": "weekly_exercise", "xp_reward": 250, "coins_reward": 30, "evolution_state_required": 4},
        {"name": "Acumular 20 km", "description": "Sumar 20 km durante la semana", "mission_type": "weekly_exercise", "xp_reward": 300, "coins_reward": 30, "evolution_state_required": 5},
        {"name": "Acumular 25 km", "description": "Sumar 25 km durante la semana", "mission_type": "weekly_exercise", "xp_reward": 350, "coins_reward": 30, "evolution_state_required": 6},

        # Misiones jefe
        {"name": "Jefe Estado 2: Despertar del iniciado", "description": "7 días activos + llegar a 102 kg", "mission_type": "boss", "xp_reward": 500, "coins_reward": 100, "evolution_state_required": 1},
        {"name": "Jefe Estado 3: El guerrero emerge", "description": "30 días activos + llegar a 99 kg + semana perfecta", "mission_type": "boss", "xp_reward": 800, "coins_reward": 100, "evolution_state_required": 2},
        {"name": "Jefe Estado 4: Élite oscuro", "description": "60 días activos + 95 kg + semana perfecta", "mission_type": "boss", "xp_reward": 1200, "coins_reward": 100, "evolution_state_required": 3},
        {"name": "Jefe Estado 5: Señor de la tormenta", "description": "90 días activos + 91 kg + mes al 90%", "mission_type": "boss", "xp_reward": 2000, "coins_reward": 100, "evolution_state_required": 4},
        {"name": "Jefe Estado 6: Guardián", "description": "120 días activos + 88 kg + 2 meses al 85%", "mission_type": "boss", "xp_reward": 3500, "coins_reward": 100, "evolution_state_required": 5},
        {"name": "Jefe Estado 7: Darkial Absoluto", "description": "150 días activos + 86 kg + mantener 85-87 kg 2 semanas", "mission_type": "boss", "xp_reward": 5000, "coins_reward": 100, "evolution_state_required": 6},
        {"name": "Misión Final: Darkial Absoluto permanente", "description": "Mantener 85 kg ±1 kg durante 30 días consecutivos", "mission_type": "boss", "xp_reward": 10000, "coins_reward": 100, "evolution_state_required": 7},
    ]

    for m in missions:
        db.add(models.Mission(**m))

    # ────────────────────────────────────────────────────────────────
    # 2. ACTIVIDADES DE CONOCIMIENTO (180 misiones del Excel)
    # ────────────────────────────────────────────────────────────────
    knowledge = [
        {"name": "Elaborar un diseño creativo para Instagram", "category": "Arte", "xp_reward": 60},
        {"name": "Ve a un museo, feria, exhibicion o alguna galeria de arte", "category": "Historia", "xp_reward": 100},
        {"name": "Aprende una nueva herramienta de Photoshop", "category": "Arte", "xp_reward": 50},
        {"name": "Aprende una nueva herramienta de Ilustrador", "category": "Arte", "xp_reward": 50},
        {"name": "Cambia tu foto de perfil de Instagram o Whatsapp", "category": "Arte", "xp_reward": 20},
        {"name": "Acuestate en un parque y observa el cielo", "category": "Bienestar", "xp_reward": 40},
        {"name": "Diseña un logo de un animal", "category": "Arte", "xp_reward": 55},
        {"name": "Diseña un logo de comida", "category": "Arte", "xp_reward": 55},
        {"name": "Diseña un logo de alguna cultura antigua", "category": "Arte", "xp_reward": 65},
        {"name": "Diseña un logo de un elemento de la naturaleza", "category": "Arte", "xp_reward": 55},
        {"name": "Aprende sobre el funcionamiento de una parte de un vehiculo", "category": "Ciencia", "xp_reward": 45},
        {"name": "Completa un Sudoku", "category": "Ciencia", "xp_reward": 35},
        {"name": "Completa un Crucigrama", "category": "Ciencia", "xp_reward": 35},
        {"name": "Completa un Rompecabezas de 100 o mas piezas", "category": "Ciencia", "xp_reward": 80},
        {"name": "Escribe una frase con tu mano No Habil", "category": "Arte", "xp_reward": 25},
        {"name": "Escribe un parrafo con tu mano No Habil", "category": "Arte", "xp_reward": 35},
        {"name": "Escribe la letra de una cancion con tu mano No Habil", "category": "Arte", "xp_reward": 50},
        {"name": "Aprende un truco de magia", "category": "Arte", "xp_reward": 60},
        {"name": "Pinta un cuadro", "category": "Arte", "xp_reward": 90},
        {"name": "Juega una partida de Ajedrez", "category": "Ciencia", "xp_reward": 40},
        {"name": "Practica una cancion de Cumbia", "category": "Musica", "xp_reward": 55},
        {"name": "Practica una cancion de Bachata", "category": "Musica", "xp_reward": 55},
        {"name": "Practica una cancion de Fiesta", "category": "Musica", "xp_reward": 55},
        {"name": "Haz Zumba", "category": "Musica", "xp_reward": 70},
        {"name": "Haz Senderismo", "category": "Bienestar", "xp_reward": 85},
        {"name": "Arregla algo que tengas pendiente en tu casa", "category": "Bienestar", "xp_reward": 75},
        {"name": "Prepara una Pizza saludable", "category": "Gastronomia", "xp_reward": 65},
        {"name": "Prepara un Chimichurri", "category": "Gastronomia", "xp_reward": 50},
        {"name": "Haz un accesorio (pulsera)", "category": "Arte", "xp_reward": 60},
        {"name": "Haz un accesorio (collar)", "category": "Arte", "xp_reward": 65},
        {"name": "Practica una cancion de Hip Hop", "category": "Musica", "xp_reward": 55},
        {"name": "Planta una planta", "category": "Bienestar", "xp_reward": 50},
        {"name": "Practica Origami", "category": "Arte", "xp_reward": 60},
        {"name": "Aprende a Bordar o Crochet", "category": "Arte", "xp_reward": 80},
        {"name": "Colorea un Dibujo", "category": "Arte", "xp_reward": 30},
        {"name": "Aprende sobre como se hace la Cerveza", "category": "Gastronomia", "xp_reward": 45},
        {"name": "Aprende como se hace el Pan Casero", "category": "Gastronomia", "xp_reward": 45},
        {"name": "Aprende como se hace el Vino Tinto", "category": "Gastronomia", "xp_reward": 45},
        {"name": "Aprende sobre los Agujeros negros y ondas gravitacionales", "category": "Ciencia", "xp_reward": 70},
        {"name": "Aprende sobre la Edicion genetica", "category": "Ciencia", "xp_reward": 70},
        {"name": "Aprende sobre la Biologia sintetica", "category": "Ciencia", "xp_reward": 70},
        {"name": "Aprende sobre Neurociencia y consciencia", "category": "Ciencia", "xp_reward": 70},
        {"name": "Aprende sobre Computacion cuantica", "category": "Ciencia", "xp_reward": 75},
        {"name": "Aprende sobre Materia y energia oscura", "category": "Ciencia", "xp_reward": 75},
        {"name": "Aprende sobre Cambio climatico", "category": "Ciencia", "xp_reward": 50},
        {"name": "Aprende sobre Impacto psicologico de la hiperconectividad", "category": "Ciencia", "xp_reward": 55},
        {"name": "Aprende sobre Crisis de la vivienda y la gentrificacion", "category": "Historia", "xp_reward": 55},
        {"name": "Lee sobre el Nuevo Orden Mundial", "category": "Historia", "xp_reward": 40},
        {"name": "Lee sobre El Plan Kalergi", "category": "Historia", "xp_reward": 40},
        {"name": "Lee sobre Sociedades Secretas", "category": "Historia", "xp_reward": 45},
        {"name": "Lee sobre Asesinato de John F. Kennedy", "category": "Historia", "xp_reward": 50},
        {"name": "Lee sobre Atentados del 11 de Septiembre", "category": "Historia", "xp_reward": 50},
        {"name": "Lee sobre Lunares Aceptadas y Aterrizajes Falsos", "category": "Historia", "xp_reward": 40},
        {"name": "Lee sobre Terraplanismo", "category": "Historia", "xp_reward": 35},
        {"name": "Lee sobre Chemtrails", "category": "Historia", "xp_reward": 35},
        {"name": "Lee sobre Microchips en vacunas", "category": "Historia", "xp_reward": 35},
        {"name": "Lee sobre La muerte de Paul McCartney", "category": "Historia", "xp_reward": 35},
        {"name": "Lee sobre Pizzagate", "category": "Historia", "xp_reward": 40},
        {"name": "Lee sobre Proyecto MKUltra", "category": "Historia", "xp_reward": 55},
        {"name": "Lee sobre Experimento de Tuskegee", "category": "Historia", "xp_reward": 60},
        {"name": "Lee sobre Operacion Northwoods", "category": "Historia", "xp_reward": 55},
        {"name": "Lee sobre los reptilianos", "category": "Historia", "xp_reward": 30},
        {"name": "Lee sobre los no humanos", "category": "Historia", "xp_reward": 30},
        {"name": "Lee sobre los Masones", "category": "Historia", "xp_reward": 45},
        {"name": "Lee sobre Chakras", "category": "Espiritualidad", "xp_reward": 40},
        {"name": "Lee sobre Energia Espiritual", "category": "Espiritualidad", "xp_reward": 40},
        {"name": "Lee sobre Numerologia", "category": "Espiritualidad", "xp_reward": 35},
        {"name": "Lee sobre Aura", "category": "Espiritualidad", "xp_reward": 35},
        {"name": "Lee sobre Canalizacion y Kundalini", "category": "Espiritualidad", "xp_reward": 45},
        {"name": "Lee sobre Reiki", "category": "Espiritualidad", "xp_reward": 40},
        {"name": "Lee sobre Geometria Sagrada y Cristales", "category": "Espiritualidad", "xp_reward": 40},
        {"name": "Lee sobre Limpieza Energetica", "category": "Espiritualidad", "xp_reward": 35},
        {"name": "Lee sobre Ley de Atraccion", "category": "Espiritualidad", "xp_reward": 45},
        {"name": "Lee sobre Registros Akashicos", "category": "Espiritualidad", "xp_reward": 50},
        {"name": "Lee sobre Mindfulness y Meditacion", "category": "Bienestar", "xp_reward": 55},
        {"name": "Lee sobre Karma y Dharma", "category": "Espiritualidad", "xp_reward": 45},
        {"name": "Lee sobre cristales o cuarzos", "category": "Espiritualidad", "xp_reward": 35},
        {"name": "Aprende sobre Cristianismo", "category": "Historia", "xp_reward": 55},
        {"name": "Aprende sobre Islam", "category": "Historia", "xp_reward": 55},
        {"name": "Aprende sobre Hinduismo", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Budismo", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Judaismo", "category": "Historia", "xp_reward": 55},
        {"name": "Aprende sobre Taoismo", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Sintoismo", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Sijismo", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Fe Bahai", "category": "Historia", "xp_reward": 60},
        {"name": "Aprende sobre Mitologia Griega", "category": "Historia", "xp_reward": 65},
        {"name": "Aprende sobre Mitologia Nordica", "category": "Historia", "xp_reward": 65},
        {"name": "Aprende sobre Mitologia Egipcia", "category": "Historia", "xp_reward": 65},
        {"name": "Aprende sobre Mitologia Mesoamericana", "category": "Historia", "xp_reward": 70},
        {"name": "Aprende sobre Cosmogonia", "category": "Ciencia", "xp_reward": 65},
        {"name": "Lee sobre Mitologia y Criptozoologia", "category": "Historia", "xp_reward": 50},
        {"name": "Lee sobre Ocultismo y Magia", "category": "Espiritualidad", "xp_reward": 50},
        {"name": "Lee sobre Lo Paranormal y Extraterrestre", "category": "Historia", "xp_reward": 45},
        {"name": "Lee sobre Poderes Mentales", "category": "Ciencia", "xp_reward": 45},
        {"name": "Haz un dibujo a lapiz", "category": "Arte", "xp_reward": 40},
        {"name": "Haz un dibujo digital", "category": "Arte", "xp_reward": 50},
        {"name": "Diseña un personaje de Anime", "category": "Arte", "xp_reward": 70},
        {"name": "Haz un retrato de alguien que conozcas", "category": "Arte", "xp_reward": 65},
        {"name": "Crea un mapa imaginario de un mundo de fantasia", "category": "Arte", "xp_reward": 75},
        {"name": "Diseña la portada de un libro que nunca ha existido", "category": "Arte", "xp_reward": 70},
        {"name": "Haz una caricatura de ti mismo", "category": "Arte", "xp_reward": 60},
        {"name": "Aprende los pasos basicos de Salsa", "category": "Musica", "xp_reward": 65},
        {"name": "Aprende los pasos basicos de Reggaeton", "category": "Musica", "xp_reward": 55},
        {"name": "Canta una cancion completa sin musica de fondo", "category": "Musica", "xp_reward": 50},
        {"name": "Aprende a tocar una melodia simple en Youtube", "category": "Musica", "xp_reward": 80},
        {"name": "Crea una lista de reproduccion de 20 canciones que representen tu vida", "category": "Musica", "xp_reward": 35},
        {"name": "Memoriza 10 datos curiosos sobre un tema que conozcas", "category": "Ciencia", "xp_reward": 45},
        {"name": "Aprende 10 palabras en Japones", "category": "Historia", "xp_reward": 60},
        {"name": "Practica hablar en Ingles", "category": "Ciencia", "xp_reward": 70},
        {"name": "Escribe una historia corta de 1 pagina con un personaje inventado", "category": "Arte", "xp_reward": 75},
        {"name": "Resuelve 5 acertijos o adivinanzas dificiles", "category": "Ciencia", "xp_reward": 50},
        {"name": "Aprende a hacer un nudo marino o de escalada", "category": "Bienestar", "xp_reward": 55},
        {"name": "Ve a un lugar de tu ciudad que nunca hayas visitado", "category": "Bienestar", "xp_reward": 80},
        {"name": "Cocina un platillo que nunca hayas preparado antes", "category": "Gastronomia", "xp_reward": 70},
        {"name": "Habla con un desconocido y aprende algo sobre su vida", "category": "Bienestar", "xp_reward": 85},
        {"name": "Observa el amanecer o atardecer completo sin celular", "category": "Bienestar", "xp_reward": 60},
        {"name": "Escribe una carta a tu yo de dentro de 5 años", "category": "Bienestar", "xp_reward": 70},
        {"name": "Aprende a hacer tortillas de maiz desde cero", "category": "Gastronomia", "xp_reward": 65},
        {"name": "Aprende la historia de un platillo tipico mexicano", "category": "Gastronomia", "xp_reward": 45},
        {"name": "Haz agua fresca de una fruta que nunca hayas preparado", "category": "Gastronomia", "xp_reward": 40},
        {"name": "Aprende la diferencia entre los tipos de chile mexicano", "category": "Gastronomia", "xp_reward": 40},
        {"name": "Aprende a usar un atajo de teclado que no conocias", "category": "Ciencia", "xp_reward": 30},
        {"name": "Crea un video corto de 60 segundos sobre cualquier tema", "category": "Arte", "xp_reward": 65},
        {"name": "Aprende la historia de la Inteligencia Artificial", "category": "Ciencia", "xp_reward": 50},
        {"name": "Configura algo en tu computadora que tenias pendiente", "category": "Ciencia", "xp_reward": 35},
        {"name": "Aprende sobre como funciona el internet", "category": "Ciencia", "xp_reward": 55},
        {"name": "Aprende sobre Seguridad Informatica", "category": "Ciencia", "xp_reward": 65},
        {"name": "Investiga sobre una civilizacion prehispanica", "category": "Historia", "xp_reward": 65},
        {"name": "Aprende sobre la Revolucion Mexicana", "category": "Historia", "xp_reward": 55},
        {"name": "Investiga sobre algun personaje historico que te agrade", "category": "Historia", "xp_reward": 50},
        {"name": "Aprende sobre el origen de una tradicion mexicana", "category": "Historia", "xp_reward": 45},
        {"name": "Investiga sobre la historia de tu ciudad o estado natal", "category": "Historia", "xp_reward": 55},
        {"name": "Haz 10 minutos de respiracion consciente o meditacion guiada", "category": "Bienestar", "xp_reward": 40},
        {"name": "Escribe 3 cosas por las que estas agradecido hoy y porque", "category": "Bienestar", "xp_reward": 35},
        {"name": "Desconectate completamente de pantallas durante 2 horas", "category": "Bienestar", "xp_reward": 70},
        {"name": "Haz una lista de 10 metas que quieras lograr en los proximos 3 años", "category": "Bienestar", "xp_reward": 50},
        {"name": "Duerme antes de las 10pm y escribe como te sientes al despertar", "category": "Bienestar", "xp_reward": 60},
        {"name": "Observa el cielo durante la noche sin celular", "category": "Bienestar", "xp_reward": 55},
        {"name": "Aprende un baile de tik tok", "category": "Musica", "xp_reward": 45},
        {"name": "Haz una caminata de 30 min en silencio absoluto", "category": "Bienestar", "xp_reward": 55},
        {"name": "Escribe en un diario como te sentiste hoy y por que", "category": "Bienestar", "xp_reward": 35},
        {"name": "Toma una ducha fria de 2 minutos completos", "category": "Bienestar", "xp_reward": 45},
        {"name": "Estira tu cuerpo durante 15 minutos al despertar", "category": "Bienestar", "xp_reward": 40},
        {"name": "Pasa un dia completo sin quejarte de nada", "category": "Bienestar", "xp_reward": 70},
        {"name": "Apaga el telefono 1 hora antes de dormir durante 3 dias seguidos", "category": "Bienestar", "xp_reward": 75},
        {"name": "Haz algo completamente solo que normalmente harias acompañado", "category": "Bienestar", "xp_reward": 65},
        {"name": "Escribe una carta de perdon a alguien", "category": "Bienestar", "xp_reward": 60},
        {"name": "Aprende sobre los ciclos del sueño y como mejorar tu descanso", "category": "Bienestar", "xp_reward": 45},
        {"name": "Pasa una tarde sin ningun plan — sin agenda, sin objetivo", "category": "Bienestar", "xp_reward": 50},
        {"name": "Aprende la historia del rock and roll desde sus origenes", "category": "Musica", "xp_reward": 55},
        {"name": "Escucha un album completo sin interrupciones y escribe que sentiste", "category": "Musica", "xp_reward": 45},
        {"name": "Aprende sobre la historia del jazz y sus subgeneros", "category": "Musica", "xp_reward": 55},
        {"name": "Investiga como se compone una cancion", "category": "Musica", "xp_reward": 60},
        {"name": "Aprende los pasos basicos de Merengue", "category": "Musica", "xp_reward": 55},
        {"name": "Aprende los pasos basicos de Quebradita", "category": "Musica", "xp_reward": 60},
        {"name": "Aprende sobre la historia de la musica mexicana", "category": "Musica", "xp_reward": 55},
        {"name": "Aprende a identificar los instrumentos de una orquesta sinfonica", "category": "Musica", "xp_reward": 60},
        {"name": "Investiga sobre la historia del anime y su musica", "category": "Musica", "xp_reward": 50},
        {"name": "Aprende sobre la historia del Hip Hop desde sus origenes", "category": "Musica", "xp_reward": 55},
        {"name": "Lee sobre el estoicismo y sus principios principales", "category": "Espiritualidad", "xp_reward": 55},
        {"name": "Aprende sobre el concepto budista del desapego", "category": "Espiritualidad", "xp_reward": 50},
        {"name": "Investiga que es la muerte segun 3 culturas diferentes", "category": "Espiritualidad", "xp_reward": 65},
        {"name": "Lee sobre Viktor Frankl y el sentido de la vida", "category": "Espiritualidad", "xp_reward": 60},
        {"name": "Aprende sobre la filosofia del Ikigai japones", "category": "Espiritualidad", "xp_reward": 55},
        {"name": "Investiga que es la conciencia segun la neurociencia y la filosofia", "category": "Espiritualidad", "xp_reward": 70},
        {"name": "Lee sobre el concepto de memento mori y como aplicarlo", "category": "Espiritualidad", "xp_reward": 50},
        {"name": "Aprende sobre el chamanismo mexicano", "category": "Espiritualidad", "xp_reward": 60},
        {"name": "Lee sobre la filosofia de Epicteto", "category": "Espiritualidad", "xp_reward": 55},
        {"name": "Investiga que es la muerte del ego segun diferentes tradiciones", "category": "Espiritualidad", "xp_reward": 65},
        {"name": "Aprende a hacer arroz rojo mexicano desde cero", "category": "Gastronomia", "xp_reward": 55},
        {"name": "Aprende la historia de la cocina mexicana y por que es Patrimonio UNESCO", "category": "Gastronomia", "xp_reward": 50},
        {"name": "Prepara frijoles de olla desde cero sin usar frijoles de lata", "category": "Gastronomia", "xp_reward": 60},
        {"name": "Aprende a hacer salsa roja asada de 3 ingredientes", "category": "Gastronomia", "xp_reward": 45},
        {"name": "Cocina un desayuno completo que nunca hayas preparado", "category": "Gastronomia", "xp_reward": 65},
        {"name": "Aprende la diferencia entre los tipos de tortilla", "category": "Gastronomia", "xp_reward": 35},
        {"name": "Investiga sobre la gastronomia de un pais que nunca hayas visitado", "category": "Gastronomia", "xp_reward": 50},
        {"name": "Aprende a marinar carne correctamente para carne asada", "category": "Gastronomia", "xp_reward": 55},
        {"name": "Haz agua de Jamaica desde cero sin azucar refinada", "category": "Gastronomia", "xp_reward": 40},
        {"name": "Aprende sobre los 5 sabores basicos y como funcionan en el paladar", "category": "Gastronomia", "xp_reward": 45},
    ]

    for k in knowledge:
        db.add(models.KnowledgeActivity(**k))

    # ────────────────────────────────────────────────────────────────
    # 3. RECOMPENSAS
    # ────────────────────────────────────────────────────────────────
    rewards = [
        # Semanales
        {"name": "Coca Cola original 600ml", "reward_type": "weekly", "coin_cost": 150, "condition_description": "Solo en semanas perfectas (100% misiones)", "requires_perfect_week": True},
        {"name": "Cerveza fria 1 litro", "reward_type": "weekly", "coin_cost": 80, "condition_description": "10 km acumulados esa semana", "requires_km": 10},
        {"name": "Cheat meal libre (1 comida)", "reward_type": "weekly", "coin_cost": 60, "condition_description": "Racha de 7 dias activos", "requires_streak": 7},
        {"name": "1 hora de videojuegos", "reward_type": "weekly", "coin_cost": 25, "condition_description": "80% de misiones completadas", "min_weekly_completion": 0.8},
        {"name": "Maraton serie o pelicula 3h", "reward_type": "weekly", "coin_cost": 40, "condition_description": "80% de misiones completadas", "min_weekly_completion": 0.8},
        {"name": "Dia de descanso total sin ejercicio", "reward_type": "weekly", "coin_cost": 100, "condition_description": "Racha de 14 dias activos", "requires_streak": 14},
        # Hitos
        {"name": "Hito 100 kg: Salida a restaurante sin restriccion", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 100 kg", "milestone_kg": 100.0},
        {"name": "Hito 100 kg: Compra setup gamer (max $300)", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 100 kg", "milestone_kg": 100.0},
        {"name": "Hito 100 kg: Noche de videojuegos 5 horas", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 100 kg", "milestone_kg": 100.0},
        {"name": "Hito 95 kg: Ropa nueva (una prenda)", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 95 kg", "milestone_kg": 95.0},
        {"name": "Hito 95 kg: Salida con amigos sin restriccion de bebidas", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 95 kg", "milestone_kg": 95.0},
        {"name": "Hito 95 kg: Gadget o accesorio (max $500)", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 95 kg", "milestone_kg": 95.0},
        {"name": "Hito 90 kg: Fin de semana sin misiones", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 90 kg", "milestone_kg": 90.0},
        {"name": "Hito 90 kg: Experiencia especial (concierto o evento)", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 90 kg", "milestone_kg": 90.0},
        {"name": "Hito 90 kg: Compra personal libre (max $1,000)", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 90 kg", "milestone_kg": 90.0},
        {"name": "Hito Final 85 kg: Darkial Absoluto — lo que el usuario decida", "reward_type": "milestone", "coin_cost": 0, "condition_description": "Llegar a 85 kg — meta final", "milestone_kg": 85.0},
    ]

    for r in rewards:
        db.add(models.Reward(**r))

    # ────────────────────────────────────────────────────────────────
    # 4. LOGROS
    # ────────────────────────────────────────────────────────────────
    achievements = [
        # Peso
        {"name": "Primer kilo perdido", "description": "Registrar 104 kg por primera vez", "achievement_type": "weight", "condition_value": 104.0, "xp_reward": 100},
        {"name": "Hito 100 kg", "description": "Llegar a 100 kg", "achievement_type": "weight", "condition_value": 100.0, "xp_reward": 300},
        {"name": "Hito 95 kg", "description": "Llegar a 95 kg", "achievement_type": "weight", "condition_value": 95.0, "xp_reward": 500},
        {"name": "Hito 90 kg", "description": "Llegar a 90 kg", "achievement_type": "weight", "condition_value": 90.0, "xp_reward": 800},
        {"name": "Darkial Absoluto", "description": "Llegar a 85 kg — meta final", "achievement_type": "weight", "condition_value": 85.0, "xp_reward": 2000, "is_legendary": True},
        # Racha
        {"name": "Primera semana", "description": "7 dias activos consecutivos", "achievement_type": "streak", "condition_value": 7, "xp_reward": 150},
        {"name": "Mes completo", "description": "30 dias activos consecutivos", "achievement_type": "streak", "condition_value": 30, "xp_reward": 400},
        {"name": "100 dias activos", "description": "100 dias activos acumulados", "achievement_type": "streak", "condition_value": 100, "xp_reward": 800},
        {"name": "150 dias activos", "description": "150 dias activos acumulados", "achievement_type": "streak", "condition_value": 150, "xp_reward": 1200},
        # Misiones
        {"name": "Dia perfecto", "description": "Completar todas las misiones del dia", "achievement_type": "missions", "condition_value": 1, "xp_reward": 50},
        {"name": "10 dias perfectos", "description": "Acumular 10 dias perfectos", "achievement_type": "missions", "condition_value": 10, "xp_reward": 300},
        {"name": "Conocimiento total", "description": "Completar 50 misiones de conocimiento", "achievement_type": "missions", "condition_value": 50, "xp_reward": 500},
        # Legendarios
        {"name": "El camino del guerrero", "description": "Completar las 7 misiones jefe", "achievement_type": "legendary", "condition_value": 7, "xp_reward": 3000, "is_legendary": True},
        {"name": "Sin caer", "description": "60 dias consecutivos sin bajar de nivel", "achievement_type": "legendary", "condition_value": 60, "xp_reward": 1000, "is_legendary": True},
    ]

    for a in achievements:
        db.add(models.Achievement(**a))

    # ────────────────────────────────────────────────────────────────
    # 5. USUARIO INICIAL (Darkial)
    # ────────────────────────────────────────────────────────────────
    user = models.User(
        name="Darkial",
        weight_current=105.0,
        weight_goal=85.0,
        height_cm=182,
        level=1,
        xp_current=0,
        xp_total=0,
        coins=0,
        streak_days=0,
        active_days_total=0,
        evolution_state=0,
        shield_available=True,
        shield_used_this_month=False,
        fault_points_week=0,
    )
    db.add(user)

    db.commit()
    print(f"Seed completado:")
    print(f"  - {len(missions)} misiones fijas")
    print(f"  - {len(knowledge)} actividades de conocimiento")
    print(f"  - {len(rewards)} recompensas")
    print(f"  - {len(achievements)} logros")
    print(f"  - Usuario Darkial creado")
    db.close()

if __name__ == "__main__":
    seed()