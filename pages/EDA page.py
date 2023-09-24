import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
import numpy as np

# Streamlit 앱 제목 설정
st.title("📊 데이터 시각화 및 분석")

# 데이터셋 불러오기 또는 파일 업로드 선택 창
st.subheader("1️⃣ 데이터 불러오기")
tab1, tab2 = st.tabs(["seaborn 데이터셋", "파일 업로드"])

# 데이터를 불러오는 로직
with tab1:
    dataset_name = st.text_input('데이터 예시: titanic, tips, taxis, penguins, iris...:')
    sample_checked = st.checkbox('seaborn 데이터 확인하기')

    if sample_checked:
        with st.spinner('샘플 데이터를 불러오는 중 입니다...'):
            try:
                df = sns.load_dataset(dataset_name)
                st.write(df.head(3))
            except:
                st.write("⚠데이터셋 이름을 다시 확인해주세요!")

with tab2:
    st.write("단, 이 방법은 csv 파일만 지원합니다.")
    custom_data = st.file_uploader("분석하고 싶은 파일을 업로드해주세요.", type=["csv", "xlsx"])
    if custom_data:
        custom_data = pd.read_csv(custom_data, encoding = 'euc-kr')
        st.session_state['custom_data'] = custom_data

    upload_checked = st.checkbox('업로드한 파일 확인하기!')
    if upload_checked:
        with st.spinner('중복을 확인하는 중입니다...'):
            try:
                st.write(custom_data.head(5))
                df = custom_data
            except:
                st.write("⚠올바른 파일을 업로드하셨는지 확인해주세요!")

