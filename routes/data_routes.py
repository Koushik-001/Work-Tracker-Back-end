from database import tasks_collection
from schema.taskSchema import TaskSchema
from fastapi import APIRouter, HTTPException
from datetime import datetime,timedelta
from bson import ObjectId
from serializer.serialize import serialize,serializeAll
root = APIRouter()

@root.post("/new_task")
async def addData(task: TaskSchema):
    # Convert task to a dictionary for insertion
    task_dict = dict(task)
    new_task = tasks_collection.insert_one(task_dict)
    
    return {
        "message": "Data insertion success",
        "task_id": str(new_task.inserted_id)  # Return the inserted task ID
    }

@root.get("/alltasks")
async def newTask():
    try:
        data = tasks_collection.find()
        serialized_data = serializeAll(data)
        return serialized_data
    except Exception as e:  # Catch all exceptions
        raise HTTPException(status_code=500, detail=str(e))

@root.patch("/update_time/{key}/{task_id}")
async def update_time(key: str, task_id: str):
    # Validate the key parameter
    valid_keys = ["start", "end"]
    if key not in valid_keys:
        raise HTTPException(status_code=400, detail="Invalid key. Use 'start' or 'end'.")

    # Get the current time and format it
    current_time = datetime.now()
    formatted_time = current_time.isoformat()
    day_of_week = current_time.strftime("%A")

    # Determine the field to update
    update_field = "start_time" if key == "start" else "end_time"
    
    # Fetch the existing task from the database
    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    # Initialize daily_work_track if it doesn't exist
    daily_work_track = updated_task.get("daily_work_track", {})
    if daily_work_track is None:
        daily_work_track = {}

    if key == "start":
        # Update start time in daily_work_track
        daily_work_track[day_of_week] = {
            "start_time": formatted_time,
            "end_time": daily_work_track.get(day_of_week, {}).get("end_time", "")
        }
    elif key == "end":
        # Check if start time is already set for today
        if day_of_week not in daily_work_track or not daily_work_track[day_of_week].get("start_time"):
            raise HTTPException(status_code=400, detail="Start time not set for today.")

        # Update end time in daily_work_track
        daily_work_track[day_of_week]["end_time"] = formatted_time

        # Calculate the difference between start and end time
        start_time = datetime.fromisoformat(daily_work_track[day_of_week]["start_time"])
        end_time = datetime.fromisoformat(formatted_time)
        time_difference = end_time - start_time
        hours, remainder = divmod(time_difference.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)

        today_hours = f"{int(hours):02}:{int(minutes):02}"

        # Update today's hours in the task
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"today_hours": today_hours}}
        )

        # Update weekly hours calculation
        total_weekly_hours = 0
        for day, times in daily_work_track.items():
            if "start_time" in times and "end_time" in times and times["end_time"]:
                start_time = datetime.fromisoformat(times["start_time"])
                end_time = datetime.fromisoformat(times["end_time"])
                diff = end_time - start_time
                total_weekly_hours += diff.total_seconds() / 3600  # Convert to hours

        # Convert total_weekly_hours to hh:mm format
        weekly_hours_int = int(total_weekly_hours)
        weekly_minutes = int((total_weekly_hours - weekly_hours_int) * 60)
        weekly_hours = f"{weekly_hours_int:02}:{weekly_minutes:02}"

        # Update weekly hours in the task
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"weekly_hours": weekly_hours}}
        )

    # Update the task with the modified daily_work_track
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"daily_work_track": daily_work_track}}
    )

    # Construct the response
    return {
        "message": f"{update_field} updated successfully",
        "updated_time": f"{day_of_week}, {formatted_time}",
        "today_hours": today_hours if key == "end" else None,
        "weekly_hours": weekly_hours if key == "end" else None,
        "daily_work_track": daily_work_track
    }
    
@root.get('/byId/{id}')
async def bytaskId(id:str):
    data = tasks_collection.find_one({"_id":ObjectId(id)})
    serialised_data = serialize(data)
    return serialised_data