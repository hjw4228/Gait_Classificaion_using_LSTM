from datetime import datetime
import sys
import os

def convert_to_unix_timestamp(date_string):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    dt_object = datetime.strptime(date_string, date_format)
    timestamp = int(dt_object.timestamp() * 1000)
    return timestamp

def process_file(input_file_path, output_file_path, isOriginallyOpen):
    isOpen = False
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        if 'L' in input_file_path: output_file.write("time,l_left_back,l_left_front,l_right_back,l_right_front,l_distance\n")
        elif 'R' in input_file_path: output_file.write("time,r_left_back,r_left_front,r_right_back,r_right_front,r_distance\n")
        for line in input_file:
            if line.strip() == '<>': isOpen = not isOpen
            if isOpen == isOriginallyOpen: continue
            
            # 무의미한 줄 건너뛰기
            if len(line.split(',')) < 3:
                continue

            # 각 줄의 데이터에서 날짜 및 시간 추출
            date_time_part = line.split(',')[0].strip()
            line = line.replace(' ', '')
            # 유닉스 타임스탬프로 변환
            unix_timestamp = convert_to_unix_timestamp(date_time_part)

            # 새로운 파일에 기록
            output_line = f"{unix_timestamp},{line.split(',')[1]},{line.split(',')[2]},{line.split(',')[3]},{line.split(',')[4]},{line.split(',')[5]}\n"
            output_file.write(output_line)

            print(f"입력된 날짜 및 시간: {date_time_part}")
            print(f"변환된 유닉스 타임스탬프: {unix_timestamp}")
            print("-------------")

    print(f"{input_file_path}로부터 변환된 데이터가 {output_file_path}에 저장되었습니다.")

def process_files_in_folder(folder_path, extension):
    for filename in os.listdir(folder_path):
        if filename.endswith(extension):
            input_file_path = os.path.join(folder_path, filename)
            output_file_1_path = os.path.join(output_folder_path, f"converted_1_{filename}")
            output_file_2_path = os.path.join(output_folder_path, f"converted_2_{filename}")
            
            process_file(input_file_path, output_file_1_path, True)
            process_file(input_file_path, output_file_2_path, False)
            
            print(f"파일 {filename} 처리 완료. 결과는 {output_file_1_path}와 {output_file_2_path}에 저장되었습니다.")

# 특정 폴더와 확장자 지정
folder_path = sys.argv[1]
output_folder_path = sys.argv[2]
file_extension = ".csv"

# 지정된 폴더 내의 모든 특정 확장자 파일 처리
process_files_in_folder(folder_path, file_extension)