import os
import sys
import pandas as pd

def merge_files(left_file_path, right_file_path, output_file_path):
    df_left = pd.read_csv(left_file_path, dtype='Int64')
    df_right = pd.read_csv(right_file_path, dtype='Int64')
    
    df_left['time'] = pd.to_datetime(df_left['time'], unit='ms')
    df_right['time'] = pd.to_datetime(df_right['time'], unit='ms')
    
    merged_df = pd.merge_asof(df_left, df_right, on='time', direction='nearest', tolerance=pd.Timedelta('100ms'))
    merged_df.to_csv(output_file_path, index=False)
    
    print(merged_df.dtypes)
    print(f"데이터 병합이 완료되었습니다. 결과는 {output_file_path}에 저장되었습니다.")

def process_files_in_folder(folder_path, output_folder_path, left_suffix="_L.csv", right_suffix="_R.csv"):
    # 폴더 내의 파일 목록을 가져오기
    files = os.listdir(folder_path)

    # L 파일과 R 파일을 찾아서 병합
    for file in files:
        if file.endswith(left_suffix):
            left_file_path = os.path.join(folder_path, file)
            right_file_path = os.path.join(folder_path, file.replace(left_suffix, right_suffix))
            
            # 해당 R 파일이 존재하는 경우에만 병합 수행
            if os.path.exists(right_file_path):
                output_file_path = os.path.join(output_folder_path, f"merged_{file}")
                merge_files(left_file_path, right_file_path, output_file_path)

# 폴더 내의 파일들을 처리
process_files_in_folder(sys.argv[1], sys.argv[2])
