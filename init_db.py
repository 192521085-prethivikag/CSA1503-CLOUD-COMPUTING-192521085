from app import create_app
from models import db
from models.user import User
from models.course import Course, Lecture, Enrollment
from models.exam import Exam, Question, Result
from models.assignment import Assignment, Submission
from models.activity import ActivityLog
from datetime import datetime, timedelta

app = create_app()

def seed_database():
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Users...")
        # Main Demo Users
        student1 = User(name="Alex Smith", email="student@cloudedu.com", role="student")
        student1.set_password("student123")

        teacher1 = User(name="Dr. Kumar", email="teacher@cloudedu.com", role="teacher")
        teacher1.set_password("teacher123")

        teacher2 = User(name="Dr. Priya", email="priya@cloudedu.com", role="teacher")
        teacher2.set_password("teacher123")

        admin1 = User(name="Cloud System Admin", email="admin@cloudedu.com", role="admin")
        admin1.set_password("admin123")

        # Additional Students for Analytics
        extra_students = [
            User(name="Rahul Sharma", email="rahul@cloudedu.com", role="student"),
            User(name="Emily Chen", email="emily@cloudedu.com", role="student"),
            User(name="Michael Brown", email="michael@cloudedu.com", role="student"),
            User(name="Sophia Davis", email="sophia@cloudedu.com", role="student")
        ]
        for s in extra_students:
            s.set_password("student123")

        db.session.add_all([student1, teacher1, teacher2, admin1] + extra_students)
        db.session.commit()

        print("Seeding Courses & Lectures...")
        # Course 1: Cloud Computing
        course_cc = Course(
            title="Cloud Computing",
            code="CC101",
            category="Cloud Architecture",
            description="Comprehensive guide covering IaaS, PaaS, SaaS, XaaS, Virtualization, and Web Services in Cloud Environments.",
            instructor_name="Dr. Kumar",
            instructor_id=teacher1.id,
            duration_weeks=12
        )
        
        # Course 2: Big Data Analytics
        course_bda = Course(
            title="Big Data Analytics",
            code="BDA201",
            category="Big Data",
            description="Explore big data processing pipelines, Pandas analytics engines, and data visualizer dashboards.",
            instructor_name="Dr. Priya",
            instructor_id=teacher2.id,
            duration_weeks=10
        )

        # Course 3: Python Enterprise Systems
        course_py = Course(
            title="Python Enterprise Systems",
            code="PY301",
            category="Software Development",
            description="Building scalable backend microservices and RESTful Web APIs using Python Flask and SQLAlchemy.",
            instructor_name="Dr. Kumar",
            instructor_id=teacher1.id,
            duration_weeks=8
        )

        db.session.add_all([course_cc, course_bda, course_py])
        db.session.commit()

        # Modules & Video Lectures for Cloud Computing
        lectures_cc = [
            Lecture(
                course_id=course_cc.id,
                module_name="Module 1 – Introduction",
                title="1.1 Overview of Cloud Computing & Paradigm Shift",
                description="Introduction to utility computing, cloud characteristics, and cloud service deployment models.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                order_num=1
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 2 – Cloud Evolution",
                title="2.1 Evolution from Grid & Cluster Computing to Cloud",
                description="Historical evolution of hardware virtualization, internet bandwidth, and web application architecture.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
                order_num=2
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 3 – Virtualization",
                title="3.1 Server Virtualization & Hypervisors (Type 1 vs Type 2)",
                description="Understanding hardware abstraction, hypervisors, VM resource allocation, and containerization.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
                order_num=3
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 4 – IaaS",
                title="4.1 Infrastructure as a Service Deep-Dive",
                description="Managing Azure Virtual Machines, Virtual Networks, Security Groups, and Cloud Block Storage.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
                order_num=4
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 5 – PaaS",
                title="5.1 Platform as a Service & Managed Application Services",
                description="Deploying Flask web applications onto Azure App Service without managing underlying OS.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
                order_num=5
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 6 – SaaS",
                title="6.1 Software as a Service & LMS Integration",
                description="Accessing educational management software on-demand via browser with zero client footprint.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
                order_num=6
            ),
            Lecture(
                course_id=course_cc.id,
                module_name="Module 7 – XaaS",
                title="7.1 Anything as a Service Architecture",
                description="Combining DBaaS, Storage as a Service, and Analytics as a Service into unified ecosystem.",
                video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnTheLakeside.mp4",
                order_num=7
            )
        ]
        db.session.add_all(lectures_cc)
        db.session.commit()

        print("Seeding Enrollments...")
        all_st = [student1] + extra_students
        for s in all_st:
            db.session.add(Enrollment(student_id=s.id, course_id=course_cc.id))
            db.session.add(Enrollment(student_id=s.id, course_id=course_bda.id))
        db.session.commit()

        print("Seeding Examinations & Questions...")
        exam1 = Exam(
            course_id=course_cc.id,
            title="Cloud Computing Quiz & Architecture Evaluation",
            duration_minutes=20
        )
        db.session.add(exam1)
        db.session.flush()

        questions = [
            Question(
                exam_id=exam1.id,
                question_text="Which cloud service model provides virtual machines, raw storage, and virtual networking?",
                option_a="SaaS (Software as a Service)",
                option_b="IaaS (Infrastructure as a Service)",
                option_c="PaaS (Platform as a Service)",
                option_d="XaaS (Anything as a Service)",
                correct_answer="B"
            ),
            Question(
                exam_id=exam1.id,
                question_text="What software layer sits directly between physical hardware and virtual machines to manage resources?",
                option_a="Hypervisor",
                option_b="Web Server",
                option_c="Database Engine",
                option_d="Load Balancer",
                correct_answer="A"
            ),
            Question(
                exam_id=exam1.id,
                question_text="Deploying a Flask web app on Azure App Service without configuring the OS is an example of:",
                option_a="IaaS",
                option_b="PaaS",
                option_c="SaaS",
                option_d="BaaS",
                correct_answer="B"
            ),
            Question(
                exam_id=exam1.id,
                question_text="Which HTTP method is typically used to retrieve resource data from a RESTful API?",
                option_a="POST",
                option_b="GET",
                option_c="DELETE",
                option_d="PUT",
                correct_answer="B"
            ),
            Question(
                exam_id=exam1.id,
                question_text="What does XaaS stand for in modern cloud architecture?",
                option_a="Extensible as a Service",
                option_b="Anything as a Service / Everything as a Service",
                option_c="XML as a Service",
                option_d="Xerox as a Service",
                correct_answer="B"
            )
        ]
        db.session.add_all(questions)
        db.session.commit()

        print("Seeding Historical Results & Assignments...")
        # Exam Results
        res1 = Result(student_id=student1.id, exam_id=exam1.id, score_percentage=80.0, total_questions=5, correct_count=4, performance_grade="GOOD")
        res2 = Result(student_id=extra_students[0].id, exam_id=exam1.id, score_percentage=100.0, total_questions=5, correct_count=5, performance_grade="EXCELLENT")
        res3 = Result(student_id=extra_students[1].id, exam_id=exam1.id, score_percentage=60.0, total_questions=5, correct_count=3, performance_grade="AVERAGE")
        db.session.add_all([res1, res2, res3])

        # Assignment
        assign1 = Assignment(
            course_id=course_cc.id,
            title="Virtualization & Hypervisor Architecture Assignment",
            description="Explain server virtualization concepts, compare Type 1 vs Type 2 hypervisors, and describe how cloud providers optimize CPU and RAM utilization.",
            due_date="2026-09-30"
        )
        db.session.add(assign1)
        db.session.flush()

        sub1 = Submission(
            assignment_id=assign1.id,
            student_id=student1.id,
            file_url="https://cloudedustorage.blob.core.windows.net/assignments/virtualization_report.pdf",
            content_text="Server virtualization uses a hypervisor (such as Azure Hyper-V) to slice physical server resources into multiple virtual machines...",
            grade="92/100",
            feedback="Excellent explanation of hypervisors and resource allocation!"
        )
        db.session.add(sub1)

        print("Seeding Activity Logs for Big Data Engine...")
        now = datetime.utcnow()
        logs = [
            ActivityLog(user_id=student1.id, activity_type="login", details="Logged into CloudEdu portal", timestamp=now - timedelta(days=5)),
            ActivityLog(user_id=student1.id, activity_type="watch_lecture", course_name="Cloud Computing", details="Watched 3.1 Server Virtualization", timestamp=now - timedelta(days=4)),
            ActivityLog(user_id=student1.id, activity_type="submit_exam", course_name="Cloud Computing", details="Scored 80% on Cloud Computing Quiz", timestamp=now - timedelta(days=2)),
            ActivityLog(user_id=extra_students[0].id, activity_type="login", details="Logged in from Azure VM IP", timestamp=now - timedelta(days=1)),
            ActivityLog(user_id=extra_students[1].id, activity_type="submit_assignment", course_name="Cloud Computing", details="Submitted Virtualization Essay", timestamp=now)
        ]
        db.session.add_all(logs)

        db.session.commit()
        print("Database initialization and seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
