"""
Log Entries Blueprint Module

Contains routes related to log entries

Routes:

    url_prefix: '/logs'

    GET '/me/<int:car_id>/' : get the user's logs for the selected car

    POST '/me/<int:car_id>/' : add a new log for the selected car

    PUT/PATCH '/me/<int:car_id>/<int:log_id>/' : update the selected log for the user car

    DELETE '/me/<int:car_id>/<int:log_id>/' : delete the selected log entry for the user car

    POST '/me/<int:car_id>/trip/calculator/' : adds a trip to the trips entity and 
    calulates the trip cost

    GET '/me/<int:car_id>/trips/' : get the trips for a user car

    DELETE '/me/<int:car_id>/trips/<int:trip_id>' : delete the selected trip for the user car

    PUT/PATCH '/me/<int:car_id>/trips/<int:trip_id>' : update the selected trip for the user car

    GET '/me/<int:car_id>/expenditure/from/<int:from_day>/<int:from_month>/<int:from_year>/to/
    <int:to_day>/<int:to_month>/<int:to_year>/' : get the expenditure summary for a time period
"""
from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.log import LogEntry, LogEntrySchema, ExpenditureSchema, ExpenditureCompareSchema
from models.car import CarSchema
from models.trip import Trip, TripSchema
from models.user_car import UserCarSchema
from blueprints.auth_bp import verify_user_car, verify_user

log_bp = Blueprint('log', __name__, url_prefix='/logs')

# get user's log for selected car
@log_bp.route('/me/<int:car_id>/')
@jwt_required()
def get_log_entries(car_id):
    """
    Log Entries for car

    Get all the log entries for specified user car

    Variables:

            <car_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # query the database and filter logs by user_car_id
        stmt = db.select(LogEntry).filter_by(user_car_id=user_car.id)
        log_entries = db.session.scalars(stmt).all()
        if log_entries:
            return LogEntrySchema(many=True).dump(log_entries)
        return {'not_found': 'No log entries for user car'}, 404
    return {'not_found': 'User car not found'}, 404

# get a single log for selected car
@log_bp.route('/me/<int:car_id>/<int:log_id>/')
@jwt_required()
def get_log_entry(car_id, log_id):
    """
    Log Entry for car

    Get a log entries for specified user car

    Variables:

            <car_id> (int)
            <log_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # query the database and filter logs by user_car_id and log_id
        stmt = db.select(LogEntry).filter_by(user_car_id=user_car.id).filter_by(id=log_id)
        log_entry = db.session.scalar(stmt)
        if log_entry:
            return LogEntrySchema().dump(log_entry)
        return {'not_found': 'Log entry not found for user car'}, 404
    return {'not_found': 'User car not found'}, 404

# add a new log
@log_bp.route('/me/<int:car_id>/', methods=['POST'])
@jwt_required()
def add_log_entry(car_id):
    """
    Add Log Entry

    Add a log entry for the specified user car

    Variables:

            <car_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # load the requeest body to the log entry schema
        log_entry_info = LogEntrySchema().load(request.json)
        # create a new log entry
        new_log_entry = LogEntry(
            current_odo= log_entry_info['current_odo'],
            fuel_quantity= log_entry_info['fuel_quantity'],
            fuel_price= log_entry_info['fuel_price'],
            user_car_id= car_id
        )
        # add and commit new log entry
        db.session.add(new_log_entry)
        db.session.commit()
        return LogEntrySchema().dump(new_log_entry)
    return {'not_found':  "User car not found"}, 404

# update a log entry
@log_bp.route('/me/<int:car_id>/<int:log_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_log_entry(car_id, log_id):
    """
    Update Log Entry

    Update an existing log entry for the specified user car

    Variables:

            <car_id> (int)

            <log_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # search for the log entry
        stmt = db.select(LogEntry).filter_by(id=log_id)
        log_entry = db.session.scalar(stmt)
        if log_entry:
            # load the reponse to the Log Entry Schema
            log_info = LogEntrySchema().load(request.json)
            # update the log entry fields
            log_entry.current_odo = log_info.get('current_odo', log_entry.current_odo)
            log_entry.fuel_quantity = log_info.get('fuel_quantity', log_entry.fuel_quantity)
            log_entry.fuel_price = log_info.get('fuel_price', log_entry.fuel_price)
            log_entry.user_car_id = car_id
            # commit the update
            db.session.commit()
            return LogEntrySchema().dump(log_entry)
        return {'not_found': 'Log entry not found'}, 404
    return {'not_found': 'User car not found'}, 404

