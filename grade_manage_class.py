# ------------------------------------------------------------------------------
# 성적 관리 프로그램 (클래스화)
# ------------------------------------------------------------------------------
# - 2022078004 이동욱
# - 학생 한 명의 정보를 Student 클래스로 정의
# - 학생 리스트 관리를 StudentManager 클래스로 정의
# - main 함수에서 프로그램 동작
# ------------------------------------------------------------------------------

class Student:
    """
    각 학생 정보를 저장하는 클래스
    [학번, 이름, 영어, C-언어, 파이썬, 총점, 평균, 학점, 등수]
    """
    def __init__(self, student_id, name, english, c_lang, python_score):
        self.student_id = student_id
        self.name = name
        self.english = english
        self.c_lang = c_lang
        self.python_score = python_score
        self.total = 0
        self.avg = 0.0
        self.grade = ""
        self.rank = 0  # 등수

    def calc_total(self):
        """3개 과목의 합계를 구해서 total에 저장"""
        self.total = self.english + self.c_lang + self.python_score

    def calc_avg(self):
        """평균을 구해서 avg에 저장 (소수 둘째 자리까지 반올림)"""
        # 과목이 3개이므로 total / 3
        self.avg = round(self.total / 3, 2)

    def calc_grade(self):
        """평균에 따라 학점을 grade에 저장"""
        if self.avg >= 95:
            self.grade = "A+"
        elif self.avg >= 90:
            self.grade = "A"
        elif self.avg >= 85:
            self.grade = "B+"
        elif self.avg >= 80:
            self.grade = "B"
        elif self.avg >= 75:
            self.grade = "C+"
        elif self.avg >= 70:
            self.grade = "C"
        elif self.avg >= 60:
            self.grade = "D"
        else:
            self.grade = "F"


class StudentManager:
    """
    학생 리스트를 관리하고, 성적 연산/출력/삭제/검색/정렬 등
    모든 기능을 처리하는 클래스
    """
    def __init__(self):
        self.students = []  # Student 객체들을 담을 리스트

    def input_data(self):
        """학생 정보를 n명 입력받아 students 리스트에 추가"""
        n = int(input("입력할 학생 수를 입력하세요: "))
        for i in range(n):
            print(f"\n[{i+1}번째 학생]")
            student_id = input("학번: ")
            name = input("이름: ")
            english = int(input("영어: "))
            c_lang = int(input("C-언어: "))
            python_score = int(input("파이썬: "))

            # Student 객체 생성 후 리스트에 추가
            new_student = Student(student_id, name, english, c_lang, python_score)
            self.students.append(new_student)

    def student_insert(self):
        """프로그램 실행 중 학생 정보 추가"""
        print("\n학생 정보를 추가합니다:")
        student_id = input("학번: ")
        name = input("이름: ")
        english = int(input("영어: "))
        c_lang = int(input("C-언어: "))
        python_score = int(input("파이썬: "))

        new_student = Student(student_id, name, english, c_lang, python_score)
        self.students.append(new_student)

    def calculate_all(self):
        """총점, 평균, 학점 계산 + 등수 산출"""
        # 1) 각 학생별 합계, 평균, 학점 계산
        for stu in self.students:
            stu.calc_total()
            stu.calc_avg()
            stu.calc_grade()
        # 2) 등수 계산 (총점 기준)
        for stu in self.students:
            rank = 1
            for other in self.students:
                if stu.total < other.total:
                    rank += 1
            stu.rank = rank

    def output_data(self):
        """모든 학생의 성적 리스트 출력"""
        print("\n                            성적관리 프로그램")
        print("===============================================================================")
        print("학번             이름        영어    C-언어    파이썬    총점    평균    학점    등수")
        print("===============================================================================")
        for stu in self.students:
            print(f"{stu.student_id:<16}{stu.name:<10}{stu.english:<8}{stu.c_lang:<9}"
                  f"{stu.python_score:<9}{stu.total:<8}{stu.avg:<8}{stu.grade:<8}{stu.rank}")

    def student_delete(self):
        """학번으로 학생 정보를 검색 후 삭제"""
        x = input("삭제할 학생의 학번을 입력하세요: ")
        for stu in self.students:
            if stu.student_id == x:
                self.students.remove(stu)
                print(f"학번 {x} 학생의 정보가 삭제되었습니다.")
                return
        print(f"학번 {x} 학생은 존재하지 않습니다.")

    def student_search(self):
        """학번으로 특정 학생을 검색하여 성적 정보 출력"""
        x = input("검색할 학생의 학번을 입력하세요: ")
        for stu in self.students:
            if stu.student_id == x:
                print(f"학번 {x} 학생의 정보는 다음과 같습니다.")
                print(f"이름: {stu.name}, 영어: {stu.english}, "
                      f"C-언어: {stu.c_lang}, 파이썬: {stu.python_score}")
                return
        print(f"학번 {x} 학생은 존재하지 않습니다.")

    def student_sort(self):
        """총점 기준으로 내림차순 정렬"""
        self.students.sort(key=lambda s: s.total, reverse=True)
        print("학생 정보가 총점 기준으로 정렬되었습니다.")

    def student_80_up_count(self):
        """평균 80점 이상인 학생 수 세어서 출력"""
        count = 0
        for stu in self.students:
            if stu.avg >= 80:
                count += 1
        print(f"80점 이상인 학생 수: {count}")


def main():
    manager = StudentManager()  # 학생 관리 객체 생성

    while True:
        print("\n=========================")
        print("학생 성적 관리 프로그램")
        print("2022078004 이동욱")
        print("=========================")
        print("\n메뉴를 선택하세요:")
        print("1. 학생 정보 입력")
        print("2. 학생 정보 추가")
        print("3. 학생 정보 계산 및 출력")
        print("4. 학생 정보 삭제")
        print("5. 학생 정보 검색")
        print("6. 학생 정보 정렬")
        print("7. 80점 이상 학생 수 세기")
        print("8. 종료")
        choice = input("선택: ")

        if choice == '1':
            manager.input_data()
        elif choice == '2':
            manager.student_insert()
        elif choice == '3':
            manager.calculate_all()
            manager.output_data()
        elif choice == '4':
            manager.student_delete()
        elif choice == '5':
            manager.student_search()
        elif choice == '6':
            manager.student_sort()
        elif choice == '7':
            manager.student_80_up_count()
        elif choice == '8':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력하세요.")


if __name__ == "__main__":
    main()
