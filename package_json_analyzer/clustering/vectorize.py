import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore


def vectorize(df: pd.DataFrame) -> pd.DataFrame:
    # データフレームXのリストを文字列に変換
    X_transformed = df.map(lambda x: " ".join(x))

    # 各カラムごとにTF-IDFベクトルを計算
    vectorizer = TfidfVectorizer()
    X_tfidf = pd.DataFrame()
    for column in X_transformed.columns:
        tfidf_matrix = vectorizer.fit_transform(X_transformed[column])
        df_tfidf = pd.DataFrame(
            tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out()
        )
        X_tfidf = pd.concat([X_tfidf, df_tfidf], axis=1)

    return X_tfidf
