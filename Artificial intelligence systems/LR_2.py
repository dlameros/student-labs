import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
import warnings

warnings.filterwarnings('ignore')

def main():

    print("Загрузка данных...")

    train = pd.read_csv('https://drive.google.com/uc?id=1N6fqhSe8a4Hpl_tTHcd8fwTiAb1VPhTo')
    test = pd.read_csv('  https://drive.google.com/uc?id=1bPnhSsDY-PZLMVp24veBDWXLAcvyhVw3')
    sample = pd.read_csv('  https://drive.google.com/uc?id=1-_pEB2kWs0C7M2bExdb-sP-dq2hX7f9g')

    original_train_shape = train.shape
    original_test_shape = test.shape

    keep_columns = [
        'AST', 'ALT', 'Gtp', 'hemoglobin', 'Cholesterol',
        'triglyceride', 'LDL', 'HDL', 'systolic', 'relaxation'
    ]

    train = train[['id', 'smoking'] + keep_columns].copy()
    test = test[['id'] + keep_columns].copy()

    valid_ranges = {
        'AST': (5, 1000),
        'ALT': (5, 1000),
        'Gtp': (5, 1000),
        'hemoglobin': (8, 20),
        'Cholesterol': (100, 600),
        'triglyceride': (30, 1000),
        'LDL': (10, 500),
        'HDL': (10, 150),
        'systolic': (70, 250),
        'relaxation': (40, 150)
    }

    def filter_valid_data(df, ranges):
        mask = pd.Series([True] * len(df))
        for col, (low, high) in ranges.items():
            if col in df.columns:
                mask &= (df[col] >= low) & (df[col] <= high) & (df[col].notna())
        return df[mask].reset_index(drop=True)

    train = filter_valid_data(train, valid_ranges)

    print(f"Размеры до фильтрации: train={original_train_shape}, test={original_test_shape}")
    print(f"Размеры после фильтрации: train={train.shape}, test={test.shape}")

    X = train[keep_columns]
    y = train['smoking']
    X_test = test[keep_columns]

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
    oof_preds = np.zeros(len(X))
    test_preds = np.zeros(len(X_test))

    print("Обучение модели...")

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)

        model = LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            num_leaves=31,
            subsample=0.7,
            colsample_bytree=0.7,
            random_state=42,
            verbose=-1
        )

        model.fit(X_train_scaled, y_train)

        val_pred = model.predict_proba(X_val_scaled)[:, 1]
        test_pred = model.predict_proba(X_test_scaled)[:, 1]

        oof_preds[val_idx] = val_pred
        test_preds += test_pred / skf.n_splits

        fold_auc = roc_auc_score(y_val, val_pred)
        print(f"Fold {fold + 1} AUC: {fold_auc:.5f}")

    final_auc = roc_auc_score(y, oof_preds)
    print(f"\nИтоговый OOF AUC: {final_auc:.5f}")

    submission = pd.DataFrame({
        'id': test['id'],
        'smoking': np.round(test_preds, 2)
    })

    submission.to_csv('submission.csv', index=False)

    print("\nФайл submission.csv сохранён!")
    print("\nСодержимое файла submission.csv:")
    print(submission.head(10))
    print(f"\nВсего строк в файле: {len(submission)}")
    print(f"Диапазон значений в столбце 'smoking': от {submission['smoking'].min():.2f} до {submission['smoking'].max():.2f}")

if __name__ == "__main__":
    main()