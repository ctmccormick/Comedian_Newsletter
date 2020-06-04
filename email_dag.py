from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 5, 13),
    'depends_on_past': False,
    'retries': 1}

dag = DAG('newsletter', default_args=default_args, schedule_interval='@daily')

get_comics = BashOperator(
    task_id='get_comedians'
    , bash_command='python3 get_comedians.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

wiki = BashOperator(
    task_id='wiki_scrape'
    , bash_command='python3 wiki_scrape1.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

news = BashOperator(
    task_id='news_scrape'
    , bash_command='python3 news_scrape2.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

clean = BashOperator(
    task_id='df_clean'
    , bash_command='python3 df_clean3.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

send = BashOperator(
    task_id='send_email'
    , bash_command='python3 email_send4.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

web_refresh = BashOperator(
    task_id='web_refresh'
    , bash_command='python3 update_web_files.py'
    , dag=dag
    , email_on_failure=True
    , email=my_email
)

get_comics >> wiki >> news >> clean >> web_refresh >> send
