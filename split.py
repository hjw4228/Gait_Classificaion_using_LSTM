import os
import sys
import pandas as pd
import numpy as np

def split_and_save_data(input_file_path, input_file_name, output_folder, chunk_size=30):
    # CSV 파일을 DataFrame으로 읽기
    df = pd.read_csv(input_file_path)
    
    # 데이터가 chunk_size 개수로 나눠지도록 조정
    num_chunks = len(df) // chunk_size
    df = df.iloc[:num_chunks * chunk_size]

    splited = None
    try: 
        splited = np.array_split(df, num_chunks)
    except ValueError: 
        return
    # 데이터를 chunk_size 개수로 나눠서 서로 다른 파일에 저장
    for i, chunk in enumerate(splited):
        output_file_path = os.path.join(output_folder, f"chunk_{i+1}_{input_file_name[:-4]}.csv")
        chunk.to_csv(output_file_path, index=False)
        print(f"데이터를 {output_file_path}에 저장했습니다.")

def process_files_in_folder(folder_path, output_path):
    # 폴더 내의 파일 목록을 가져오기
    files = os.listdir(folder_path)

    # CSV 파일들을 처리
    for file in files:
        if file.endswith(".csv"):
            input_file_path = os.path.join(folder_path, file)
            
            # 데이터를 100개씩 나눠서 저장
            split_and_save_data(input_file_path, file, output_path)

# 폴더 내의 파일들을 처리
process_files_in_folder(sys.argv[1], sys.argv[2])
