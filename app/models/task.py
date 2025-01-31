from app import db
from app.models.goal import Goal


class Task(db.Model):
    """Task definition"""
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def task_from_dict(cls, task_data):
        """Input task as a dictionary. Assumes None/null for completed_at"""

        if not "completed_at" in task_data:
            task_data["completed_at"] = None

        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["completed_at"])
        return new_task

    def task_to_dict(self):
        """Output task information as a dictionary"""
        task_as_dict = {}

        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at != None

        return task_as_dict
    
    def task_with_goal_to_dict(self):
        task_as_dict = {}

        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at != None
        task_as_dict["goal_id"] = self.goal_id

        return task_as_dict
