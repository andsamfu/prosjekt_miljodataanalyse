import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, DateFormatter
import os

def load_data(db_path):
    """
    Laster inn data fra SQLite-databasen.

    Args:
        db_path (str): Stien til SQLite-databasen.

    Returns:
        pd.DataFrame: DataFrame med værdata.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df

def preprocess_data(df):
    """
    Forbehandler data: konverterer datoer og lager nødvendige funksjoner.

    Args:
        df (pd.DataFrame): DataFrame med rådata.

    Returns:
        pd.DataFrame: DataFrame med forbehandlede data.
    """
    # Konverter datoer til datetime-format
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    # Sorter data etter dato
    df = df.sort_values('referenceTime')
    # Legg til dag i året og måned som funksjoner
    df['DayOfYear'] = df['referenceTime'].dt.dayofyear
    df['Month'] = df['referenceTime'].dt.month
    # Beregn sin og cos for årssykluser
    df['sin_day'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)
    return df

def split_data(df, split_ratio=0.75):
    """
    Deler data i treningssett og valideringssett.

    Args:
        df (pd.DataFrame): DataFrame med forbehandlede data.
        split_ratio (float): Andel av data som skal brukes til trening.

    Returns:
        pd.DataFrame, pd.DataFrame: Treningssett og valideringssett.
    """
    split_point = int(len(df) * split_ratio)
    return df[:split_point], df[split_point:]

def create_future_features(df_future, end_year=2024):
    """
    Lager fremtidige funksjoner for prediksjon frem til et spesifikt år.

    Args:
        df_future (pd.DataFrame): Valideringssett.
        end_year (int): Året prediksjonen skal stoppe (inkludert).

    Returns:
        pd.DataFrame: DataFrame med fremtidige funksjoner.
    """
    # Startdato er den første datoen i valideringssettet
    start_date = df_future['referenceTime'].iloc[0]
    # Sluttdato er slutten av det spesifiserte året
    end_date = pd.Timestamp(f"{end_year}-12-31")
    # Generer datoer mellom start- og sluttdato
    future_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq='D'
    )
    # Lag DataFrame med fremtidige datoer og funksjoner
    future_df = pd.DataFrame({'referenceTime': future_dates})
    future_df['DayOfYear'] = future_df['referenceTime'].dt.dayofyear
    future_df['Month'] = future_df['referenceTime'].dt.month
    future_df['sin_day'] = np.sin(2 * np.pi * future_df['DayOfYear'] / 365)
    future_df['cos_day'] = np.cos(2 * np.pi * future_df['DayOfYear'] / 365)
    return future_df

def train_model(X_train, y_train):
    """
    Trener en lineær regresjonsmodell.

    Args:
        X_train (pd.DataFrame): Treningsfunksjoner.
        y_train (pd.Series): Treningsmål.

    Returns:
        LinearRegression: Trenet modell.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluerer modellen på testsettet.

    Args:
        model (LinearRegression): Trenet modell.
        X_test (pd.DataFrame): Testfunksjoner.
        y_test (pd.Series): Testmål.

    Returns:
        float, float, np.ndarray: Mean Squared Error, R²-score og prediksjoner.
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred

def split_into_segments(dates, values, max_gap_days=31):
    """
    Deler data i segmenter for plotting.

    Args:
        dates (pd.Series): Tidsstempler.
        values (pd.Series): Verdier som skal plottes.
        max_gap_days (int): Maksimalt antall dager mellom punkter i samme segment.

    Returns:
        list, list: Lister over segmenterte datoer og verdier.
    """
    if len(dates) == 0:
        return [], []
        
    segments_x = []
    segments_y = []
    current_x = [dates.iloc[0]]
    current_y = [values.iloc[0]]
    
    for i in range(1, len(dates)):
        gap = (dates.iloc[i] - dates.iloc[i-1]).days
        if gap > max_gap_days:
            segments_x.append(current_x)
            segments_y.append(current_y)
            current_x = []
            current_y = []
        current_x.append(dates.iloc[i])
        current_y.append(values.iloc[i])
    
    if current_x: 
        segments_x.append(current_x)
        segments_y.append(current_y)
    return segments_x, segments_y

