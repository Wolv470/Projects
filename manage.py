import sqlite3
import datetime
from random import choice



def get_data():
    conn = sqlite3.connect('todo')
    c = conn.cursor()

    #c.execute("SELECT * FROM tasks  ORDER BY dead_line ASC")
    c.execute("SELECT * FROM tasks")
    # c.execute("SELECT * FROM tasks ORDER BY relevance ASC")

    list_true = []
    database_to_list = []
    relevance_to_list = []

    for row in c.fetchall():
        database_to_list.append([row[0], row[1], row[2]])
        relevance_to_list.append([row[4]])
        list_true.append([row[3]])


    return database_to_list, relevance_to_list, list_true


def repeate_tasks(request_date2, add_time, name, date_time_sql, important, newid):

    conn = sqlite3.connect('todo')
    c = conn.cursor()


    time = datetime.datetime.strptime(request_date2, '%Y-%m-%d %H:%M:%S')
    new_time = time + add_time
    print(new_time)
    query1 = f'INSERT INTO repeat_task (text, task_creation_time, dead_line, completed, relevance, id_generated)  VALUES("{name}", "{date_time_sql}","{new_time}", "False", "{important}", "{newid}")'
    c.execute(query1)
    conn.commit()



def insert_repeated_task():

    conn=sqlite3.connect('todo')
    c=conn.cursor()

    data_generated = datetime.datetime.now()
    date = data_generated.strftime('%Y-%m-%d %H:%M:%S')
    date_datime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


    task_list = []
    query1 = 'SELECT id_generated FROM tasks'
    c.execute(query1)
    for name in c.fetchall():
        task_list.append(name[0])


    reapeate_task_list = []
    query3 = f'SELECT id_generated FROM repeat_task WHERE dead_line <= "{date_datime}" '
    c.execute(query3)
    for name2 in c.fetchall():
        reapeate_task_list.append(name2[0])

    list3 = list(set(reapeate_task_list) - set(task_list))
    print(list3)
    for each in list3:
        query2 = f'INSERT INTO tasks  SELECT * FROM repeat_task WHERE  id_generated ="{each}" '
        c.execute(query2)
        conn.commit()




def verified_delete(completed):
    conn = sqlite3.connect('todo')
    c = conn.cursor()


    c.execute("SELECT completed_time FROM tasks")
    delete_completed_time = []

    for every in c.fetchall():
        delete_completed_time.append(every)
    for every in completed:

        every_element_delete = str(delete_completed_time[int(every)]).replace('(', '').replace(')', '').replace(',','').replace('\"', '').replace('\'', '')
        try:
            every_element_delete = datetime.datetime.strptime(every_element_delete, '%Y-%m-%d %H:%M:%S.%f')
            add_1 = datetime.timedelta(minutes=-1)
            delete_after_time = every_element_delete + add_1

            query3 = f'DELETE FROM tasks WHERE completed_time <= "{every_element_delete}" '
            c.execute(query3)
            conn.commit()
        except Exception as e:
            print(e)



def idgenerated():
    conn =sqlite3.connect('todo')
    c =conn.cursor()

    id_generated_repeat_task=[]
    c.execute('SELECT id_generated FROM repeat_task')
    for name in c.fetchall():
        id_generated_repeat_task.append(name[0])

    id_generated_tasks=[]
    c.execute('SELECT id_generated FROM tasks')
    for name2 in c.fetchall():
        id_generated_tasks.append(name2[0])

    newid = choice([i for i in range(1000, 9999) if i not in id_generated_repeat_task and i not in id_generated_tasks])

    return newid







"""
def dead_line_delete():
    conn =sqlite3.connect('todo')
    c=conn.cursor()
    data_generated = datetime.datetime.now()
    date = data_generated.strftime('%Y-%m-%d %H:%M:%S')
    query = f'DELETE FROM tasks WHERE dead_line ="{date}"'
    print(query)
    c.execute(query)
    conn.commit()

"""