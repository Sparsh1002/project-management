from datetime import date

from app.db.database import SessionLocal

from app.models.user import User
from app.models.project import Project
from app.models.sprint import Sprint
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.activity_log import ActivityLog
from app.models.notification import Notification
from app.models.watcher import Watcher



def seed_data():
    """
    Seed demo data for local development.

    Runs only if database is empty.
    """

    db = SessionLocal()

    try:

        existing_user = db.query(User).first()

        if existing_user:

            print("Seed data already exists")

            return

        print("Creating seed data...")


        # pass is Admin1234
        user_1 = User(
            name="sparsh",
            email="sparshlodha04@gmail.com",
            hashed_password="$2b$12$wbEA70N5GZp.VeEfHove.OvbCu7YTdBGatCWhOiwVw9ZlkojuJUK6"
        )

        user_2 = User(
            name="alice",
            email="alice@example.com",
            hashed_password="$2b$12$wbEA70N5GZp.VeEfHove.OvbCu7YTdBGatCWhOiwVw9ZlkojuJUK6"
        )

        user_3 = User(
            name="bob",
            email="bob@example.com",
            hashed_password="$2b$12$wbEA70N5GZp.VeEfHove.OvbCu7YTdBGatCWhOiwVw9ZlkojuJUK6"
        )

        db.add_all([
            user_1,
            user_2,
            user_3
        ])

        db.flush()

        project_1 = Project(
            name="Swiggy Delivery Platform",
            key="SWIG"
        )

        project_2 = Project(
            name="Swiggy Partner Operations",
            key="DEL"
        )

        db.add_all([
            project_1,
            project_2
        ])

        db.flush()

        sprint_1 = Sprint(
            name="Sprint 1",
            status="active",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 15),
            project_id=project_1.id
        )

        sprint_2 = Sprint(
            name="Sprint 2",
            status="planned",
            start_date=date(2026, 5, 16),
            end_date=date(2026, 5, 30),
            project_id=project_1.id
        )

        sprint_3 = Sprint(
            name="Delivery Operations Sprint",
            status="active",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
            project_id=project_2.id
        )

        db.add_all([
            sprint_1,
            sprint_2,
            sprint_3
        ])

        db.flush()

        epic_issue = Issue(
            issue_key="SWIG-1",
            title="Delivery Tracking Module",
            description="Main delivery operations epic",
            type="Epic",
            status="In Progress",
            priority="High",
            project_id=project_1.id,
            sprint_id=sprint_1.id,
            reporter_id=user_1.id,
            assignee_id=user_2.id,
            story_points=13,
            labels=["delivery", "tracking"]
        )

        db.add(epic_issue)

        db.flush()

        story_issue = Issue(
            issue_key="SWIG-2",
            title="Live Order Tracking",
            description="Implement realtime order tracking for delivery partners",
            type="Story",
            status="To Do",
            priority="High",
            project_id=project_1.id,
            sprint_id=sprint_1.id,
            reporter_id=user_1.id,
            assignee_id=user_3.id,
            parent_issue_id=epic_issue.id,
            story_points=8,
            labels=["tracking"]
        )

        bug_issue = Issue(
            issue_key="SWIG-3",
            title="Delivery ETA Calculation Bug",
            description="Fix incorrect ETA calculation during peak rain hours",
            type="Bug",
            status="In Review",
            priority="Critical",
            project_id=project_1.id,
            sprint_id=sprint_1.id,
            reporter_id=user_2.id,
            assignee_id=user_3.id,
            story_points=3,
            labels=["bug", "delivery"]
        )

        payment_issue = Issue(
            issue_key="DEL-1",
            title="Partner Earnings Settlement",
            description="Implement weekly payout settlement for delivery partners",
            type="Task",
            status="Done",
            priority="Medium",
            project_id=project_2.id,
            sprint_id=sprint_3.id,
            reporter_id=user_2.id,
            assignee_id=user_1.id,
            story_points=5,
            labels=["operations"]
        )

        db.add_all([
            story_issue,
            bug_issue,
            payment_issue
        ])

        db.flush()

        comment_1 = Comment(
            issue_id=story_issue.id,
            content="@sparsh please review delivery tracking flow"
        )

        db.add(comment_1)

        db.flush()

        comment_2 = Comment(
            issue_id=story_issue.id,
            content="@alice Looks good to me",
            parent_comment_id=comment_1.id
        )

        comment_3 = Comment(
            issue_id=bug_issue.id,
            content="ETA refresh logic failing for long-distance deliveries"
        )

        db.add_all([
            comment_2,
            comment_3
        ])

        db.flush()


        activity_1 = ActivityLog(
            issue_id=story_issue.id,
            action="Issue created"
        )

        activity_2 = ActivityLog(
            issue_id=story_issue.id,
            action="To Do -> In Progress"
        )

        activity_3 = ActivityLog(
            issue_id=bug_issue.id,
            action="Comment added"
        )

        db.add_all([
            activity_1,
            activity_2,
            activity_3
        ])


        notification_1 = Notification(
            user_id=user_2.id,
            message="You were assigned SWIG-1",
            is_read=False
        )

        notification_2 = Notification(
            user_id=user_3.id,
            message="You were mentioned in a comment",
            is_read=False
        )

        notification_3 = Notification(
            user_id=user_1.id,
            message="Delivery Sprint 1 started",
            is_read=True
        )

        db.add_all([
            notification_1,
            notification_2,
            notification_3
        ])

        watcher_1 = Watcher(
            user_id=user_1.id,
            issue_id=story_issue.id
        )

        watcher_2 = Watcher(
            user_id=user_2.id,
            issue_id=story_issue.id
        )

        watcher_3 = Watcher(
            user_id=user_3.id,
            issue_id=bug_issue.id
        )

        db.add_all([
            watcher_1,
            watcher_2,
            watcher_3
        ])

        db.commit()

        print("Seed data inserted successfully")

    finally:

        db.close()