def plot_predictions(df_train, df_future, future_df, y_pred_extended):
    """
    Plotter treningsdata, valideringsdata og prediksjoner.

    Args:
        df_train (pd.DataFrame): Treningssett.
        df_future (pd.DataFrame): Valideringssett.
        future_df (pd.DataFrame): Fremtidige funksjoner.
        y_pred_extended (np.ndarray): Predikerte verdier for fremtidige data.
    """
    plt.figure(figsize=(15, 6))

    # Plot treningsdata (reell)
    mask_train_real = df_train['generated_mean_air_temperature'] == 0
    dates_real = df_train.loc[mask_train_real, 'referenceTime']
    temps_real = df_train.loc[mask_train_real, 'mean_air_temperature']
    segments_x, segments_y = split_into_segments(dates_real, temps_real)
    for seg_x, seg_y in zip(segments_x, segments_y):
        plt.plot(seg_x, seg_y, color='blue', alpha=0.7, label='Trenings data')

    # Plot treningsdata (generert)
    mask_train_gen = df_train['generated_mean_air_temperature'] == 1
    dates_gen = df_train.loc[mask_train_gen, 'referenceTime']
    temps_gen = df_train.loc[mask_train_gen, 'mean_air_temperature']
    segments_x, segments_y = split_into_segments(dates_gen, temps_gen)
    for seg_x, seg_y in zip(segments_x, segments_y):
        plt.plot(seg_x, seg_y, color='red', alpha=0.7, label='Imputert data')

    # Plot valideringsdata (reell)
    mask_future_real = df_future['generated_mean_air_temperature'] == 0
    dates_future = df_future.loc[mask_future_real, 'referenceTime']
    temps_future = df_future.loc[mask_future_real, 'mean_air_temperature']
    segments_x, segments_y = split_into_segments(dates_future, temps_future)
    for seg_x, seg_y in zip(segments_x, segments_y):
        plt.plot(seg_x, seg_y, color='seagreen', alpha=0.7, label='Validerings data')

    # Plot valideringsdata (generert)
    mask_future_gen = df_future['generated_mean_air_temperature'] == 1
    dates_future_gen = df_future.loc[mask_future_gen, 'referenceTime']
    temps_future_gen = df_future.loc[mask_future_gen, 'mean_air_temperature']
    segments_x, segments_y = split_into_segments(dates_future_gen, temps_future_gen)
    for seg_x, seg_y in zip(segments_x, segments_y):
        plt.plot(seg_x, seg_y, color='red', alpha=0.7)

    # Plot prediksjoner
    plt.plot(future_df['referenceTime'], y_pred_extended, color='darkblue', linestyle='--', linewidth=2, label='Predikert data')

    # Formater X-aksen for å vise hvert år
    ax = plt.gca()
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))

    plt.xlabel('År')
    plt.ylabel('Temperatur (°C)')
    plt.title('Prediksjon av gjennomsnittlig lufttemperatur i Trondheim')
    
    # Fix duplicate labels in legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main_frost_prediciton(path, end_year=2024):
    """
    Hovedfunksjon for å kjøre hele funksjonaliteten.

    Args:
        db_path (str): Stien til SQLite-databasen.
        end_year (int): Året prediksjonen skal stoppe (inkludert).
    """
    path_file = os.path.join(path, 'data', 'clean', 'frost.db')
    df = load_data(path_file)
    df = preprocess_data(df)
    df_train, df_future = split_data(df)
    future_df = create_future_features(df_future, end_year=end_year)

    X_train = df_train[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
    y_train = df_train['mean_air_temperature']
    model = train_model(X_train, y_train)

    X_future_extended = future_df[['DayOfYear', 'Month', 'sin_day', 'cos_day']]
    y_pred_extended = model.predict(X_future_extended)

    mse, r2, _ = evaluate_model(model, df_future[['DayOfYear', 'Month', 'sin_day', 'cos_day']], df_future['mean_air_temperature'])
    print(f"Modellens ytelse:\nMean Squared Error: {mse:.2f}\nR² Score: {r2:.2f}")

    plot_predictions(df_train, df_future, future_df, y_pred_extended)

if __name__ == "__main__":
    main_frost_prediciton('', 2024)