# delete a log entry
@log_bp.route('/me/<int:car_id>/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log_entry(car_id, log_id):
    """
    Delete Log Entry

    Delete and existing log entry for the specified user car

    Variables:

            <car_id> (int)

            <log_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # search for the log entry
        stmt = db.select(LogEntry).filter_by(id=log_id)
        log_entry = db.session.scalar(stmt)
        if log_entry:
            # delete the log and commit
            db.session.delete(log_entry)
            db.session.commit()
            return {'deleted': 'Log entry deleted from user car'}
        return {'not_found': 'Log entry not found'}, 404
    return {'not_found': 'User car not found'}, 404

# calculate the average consumption
# calculate the trip cost
@log_bp.route('/me/<int:car_id>/trip/calculator/', methods=['POST'])
@jwt_required()
def calculate_avg_consuption(car_id):
    """
    Trip calculator and Average Consumption

    Calculates the average fuel consumption. Queries the database for the last 2 log entries
    and calculates the distance between fill ups.

    Calculates how much fuel was used from previous fills.

    Average will only be calculated once there is more than 2 log entries for the user car.

    The trip calculator relies on the average. Once the average can be calculated, the trip
    cost will be calculated based on the average.

    Variables:

            <car_id> (int)

    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    # query the database for user car's id
    user_car = verify_user_car(car_id)
    if user_car:
        # filter the log entries using the user car id, order by date added
        stmt = db.select(LogEntry).filter_by(
                                    user_car_id=car_id
                                ).order_by(LogEntry.date_added.desc())
        log_entries = db.session.scalars(stmt).all()
        if len(log_entries) > 2:
            # load the request body to the trip schema
            trip_info = TripSchema().load(request.json)
            # see if the trip exists already, if it does, skip the adding part (avoid dulplicates)
            stmt = db.select(Trip).where(
                db.and_(
                    Trip.fuel_price == trip_info['fuel_price'],
                    Trip.distance == trip_info['distance'],
                    Trip.user_car_id == car_id
                )
            )
            check_trip = db.session.scalar(stmt)
            if not check_trip:
            # add a new trip
                new_trip = Trip(
                    fuel_price= trip_info['fuel_price'],
                    distance= trip_info['distance'],
                    user_car_id= car_id
                )
                # add and commit the trip
                db.session.add(new_trip)
                db.session.commit()
            # if trip exists, assign to new_trip
            new_trip = check_trip
            # last 2 entries are in list position's 0 and 1
            # calculate the distance travelled from one fill up
            # gather as many data points for distance travelled
            distance_travelled = log_entries[0].current_odo - log_entries[-2].current_odo
            # average fuel consumed from last fill up
            # is isn't the real average consumption as the fuel left in the tank isn't recorded
            # fuel total
            total_fuel = 0
            for index in range(1, len(log_entries) - 1):
                total_fuel += log_entries[index].fuel_quantity
            # average consumption
            avg_consumption = (total_fuel) / (distance_travelled / 100)
            # esitmated fuel needed for trip
            trip_fuel = avg_consumption * (trip_info['distance'] / 100)
            # estimated trip cost
            trip_cost = trip_fuel * trip_info['fuel_price']
            return {
                'avg_consumption': f"{format(avg_consumption, '.2f')} L/100km",
                'estimated_trip_fuel': f"{format(trip_fuel, '.2f')} L",
                'esitmated_trip_cost': f"${format(trip_cost, '.2f')}",
                'car': CarSchema(exclude=['id', 'user_car']).dump(user_car.car)
            }
        return {
            'calc_error': 'Unable to calc average consumption due to num of log entries present',
            'log_entries_required': 'Require more than 2 log entries for user car'
        }, 400
    return {'not_found': 'User car not found'}

# get trips for user car
@log_bp.route('/me/<int:car_id>/trips/')
@jwt_required()
def get_all_trips(car_id):
    """
    Get Trips

    Get all trips related to the specified user car

    Variables:

            <car_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    user = verify_user_car(car_id)
    # query the database and filter by car_id
    stmt = db.select(Trip).filter_by(user_car_id=car_id)
    all_trips = db.session.scalars(stmt).all()
    if user:
        if all_trips:
            # get the user's trips and place in a list
            user_trips = [trip for trip in all_trips if trip.usercar.user_id == get_jwt_identity()]
            return TripSchema(many=True, exclude=['usercar']).dump(user_trips)
        return {'not_found': 'User car has no trips'}, 404
    return {'not_found': 'User car not found'}, 404

# get a trip for user car
@log_bp.route('/me/<int:car_id>/trips/<int:trip_id>/')
@jwt_required()
def get_a_trip(car_id, trip_id):
    """
    Get a Trip

    Get a trip related to the specified user car

    Variables:

            <car_id> (int)
            <trip_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    user = verify_user_car(car_id)
    # query the database and filter by car_id, trip_id
    stmt = db.select(Trip).filter_by(user_car_id=car_id).filter_by(id=trip_id)
    trip = db.session.scalar(stmt)
    if user:
        if trip:
            # get the user's id
            if trip.usercar.user_id == get_jwt_identity():
                return TripSchema(exclude=['usercar']).dump(trip)
        return {'not_found': 'User car trip not found'}, 404
    return {'not_found': 'User car not found'}, 404

# delete trips
@log_bp.route('/me/<int:car_id>/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trips(car_id, trip_id):
    """
    Delete trips

    Allows the user to delete a trip for the specified user car

    Variables:

            <car_id> (int)

            <trip_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    user = verify_user_car(car_id)
    # query the database
    stmt = db.select(Trip).filter_by(id=trip_id)
    trip = db.session.scalar(stmt)
    if user:
        if trip and trip.usercar.user_id == get_jwt_identity() and trip.user_car_id == car_id:
            # delete the trip and commit
            db.session.delete(trip)
            db.session.commit()
            return {'deleted': 'Trip successfully deleted'}
        return {'not_found': 'User car trip does not exsist'}, 404
    return {'not_found': 'User car not found'}, 404

# update trips
@log_bp.route('/me/<int:car_id>/trips/<int:trip_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_trips(car_id, trip_id):
    """
    Update trips

    Allows the user to update a trip for the specified user car

    Variables:

            <car_id> (int)

            <trip_id> (int)
    """
    # verify the user
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403
    user = verify_user_car(car_id)
    # query the database
    stmt = db.select(Trip).filter_by(id=trip_id)
    trip = db.session.scalar(stmt)
    if user:
        if trip and trip.usercar.user_id == get_jwt_identity() and trip.user_car_id == car_id:
            # load the request body to the trip schema
            trip_info = TripSchema().load(request.json)
            # update the trip
            trip.fuel_price = trip_info.get('fuel_price', trip.fuel_price)
            trip.distance = trip_info.get('distance', trip.distance)
            trip.user_car_id = car_id
            # commit the update
            db.session.commit()
            return TripSchema(exclude=['usercar']).dump(trip)
        return {'not_found': 'User car trip does not exist'}, 404
    return {'not_found': 'User car not found'}, 404

# expenditure summary
@log_bp.route(
    '/me/<int:car_id>/expenditure/', methods=['POST']
)
@jwt_required()
def expenditure_summary(car_id):
    """
    Expenditure Summary

    Allows the user to generate an expenditure report for the specified time period

    Variables:

            <car_id> (int)
    """
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403

    dates = ExpenditureSchema().load(request.json)
    # convert "from" date to format stored in database "unix"
    from_date = datetime(
        int(dates['from_date'].strftime("%Y")),
        int(dates['from_date'].strftime("%m")),
        int(dates['from_date'].strftime("%d"))
    ).timestamp()
    # 'to' date
    to_date = datetime(
        int(dates['to_date'].strftime("%Y")),
        int(dates['to_date'].strftime("%m")),
        int(dates['to_date'].strftime("%d"))
    ).date()

    # if "to" date is the same as the current date
    # assign it using the .now() function
    if to_date == datetime.now().date():
        to_date = datetime.now()
    else:
        to_date = datetime(
            int(dates['to_date'].strftime("%Y")),
            int(dates['to_date'].strftime("%m")),
            int(dates['to_date'].strftime("%d"))
        )
    # convert "to" date to timestamp
    to_date = to_date.timestamp()
    if to_date < from_date:
        return {"logic_error": "to_date must be after from_date"}, 400
    # filter the logs using the to and from dates
    stmt = db.select(LogEntry).where(
        db.and_(
            LogEntry.date_added <= to_date,
            LogEntry.date_added >= from_date
        )
    )
    logs_for_period = db.session.scalars(stmt).all()
    # verify the user is allowed to access the logs
    user = verify_user_car(car_id)
    if user:
        if logs_for_period:
            # filter out the logs that belong to the user and car
            user_logs_for_period = [log for log in logs_for_period if log.user_car_id == car_id]
            # calculate the total cost for the period and total distance
            total_cost = 0
            total_distance = user_logs_for_period[-1].current_odo \
                                    - user_logs_for_period[0].current_odo
            for log in user_logs_for_period:
                total_cost += log.fuel_price * log.fuel_quantity


            return {
                    'total_cost_for_period': f"${format(total_cost, '.2f')}",
                    'total_distance_for_period': f"{total_distance} km",
                    "expenditure_summary_for" : ExpenditureSchema().dump(dates),
                    'user_car': UserCarSchema(only=['car']).dump(user)
            }
        return {'not_found': 'No expenditure for period specified'}, 404
    return{'not_found': 'User car not found'}, 404

# expanditure compare
@log_bp.route(
    '/me/<int:car_id>/expenditure/compare/', methods=['POST']
)
@jwt_required()
def expenditure_compare(car_id):
    """
    Expenditure Compare

    Allows the user to compare expenditure reports for specified time periods

    Variables:

            <car_id> (int)
    """
    user = verify_user()
    if not user:
        return {"forbidden": "You must be logged in to access resource"}, 403

    dates = ExpenditureCompareSchema().load(request.json)
    # convert "from" date to format stored in database "unix"
    from_date = datetime(
        int(dates['from_date'].strftime("%Y")),
        int(dates['from_date'].strftime("%m")),
        int(dates['from_date'].strftime("%d"))
    ).timestamp()
    # 'to' date placed into datetime
    to_date = datetime(
        int(dates['to_date'].strftime("%Y")),
        int(dates['to_date'].strftime("%m")),
        int(dates['to_date'].strftime("%d"))
    ).date()
    # convert "compare_from" date to format stored in database "unix"
    compare_from_date = datetime(
        int(dates['compare_from_date'].strftime("%Y")),
        int(dates['compare_from_date'].strftime("%m")),
        int(dates['compare_from_date'].strftime("%d"))
    ).timestamp()
    # 'compare_to' date placed into datetime
    compare_to_date = datetime(
        int(dates['compare_to_date'].strftime("%Y")),
        int(dates['compare_to_date'].strftime("%m")),
        int(dates['compare_to_date'].strftime("%d"))
    ).date()

    # if "to" dates are the same as the current date
    # assign them using the .now() function
    if to_date == datetime.now().date() or compare_to_date == datetime.now().date():
        to_date = datetime.now()
        compare_to_date = datetime.now()
    else:
        to_date = datetime(
            int(dates['to_date'].strftime("%Y")),
            int(dates['to_date'].strftime("%m")),
            int(dates['to_date'].strftime("%d"))
        )
        compare_to_date = datetime(
            int(dates['compare_to_date'].strftime("%Y")),
            int(dates['compare_to_date'].strftime("%m")),
            int(dates['compare_to_date'].strftime("%d"))
        )
    # convert "to" dates to timestamp
    to_date = to_date.timestamp()
    compare_to_date = compare_to_date.timestamp()
    if to_date < from_date or compare_to_date < compare_from_date:
        return {"logic_error": "to_date and compared_to_date must be after from_dates"}, 400
    # filter the logs using the to and from dates
    stmt = db.select(LogEntry).where(
        db.and_(
            LogEntry.date_added <= to_date,
            LogEntry.date_added >= from_date
        )
    )
    logs_for_period_one = db.session.scalars(stmt).all()
    # filter the logs using the "compare" to and from dates
    stmt2 = db.select(LogEntry).where(
        db.and_(
            LogEntry.date_added <= compare_to_date,
            LogEntry.date_added >= compare_from_date
        )
    )
    logs_for_period_two = db.session.scalars(stmt2).all()
    # verify the user is allowed to access the logs
    user = verify_user_car(car_id)
    if user:
        if logs_for_period_one and logs_for_period_two:
            # filter out the logs that belong to the user and car
            user_logs_for_period_one = [
                log for log in logs_for_period_one if log.user_car_id == car_id
            ]
            user_logs_for_period_two = [
                log for log in logs_for_period_two if log.user_car_id == car_id
            ]
            # calculate the total costs and distances for the periods
            total_cost_one = 0
            total_cost_two = 0
            total_distance_one = user_logs_for_period_one[-1].current_odo \
                                    - user_logs_for_period_one[0].current_odo
            total_distance_two = user_logs_for_period_two[-1].current_odo \
                                    - user_logs_for_period_two[0].current_odo

            for log in user_logs_for_period_one:
                total_cost_one += log.fuel_price * log.fuel_quantity
            for log in user_logs_for_period_two:
                total_cost_two += log.fuel_price * log.fuel_quantity


            return {
                "period_one" : {
                    "expenditure_summary_for" : ExpenditureCompareSchema(
                                                        only=['to_date', 'from_date']
                                                ).dump(dates),
                    'total_cost_for_period': f"${format(total_cost_one, '.2f')}",
                    'total_distance_for_period': f"{total_distance_one} km",
                    'user_car': UserCarSchema(only=['car']).dump(user)
                },
                "period_two" : {
                    "expenditure_summary_for" : ExpenditureCompareSchema(
                                                        exclude=['to_date', 'from_date']
                                                ).dump(dates),
                    'total_cost_for_period': f"${format(total_cost_two, '.2f')}",
                    'total_distance_for_period': f"{total_distance_two} km",
                    'user_car': UserCarSchema(only=['car']).dump(user)
                }
            }
        return {'not_found': 'No expenditure for periods specified'}, 404
    return{'not_found': 'User car not found'}, 404
