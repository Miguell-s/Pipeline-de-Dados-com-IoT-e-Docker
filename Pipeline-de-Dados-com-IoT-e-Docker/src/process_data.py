import pandas as pd
from sqlalchemy.orm import Session
from database import init_db, get_db, TemperatureReading
import os


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    df = df.dropna()
    df['noted_date'] = pd.to_datetime(df['noted_date'])
    return df


def insert_data_to_db(df, db: Session):
    for _, row in df.iterrows():
        reading = TemperatureReading(
            room_id=row['room_id/id'],
            noted_date=row['noted_date'],
            temp=row['temp'],
            out_or_in=row['out/in']
        )
        db.add(reading)
    db.commit()


def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'IOT-temp.csv')
    
    print("Inicializando banco de dados...")
    init_db()
    
    print("Carregando dados...")
    df = load_data(data_path)
    
    print("Limpando dados...")
    df_clean = clean_data(df)
    
    print("Inserindo dados no banco...")
    db = next(get_db())
    insert_data_to_db(df_clean, db)
    
    print("Processamento concluído com sucesso!")


if __name__ == "__main__":
    main()
