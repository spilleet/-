a = [[0] * 9 for _ in range(5)]  # 0~8: 학번, 이름, 영어, C, 파이썬, 총점, 평균, 학점, 등수

def inputData():
    for i in range(5):
        a[i][0] = input("학번:\n")
        a[i][1] = input("이름:\n")
        a[i][2] = int(input("영어:\n"))
        a[i][3] = int(input("C-언어:\n"))
        a[i][4] = int(input("파이썬:\n"))

def sumScore():
    for i in range(5):
        a[i][5] = a[i][2] + a[i][3] + a[i][4]

def avgScore():
    for i in range(5):
        a[i][6] = round(a[i][5] / 3, 2)

def avgGrade():
    for i in range(5):
        avg = a[i][6]
        if avg >= 95:
            a[i][7] = "A+"
        elif avg >= 90:
            a[i][7] = "A"
        elif avg >= 85:
            a[i][7] = "B+"
        elif avg >= 80:
            a[i][7] = "B"
        elif avg >= 75:
            a[i][7] = "C+"
        elif avg >= 70:
            a[i][7] = "C"
        elif avg >= 60:
            a[i][7] = "D"
        else:
            a[i][7] = "F"

def rankScore():
    for i in range(5):
        rank = 1
        for j in range(5):
            if a[i][5] < a[j][5]:
                rank += 1
        a[i][8] = rank

def outputData():
    print("\n                            성적관리 프로그램")
    print("===============================================================================")
    print("학번             이름        영어    C-언어    파이썬    총점    평균    학점    등수")
    print("===============================================================================")
    for i in range(5):
        print(f"{a[i][0]:<16}{a[i][1]:<10}{a[i][2]:<8}{a[i][3]:<9}{a[i][4]:<9}{a[i][5]:<8}{a[i][6]:<8}{a[i][7]:<8}{a[i][8]}")


inputData()
sumScore()
avgScore()
avgGrade()
rankScore()
outputData()