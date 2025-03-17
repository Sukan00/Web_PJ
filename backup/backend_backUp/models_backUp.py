from database import get_db_connection 

class User:
    def __init__(self, email, role):
        self.email = email
        self.role = role
    
    """ ตรวจสอบความถูกต้องของ user และส่งคืน email & role ไปที่ Subclass """
    @classmethod
    def authenticate(cls, email, password, role):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT user_email, role FROM "user" '
                    'WHERE user_email = %s AND password = %s AND role = %s',
                    (email, password, role)
                )
                if user_data := cur.fetchone():
                    if role == "student":
                        return Student(user_data[0], user_data[1])
                    return Teacher(user_data[0], user_data[1])
                return None
        finally:
            conn.close()

##############################################
class Student(User):
    def __init__(self, email, role):
        super().__init__(email, role)
        self.student_id = email.split("@")[0]
        self.projects = []
    
    def get_projects(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # @> คือตัวดำเนินการ "contains" สำหรับ arrays ใน PostgreSQL, ตรวจสอบว่า array ทางซ้ายมี array ทางขวาเป็นสมาชิกไหม
                cur.execute('SELECT * FROM report WHERE author @> ARRAY[%s]::varchar[]', (self.student_id,)) 
                self.projects = cur.fetchall()
                return self.projects
        finally:
            conn.close()

##############################################
class Teacher(User):
    def __init__(self, email, role):
        super().__init__(email, role)
        self.projects = []
    
    def get_all_projects(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM report')
                self.projects = cur.fetchall()
                return self.projects
        finally:
            conn.close()

##############################################
class Report:
    def __init__(self, title, category, user_email, author_ids):
        self.title = title
        self.category = category
        self.user_email = user_email
        self.author_ids = author_ids
    
    def save(self, form_data, pdf_path):  
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Check data of advisor
                cur.execute('SELECT advisor_email FROM advisor WHERE advisor_name = %s', (form_data['name_advisor'],))
                advisor_result = cur.fetchone()
                if not advisor_result:
                    raise ValueError("Advisor not found")
                advisor_email = advisor_result[0]      
            
                # Insert report
                cur.execute(
                    '''INSERT INTO report (
                        title, intro, year, category, org, 
                        type_org, position, path, user_email, advisor_email, author
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING report_id''',
                    (
                        form_data['title'],
                        form_data['intro'],
                        form_data['year'],
                        self.category,
                        form_data.get('org'),
                        form_data.get('type_org'),
                        form_data.get('position'),
                        pdf_path,
                        self.user_email,
                        advisor_email,
                        self.author_ids
                    )
                )
                report_id = cur.fetchone()[0]
                
                # Insert report type
                report_types = form_data.getlist('report_types')
                if form_data['other_input']:
                    report_types[report_types.index('Other')] = form_data['other_input']
                cur.execute(
                    'INSERT INTO report_type VALUES (%s,%s)',
                    (report_id, "{" + ",".join(report_types) + "}")
                )
                
                # Update authors
                cur.execute(
                    f'UPDATE author SET report_id = %s WHERE au_id IN ({",".join(["%s"]*len(self.author_ids))})',
                    [report_id] + self.author_ids
                )

                
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
##############################################
class CoOpReport(Report):
    def __init__(self, title, user_email, author_ids):
        super().__init__(title, "co-op", user_email, author_ids)