import glob
import pandas as pd
import camelot  # 安装camelot-py包，以及依赖包opencv-python


# 冒号分割
header_1 = ['预录入编号','海关编号']

# 换行分割
header_2 = ['境内收发货人','进口口岸','进口日期','申报日期','运输方式','消费使用单位','贸易方式','征税比例','启运国','境内目的地']

# 换格分割
header_3 = ['数量及单位','原产国','单价','总价','币制']

def pdf2df(file_nm):
    tables = camelot.read_pdf(file_nm, pages='all', flavor='stream', row_tol=20, table_areas=['0, 750, 600, 450'])
    df_out = pd.DataFrame(columns = header_1 + header_2 + header_3)

    for tb in tables:
        df = tb.df

        res_1 = {}
        for ix, line in df.iterrows():
            for _, col in line.dropna().iteritems():
                items = col.split('：')
                if len(items) >= 2:
                    for h in header_1:
                        if items[0].startswith(h):
                            res_1[h] = [items[1]]

        res_2 = {}
        for ix, line in df.iterrows():
            for _, col in line.dropna().iteritems():
                items = col.split('\n')
                if len(items) >= 2:
                    for h in header_2:
                        if items[0].startswith(h):
                            res_2[h] = [items[-1]]

        res_3 = {}
        for ix, line in df.iterrows():
            for _, col in line.iteritems():
                for h in header_3:
                    if str(col).startswith(h):
                        res_3[h] = [df.iloc[ix+1, _].split('\n')[0]]

        res_1.update(res_2); res_1.update(res_3)
        df_tmp = pd.DataFrame(res_1)

    return df_out.append(df_tmp)


if __name__ == '__main__':
    file_nm_ls = glob.glob('*.pdf')
    df = pd.DataFrame(columns = header_1 + header_2 + header_3)
    for file_nm in file_nm_ls:
        df = df.append(pdf2df(file_nm))
    df.to_excel('result.xlsx', index=False)



