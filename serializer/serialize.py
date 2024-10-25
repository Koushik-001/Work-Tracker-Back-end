def serialize(doc):
    return {
        "id":str(doc.get("_id")),
        "task_name": doc.get("task_name",""),
        "start_time": doc.get("start_time",""),
        "end_time": doc.get("end_time",""),
        "today_hours": doc.get("today_hours",""),
        "weekly_hours": doc.get("weekly_hours",""),
        "daily_work_track": doc.get("daily_work_track",""),
    }
    
def serializeAll(docs)->list:
    return [serialize(doc) for doc in docs]

