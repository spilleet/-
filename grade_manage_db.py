############################################################################
# 프로그램명: grade_manage_db.py
# 작성자: 소프트웨어학부/2022078004 이동욱
# 작성일: 2025-06-11
# 프로그램 설명:
# 학생들의 성적 정보를 관리하는 프로그램입니다.
# 학번, 이름, 3과목 점수를 입력받아 총점, 평균, 학점을 계산하고
# SQLite 데이터베이스에 영구적으로 저장하여 관리합니다.
# 주요 기능: 정보 입력, 추가, 삭제, 검색(학번/이름), 전체 조회(등수 정렬),
# 평균 80점 이상 학생 수 확인.
############################################################################
import sqlite3
import os

class GradeDBManager:
    """
    SQLite 데이터베이스를 사용하여 학생 성적을 관리하는 클래스
    """
    def __init__(self, db_name="students.db"):
        """DB 연결 및 테이블 생성"""
        self.db_name = db_name
        # 데이터베이스 파일이 현재 작업 디렉토리에 있도록 경로 설정
        db_path = os.path.join(os.getcwd(), db_name)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """학생 정보 저장을 위한 테이블 생성"""
        # student_id는 고유해야 하므로 PRIMARY KEY로 설정
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                english INTEGER,
                c_lang INTEGER,
                python_score INTEGER,
                total INTEGER,
                avg REAL,
                grade TEXT
            )
        ''')
        self.conn.commit()
    
    def _calculate_grade(self, avg):
        """평균에 따른 학점 계산 (헬퍼 함수)"""
        if avg >= 95: return "A+"
        elif avg >= 90: return "A"
        elif avg >= 85: return "B+"
        elif avg >= 80: return "B"
        elif avg >= 75: return "C+"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        else: return "F"

    def student_insert(self, is_initial_input=False, n=1):
        """학생 정보를 입력받아 DB에 추가"""
        count = n if is_initial_input else 1
        for i in range(count):
            if is_initial_input:
                print(f"\n[{i+1}/{n}번째 학생]")
            else:
                print("\n학생 정보를 추가합니다:")
            
            try:
                student_id = input("학번: ")
                # 학번 중복 체크
                self.cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
                if self.cursor.fetchone():
                    print(f"오류: 학번 '{student_id}'는 이미 존재합니다.")
                    continue

                name = input("이름: ")
                english = int(input("영어: "))
                c_lang = int(input("C-언어: "))
                python_score = int(input("파이썬: "))

                total = english + c_lang + python_score
                avg = round(total / 3, 2)
                grade = self._calculate_grade(avg)
                
                self.cursor.execute('''
                    INSERT INTO students (student_id, name, english, c_lang, python_score, total, avg, grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student_id, name, english, c_lang, python_score, total, avg, grade))
                self.conn.commit()
                print(f"'{name}' 학생의 정보가 성공적으로 저장되었습니다.")

            except ValueError:
                print("오류: 점수는 숫자로 입력해야 합니다.")
            except Exception as e:
                print(f"오류가 발생했습니다: {e}")
                self.conn.rollback()

    def student_delete(self):
        """학번으로 학생 정보를 DB에서 삭제"""
        student_id = input("삭제할 학생의 학번을 입력하세요: ")
        self.cursor.execute("SELECT name FROM students WHERE student_id=?", (student_id,))
        student = self.cursor.fetchone()
        
        if student:
            self.cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
            self.conn.commit()
            print(f"학번 {student_id} ({student[0]}) 학생의 정보가 삭제되었습니다.")
        else:
            print(f"학번 {student_id} 학생은 존재하지 않습니다.")

    def _print_students_data(self, students_list):
        """학생 데이터 리스트를 표 형식으로 출력 (헬퍼 함수)"""
        if not students_list:
            print("\n표시할 학생 정보가 없습니다.")
            return

        print("\n                                     성적 현황")
        print("=======================================================================================")
        print("학번              이름        영어     C-언어   파이썬   총점     평균     학점     등수")
        print("=======================================================================================")
        for row in students_list:
            # row: (student_id, name, english, ..., grade, rank)
            print(f"{row[0]:<16}{row[1]:<10}{row[2]:<9}{row[3]:<9}{row[4]:<9}{row[5]:<9}{row[6]:<9.2f}{row[7]:<8}{row[8]}")
        print("=======================================================================================")

    def output_data(self):
        """모든 학생 정보를 등수와 함께 출력 (총점 기준 정렬)"""
        # RANK() 윈도우 함수를 사용하여 실시간으로 등수 계산
        query = '''
            SELECT *, RANK() OVER (ORDER BY total DESC) as rank 
            FROM students 
            ORDER BY total DESC
        '''
        self.cursor.execute(query)
        all_students = self.cursor.fetchall()
        self._print_students_data(all_students)

    def student_search(self):
        """학번 또는 이름으로 학생 검색"""
        print("\n--- 학생 정보 검색 ---")
        print("1. 학번으로 검색")
        print("2. 이름으로 검색")
        choice = input("선택: ")

        # RANK()를 포함한 기본 쿼리
        query_base = "SELECT *, RANK() OVER (ORDER BY total DESC) as rank FROM students"
        
        if choice == '1':
            search_key = input("검색할 학생의 학번을 입력하세요: ")
            # ORDER BY는 순위 산정에만 필요하고, 최종 결과는 WHERE 조건에 맞는 것만 나오므로 정렬은 불필요
            query = f"SELECT * FROM ({query_base}) WHERE student_id = ?"
            params = (search_key,)
        elif choice == '2':
            search_key = input("검색할 학생의 이름을 입력하세요: ")
            query = f"SELECT * FROM ({query_base}) WHERE name = ?"
            params = (search_key,)
        else:
            print("잘못된 선택입니다.")
            return

        self.cursor.execute(query, params)
        found_students = self.cursor.fetchall()
        self._print_students_data(found_students)

    def student_80_up_count(self):
        """평균 80점 이상인 학생 수 카운트"""
        self.cursor.execute("SELECT COUNT(*) FROM students WHERE avg >= 80")
        count = self.cursor.fetchone()[0]
        print(f"\n평균 80점 이상인 학생 수: {count}명")
    
    def close(self):
        """DB 연결 종료"""
        if self.conn:
            self.conn.close()
            print(f"\n데이터베이스 '{self.db_name}' 연결이 종료되었습니다.")


def main():
    # 2022078004 이동욱
    db_manager = GradeDBManager()

    try:
        while True:
            print("\n=========================")
            print("  DB 기반 성적 관리 프로그램")
            print("=========================")
            print("1. 학생 정보 일괄 입력")
            print("2. 학생 정보 추가")
            print("3. 학생 정보 출력 (총점순)")
            print("4. 학생 정보 삭제")
            print("5. 학생 정보 검색 (학번/이름)")
            print("6. 평균 80점 이상 학생 수")
            print("7. 종료")
            print("-------------------------")
            choice = input("선택: ")

            if choice == '1':
                try:
                    n = int(input("입력할 학생 수를 입력하세요: "))
                    if n > 0:
                        db_manager.student_insert(is_initial_input=True, n=n)
                except ValueError:
                    print("오류: 숫자를 입력해주세요.")
            elif choice == '2':
                db_manager.student_insert()
            elif choice == '3':
                db_manager.output_data()
            elif choice == '4':
                db_manager.student_delete()
            elif choice == '5':
                db_manager.student_search()
            elif choice == '6':
                db_manager.student_80_up_count()
            elif choice == '7':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 입력하세요.")
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
