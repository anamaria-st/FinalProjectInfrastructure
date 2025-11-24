from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from .models import db, User, Habit, HabitCompletion
from datetime import date, datetime, timedelta
import calendar

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return redirect(url_for("main.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        # 1. Validar passwords iguales
        if password != confirm:
            return render_template("register.html", error="Passwords do not match")

        # 2. Validar usuario repetido
        existing = User.query.filter_by(username=username).first()
        if existing:
            return render_template("register.html", error="Username already exists")

        # 3. Crear usuario nuevo
        new_user = User(username=username)
        new_user.set_password(password)  # tu modelo debe tener esta función

        db.session.add(new_user)
        db.session.commit()

        return render_template("register.html", success=True)

    return render_template("register.html")



@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main.dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


def current_user():
    uid = session.get("user_id")
    if uid is None:
        return None
    return User.query.get(uid)


def login_required():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))


@bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    return render_template("dashboard.html")


@bp.route("/habits/<category>")
def habits_by_category(category):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()
    if user is None:
        return redirect(url_for("main.login"))

    valid_categories = {
        "physical": "Physical health",
        "mental": "Mental",
        "social": "Social",
        "hobbies": "Hobbies",
    }
    if category not in valid_categories:
        return redirect(url_for("main.dashboard"))

    # Obtener hábitos de ese usuario y categoría
    habits = (
        Habit.query.filter_by(user_id=user.id, category=category)
        .order_by(Habit.id.asc())
        .all()
    )

    # Mapear iconos según categoría (ajusta nombres de archivo)
    icon_map = {
        "physical": "cardio.png",
        "mental": "mental.png",
        "social": "social.png",
        "hobbies": "hobbies.png",
    }

    return render_template(
        "habits_list.html",
        category=category,
        category_label=valid_categories[category],
        icon_filename=icon_map[category],
        habits=habits,
    )


# Ruta simple para crear un hábito de ejemplo (puedes añadir un formulario más adelante)
@bp.route("/habits/<category>/add", methods=["POST"])
def add_habit(category):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()
    name = request.form.get("name", "Example text loremipsum")
    periodicity = request.form.get("periodicity", "every week")
    frequency = request.form.get("frequency", "Monday")

    habit = Habit(
        user_id=user.id,
        category=category,
        name=name,
        periodicity=periodicity,
        frequency=frequency,
    )
    db.session.add(habit)
    db.session.commit()

    return redirect(url_for("main.habits_by_category", category=category))

@bp.route("/habits/<category>/new", methods=["GET", "POST"])
def new_habit(category):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()

    valid_categories = {
        "physical": "Physical health",
        "mental": "Mental",
        "social": "Social",
        "hobbies": "Hobbies",
    }

    if category not in valid_categories:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        periodicity = request.form.get("periodicity")
        frequency = request.form.get("frequency")
        category_from_form = request.form.get("category")

        habit = Habit(
            user_id=user.id,
            category=category_from_form,
            name=name,
            periodicity=periodicity,
            frequency=frequency,
        )
        db.session.add(habit)
        db.session.commit()

        return redirect(url_for("main.habits_by_category", category=category_from_form))

    return render_template(
        "habit_form.html",
        mode="new",
        category=category,
        category_label=valid_categories[category],
    )

@bp.route("/habits/<int:habit_id>/edit", methods=["GET", "POST"])
def edit_habit(habit_id):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if not habit:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        habit.name = request.form.get("name")
        habit.category = request.form.get("category")
        habit.periodicity = request.form.get("periodicity")
        habit.frequency = request.form.get("frequency")

        db.session.commit()
        return redirect(url_for("main.habits_by_category", category=habit.category))

    # GET → mostrar formulario con los datos previos
    valid_categories = {
        "physical": "Physical health",
        "mental": "Mental",
        "social": "Social",
        "hobbies": "Hobbies",
    }

    return render_template(
        "habit_form.html",
        mode="edit",
        habit=habit,
        category=habit.category,
        category_label=valid_categories[habit.category],
    )


@bp.route("/habits/<int:habit_id>/delete")
def delete_habit(habit_id):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if habit:
        db.session.delete(habit)
        db.session.commit()

    return redirect(url_for("main.habits_by_category", category=habit.category))

@bp.route("/calendar")
def calendar_view():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    user = current_user()

    today = date.today()
    year = today.year
    month = today.month

    # Crear matriz del mes
    cal = calendar.Calendar(firstweekday=0)
    month_days = list(cal.itermonthdates(year, month))

    # Habits del usuario agrupados por categoría
    habits = Habit.query.filter_by(user_id=user.id).all()

    # Mapa de colores por categoría
    category_colors = {
        "physical": "#FFE5B4",
        "mental": "#9cc7f5",
        "social": "#76b34e",
        "hobbies": "#f48aa2",
    }

    # Puntos en calendario → por día
    dots = {d: [] for d in month_days}

    for habit in habits:

        # Every day → mark all days
        if habit.periodicity == "everyday":
            for d in month_days:
                dots[d].append(category_colors[habit.category])
            continue

        # Every week → match weekday (Monday, Tuesday, etc.)
        if habit.periodicity == "every week":
            for d in month_days:
                if d.strftime("%A").lower() == habit.frequency.lower():
                    dots[d].append(category_colors[habit.category])
            continue

        # Every month → e.g., "3rd week"
        if habit.periodicity == "every month":
            week_number = int(habit.frequency[0])  # 1, 2, 3, 4, 5...
            
            # Calculate weeks
            weeks = []
            current_week = []
            start_weekday = month_days[0].weekday()

            for day in month_days:
                if day.weekday() == 0 and current_week:
                    weeks.append(current_week)
                    current_week = []
                current_week.append(day)
            if current_week:
                weeks.append(current_week)

            # Place dot on any day in that week (usually Monday)
            if week_number <= len(weeks):
                target_day = weeks[week_number - 1][0]  # Monday of that week
                dots[target_day].append(category_colors[habit.category])

            continue


    # Hábitos de hoy
    todays_habits = []
    today = date.today()

    for habit in habits:

        # EVERY DAY
        if habit.periodicity == "everyday":
            todays_habits.append(habit)
            continue

        # EVERY WEEK
        if habit.periodicity == "every week":
            if today.strftime("%A").lower() == habit.frequency.lower():
                todays_habits.append(habit)
            continue

        # EVERY MONTH
        if habit.periodicity == "every month":

            # obtener número de semana actual del mes
            month_start = date(today.year, today.month, 1)
            week_index_today = ((today.day - 1 + month_start.weekday()) // 7) + 1

            # frequency → "1st week", "2nd week", etc.
            habit_week = int(habit.frequency[0])

            if week_index_today == habit_week:
                todays_habits.append(habit)

            continue


    return render_template(
        "calendar.html",
        today=today,
        month_days=month_days,
        year=year,
        month=calendar.month_name[month],
        dots=dots,
        todays_habits=todays_habits,
        category_colors=category_colors
    )

@bp.post("/habit/<int:habit_id>/toggle")
def toggle_habit(habit_id):
    today = date.today()

    entry = HabitCompletion.query.filter_by(
        habit_id=habit_id,
        date=today
    ).first()

    if entry:
        db.session.delete(entry)
    else:
        db.session.add(HabitCompletion(habit_id=habit_id, date=today))

    db.session.commit()
    return redirect(url_for("main.calendar_view"))