try:
    # 열 이름 가져오기
    column_names = df.columns.tolist()

    # 열 이름을 리스트로 나열하고 클릭 가능하게 만들기
    selected_columns = st.multiselect('분석하고자 하는 열을 선택하세요:', column_names, default=column_names)

    # 선택된 열의 데이터 표시
    if selected_columns:
        st.write(df[selected_columns].head(3))

    tab1, tab2 = st.tabs(["기술통계량", "데이터 시각화"])

    with tab1:
        st.write('# 기술통계량')
        # 열 이름 가져오기

    with tab2:
        # 라디오 버튼 생성
        variable_type = st.radio("일변량 데이터를 선택해주세요.", ("수치형", "범주형"))

        def get_slider_step(min_value, max_value):
            value_range = max_value - min_value
            bins_size_min = float((min_value // 5) * 5)
            bins_size_max = float((value_range) / 5) if value_range != 0 else 1.0

            if value_range < 1:
                step = 0.1
            elif value_range < 10:
                step = 0.5
            else:
                step = 1
                bins_size_min = int(bins_size_min)
                bins_size_max = int(bins_size_max)

            return bins_size_min+step, bins_size_max, step

        # 라디오 버튼의 선택에 따라 실행되는 코드 블록
        if variable_type == "수치형":
            # 변량이 수치형인 경우 실행되는 코드
            st.write("수치형 데이터를 히스토그램과 상자그림으로 표현합니다. ")


            try:
                colname = st.text_input("시각화하고 싶은 열 이름을 써주세요!")
                if colname != "":
                    data = df[colname]
                    # 데이터의 기술통계량 계산
                    summary_stats = pd.DataFrame({
                        '평균': np.mean(data),
                        '표준편차': np.std(data),
                        '최솟값': np.min(data),
                        '중앙값': np.median(data),
                        '최댓값': np.max(data)
                    }, index=['통계량'])

                    st.write(summary_stats)
                    minvalue = min(df[colname])
                    maxvalue = max(df[colname])
                    st.write(colname, '의 최솟값:', minvalue, '의 최댓값:',maxvalue)
                    bins_size_min, bins_size_max, step = get_slider_step(minvalue, maxvalue)
                    st.write(step)
                    bins_size = st.slider("계급의 크기를 설정해주세요.",
                                        min_value=bins_size_min, 
                                        max_value=bins_size_max, 
                                        step=step)

                    # Create a figure and adjust the histogram parameters
                    fig = plt.figure(figsize=(5, 3))

                    # bins_size = st.slider("계급의 크기를 설정해주세요.", 
                    #                       min_value= 0.5,#+ int((minvalue // 5) * 5), 
                    #                       max_value= 1.0+ int((max(df[colname]-min(df[colname])))/5),
                    #                       step= 0.5)



                    st.write("히스토그램의 계급의 크기:",bins_size)
                    # Plot the histogram with adjusted parameters
                    sns.set_style("darkgrid")
                    plt.title('Histogram of {}'.format(colname))
                    sns.histplot(x=df[colname], binwidth=bins_size, binrange = [min(df[colname]), max(df[colname])], kde=False)
                    plt.xlabel("")
                    st.pyplot(fig)

                    # 이상치 숨기기 체크박스
                    hide_outliers = st.checkbox("이상치 숨기기")

                    # 이상치를 숨기는 옵션 설정
                    showfliers = not hide_outliers
                    fig2 = plt.figure(figsize=(5, 1))
                    plt.title('Boxplot of {}'.format(colname))
                    sns.set_style("darkgrid")
                    # 박스 플롯 그리기
                    sns.boxplot(x=df[colname], palette="Set2", showfliers=showfliers)
                    plt.xlabel("")
                    st.pyplot(fig2)

            except ValueError:
                st.write("올바른 열 이름을 써주세요!")
                st.stop()

        # 범주형
        elif variable_type =='범주형':
            # 변량이 범주형인 경우 실행되는 코드
            st.write("범주형 데이터를 막대그래프로 표현합니다.")

            try:
                colname = st.text_input("시각화하고 싶은 열 이름을 입력해주세요!")
                if colname != "":
                    # Create a figure and adjust the bar plot parameters
                    fig = plt.figure(figsize=(5,3))
                    ax = sns.countplot(x=df[colname], palette="Blues")

                    # Add frequency labels on top of each bar with white outline
                    for p in ax.patches:
                        height = p.get_height()
                        ax.annotate(format(height, ','),
                                    (p.get_x() + p.get_width() / 2, height),
                                    ha='center', va='center',
                                    xytext=(0, -10), textcoords='offset points',
                                    fontsize=10, color='black',
                                    path_effects=[path_effects.Stroke(linewidth=3, foreground='white'),
                                                path_effects.Normal()])

                    plt.title('Barplot of {}'.format(colname))
                    sns.set_style("darkgrid")
                    plt.xlabel("")
                    st.pyplot(fig)

            except ValueError:
                st.write("올바른 열 이름을 입력해주세요!")
                st.stop()


        variable_type_group = st.radio("그룹별 데이터를 선택해주세요. (예: 클래스에 따른 생존율)", ("수치형", "범주형"))


        if variable_type_group == "수치형":
            # 변량이 수치형인 경우 실행되는 코드
            st.write("그룹별 수치형 데이터를 히스토그램과 상자그림으로 표현합니다. ")


            try:
                colname_group = st.text_input("그룹 열 이름을 써주세요!")
                colname_2 = st.text_input("그룹별로 시각화하고 싶은 수치형 열 이름을 써주세요!")
                if colname_2 != "":

                    data = df[[colname_2, colname_group]]
                    # 데이터의 기술통계량 계산
                    stat = data.groupby(colname_group)[colname_2].agg(
                        mean='mean',
                        std='std',
                        min='min',
                        median='median',
                        max='max'
                    )
                    stat.columns = ['평균', '표준편차', '최솟값', '중앙값', '최댓값']
                    st.write(stat)

                    minvalue = min(df[colname_2])
                    maxvalue = max(df[colname_2])
                    st.write(colname_2, '의 최솟값:', minvalue, '의 최댓값:',maxvalue)
                    bins_size_min, bins_size_max, step = get_slider_step(minvalue, maxvalue)
                    st.write(step)
                    bins_size = st.slider("계급의 크기를 설정해주세요. (group)",
                                        min_value=bins_size_min, 
                                        max_value=bins_size_max, 
                                        step=step)

                    # Create a figure and adjust the histogram parameters
                    fig = plt.figure(figsize=(5, 3))

                    st.write("히스토그램의 계급의 크기:",bins_size)
                    # Plot the histogram with adjusted parameters
                    sns.set_style("darkgrid")
                    plt.title('Histogram of {}'.format(colname_2))
                    sns.histplot(data = data, x = colname_2, hue = colname_group, binwidth=bins_size, binrange = [min(df[colname_2]), max(df[colname_2])], kde=False)
                    plt.xlabel("")
                    st.pyplot(fig)

                    # 이상치 숨기기 체크박스
                    hide_outliers = st.checkbox("이상치 숨기기 ")

                    # 이상치를 숨기는 옵션 설정
                    showfliers = not hide_outliers
                    fig2 = plt.figure(figsize=(5, 5))
                    plt.title('Boxplot of {}'.format(colname_2))
                    sns.set_style("darkgrid")
                    # 박스 플롯 그리기
                    sns.boxplot(data = df, x = colname_group, y = colname_2, palette="Set2", showfliers=showfliers)
                    plt.xlabel("")
                    st.pyplot(fig2)

            except ValueError:
                st.write("올바른 열 이름을 써주세요!")
                st.stop()

        # 범주형
        elif variable_type_group=='범주형':
            # 변량이 범주형인 경우 실행되는 코드
            st.write("범주형 데이터를 막대그래프로 표현합니다.")

            try:
                colname_group = st.text_input("그룹 열 이름을 써주세요!")
                colname_2 = st.text_input("그룹별로 시각화하고 싶은 수치형 열 이름을 입력해주세요!")
                if colname_2 != "":
                    # Create a figure and adjust the bar plot parameters
                    fig = plt.figure(figsize=(5,3))
                    ax = sns.countplot(x=df[colname_2], palette="Blues")

                    # Add frequency labels on top of each bar with white outline
                    for p in ax.patches:
                        height = p.get_height()
                        ax.annotate(format(height, ','),
                                    (p.get_x() + p.get_width() / 2, height),
                                    ha='center', va='center',
                                    xytext=(0, -10), textcoords='offset points',
                                    fontsize=10, color='black',
                                    path_effects=[path_effects.Stroke(linewidth=3, foreground='white'),
                                                path_effects.Normal()])

                    plt.title('Barplot of {}'.format(colname_2))
                    sns.set_style("darkgrid")
                    plt.xlabel("")
                    st.pyplot(fig)

            except ValueError:
                st.write("올바른 열 이름을 입력해주세요!")
                st.stop()

except NameError as e:
    st.warning('데이터를 먼저 입력해주세요. ')