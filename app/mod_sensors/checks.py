def sensor_checks():
    """
    Finds observations in the database of "problem rooms" with 
    occupancy predicted but no sensor checks triggering and 
    changes them.
    """
    
    # Rooms with a "leaking" effect, determined in /stats/problem_rooms.py.
    problem_rooms = ["B004", "B002", "B003"]

    # Select from database where room in problem_rooms, counts_predicted_is_occupied != 0 and time = xx:15
        # Read sensors table for that hour where both checks are 0.
            # Change counts_predicted_is_occupied to 0 at those times. 
