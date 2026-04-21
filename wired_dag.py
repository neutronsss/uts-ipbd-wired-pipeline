from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests

default_args = {
    'owner': 'jimly',
    'start_date': datetime(2026, 4, 20),
    'retries': 1,
}

dag = DAG(
    'wired_etl_pipeline_docker',
    default_args=default_args,
    description='Pipeline ETL UTS IPBD (Docker + Postgres)',
    schedule='@daily',
    catchup=False
)

# extract
def extract_from_api():
    api_url = "http://host.docker.internal:8000/articles"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            raise Exception(f"API Lokal merespons error: {data['error']}")
            
        articles = data.get("articles", [])
        print(f"Berhasil mengambil {len(articles)} artikel dari API lokal.")

        return articles
    else:
        raise Exception(f"Gagal memanggil API. Status Code: {response.status_code}")

# transform
def transform_data(ti):
    raw_articles = ti.xcom_pull(task_ids='extract_task')

    if not raw_articles:
        raise ValueError("Data raw_articles kosong! Proses tidak bisa dilanjutkan.")
        
    clean_articles = []
    for art in raw_articles:
        date_obj = datetime.fromisoformat(art['scraped_at'])
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        
        clean_articles.append({
            "title": art['title'],
            "url": art['url'],
            "description": art['description'],
            "author": art['author'],
            "scraped_at": formatted_date
        })
    
    print("Transformasi tanggal selesai.")
    return clean_articles 

# Loaf
def load_to_postgres(ti):
    clean_articles = ti.xcom_pull(task_ids='transform_task')
    
    if not clean_articles:
        raise ValueError("Data bersih kosong. Tidak ada yang bisa dimasukkan ke database.")
        
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')

    pg_hook.run("DROP TABLE IF EXISTS wired_articles;")    
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS wired_articles (
        id SERIAL PRIMARY KEY,
        title TEXT,
        url TEXT,
        description TEXT,
        author TEXT,
        scraped_at TIMESTAMP
    );
    """
    pg_hook.run(create_table_query)
    
    insert_query = """
    INSERT INTO wired_articles (title, url, description, author, scraped_at)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    for art in clean_articles:
        pg_hook.run(insert_query, parameters=(
            art['title'], 
            art['url'], 
            art['description'], 
            art['author'], 
            art['scraped_at']
        ))
        
    print("Data berhasil dimasukkan ke PostgreSQL!")

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_from_api,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_to_postgres,
    dag=dag,
)

extract_task >> transform_task >> load_task