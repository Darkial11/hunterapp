import './Routine.css'

const ROUTINE = {
  1: { // Lunes
    exercise: 'Espalda y bíceps',
    meals: [
      { time: '06:30', label: 'Desayuno', kcal: '~350 kcal', content: '3 huevos revueltos con morrón, jitomate y cebolla + 2 tortillas' },
      { time: '11:00', label: 'Colación', kcal: '~200 kcal', content: 'Manzana + almendras (20g)' },
      { time: '14:30', label: 'Comida', kcal: '~900 kcal', content: 'Pechuga de pollo a la plancha + 3 tortillas + ensalada jitomate/cebolla/morrón' },
      { time: '20:00', label: 'Cena', kcal: '~200-400 kcal', content: 'Atún en lata con jitomate y cebolla' },
    ]
  },
  2: { // Martes
    exercise: 'Pecho y tríceps',
    meals: [
      { time: '06:30', label: 'Desayuno', kcal: '~350 kcal', content: '3 huevos — omelette con morrón, cebolla + 1 rebanada jamón + 1 tortilla' },
      { time: '11:00', label: 'Colación', kcal: '~200 kcal', content: 'Mandarina + nueces (20g)' },
      { time: '14:30', label: 'Comida', kcal: '~900 kcal', content: 'Bistec de res a la plancha + frijoles de olla + 3 tortillas + jitomate' },
      { time: '20:00', label: 'Cena', kcal: '~200-400 kcal', content: 'Jitomate + queso seco + cebolla + jalapeño + 1 tostada' },
    ]
  },
  3: { // Miércoles
    exercise: 'Descanso',
    meals: [
      { time: '06:30', label: 'Desayuno', kcal: '~350 kcal', content: '3 huevos revueltos con morrón y cebolla + 2 tortillas' },
      { time: '11:00', label: 'Colación', kcal: '~200 kcal', content: 'Jícama con limón y chile' },
      { time: '14:30', label: 'Comida', kcal: '~900 kcal', content: 'Pechuga de pollo a la plancha + 3 tortillas + ensalada jitomate/cebolla/morrón' },
      { time: '20:00', label: 'Cena', kcal: '~200-400 kcal', content: 'Atún en lata con jitomate y cebolla' },
    ]
  },
  4: { // Jueves
    exercise: 'Pierna',
    meals: [
      { time: '06:30', label: 'Desayuno', kcal: '~350 kcal', content: '3 huevos revueltos con morrón y cebolla + 2 tortillas' },
      { time: '11:00', label: 'Colación', kcal: '~200 kcal', content: 'Manzana + almendras (20g)' },
      { time: '14:30', label: 'Comida', kcal: '~900 kcal', content: 'Bistec de res a la plancha + frijoles de olla + 3 tortillas + jitomate' },
      { time: '20:00', label: 'Cena', kcal: '~200-400 kcal', content: 'Jitomate + queso seco + cebolla + jalapeño + 1 tostada' },
    ]
  },
  5: { // Viernes
    exercise: 'Hombros y abdomen',
    meals: [
      { time: '06:30', label: 'Desayuno', kcal: '~350 kcal', content: '3 huevos — omelette con morrón, cebolla + 1 rebanada jamón + 1 tortilla' },
      { time: '11:00', label: 'Colación', kcal: '~200 kcal', content: 'Mandarina + nueces (20g)' },
      { time: '14:30', label: 'Comida', kcal: '~900 kcal', content: 'Salmón a la plancha + verduras salteadas (morrón, cebolla, jitomate) + 2 tortillas' },
      { time: '20:00', label: 'Cena', kcal: '~200-400 kcal', content: 'Libre o ligera' },
    ]
  },
  6: { // Sábado
    exercise: 'Día libre',
    meals: []
  },
  0: { // Domingo
    exercise: 'Día libre',
    meals: []
  },
}

const DAY_NAMES = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

const MEAL_COLORS = {
  'Desayuno': '#51cf66',
  'Colación': '#f0c040',
  'Comida': '#4a9eff',
  'Cena': '#cc5de8',
}

export default function Routine() {
  const today = new Date()
  const dayOfWeek = today.getDay()
  const dayName = DAY_NAMES[dayOfWeek]
  const routine = ROUTINE[dayOfWeek]

  return (
    <div className="routine">
      <div className="routine-header">
        <h1>Rutina del día</h1>
        <div className="routine-day">{dayName}</div>
      </div>

      {/* Ejercicio */}
      <div className="routine-exercise-card">
        <div className="routine-section-label">💪 Ejercicio — 05:30</div>
        <div className={`routine-exercise-name ${routine.exercise === 'Descanso' || routine.exercise === 'Día libre' ? 'rest' : ''}`}>
          {routine.exercise}
        </div>
      </div>

      {/* Macros del día */}
      <div className="routine-macros">
        <div className="macro-card">
          <div className="macro-value">~2,750</div>
          <div className="macro-label">kcal meta</div>
        </div>
        <div className="macro-card">
          <div className="macro-value">~500</div>
          <div className="macro-label">déficit</div>
        </div>
        <div className="macro-card">
          <div className="macro-value">~0.5 kg</div>
          <div className="macro-label">pérdida/semana</div>
        </div>
      </div>

      {/* Comidas */}
      {routine.meals.length > 0 ? (
        <div className="routine-meals">
          <div className="routine-section-label">🍽️ Plan alimenticio</div>
          {routine.meals.map((meal, i) => (
            <div key={i} className="meal-card">
              <div className="meal-time-col">
                <div className="meal-time">{meal.time}</div>
                <div
                  className="meal-label"
                  style={{ color: MEAL_COLORS[meal.label] }}
                >
                  {meal.label}
                </div>
                <div className="meal-kcal">{meal.kcal}</div>
              </div>
              <div className="meal-content">{meal.content}</div>
            </div>
          ))}
        </div>
      ) : (
        <div className="routine-free-day">
          <div className="free-day-icon">🎮</div>
          <div className="free-day-text">Día libre — descansa y recarga energía</div>
          <div className="free-day-sub">La nutrición sigue siendo importante hoy</div>
        </div>
      )}

      {/* Nota */}
      <div className="routine-note">
        --------
      </div>
    </div>
  )
}