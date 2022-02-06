




"""elif dead_line_repeat == "2":
add = datetime.timedelta(minutes=1)
repeate_tasks(request_date2, add, name, date_time_sql, important, num1)

elif dead_line_repeat == "3":
add = datetime.timedelta(days=7)
repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, num1)
elif dead_line_repeat == "4":
add = datetime.timedelta(weeks=4)
repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, num1)
elif dead_line_repeat == "5":
add = datetime.timedelta(days=365)
repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, num1)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def repeate_tasks(time_request, add_time, name, date_time_sql, important, num1):

    conn = sqlite3.connect('todo')
    c = conn.cursor()


    time = datetime.datetime.strptime(time_request, '%Y-%m-%d %H:%M:%S')
    new_time = time + add_time
    print(new_time)
    query1 = f'INSERT INTO repeat_task (text, task_creation_time, dead_line, completed, relevance, id_generated)  VALUES("{name}", "{date_time_sql}","{new_time}", "False", "{important}", "{num1}")'
    c.execute(query1)
    conn.commit()

def insert_task():

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

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        query4 = "SELECT task_creation_time FROM tasks "
            c.execute(query4)
            conn.commit()
            update_completed_time = []

            for each in c.fetchall():
                update_completed_time.append(each[0])
            print(update_completed_time)
            for each in completed:

                each_element_update = update_completed_time[int(each)]

                print(each_element_update)

                query5 = f'UPDATE tasks SET completed_time = "{data_generated}" WHERE task_creation_time ={each_element_update}'
                c.execute(query5)
                conn.commit()
                print(query5)

            query6 = "SELECT completed_time FROM tasks"
            c.execute(query6)
            conn.commit()

            delete_completed_time = []
            for every in c.fetchall():
                delete_completed_time.append(every[0])
            for every in completed:
                every_element_delete = str(delete_completed_time[int(every)])

                every_element_delete = datetime.datetime.strptime(every_element_delete, '%Y-%m-%d %H:%M:%S.%f')
                add_1 = datetime.timedelta(minutes=-1)
                delete_after_time = every_element_delete + add_1

                query3 = f'DELETE FROM tasks WHERE completed_time <= "{every_element_delete}" '
                c.execute(query3)
                conn.commit()



        """
