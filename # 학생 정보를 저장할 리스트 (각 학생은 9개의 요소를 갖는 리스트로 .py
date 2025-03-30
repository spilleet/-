# 학생 정보를 저장할 리스트 (각 학생은 9개의 요소를 갖는 리스트로 표현)
# [학번, 이름, 영어, C-언어, 파이썬, 총점, 평균, 학점, 등수]
a = []

def inputData():
    global a
    n = int(input("입력할 학생 수를 입력하세요: "))
    for i in range(n):
        print(f"\n[{i+1}번째 학생]")
        student = [0] * 9
        student[0] = input("학번: ")
        student[1] = input("이름: ")
        student[2] = int(input("영어: "))
        student[3] = int(input("C-언어: "))
        student[4] = int(input("파이썬: "))
        a.append(student)

def sumScore():
    for student in a:
        student[5] = student[2] + student[3] + student[4]

def avgScore():
    for student in a:
        student[6] = round(student[5] / 3, 2)

def avgGrade():
    for student in a:
        avg = student[6]
        if avg >= 95:
            student[7] = "A+"
        elif avg >= 90:
            student[7] = "A"
        elif avg >= 85:
            student[7] = "B+"
        elif avg >= 80:
            student[7] = "B"
        elif avg >= 75:
            student[7] = "C+"
        elif avg >= 70:
            student[7] = "C"
        elif avg >= 60:
            student[7] = "D"
        else:
            student[7] = "F"

def rankScore():
    for student in a:
        rank = 1
        for other in a:
            if student[5] < other[5]:
                rank += 1
        student[8] = rank

def outputData():
    print("\n                            성적관리 프로그램")
    print("===============================================================================")
    print("학번             이름        영어    C-언어    파이썬    총점    평균    학점    등수")
    print("===============================================================================")
    for student in a:
        print(f"{student[0]:<16}{student[1]:<10}{student[2]:<8}{student[3]:<9}{student[4]:<9}"
              f"{student[5]:<8}{student[6]:<8}{student[7]:<8}{student[8]}")

def studentInsert():
    global a
    print("\n학생 정보를 추가합니다:")
    new_student = [0] * 9
    new_student[0] = input("학번: ")
    new_student[1] = input("이름: ")
    new_student[2] = int(input("영어: "))
    new_student[3] = int(input("C-언어: "))
    new_student[4] = int(input("파이썬: "))
    a.append(new_student)

def calculateAll():
    sumScore()
    avgScore()
    avgGrade()
    rankScore()

def studentDelete(a):
    x = input("삭제할 학생의 학번을 입력하세요: ")
    for student in a:
        if student[0] == x:
            a.remove(student)
            print(f"학번 {x} 학생의 정보가 삭제되었습니다.")
            return
    print(f"학번 {x} 학생은 존재하지 않습니다.")

def studentSerarch(a):
    x = input("검색할 학생의 학번을 입력하세요: ")
    for student in a:
        if student[0] == x:
            print(f"학번 {x} 학생의 정보는 다음과 같습니다.")
            print(f"이름: {student[1]}, 영어: {student[2]}, C-언어: {student[3]}, 파이썬: {student[4]}")
            return
    print(f"학번 {x} 학생은 존재하지 않습니다.")

def studentSort(a): 
    a.sort(key=lambda x: x[5], reverse=True)  
    print("학생 정보가 총점 기준으로 정렬되었습니다.")

def student80UPcount(a): 
    count = 0
    for student in a:
        if student[6] >= 80:
            count += 1
    print(f"80점 이상인 학생 수: {count}")

def main():
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
            inputData()
        elif choice == '2':
            studentInsert()
        elif choice == '3':
            calculateAll()
            outputData()
        elif choice == '4':
            studentDelete(a)
        elif choice == '5':
            studentSerarch(a)
        elif choice == '6':
            studentSort(a)
        elif choice == '7':
            student80UPcount(a)
        elif choice == '8':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력하세요.")

if __name__ == "__main__":
    main()